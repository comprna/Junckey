#!/bin/sh
# format_STAR_output_pipeline_cluster_part2.sh
#$ -S /bin/sh
#$ -N format_STAR_output_pipeline_cluster_part2
#$ -cwd
#
# ==============================================================================================
# format_STAR_output_pipeline_cluster_part2:
#
# Description: This part2 gather all the information generated with the part1 in one file#
#
# Input: arg[1] --> path to the STAR output file (one folder per sample)
# ==============================================================================================

io_dir=$1

#Export this library for using R-3.3.2
export LD_LIBRARY_PATH=/soft/devel/gcc-4.9.3/lib64:$LD_LIBRARY_PATH

echo "Starting execution. "$(date)

#1. Format the Log.Final.out files
echo "Formatting Log.Final.out files..."
/soft/R/R-3.3.2/bin/Rscript /projects_rg/SCLC_cohorts/scripts/format_Log_STAR.R "$io_dir"/

#2. Pool the reads from all the samples in one file
echo "Gathering all files into one..."
python /projects_rg/SCLC_cohorts/scripts/pool_results.py "$io_dir"

echo "End of execution. "$(date)
exit 0
