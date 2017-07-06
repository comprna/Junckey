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
#	 arg[3] --> name of the output final file


junctions_file=$1
gtf_dir=$2
output_file=$3

echo "Starting execution. "$(date)

#Export this library for using R-3.3.2
export LD_LIBRARY_PATH=/soft/devel/gcc-4.9.3/lib64:$LD_LIBRARY_PATH
#Use this version with pandas
export PATH=/soft/devel/python-2.7/bin:$PATH

#Store the path where the scripts are
MYSELF="$(readlink -f "$0")"
MYDIR="${MYSELF%/*}"

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
/soft/R/R-3.3.2/bin/Rscript "$MYDIR"/GenestoJunctions_v2.R "$path"/aux.bed "$path"/aux.sorted.enriched.unique.bed "$path"/aux.sorted.enriched.filtered.bed "$path"/aux.junction.type.bed "$path"/aux.sorted.geneAnnotated.bed

#4. Associate the genes of geneAnnotated.bed to the original junctions_file
python "$MYDIR"/change_gtf.py "$path"/aux.sorted.geneAnnotated.bed "$junctions_file" "$output_file"

#5. Remove the previous aux files
#rm "$path"/aux.bed
#rm "$path"/aux.sorted.bed
#rm "$path"/aux.sorted.enriched.bed
#rm "$path"/aux.sorted.enriched.filtered.bed
#rm "$path"/aux.sorted.enriched.unique.bed
#rm "$path"/aux.sorted.geneAnnotated.bed

echo "End of execution. "$(date)
exit 0




