#!/usr/bin/env bash

#
# ==============================================================================================
# get_total_mapped_reads:
#
# Description: Generate a tab file with the total mapped reads per sample from STAR
#
# Input: arg[1] --> path to the STAR output file (one folder per sample)
# Output: arg[1]/totalMappedReads.tab
# ==============================================================================================


io_dir=$1

echo "Starting execution. "$(date)

touch $(echo $io_dir)/totalMappedReads_CULO.tab
for sample in $(ls "$io_dir"/*/Log.final.out);do
	var1=$(grep "Uniquely mapped reads number" $(echo $sample) | cut -d'|' -f2)
	id_sample=$(echo $sample | rev | cut -d'/' -f2 | rev)
	echo -e $(echo $id_sample)'\t'$(echo $var1) >> $(echo $io_dir)/totalMappedReads.tab
done

echo "Generated $io_dir/totalMappedReads.tab. Done. "$(date)
