#!/bin/sh
# change_gtf:
#
# Description: This script is based on the pipeline of format_STAR_output.sh
#		It takes any file with a list of junctions (i.e. readCounts.tab) and a gtf 
#		annotation and recalculate the type of the junctions compared to this gtf
#		and the overlapping with genes. Per junction, we will obatin the overlap 
#		with genes and the type of the junction:
#				1: Fully annotated junction
#				2: Junction overlapping with known exons, but new connection
#				3: Alternative donor site
#				4: Alternative acceptor site
#				5: Novel junction, neither donor nor acceptor site is annotated
#
# Input: arg[1] --> path to the junctions file (the first column sholud be the id of the junctions)
#	 arg[2] --> path to the GTF annotation file
#


junctions_file=$1
gtf_dir=$2
output_file=$3

echo "Starting execution. "$(date)

#Export this library for using R-3.3.2
export LD_LIBRARY_PATH=/soft/devel/gcc-4.9.3/lib64:$LD_LIBRARY_PATH

#1. Extract from the junctions_file the coordinates of the file and create a bed file
path=$(dirname "${junctions_file}")
awk -v OFS='\t' 'FNR > 1 {print $2,$3,$4,$1,"0",$5, $6}' "$junctions_file" > "$path"/aux.bed

#2. Sort the bed file
/soft/bio/sequence/bedtools-2.26/bin/sortBed -i "$path"/aux.bed > "$path"/aux.sorted.bed
/soft/bio/sequence/bedtools-2.26/bin/intersectBed -wao -a "$path"/aux.sorted.bed -b "$gtf_dir" -s > "$path"/aux.sorted.enriched.bed

#3. Format the enriched.bed file for those that exactly match with the junctions and associate the info to the original bed file
echo "Recovering gene and junction type... "
#Get the junctions that match with the annotation
awk -F"\t" '$17 == "1" { print }' "$path"/aux.sorted.enriched.bed > "$path"/aux.sorted.enriched.filtered.bed
#Extract the unique values for the id and the associated gene
awk '{print $4,$17}' "$path"/aux.sorted.enriched.bed | sort -u > "$path"/aux.sorted.enriched.unique.bed
#Replace the junctions associated to genes "0" with a blank space
sed -i -e 's/ 0/ "";/g' "$path"/aux.sorted.enriched.unique.bed
#Associate the list of genes to each junction to the original bed file
/soft/R/R-3.3.2/bin/Rscript /projects_rg/SCLC_cohorts/scripts/GenestoJunctions.R "$path"/aux.bed "$path"/aux.sorted.enriched.unique.bed "$path"/aux.sorted.enriched.filtered.bed "$path"/aux.sorted.geneAnnotated.bed

#4. Associate the genes of geneAnnotated.bed to the original junctions_file
python /genomics/users/juanluis/comprna/Junckey/change_gtf.py "$path"/aux.sorted.geneAnnotated.bed "$junctions_file" "$path"/"$output_file"

echo "End of execution. "$(date)
exit 0












#Export this library for using R-3.3.2
export LD_LIBRARY_PATH=/soft/devel/gcc-4.9.3/lib64:$LD_LIBRARY_PATH

echo "Starting execution. "$(date)

#1. Convert the output file from STAR with the junctions to bed format
for sample in $(ls "$io_dir");do
	echo "Converting to BED $sample... "	
	/soft/R/R-3.3.2/bin/Rscript /projects_rg/SCLC_cohorts/scripts/STARtoBED.R "$io_dir"$(echo $sample)/SJ.out.tab "$io_dir"$(echo $sample)/SJ.out.bed
done

#2. Use bedtools for finding in which regions the junctions are falling in the annotation
#Sort the annotation file
echo "Sorting annotation file... "		
/soft/bio/sequence/bedtools-2.26/bin/sortBed -i $(echo $gtf_dir) >> ${gtf_dir:0:${#gtf_dir} - 4}.sorted.gtf

#Apply the intersection with the files sorted
for sample in $(ls "$io_dir");do
	echo "Enriching output $sample... "
	#Sort the bed file
	/soft/bio/sequence/bedtools-2.26/bin/sortBed -i "$io_dir"$(echo $sample)/SJ.out.bed >> "$io_dir"$(echo $sample)/SJ.out.sorted.bed
	/soft/bio/sequence/bedtools-2.26/bin/intersectBed -wao -a "$io_dir"$(echo $sample)/SJ.out.sorted.bed -b $(echo ${gtf_dir:0:${#gtf_dir} - 4}.sorted.gtf) -s >> "$io_dir"$(echo $sample)/SJ.out.enriched.bed
	#/soft/bio/sequence/bedtools-2.26/bin/intersectBed -wao -sorted -a "$io_dir"$(echo $sample)/SJ.out.sorted.bed -b $(echo ${gtf_dir:0:${#gtf_dir} - 4}.sorted.gtf) -s >> "$io_dir"$(echo $sample)/SJ.out.enriched.bed
done

#3. Format the enriched.bed file for those that exactly match with the junctions and associate the info to the original bed file
for sample in $(ls "$io_dir");do
	echo "Recovering gene and junction type with $sample... "
	#Get the junctions that match with the annotation
	awk -F"\t" '$17 == "1" { print }' "$io_dir"$(echo $sample)/SJ.out.enriched.bed > "$io_dir"$(echo $sample)/SJ.out.enriched.filtered.bed
	#Extract the unique values for the id and the associated gene
	awk '{print $4,$17}' "$io_dir"$(echo $sample)/SJ.out.enriched.bed | sort -u > "$io_dir"$(echo $sample)/SJ.out.enriched.unique.bed
	#Replace the junctions associated to genes "0" with a blank space
	sed -i -e 's/ 0/ "";/g' "$io_dir"$(echo $sample)/SJ.out.enriched.unique.bed
	#Associate the list of genes to each junction to the original bed file
	/soft/R/R-3.3.2/bin/Rscript /projects_rg/SCLC_cohorts/scripts/GenestoJunctions.R "$io_dir"$(echo $sample)/SJ.out.bed "$io_dir"$(echo $sample)/SJ.out.enriched.unique.bed "$io_dir"$(echo $sample)/SJ.out.enriched.filtered.bed "$io_dir"$(echo $sample)/SJ.out.geneAnnotated.bed
done

#4. Pool the reads from all the samples in one file
#echo "Gathering all files into one..."
#/soft/R/R-3.2.3/bin/Rscript /projects_rg/SCLC_cohorts/scripts/pool_results.R "$io_dir"

#NEW VERSION WITH POOL RESULTS ON PYTHON!!!!

#4. Format the Log.Final.out files
echo "Formatting Log.Final.out files..."
/soft/R/R-3.3.2/bin/Rscript /projects_rg/SCLC_cohorts/scripts/format_Log_STAR.R "$io_dir"

#5. Pool the reads from all the samples in one file
echo "Gathering all files into one..."
python /projects_rg/SCLC_cohorts/scripts/pool_results.py "$io_dir"

echo "End of execution. "$(date)
exit 0
