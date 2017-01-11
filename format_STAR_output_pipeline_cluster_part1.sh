#!/bin/sh
# format_STAR_output_pipeline_cluster_part1.sh
#$ -S /bin/sh
#$ -N format_STAR_output_pipeline_cluster_part1
#$ -cwd
#
# ==============================================================================================
# format_STAR_output_pipeline_cluster_part1:
#
# Description: The next pipeline run format_STAR_output_per_sample.sh in the cluster per sample,
#		given a path with the STAR files. After this, it will be necessary to run 
#		format_STAR_output_pipeline_cluster_part2.sh
#
# Input: arg[1] --> path to the STAR output file (one folder per sample)
#	 arg[2] --> path to the GTF annotation file
# ==============================================================================================

io_dir=$1
gtf_dir=$2

source /usr/local/sge/default/common/settings.sh

echo "Starting execution. "$(date)
echo "Sending jobs to gencluster..."

cnt=0
for sample in $(ls -d "$io_dir"/*);do
	echo "Processing sample $sample..."
	command="/projects_rg/SCLC_cohorts/scripts/format_STAR_output_per_sample.sh $(echo $sample) $(echo $gtf_dir)"
	qsub -N format_STAR_"$cnt" -S /bin/sh -cwd -q bigmem,long,normal -pe serial 2 -b y $command
	cnt=$((cnt+1))
done

echo "When all the jobs have finished, run format_STAR_output_pipeline_cluster_part2.sh"
echo "End of execution. "$(date)

exit 0

