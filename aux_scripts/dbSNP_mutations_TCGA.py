"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

dbSNP_mutations_TCGA.py: given a list of mutations, we will check which
ones are in the dbSNP database and filter out
"""

import pandas as pd
from argparse import ArgumentParser, RawTextHelpFormatter
# from threading import Thread

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
    "given a list of mutations, we will check which ones are in the dbSNP database and filter out"

parser = ArgumentParser(description=description, formatter_class=RawTextHelpFormatter,add_help=True)
parser.add_argument("-db", "--SNP", required=True,
                    help="File with the SNP")
parser.add_argument("-g", "--genotype", required=True,
                    help="File with the mutations table")
parser.add_argument("-o", "--output", required=True,
                    help="Output file")


def main():

    args = parser.parse_args()

    dbSNP_path = args.phenotype
    genotype_path = args.genotype
    output_path = args.output
    n = args.n


    # dbSNP_path = "/genomics/users/juanluis/dbSNP144.TEST.tab"
    # genotype_path = "/genomics/users/juanluis/mutations_tcga_substitution_formatted.tsv.mut.out.sorted.TEST"
    # output_path = "/genomics/users/juanluis/mutations_formatted.TEST"
    # n = 2

    # 1. Load the dbSNP file
    logger.info("Loading " + dbSNP_path + "...")
    # dbSNP = pd.read_table(dbSNP_path, delimiter="\t")
    # dbSNP.columns = ['id','chr', 'start', 'end', 'id', 'number1', 'strand', 'original',
    #                     'mutation', 'ori_mut','info','unknown','number1','number2', 'id2', 'id3', 'number3','info2',
    #                  'gene','number4','0','1','2','3','4','5']
    logger.info("Creating dictionary...")
    dbSNP_dict = {}
    for line in open(dbSNP_path):
        tokens = line.rstrip().split("\t")
        id = tokens[1]+"_"+tokens[2]+"_"+tokens[3]
        dbSNP_dict[id] = tokens[9]



    # 2. We are gonna split the mutations table in n pieces and run a thread per each piece


    # # 3. Load the dbSNP file
    # logger.info("Loading " + genotype_path + "...")
    # # genotype = pd.read_table(genotype_path, delimiter="\t")
    # # genotype.columns = ['chr', 'start', 'end', 'cancer_type', 'id', 'number1', 'number2', 'number3', 'original',
    # #                     'mutation','score','p_value','chr2','start2', 'end2', 'id2', '.','strand']
    #
    # # 4. For each mutation in genotype, look if that mutation appears in dbSNP
    # logger.info("Looking for mutations...")
    #
    # inFileData = [line.rstrip().split("\t") for line in open(genotype_path)]
    #
    # for rowItems in inFileData:
    #     #Look for the mutation in the dbSNP file
    #     mutation = rowItems[9]
    #     chr = rowItems[0]
    #     start = rowItems[1]
    #     end = rowItems[2]
    #     # TODO: terminar
    #     # row = (dbSNP.loc[dbSNP['chr'] == chr])
    #     row = dbSNP.loc[dbSNP['chr'] == chr & dbSNP['start'] == start & dbSNP['end'] == end]












    #
    #
    #
    #
    # print("Starting execution: "+time.strftime('%H:%M:%S'))
    #
    # print("Loading dbSNP...")
    # dbSNP = pd.read_table("/projects_rg/Annotation/dbSNP/dbSNP144_part1.tab", delimiter="\t")
    #
    # # print(dbSNP)
    #
    # bashCommand = "ls /projects_rg/SCLC_cohorts/George/data/Mutation_files/*_mutcall_filtered.bed"
    # bed_files = os.popen(bashCommand, "r")
    #
    # for line in bed_files:
    #
    #     print("Loading file: " + line.rstrip() + "...\n")
    #
    #     mutation = pd.read_table(line.rstrip(), header=None, delimiter="\t")
    #     columns = ['chr', 'start', 'end', 'name', 'score', 'expected', 'observed', 'status', 'others']
    #     mutation.columns = columns
    #
    #     print("Merge the tables...")
    #     merge_table = pd.merge(dbSNP,mutation,how='inner',left_on="name",right_on="name")
    #
    #     # Check if the mutations (column 6) are included in the observed cases for each SNP (column observed)
    #     columns2 = ['chr', 'start', 'end', 'name', 'score_y', 'expected', 'observed_y', 'status', 'others', 'observed_x']
    #     df = pd.DataFrame(index=xrange(0, len(merge_table.index)), columns=columns2)
    #
    #     cont = 0
    #
    #     for x in xrange(0, len(merge_table.index)):
    #         if(merge_table["observed_y"][x] not in merge_table["observed_x"][x]):
    #             df.ix[cont] = merge_table.ix[x][['chr', 'start', 'end', 'name', 'score_y', 'expected', 'observed_y', 'status', 'others', 'observed_x']]
    #             cont = cont + 1
    #
    #     df = df[pd.notnull(df['chr'])]
    #
    #     #Save the file
    #     print("Saving results...")
    #     df.to_csv(line.rstrip()[:-4]+"_part1.bed", sep="\t")
    #
    # print("End of execution: "+time.strftime('%H:%M:%S'))




if __name__ == '__main__':
    try:
        main()
        logger.info("Done.")


    except Exception as error:
        logger.error(repr(error))
        logger.error('Aborting execution')
        exit(1)
