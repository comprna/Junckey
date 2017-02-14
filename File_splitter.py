
"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

File_splitter.py: Split an input file into n pieces and generate a command for Format_genotype.py for
each piece

"""

#V2: This is exactly as V1, but adapted for running Format_genotype_v4.py

import sys
import pandas as pd
import time

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
parser.add_argument("-p", "--phenotype", required=True,
                    help="Psi file")
parser.add_argument("-g", "--genotype", required=True,
                    help="Psi file")
parser.add_argument("-o", "--output", required=True,
                    help="Output folder")
parser.add_argument("-s", "--script", required=True,
                    help="Location of the script to run")
parser.add_argument("-m", "--mode", required=True,
                    help="Mode of execution (SCLC or TCGA)")

def main():

    args = parser.parse_args()

    try:

        print("Starting execution: " + time.strftime('%H:%M:%S'))
        print("File "+args.input+" will be splitted in "+args.n+" pieces")

        # 1. Load the input file
        print("Loading "+args.input+"...")
        input_file = pd.read_table(args.input, delimiter="\t")
        # input_file = pd.read_table("/genomics/users/juanluis/FastQTL_analysis/SCLC/Junctions/data/INTRON/psi_all_samples.txt", delimiter="\t")
        nameFileaux = args.input.split("/")[-1]

        # 2. Split the file
        #Generate also a file with the commands for being executed in the cluster
        n = int(args.n)
        output_commands_path = args.output + "/commands_splitter_"+str(n)+".txt"
        commands_file = open(output_commands_path, 'w')
        print("Splitting the file...")
        #Get the size of each piece
        size = int(len(input_file)/n)
        for i in range(n):
            start = i * size
            end = (i+1)*size
            piece = input_file[start:end]
            #Save each piece in a separate file
            output_path = args.output + "/" + nameFileaux + ".part" + str(i)
            piece.to_csv(output_path, sep="\t", index=False)
            commands_file.write("python3.4 "+ args.script +" -"+ args.mode +" -p " + args.phenotype +
                " -g "+ args.genotype +" -c "+ output_path +
                " -o "+ args.output +"/formatted_genotype.vcf.part" + str(i) +
                " -i "+ args.output +"/ids_not_found.txt.part" + str(i) + "\n")
        if(end<len(input_file)):
            print("Extra piece number "+str(i+1))
            start = end
            end = len(input_file) + 1
            piece = input_file[start:end]
            # Save each piece in a separate file
            output_path = args.output + "/" + nameFileaux + ".part" + str(i+1)
            piece.to_csv(output_path, sep="\t", index=False)
            commands_file.write("python3.4 "+ args.script +" -"+ args.mode +" -p " + args.phenotype +
                " -g "+ args.genotype +" -c "+ output_path +
                " -o "+ args.output +"/formatted_genotype.vcf.part" + str(i+1) +
                " -i "+ args.output +"/ids_not_found.txt.part" + str(i+1) + "\n")

        print("Saved " + output_commands_path)
        commands_file.close()

        print("Done. Exiting program. "+time.strftime('%H:%M:%S')+"\n\n")

        exit(0)

    except Exception:
        print(Exception)
        sys.exit(1)


if __name__ == '__main__':
    main()