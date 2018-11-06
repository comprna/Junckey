"""
@authors: Juan L. Trincado
@email: juanluis.trincado@upf.edu

GenestoJunctions.py: The next code will get the unique genes associated to each junction and will associate this list of genes to each junctions in the original bed file
Additionally, we will study the type of each junction (1: Annotated, 2: New connection, 3: 5ss, 4: 3ss, 5: New junction)
arg[1]: Input file --> SJ.out.enriched.filtered.bed: file with the exons that overlaps exactly with the junction
arg[2]: Output file --> SJ.out.junction.type: output file with the list junction and the type of each junction

"""

import logging, sys
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


def consecutives_exons(dict):
    '''
    Check if in the dictionary there are two consecutive
    exons associated to the same transcript
    '''

    # For each key in the dict, sort the list
    for key in dict:
        list_exons = dict[key]
        sortedlist = []
        for x in sorted(list_exons): sortedlist.append(x)
        #Iterate the list, checking if there are consecutive exons
        for i in range(1,len(sortedlist)):
            if(int(sortedlist[i-1])==int(sortedlist[i])-1):
                return True
    return False


def main():

    try:

        print('\t\tGenestoJunctions.py: Starting')

        # Load the fasta file
        original_file_bed_filtered_path = sys.argv[1]
        output_path = sys.argv[2]

        # original_file_bed_filtered_path = "/projects_rg/test_Junckey/SAMPLE/SJ.out.enriched.filtered.bed"
        # output_path = "/projects_rg/test_Junckey/SAMPLE/SJ.out.junction.type.bed"

        # 1. Load the intersect file between the junctions and the annotation
        original_file_bed_filtered = pd.read_table(original_file_bed_filtered_path, delimiter="\t", header=None)
        original_file_bed_filtered.columns = ['chr', 'start', 'end', 'id', 'score', 'strand', 'annotated',
                                              'chr2', 'info1', 'info2', 'start2', 'end2', 'dot', 'strand2',
                                              'dot2', 'large_info', 'score2']

        # 2. Get the transcript and exon_number info
        # transcript_id = original_file_bed_filtered['large_info'].apply(lambda x: x.split(";")[1][16:31]).tolist()
        transcript_id = original_file_bed_filtered['large_info'].apply(lambda x: x.split("transcript_id")[1].split(";")[0].strip().replace('\"','')).tolist()
        # exon_number = original_file_bed_filtered['large_info'].apply(lambda x: x.split(";")[2].split("\"")[1]).tolist()
        exon_number = original_file_bed_filtered['large_info'].apply(lambda x: x.split("exon_number")[1].split(";")[0].strip().replace('\"','')).tolist()

        #Iterate over the genotype file
        flag_Anno, flag_5s, flag_3s= 0, 0, 0
        transcript_dict = {}
        id = ""
        output_file = open(output_path, 'w')
        for i in range(len(original_file_bed_filtered)):
            percentage = str(round(i*100/len(original_file_bed_filtered),3))+ "%"
            sys.stdout.write("\r%s" % percentage)
            sys.stdout.flush()
            line = original_file_bed_filtered.iloc[i,]
            if(i==0):
                id = original_file_bed_filtered.iloc[i,3]
            elif(id!=original_file_bed_filtered.iloc[i,3]):
                # # Case 1: Annotated junction
                # if(flag_Anno==1):
                #     output_file.write(id+"\t1\n")
                # # Case 2: New connection (from annotated exons)
                # elif(flag_5s==1 & flag_3s==1):
                #     #If there are two exons folowwing each other, then it's a case 1
                #     if(consecutives_exons(transcript_dict)):
                #         output_file.write(id + "\t1\n")
                #     else:
                #         output_file.write(id+"\t2\n")
                # Case 1: Annotated junction

                if(flag_5s==1 & flag_3s==1):
                    #If there are two exons folowwing each other, then it's a case 1
                    if(consecutives_exons(transcript_dict)):
                        # Case 1: Annotated junction
                        output_file.write(id + "\t1\n")
                    else:
                        # Case 2: New connection (from annotated exons)
                        output_file.write(id+"\t2\n")
                # Case 3: A5ss
                elif (flag_5s == 1 and flag_3s == 0):
                    output_file.write(id+"\t3\n")
                # Case 4: A3ss
                elif (flag_5s == 0 and flag_3s == 1):
                    output_file.write(id+"\t4\n")
                # Case 0: Not studied
                else:
                    output_file.write(id+"\t \n")
                id = original_file_bed_filtered.iloc[i, 3]
                flag_Anno, flag_5s, flag_3s = 0, 0, 0
                transcript_dict = {}
            # Check the new line
            # if(original_file_bed_filtered.iloc[i,6]==1):
            #     flag_Anno = 1
            # elif (original_file_bed_filtered.iloc[i,1]==original_file_bed_filtered.iloc[i,11]-1):
            if (original_file_bed_filtered.iloc[i, 1] == original_file_bed_filtered.iloc[i, 11] - 1):
                flag_5s = 1
                #Save the transcript id and the exon number
                #If the key already exists, add it to the list of exons
                if(transcript_id[i] in transcript_dict):
                    transcript_dict[transcript_id[i]].append(exon_number[i])
                #If the key doesn't exist, create a new list
                else:
                    transcript_dict[transcript_id[i]] = [exon_number[i]]
            elif (original_file_bed_filtered.iloc[i, 2] == original_file_bed_filtered.iloc[i, 10]):
                flag_3s = 1
                #Save the transcript id and the exon number
                #If the key already exists, add it to the list of exons
                if(transcript_id[i] in transcript_dict):
                    transcript_dict[transcript_id[i]].append(exon_number[i])
                #If the key doesn't exist, create a new list
                else:
                    transcript_dict[transcript_id[i]] = [exon_number[i]]

        percentage = "100%\n"
        sys.stdout.write("\r%s" % percentage)

        # 3. Close the file handler
        print('\t\tGenestoJunctions.py: Saved ' + output_path)
        output_file.close()

        print('\t\tGenestoJunctions.py: Finish')

        exit(0)

    except Exception as error:
        logger.error('\nERROR: ' + repr(error))
        logger.error('\t\tGenestoJunctions.py: Aborting execution')
        exit(1)


if __name__ == '__main__':
    main()