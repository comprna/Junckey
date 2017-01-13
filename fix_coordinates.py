"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

fix_coordinates.py: Takes any file and transform the start and end coordinates it to integer
The user must provide the position in the file of this two columns (first column will be 1)

"""

import pandas as pd
import sys, time

try:

    print("Starting execution: " + time.strftime('%H:%M:%S'))

    file_path = sys.argv[1]
    pos_start = int(sys.argv[2])+1
    pos_end = int(sys.argv[3])+1
    output_path = sys.argv[4]

    # file_path = "/projects_rg/Annotation/Junctions/test.tab"
    # pos_start = 2
    # pos_end = 3
    # output_path = "/projects_rg/Annotation/Junctions/test2.tab"

    # Load the file
    print("Loading file "+file_path)
    file = pd.read_table(file_path, delimiter="\t")

    # Transform to int the start and end coordinates
    file.ix[:, pos_start] = file.ix[:, pos_start].astype(int)
    file.ix[:, pos_end] = file.ix[:, pos_end].astype(int)

    #Save it
    print("Saving file "+output_path)
    file.to_csv(output_path, sep="\t", index=False)

    print("Done. Exiting program. " + time.strftime('%H:%M:%S') + "\n\n")
    exit(0)

except Exception as error:
    print('\nERROR: ' + repr(error))
    print("Aborting execution")
    sys.exit(1)
