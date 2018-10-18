import os, sys, glob, math

# TODO The rpkm.tab generation is actually commented because some error converting to int, fix this

try:
    inFilePattern = sys.argv[1]+"/*/SJ.out.geneAnnotated.bed"
    # totalMappedReadsFilePath = sys.argv[1]+"/totalMappedReads.tab"
    # averageLengthFilePath = sys.argv[1]+"/averageLength.tab"
    outCountsFilePath = sys.argv[2]+"/readCounts.tab"
    outCountsNormFilePath = sys.argv[2]+"/readNormCounts.tab"
    # outRpkmFilePath = sys.argv[2]+"/rpkm_final.tab"
    totalJunctionReadsPath = sys.argv[3]

    # inFilePattern = "/projects_rg/SCLC_cohorts/George/STAR/v2/*/SJ.out.geneAnnotated.bed"
    # # totalMappedReadsFilePath = "/projects_rg/Bellmunt/STAR/TEST/totalMappedReads.tab"
    # # averageLengthFilePath = "/projects_rg/Bellmunt/STAR/TEST/averageLength.tab"
    # totalJunctionReadsPath = "/projects_rg/SCLC_cohorts/tables/splice_junctions_mapped_STAR_all_cohorts.tab"
    # outCountsFilePath = "/projects_rg/SCLC_cohorts/George/STAR/v2/readCounts_v2.tab"
    # outCountsNormFilePath = "/projects_rg/SCLC_cohorts/George/STAR/v2/normReadCounts.tab"
    # # outRpkmFilePath = "/projects_rg/Bellmunt/STAR/TEST/rpkm_final.tab"

    # Load the mapped junction reads
    totalJunctionReads = {}

    with open(totalJunctionReadsPath) as f:
        for line in f:
            id_sample = line.rstrip().split("\t")[0].split("/")[1]
            spliced_reads = int(line.rstrip().split("\t")[1])
            if(id_sample not in totalJunctionReads):
                totalJunctionReads[id_sample] = spliced_reads
            else:
                pass

    inFilePaths = glob.glob(inFilePattern)

    print("\tpool_results.py: Pooling data...")

    metaDict = {}
    countDict, countNormDict = {}, {}
    headerItems = None
    samples = []
    for inFilePath in inFilePaths:
        inFileData = [line.rstrip().split("\t") for line in open(inFilePath)]
        sampleID = os.path.basename(os.path.dirname(inFilePath))
        print("\t\tpool_results.py: Processing "+sampleID+"...")

        if inFilePath == inFilePaths[0]:
            headerItems = inFileData.pop(0)
            headerItems = headerItems[:4] + headerItems[5:]
        else:
            inFileData.pop(0)

        #headerItems.append(sampleID)
        samples.append(sampleID)
        if(sampleID in totalJunctionReads):
            totalJunctionReads_aux = totalJunctionReads[sampleID]
        else:
            print("\t\tpool_results.py: " + sampleID + " not in STAR mapped reads")
            totalJunctionReads_aux = -1

        for rowItems in inFileData:
            metaItems = rowItems[:4] + rowItems[5:]
            rowID = metaItems[0]
            counts = rowItems[4]

            #Normalize the counts by the total number of junction reads and multiply by 10⁶
            if(counts!=0 and totalJunctionReads_aux!=-1):
                normcounts = str((int(counts)/totalJunctionReads_aux)*1000000)
            else:
                normcounts = 0

            if not rowID in metaDict:
                metaDict[rowID] = metaItems

            if not rowID in countDict:
                countDict[rowID] = {}

            if not rowID in countNormDict:
                countNormDict[rowID] = {}

            countDict[rowID][sampleID] = counts
            countNormDict[rowID][sampleID] = normcounts

    for item in sorted(samples):
        headerItems.append(item)

    # totalMappedReads = {}
    # for line in open(totalMappedReadsFilePath):
    #     lineitems = line.rstrip().split("\t")
    #     totalMappedReads[lineitems[0]] = lineitems[1]
    #
    # averageLength = {}
    # for line in open(averageLengthFilePath):
    #     lineitems = line.rstrip().split("\t")
    #     averageLength[lineitems[0]] = lineitems[1]

    outCountsFile = open(outCountsFilePath, 'w')
    outCountsFile.write("\t".join(headerItems) + "\n")

    outNormCountsFile = open(outCountsNormFilePath, 'w')
    outNormCountsFile.write("\t".join(headerItems) + "\n")

    # outRpkmFile = open(outRpkmFilePath, 'w')
    # outRpkmFile.write("\t".join(headerItems) + "\n")

    print("\tpool_results.py: There are %d genes to calculate" % len(metaDict))
    print("")

    i = 1
    for rowID in sorted(metaDict):
        sys.stdout.write("\rCurrently on: %d" % i,)
        sys.stdout.flush()
        outCountsRow = list(metaDict[rowID])
        outNormCountsRow = list(metaDict[rowID])
        # outRpkmRow = list(metaDict[rowID])
        for sampleID in headerItems[8:]:
            sampleCount = "0"
            sampleNormCount = "0"
            # rpkm = "0"
            if sampleID in countDict[rowID]:
                sampleCount = str(countDict[rowID][sampleID])
                # tmr = float(totalMappedReads[sampleID])
                # al = float(averageLength[sampleID])
                # rpkm = "%.9f" % ((math.pow(10,9) * float(sampleCount)) / (tmr * al))
            outCountsRow.append(sampleCount)
            if sampleID in countNormDict[rowID]:
                sampleNormCount = str(countNormDict[rowID][sampleID])
                # tmr = float(totalMappedReads[sampleID])
                # al = float(averageLength[sampleID])
                # rpkm = "%.9f" % ((math.pow(10,9) * float(sampleCount)) / (tmr * al))
            outNormCountsRow.append(sampleNormCount)
            # outRpkmRow.append(rpkm)
        outCountsFile.write("\t".join(outCountsRow) + "\n")
        outNormCountsFile.write("\t".join(outNormCountsRow) + "\n")
        # outRpkmFile.write("\t".join(outRpkmRow) + "\n")
        i += 1

    i -= 1
    sys.stdout.write("\t\rCurrently on: %d\n" % i, )
    outCountsFile.close()
    print("\tpool_results.py: Generated file "+outCountsFilePath)
    outNormCountsFile.close()
    print("\tpool_results.py: Generated file "+outCountsNormFilePath)
    # outRpkmFile.close()
    # print("pool_results.py: Generated file " + outRpkmFilePath)

except Exception as error:
    print('\nERROR: ' + repr(error))
    print("\tpool_results.py: Aborting execution")
    sys.exit(1)
