
"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

File_splitter.py: Split an input file into n pieces and generate a command for Format_genotype.py for
each piece

"""

#V2: This is exactly as V1, but adapted for running Format_genotype_v4.py

import pandas as pd

import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create console handler and set level to info
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

from argparse import ArgumentParser, RawTextHelpFormatter

description = \
    "Description:\n\n" + \
    "This script splits an input file the file into n pieces"

parser = ArgumentParser(description=description, formatter_class=RawTextHelpFormatter,
                        add_help=True)
parser.add_argument("-i", "--input", required=True,
                    help="Input file")
parser.add_argument("-n", "--n", required=True,
                    help="Number of pieces")
parser.add_argument("-p", "--phenotype", required=False,
                    help="Psi file")
parser.add_argument("-g", "--genotype", required=False,
                    help="Psi file")
parser.add_argument("-o", "--output", required=False,
                    help="Output folder")
parser.add_argument("-s", "--script", required=True,
                    help="Location of the script to run")
parser.add_argument("-m", "--mode", required=False,
                    help="Mode of execution (SCLC or TCGA)")
parser.add_argument("-e", "--execution", required=True,
                    help="Execution options (J for Junctions, IR for Intron Retention)")



def main():

    args = parser.parse_args()

    try:

        input = args.input
        output = args.output
        n = int(args.n)
        phenotype = args.phenotype
        genotype = args.genotype
        script = args.script
        mode = args.mode
        execution = args.execution


        # input = "/projects_rg/SCLC_cohorts/George/IR/normalized_tpm_George_Peifer.tab"
        # output = "/data/users/juanluis/SCLC_quantifications/George/v2/IR/format"
        # n = 100
        # # phenotype = args.phenotype
        # genotype = "/genomics/users/juanluis/FastQTL_analysis/v3/SCLC/Junctions/tables/introns_Ensembl_mutations_filtered.bed"
        # script = "/genomics/users/juanluis/comprna/Junckey/Format_genotype_v5.py"
        # mode = "SCLC"
        # execution = "IR"


        logger.info("File "+input+" will be splitted in "+str(n)+" pieces")

        # 1. Load the input file
        logger.info("Loading "+input+"...")
        input_file = pd.read_table(input, delimiter="\t")
        nameFileaux = input.split("/")[-1]

        # 2. Split the file
        logger.info("Splitting the file...")
        #Generate also a file with the commands for being executed in the cluster
        n = int(n)
        output_commands_path = output + "/commands_splitter_"+str(n)+".txt"
        commands_file = open(output_commands_path, 'w')
        #Get the size of each piece
        size = int(len(input_file)/n)
        for i in range(n):
            start = i * size
            end = (i+1)*size
            piece = input_file[start:end]
            #Save each piece in a separate file
            output_path = output + "/" + nameFileaux + ".part" + str(i)
            if(execution=="J"):
                piece.to_csv(output_path, sep="\t", index=False)
                commands_file.write("python3.4 "+ script +" -"+ mode +" -p " + phenotype +
                    " -g "+ genotype +" -c "+ output_path +
                    " -o "+ output +"/formatted_genotype.vcf.part" + str(i) +
                    " -i "+ output +"/ids_not_found.txt.part" + str(i) + "\n")
            elif(execution=="IR"):
                piece.to_csv(output_path, sep="\t", index=True)
                commands_file.write("python "+ script +" -"+ mode +" -p " + output_path +
                    " -g "+ genotype + " -o "+ output + "/formatted_genotype.vcf.part" + str(i) + "\n")
            else:
                raise Exception("Set one of the execution flags (-J or -IR)")

        if(end<len(input_file)):
            logger.info("Extra piece number "+str(i+1))
            start = end
            end = len(input_file) + 1
            piece = input_file[start:end]
            # Save each piece in a separate file
            output_path = output + "/" + nameFileaux + ".part" + str(i+1)
            if(execution=="J"):
                piece.to_csv(output_path, sep="\t", index=False)
                commands_file.write("python3.4 "+ script +" -"+ mode +" -p " + phenotype +
                    " -g "+ genotype +" -c "+ output_path +
                    " -o "+ output +"/formatted_genotype.vcf.part" + str(i+1) +
                    " -i "+ output +"/ids_not_found.txt.part" + str(i+1) + "\n")
            elif (execution == "IR"):
                piece.to_csv(output_path, sep="\t", index=True)
                commands_file.write("python "+ script +" -"+ mode +" -p " + output_path +
                    " -g "+ genotype + " -o "+ output + "/formatted_genotype.vcf.part" + str(i+1) + "\n")
            else:
                raise Exception("Set one of the execution flags (-J or -IR)")

        logger.info("Saved " + output_commands_path)
        commands_file.close()

        logger.info("Done. Exiting program. ")

        exit(0)

    except Exception as error:
        logger.error(repr(error))
        logger.error("Aborting execution")
        exit(1)


if __name__ == '__main__':
    main()