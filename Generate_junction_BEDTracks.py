"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

Generate_junction_BEDTracks.py: Generate bed tracks for visualizing the information in the genome browser of the final results
"""

import sys
import time
from argparse import ArgumentParser, RawTextHelpFormatter

import pandas as pd

description = \
    "Description:\n\n" + \
    "generate bed tracks for visualizing the information in the genome browser of the final results\n"

parser = ArgumentParser(description=description, formatter_class=RawTextHelpFormatter,
                        add_help=True)
parser.add_argument("-p", "--psi_samples", required=True,
                    help="PSI of the clustered junctions.")
parser.add_argument("-o", "--output_folder", required=True, help="Output folder")

def main():

    args = parser.parse_args()

    try:
        print("Starting execution: "+time.strftime('%H:%M:%S')+"\n")

        # 1. Load the file with the psi_samples
        print("Loading "+args.psi_samples+"...")
        psi_samples = pd.read_table(args.psi_samples, delimiter="\t")
        # psi_samples = pd.read_table("/genomics/users/juanluis/FastQTL_analysis/SCLC/Junctions/data/INTRON/psi_all_samples.txt", delimiter="\t")

        # 2. Generate junction_id tracks
        print("Generating junction_id tracks...")

        # Create the output file
        path = args.output_folder + "/Junction_BED_tracks.bed"
        # path = "/home/juanluis/Desktop/Junction_BED_track.bed"
        output_file = open(path, 'w')

        df_aux = psi_samples[['chr', 'start', 'end', 'Index']]
        output_file.write("track name=Cluster_Junctions description=\"Cluster junctions id info\" color=160,160,160\n")
        df_aux.to_csv(output_file, sep="\t", index=False, header=False, mode='a')

        # 3. Close the file handler
        print("Saved " + path)
        output_file.close()

        print("Done. Exiting program. "+time.strftime('%H:%M:%S')+"\n\n")

        exit(0)

    except Exception:
        print(sys.exc_info()[0])
        sys.exit(1)


if __name__ == '__main__':
    main()