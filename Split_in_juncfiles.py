#This script take the junctions with the read counts and generate a .junc file per column

#arg[1]: path to the STAR output file (one folder per sample)

__author__ = 'juanluis'

import sys
import pandas as pd
import os
import shlex
import time
from copy import deepcopy

def main():
    try:

        # 1. Load the junction file with pandas
        print("Loading phenotype...")
        junctions = pd.read_table(sys.argv[1], delimiter="\t")
        path = sys.argv[1].split("/")
        del path[-1]
        path2 = "/".join(path)

        # 2. Per column, we will create a data frame and save it
        # Open a file for putting the location of each file
        path_index = path2 + "/index_juncfiles.txt"
        index_file = open(path_index, "w")
        for i in range(8,len(junctions.columns)):
            list = [1,2,3,4]
            list.insert(3, i)
            aux_df = junctions.iloc[:,list]

            #Add an extra column with dots and resort the columns
            aux_df['aux'] = "."
            cols = aux_df.columns.tolist()
            cols2 = cols[0:3] + cols[5].split(" ") + cols[3:5]
            aux_df = aux_df[cols2]

            idSample = junctions.columns.values[i]
            nameFile = path2 + "/" + idSample + ".junc"
            # nameFile = "/projects_rg/Annotation/Junctions/Junc_files/" + idSample + ".junc"
            #Save the dataframe
            print("Creating files "+nameFile+"...")
            aux_df.to_csv(nameFile, sep="\t", index=False,  float_format='%.f', header=False)
            #Save the path to each junc file in an external text file
            index_file.write(nameFile+"\n")

        index_file.close()
        print("Done. Exiting program. "+time.strftime('%H:%M:%S')+"\n\n")

        exit(0)

    except Exception:
        sys.exit(1)


if __name__ == '__main__':
    main()
