#!/bin/sh
# format_STAR_output_per_sample_slurm:
#
# Description: The next pipeline takes the junctions information generated with STAR and
#			pool all the information in one file. The output file will be the 
#			read counts per sample and per junction. Per junction, we will
#			obtain the overlap with genes and the type of the junction:
#				1: Fully annotated junction
#				2: Junction overlapping with known exons, but new connection
#				3: Alternative donor site
#				4: Alternative acceptor site
#				5: Novel junction, neither donor nor acceptor site is annotated
#
# This version accepts a sample and process just that sample
#
# Input: arg[1] --> path to the STAR output file (one folder per sample)
#	 arg[2] --> path to the GTF annotation file
#

#SBATCH --partition=short
#SBATCH --mem 5000

sample=$1
gtf_dir=$2
output_dir=$3
scripts_dir=$4

#Export this library for using R-3.3.2
#export LD_LIBRARY_PATH=/soft/devel/gcc-4.9.3/lib64:$LD_LIBRARY_PATH
module load R
module load RStudio
module load BEDTools
module load Python/2.7.11

echo "Starting execution. "$(date)
echo "Processing sample $sample..."

#Store the path where the scripts are
MYSELF="$(readlink -f "$0")"
MYDIR="${MYSELF%/*}"

#1. Convert the output file from STAR with the junctions to bed format
echo "Converting to BED $sample... "	
Rscript "$scripts_dir"/STARtoBED.R "$sample"/SJ.out.tab "$output_dir"/$(echo ${sample##*/})/SJ.out.bed

#2. Use bedtools for finding in which regions the junctions are falling in the annotation
echo "Enriching output $sample... "
sortBed -i "$output_dir"/$(echo ${sample##*/})/SJ.out.bed > "$output_dir"/$(echo ${sample##*/})/SJ.out.sorted.bed
intersectBed -wao -a "$output_dir"/$(echo ${sample##*/})/SJ.out.sorted.bed -b $(echo $gtf_dir) -s > "$output_dir"/$(echo ${sample##*/})/SJ.out.enriched.bed

#3. Format the enriched.bed file for those that exactly match with the junctions and associate the info to the original bed file
echo "Recovering gene and junction type with $sample... "
#3.1. Get the junctions that match with the annotation
awk -F"\t" '$17 == "1" { print }' "$output_dir"/$(echo ${sample##*/})/SJ.out.enriched.bed > "$output_dir"/$(echo ${sample##*/})/SJ.out.enriched.filtered.bed
#3.2. Extract the unique values for the id and the associated gene
awk '{print $4,$17}' "$output_dir"/$(echo ${sample##*/})/SJ.out.enriched.bed | sort -u > "$output_dir"/$(echo ${sample##*/})/SJ.out.enriched.unique.bed
#3.3 Replace the junctions associated to genes "0" with a blank space
sed -i -e 's/ 0/ "";/g' "$output_dir"/$(echo ${sample##*/})/SJ.out.enriched.unique.bed
#3.4. Associate the list of genes to each junction to the original bed file
#/soft/R/R-3.3.2/bin/Rscript "$MYDIR"/GenestoJunctions.R "$sample"/SJ.out.bed "$sample"/SJ.out.enriched.unique.bed "$sample"/SJ.out.enriched.filtered.bed "$sample"/SJ.out.geneAnnotated.bed

#Associate the list of genes to each junction to the original bed file
Rscript "$scripts_dir"/GenestoJunctions_v2.R "$output_dir"/$(echo ${sample##*/})/SJ.out.bed "$output_dir"/$(echo ${sample##*/})/SJ.out.enriched.unique.bed "$output_dir"/$(echo ${sample##*/})/SJ.out.enriched.filtered.bed "$output_dir"/$(echo ${sample##*/})/SJ.out.junction.type.bed "$output_dir"/$(echo ${sample##*/})/SJ.out.geneAnnotated.bed

echo "End of execution. "$(date)
exit 0
