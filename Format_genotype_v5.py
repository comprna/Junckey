# The next script will accept a phenotype table (junctions, events, transcripts...)
# and a genotype table (mutations associated to K-mers or SMRs).

#V5: version oriented for using with IR values

"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

Format_genotype_v5.py: given a file with introns and a file with this introns and the mutations falling in each one
this script generates a file with the same introns and which samples are mutated
"""

import pandas as pd
from argparse import ArgumentParser, RawTextHelpFormatter

import logging, sys

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

description = \
    "Description:\n\n" + \
    "given a file with introns and a file with this introns and the mutations falling in each one this script \n" + \
    "generates a file with the same introns and which samples are mutated"

parser = ArgumentParser(description=description, formatter_class=RawTextHelpFormatter,
                        add_help=True)
parser.add_argument("-p", "--phenotype", required=True,
                    help="Phenotype table")
parser.add_argument("-g", "--genotype", required=True,
                    help="Genotype table")
parser.add_argument("-o", "--output", required=True,
                    help="Output file")
parser.add_argument("-TCGA", "--TCGA", default=False, action="store_true",
                    help="Activate this flag the data belong to TCGA")
parser.add_argument("-SCLC", "--SCLC", default=False, action="store_true",
                    help="Activate this flag the data belong to SCLC")




def get_middle_point(start, end):
    """
    Given two lists of integers, get another list with the middle point
    for each point between the two lists
    """
    pos_list = []
    for i in range(len(start)):
        pos_list.append(int((int(start[i])+int(end[i]))/2))
    return pos_list


def main():

    args = parser.parse_args()

    try:

        phenotype_path = args.phenotype
        genotype_path = args.genotype
        output_path = args.output

        # phenotype_path = "/projects_rg/SCLC_cohorts/George/IR/normalized_tpm_George_Peifer.tab.part0"
        # genotype_path = "/genomics/users/juanluis/FastQTL_analysis/v3/SCLC/Junctions/tables/introns_Ensembl_mutations_filtered.bed"
        # output_path = "/projects_rg/SCLC_cohorts/George/IR/formatted_genotype.vcf"

        if (args.TCGA == False and  args.SCLC == False):
            raise Exception("Set one of the data flag (-TCGA or -SCLC)")

        # 1. Load the phenotype and genotype tables using pandas
        logger.info("Loading "+phenotype_path+"...")
        # phenotype = pd.read_table(phenotype_path, delimiter="\t")
        phenotype = pd.read_table(phenotype_path, delimiter="\t", index_col=0)
        #Take the ids of the introns in the phenotype file, for creating the same rows in df_output
        id_introns = list(phenotype.index)
        #Take the ids of the samples in the phenotype file, for creating the same columns in df_output
        id_phenotypes = phenotype.columns.values

        #If is SCLC samples, remove the T from the id samples
        if(args.SCLC == True):
            id_phenotypes = [s.replace('T', '') for s in id_phenotypes]
        elif(args.TCGA == True):
            pass

        # id_phenotypes = [s.replace('T', '') for s in id_phenotypes]

        #Create the output genotype df and initialize it to 0
        df_output = pd.DataFrame(index=id_introns, columns=id_phenotypes)
        df_output = df_output.fillna(0)

        logger.info("Loading "+genotype_path+"...")
        genotype = pd.read_table(genotype_path, delimiter="\t", header=None)
        genotype.columns = ['chr1', 'start1', 'end1', 'id_intron', 'chr2', 'start2', 'end2', 'cancer_type', 'id_sample', 'mut_orig',
                            'mut_final', 'pass', 'info', 'chr2', 'start2', 'end2', 'gene', 'dot', 'strand']
        #Create a variable with the 3 first columns
        chr = genotype['chr1'].apply(lambda x: x[3:])
        new_id = chr.map(str) + ":" + genotype['start1'].map(str) + "-" + genotype['end1'].map(str)

        # 2. Iterate through the mutations file annotating all the mutations observed in df_output
        not_found = {}

        #Iterate over the phenotype file. For each intron, find all the possible mutations
        #for i in range(len(phenotype)):
        #    intron_id = id_introns[i]
        #    percentage = "Formatting genotype..."+str(round(i*100/len(phenotype),3))+ "%"
        #    sys.stdout.write("\r%s" % percentage)
        #    sys.stdout.flush()
        #    for j in range(len(genotype)):
        #        if(new_id[j] == intron_id and genotype.iloc[j,8] in id_phenotypes):
        #            df_output.loc[new_id[j], genotype.iloc[j,8]] = df_output.loc[new_id[j], genotype.iloc[j,8]] + 1

        logger.info("Formatting genotype...")
        #Iterate over the genotype file
        for i in range(len(genotype)):
            percentage = str(round(i*100/len(phenotype),3))+ "%"
            logger.info("\r%s" % percentage)
            # sys.stdout.write("\r%s" % percentage)
            # sys.stdout.flush()
            id_sample = genotype.iloc[i,8]
            id_intron = new_id[i]
            if(id_sample in id_phenotypes):
                df_output.loc[id_intron,id_sample] = df_output.loc[id_intron,id_sample] + 1

        percentage = "Formatting genotype..." + "100%\n"
        sys.stdout.write("\r%s" % percentage)

        # Save the output file
        logger.info("Saving "+output_path+"...")
        df_output.to_csv(output_path, sep="\t", index=True)

        logger.info("Done. Exiting program")

        exit(0)

    except Exception as error:
        logger.error(repr(error))
        logger.error('Aborting execution')
        exit(1)

if __name__ == '__main__':
    main()
