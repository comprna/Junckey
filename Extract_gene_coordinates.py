"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

Extract_gene_coordinates.py: Given an annotation, extracts the positions for each gene

"""

import logging

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


def main():

    try:

        logger.info('Starting execution')

        # file_path = sys.argv[1]
        # output_path = sys.argv[2]

        file_path = "/projects_rg/SUPPA2/general_files/Homo_sapiens.GRCh37.75.formatted.V2.gtf"
        output_path = "/projects_rg/SUPPA2/general_files/gene_coordinates.tab"

        # 1. Read the annotation saving the coordinates for each gene

        logger.info('Reading annotation...')

        dict_start, dict_end,  dict_chr, dict_strand = {}, {}, {}, {}
        with open(file_path) as f:
            for line in f:
                tokens = line.rstrip().split("\t")
                gene_id = tokens[8].split(";")[0][8:]
                # If the gene is not in the dictionaries, initialize the values
                if (gene_id not in dict_start.keys()):
                    dict_start[gene_id] = tokens[3]
                    dict_end[gene_id] = tokens[4]
                    dict_chr[gene_id] = tokens[0]
                    dict_strand[gene_id] = tokens[6]
                # If not, compare the start and the end with the ones in the dictionaries
                # If they are greater or smaller, update the values
                else:
                    if (dict_start[gene_id] > tokens[3]):
                        dict_start[gene_id] = tokens[3]
                    if (dict_end[gene_id] < tokens[3]):
                        dict_end[gene_id] = tokens[4]

        # 2. Create the output file and output the results
        logger.info('Saving results...')
        output_file = open(output_path, 'w')

        for key in sorted(dict_start.keys()):
            output_file.write(key + "\t" + str(dict_start[key]) + "\t" + str(dict_end[key]) + "\t" +
                              str(dict_chr[key]) + "\t" + str(dict_strand[key]) + "\n")

        # 3. Close the file handler
        logger.info('Saved ' + output_path)
        output_file.close()

        logger.info('Done. Exiting program.')

        exit(0)

    except Exception as error:
        logger.error('\nERROR: ' + repr(error))
        logger.error('Aborting execution')
        exit(1)


if __name__ == '__main__':
    main()