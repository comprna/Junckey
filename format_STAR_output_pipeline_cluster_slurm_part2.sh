#!/bin/sh

#SBATCH --partition=short
#SBATCH --mem 10000

# ==============================================================================================
# format_STAR_output_pipeline_cluster_slurm_part2:
#
# Description: This part2 gather all the information generated with the part1 in one file#
#
# Input: arg[1] --> path to the STAR output file (one folder per sample)
# ==============================================================================================

i_dir=$1
o_dir=$2

#Export this library for using R-3.3.2
#export LD_LIBRARY_PATH=/soft/devel/gcc-4.9.3/lib64:$LD_LIBRARY_PATH

module load R
module load RStudio
module load BEDTools
moudle load Python

echo "Starting execution. "$(date)

#Store the path where the scripts are
MYSELF="$(readlink -f "$0")"
MYDIR="${MYSELF%/*}"

#1. Format the Log.Final.out files
echo "Formatting Log.Final.out files..."
Rscript /projects_rg/SCLC_cohorts/scripts/format_Log_STAR.R "$i_dir"/

#2. Pool the reads from all the samples in one file
echo "Gathering all files into one..."
python "$MYDIR"/pool_results.py "$i_dir" "$o_dir"

echo "End of execution. "$(date)
exit 0
