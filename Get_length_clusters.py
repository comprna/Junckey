"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

Get_length_clusters.py: Given the file with all the clusters, get the start and end of each cluster
"""

import sys
import time
from argparse import ArgumentParser, RawTextHelpFormatter

import pandas as pd

description = \
    "Description:\n\n" + \
    "Given the file with all the clusters, get the start and end of each cluster\n"

parser = ArgumentParser(description=description, formatter_class=RawTextHelpFormatter,
                        add_help=True)
parser.add_argument("-p", "--psi_junctions", required=True,
                    help="PSI of the clustered junctions.")
parser.add_argument("-o", "--output_folder", required=True, help="Output folder")

def main():

    args = parser.parse_args()

    try:
        print("Starting execution: "+time.strftime('%H:%M:%S')+"\n")

        # 1. Load the file with the psi_junctions
        print("Loading " + args.psi_junctions + "...")
        psi_junctions = pd.read_table(args.psi_junctions, delimiter="\t")

        # 2. Iterate trough the psi_junctions file getting the start and end of each cluster
        print("Getting cluster sizes...")
        cluster_start, cluster_end, cluster_chr = {}, {}, {}
        for i in range(len(psi_junctions)):
            # print("Linea: "+i+" --> "+psi_junctions["cluster"][i])
            # input()
            #If the cluster is not in the dictionaries, initialize the values
            if (psi_junctions["cluster"][i] not in cluster_start.keys()):
                cluster_chr[psi_junctions["cluster"][i]] = psi_junctions["chr"][i]
                cluster_start[psi_junctions["cluster"][i]] = psi_junctions["start"][i]
                cluster_end[psi_junctions["cluster"][i]] = psi_junctions["end"][i]
            # If not, compare the start and the end with the ones in the dictionaries
            # If they are greater or smaller, update the values
            else:
                if(cluster_start[psi_junctions["cluster"][i]] > psi_junctions["start"][i]):
                    cluster_start[psi_junctions["cluster"][i]] = psi_junctions["start"][i]
                if(cluster_end[psi_junctions["cluster"][i]] < psi_junctions["end"][i]):
                    cluster_end[psi_junctions["cluster"][i]] = psi_junctions["end"][i]
                if(cluster_chr[psi_junctions["cluster"][i]] != psi_junctions["chr"][i]):
                    print("Different chromosomes in the same cluster!!"+cluster_chr[psi_junctions["cluster"][i]]+" and "+
                          psi_junctions["chr"][i])

        # 3. Create the output file and output the results
        print("Saving results...")
        path = args.output_folder + "/length_clusters.tab"
        output_file = open(path, 'w')

        for key in sorted(cluster_start.keys()):
            output_file.write(str(cluster_chr[key])+"\t"+str(cluster_start[key])+"\t"+str(cluster_end[key])+"\t"+key+"\n")

        # 4. Close the file handler
        print("Saved " + path)
        output_file.close()

        print("Done. Exiting program. "+time.strftime('%H:%M:%S')+"\n\n")

        exit(0)

    except Exception as error:
        print('ERROR: ' + repr(error))
        print("Aborting execution")
        sys.exit(1)


if __name__ == '__main__':
    main()