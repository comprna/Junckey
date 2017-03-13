"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

Get_length_clusters.py: Given the file with all the clusters, get the start and end of each cluster.
Optionally, the user can adjust a wider window for searching mutations before the start of the cluster
"""

import sys
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import pandas as pd

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
    "Given the file with all the clusters, get the start and end of each cluster\n"

parser = ArgumentParser(description=description, formatter_class=RawTextHelpFormatter,
                        add_help=True)
parser.add_argument("-p", "--psi_junctions", required=True,
                    help="PSI of the clustered junctions.")
parser.add_argument("-w", "--window", required=False, default=0,
                    help="Number of bp for looking for mutations before the start of the gene")
parser.add_argument("-o", "--output_folder", required=True, help="Output folder")

def main():

    args = parser.parse_args()

    psi_junctions_path = args.psi_junctions
    output_folder = args.output_folder
    window = args.window


    try:

        # 1. Load the file with the psi_junctions
        logger.info("Loading " + psi_junctions_path + "...")
        psi_junctions = pd.read_table(psi_junctions_path, delimiter="\t")

        # 2. Iterate trough the psi_junctions file getting the start and end of each cluster
        logger.info("Getting cluster sizes...")
        cluster_start, cluster_end, cluster_chr, cluster_strand = {}, {}, {}, {}
        for i in range(len(psi_junctions)):
            # print("Linea: "+i+" --> "+psi_junctions["cluster"][i])
            # input()
            #If the cluster is not in the dictionaries, initialize the values
            if (psi_junctions["cluster"][i] not in cluster_start.keys()):
                cluster_chr[psi_junctions["cluster"][i]] = psi_junctions["chr"][i]
                cluster_start[psi_junctions["cluster"][i]] = psi_junctions["start"][i]
                cluster_end[psi_junctions["cluster"][i]] = psi_junctions["end"][i]
                cluster_strand[psi_junctions["cluster"][i]] = psi_junctions["strand"][i]
            # If not, compare the start and the end with the ones in the dictionaries
            # If they are greater or smaller, update the values
            else:
                if(cluster_start[psi_junctions["cluster"][i]] > psi_junctions["start"][i]):
                    cluster_start[psi_junctions["cluster"][i]] = psi_junctions["start"][i]
                if(cluster_end[psi_junctions["cluster"][i]] < psi_junctions["end"][i]):
                    cluster_end[psi_junctions["cluster"][i]] = psi_junctions["end"][i]
                if(cluster_chr[psi_junctions["cluster"][i]] != psi_junctions["chr"][i]):
                    logger.error("Different chromosomes in the same cluster!!"+cluster_chr[psi_junctions["cluster"][i]]+" and "+
                          psi_junctions["chr"][i])
                if(cluster_strand[psi_junctions["cluster"][i]] != psi_junctions["strand"][i]):
                    logger.error("Different strans in the same cluster!!"+cluster_strand[psi_junctions["cluster"][i]]+" and "+
                          psi_junctions["strand"][i])

        # 3. If the user had specified a window size, update the values of the clusters
        if(window!=0):
            logger.info("Adding window shift...")
            for key in sorted(cluster_start.keys()):
                if(cluster_strand[key]=="+"):
                    cluster_start[key] = cluster_start[key] - window
                    if (cluster_start[key]<0):
                        cluster_start[key] = 0
                else:
                    cluster_end[key] = cluster_end[key] + window

        # 4. Create the output file and output the results
        logger.info("Saving results...")
        path = output_folder + "/length_clusters.tab"
        output_file = open(path, 'w')

        for key in sorted(cluster_start.keys()):
            output_file.write(str(cluster_chr[key])+"\t"+str(cluster_start[key])+"\t"+str(cluster_end[key])+"\t"+key+"\n")

        # 5. Close the file handler
        logger.info("Saved " + path)
        output_file.close()

        logger.info("Done. Exiting program.")

        exit(0)

    except Exception as error:
        logger.error(repr(error))
        logger.error("Aborting execution")
        sys.exit(1)


if __name__ == '__main__':
    main()