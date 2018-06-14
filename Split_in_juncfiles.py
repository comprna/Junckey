"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

Split_in_juncfiles.py: Takes the file with the read counts of the junctions and all the samples
and generates a .junc file per sample for running LeafCutter

"""

import sys
import pandas as pd
import time
import os

def main():
    try:

        readCounts_path = sys.argv[1]
        # readCounts_path = "/projects_rg/Annotation/Junctions/test.tab"

        # 1. Load the junction file with pandas
        print("Loading phenotype...")
        readCounts_file = pd.read_table(readCounts_path, delimiter="\t")
        path = readCounts_path.split("/")
        del path[-1]
#        path2 = "/".join(path)+"/Junc_files"
        path2 = sys.argv[2]

        # 2. Per column, we will create a data frame and save it
        #Create the directory, if it doesn't exist
        if not os.path.exists(path2):
            os.makedirs(path2)
        # Open a file for putting the location of each file
        path_index = path2 + "/index_juncfiles.txt"
        index_file = open(path_index, "w")
        for i in range(8,len(readCounts_file.columns)):
            # print(i)
            list = [1,2,3,4]
            list.insert(3, i)
            aux_df = readCounts_file.iloc[:,list]

            #Add an extra column with dots and resort the columns
            aux_df['aux'] = "."
            cols = aux_df.columns.tolist()
            cols2 = cols[0:3] + cols[5].split(" ") + cols[3:5]
            aux_df = aux_df[cols2]

            idSample = readCounts_file.columns.values[i]
            nameFile = path2 + "/" + idSample + ".junc"

            #Save the dataframe
            print("Creating files "+nameFile+"...")
            aux_df.to_csv(nameFile, sep="\t", index=False,  float_format='%.f', header=False)
            #Save the path to each junc file in an external text file
            index_file.write(nameFile+"\n")

        index_file.close()
        print("Done. Exiting program. "+time.strftime('%H:%M:%S')+"\n\n")

        exit(0)

    except Exception as error:
        print('\nERROR: ' + repr(error))
        print("Aborting execution")
        sys.exit(1)


if __name__ == '__main__':
    main()
