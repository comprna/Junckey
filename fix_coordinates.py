"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

fix_coordinates.py: Takes any file and transform the id, start and end coordinates it to integer
The user must provide the position in the file of this three columns (first column will be 1)

"""

import sys, time

try:

    print("Starting execution: " + time.strftime('%H:%M:%S'))

    file_path = sys.argv[1]
    pos_id = int(sys.argv[2])-1
    pos_start = int(sys.argv[3])-1
    pos_end = int(sys.argv[4])-1
    output_path = sys.argv[5]

    # file_path = "/projects_rg/Annotation/Junctions/test.tab"
    # pos_start = 2
    # pos_end = 3
    # output_path = "/projects_rg/Annotation/Junctions/test2.tab"

    print("Formatting file " + file_path + "...")

    outFile = open(output_path, 'w')

    # Load the file
    with open(file_path) as f:
        outFile.write(next(f))
        for line in f:
            tokens = line.rstrip().split("\t")
            id = tokens[pos_id].split(";")
            id[1] = str(int(float(id[1])))
            id[2] = str(int(float(id[2])))
            tokens[pos_id] = ";".join(id)
            tokens[pos_start] = str(int(float(tokens[pos_start])))
            tokens[pos_end] = str(int(float(tokens[pos_end])))
            new_line = "\t".join(tokens)
            outFile.write(new_line + "\n")

    outFile.close()

    print("Saved " + output_path)

    print("Done. Exiting program. " + time.strftime('%H:%M:%S') + "\n\n")
    exit(0)

except Exception as error:
    print('\nERROR: ' + repr(error))
    print("Aborting execution")
    sys.exit(1)
