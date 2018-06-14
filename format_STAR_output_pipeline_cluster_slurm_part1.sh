#!/bin/sh

#
# ==============================================================================================
# format_STAR_output_pipeline_cluster_slurm_part1:
#
# Description: The next pipeline run format_STAR_output_per_sample.sh in the cluster per sample,
#		given a path with the STAR files. After this, it will be necessary to run 
#		format_STAR_output_pipeline_cluster_part2.sh
#
# Input: arg[1] --> path to the STAR output file (one folder per sample)
#	 arg[2] --> path to the GTF annotation file
#    arg[3] --> path to output folder
# ==============================================================================================

io_dir=$1
gtf_dir=$2
output_dir=$3

#source /usr/local/sge/default/common/settings.sh

echo "Starting execution. "$(date)
echo "Sending jobs to gencluster..."

#Store the path where the scripts are
MYSELF="$(readlink -f "$0")"
scripts_dir="${MYSELF%/*}"

for sample in $(ls -d "$io_dir"/*);do
	echo "Processing sample $sample..."
	command="sbatch -J format_STAR_"$cnt" $(echo $scripts_dir)/format_STAR_output_per_sample_slurm.sh $(echo $sample) $(echo $gtf_dir) $(echo $output_dir)"
	#echo $command
	sbatch -J $(echo ${sample##*/})_Junckey $(echo $scripts_dir)/format_STAR_output_per_sample_slurm.sh $(echo $sample) $(echo $gtf_dir) $(echo $output_dir) $(echo $scripts_dir)
	#qsub -N format_STAR_"$cnt" -S /bin/sh -cwd -q bigmem,long,normal -pe serial 2 -b y $command
done

echo "When all the jobs have finished, run format_STAR_output_pipeline_cluster_slurm_part2.sh"
echo "End of execution. "$(date)

exit 0
