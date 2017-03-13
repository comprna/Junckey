"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

dbSNP_mutations_TCGA.py: given a list of mutations, we will check which
ones are in the dbSNP database and filter out
"""

import pandas as pd
from argparse import ArgumentParser, RawTextHelpFormatter
# from threading import Thread

import logging, sys, time, random

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

parser = ArgumentParser(description=description, formatter_class=RawTextHelpFormatter, add_help=True)
parser.add_argument("-db", "--SNP", required=True, help="File with the SNP")
parser.add_argument("-g", "--genotype", required=True, help="File with the mutations table")
# parser.add_argument("-n", "--n", required=False, default=1, help="Number of threads")
parser.add_argument("-o", "--output", required=True, help="Output file")


#
# class MyThread(Thread):
#     def __init__(self, val):
#         ''' Constructor. '''
#
#         Thread.__init__(self)
#         self.val = val
#
#     def run(self):
#         for i in range(1, self.val):
#             print('Value %d in thread %s' % (i, self.getName()))
#
#             # Sleep for random time between 1 ~ 3 second
#             secondsToSleep = random.randint(1, 5)
#             print('%s sleeping fo %d seconds...' % (self.getName(), secondsToSleep))
#             time.sleep(secondsToSleep)

def main():

    args = parser.parse_args()
    dbSNP_path = args.SNP
    genotype_path = args.genotype
    output_path = args.output
    # n = args.n
    output_discarded_path = "/".join(output_path.split("/")[:-1]) + "/discarded.tab"

    print(output_discarded_path)


    # dbSNP_path = "/genomics/users/juanluis/dbSNP144.TEST.tab"
    # genotype_path = "/genomics/users/juanluis/mutations_tcga_substitution_formatted.tsv.mut.out.sorted.TEST"
    # output_path = "/genomics/users/juanluis/mutations_formatted.TEST"
    # n = 2

    # 1. Load the dbSNP file
    logger.info("Loading " + dbSNP_path + "...")
    dbSNP_dict = {}
    for line in open(dbSNP_path):
        tokens = line.rstrip().split("\t")
        id = tokens[1]+"_"+tokens[2]+"_"+tokens[3]
        mutation_list = tokens[9].split("/")
        #If the id exists, add this mutation to the list (if it doesn't exist)
        if id not in dbSNP_dict:
            dbSNP_dict[id] = mutation_list
        else:
            # logger.info("Repeated SNP in " + id)
            dictionary_mutation_list = dbSNP_dict[id]
            for x in mutation_list:
                if (x not in dictionary_mutation_list):
                    dbSNP_dict[id].append(x)

    logger.info("Scanning "+genotype_path+"...")

    #Create a new output file
    outFile = open(output_path, 'w')
    out_discardedFile = open(output_discarded_path, 'w')


    inFileData = [line.rstrip().split("\t") for line in open(genotype_path)]
    cont = 0

    for i,rowItems in enumerate(inFileData):
        percentage = "Scanning dbSNP file......" + str(round(i * 100 / len(inFileData), 3)) + "%"
        sys.stdout.write("\r%s" % percentage)
        sys.stdout.flush()
        id_genotype = rowItems[0]+"_"+rowItems[1]+"_"+rowItems[2]
        mutation_genotype = rowItems[9]
        # If the mutation is the same as in dbSNP, don't output this line
        if id_genotype in dbSNP_dict:
            dictionary_mutation_list = dbSNP_dict[id_genotype]
            if (mutation_genotype in dictionary_mutation_list):
                cont = cont + 1
                out_discardedFile.write("\t".join(rowItems) + "\n")
                continue
        outFile.write("\t".join(rowItems) + "\n")

    percentage = "Scanning dbSNP file......" + "100%\n"
    sys.stdout.write("\r%s" % percentage)

    # 3. Close the output file
    logger.info(str(cont) + " mutations filtered")
    logger.info("Saved results in " + output_path)
    outFile.close()
    out_discardedFile.close()

if __name__ == '__main__':
    try:
        main()

    except Exception as error:
        logger.error(repr(error))
        logger.error('Aborting execution')
        exit(1)
