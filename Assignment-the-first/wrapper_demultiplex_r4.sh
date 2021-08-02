#!/bin/bash
#SBATCH --partition=bgmp        ### Partition
#SBATCH --job-name=demult_r4_%j      ### Job Name
#SBATCH --output=demult_r4_%j.out         ### File in which to store job output
#SBATCH --error=demult_r4_%j.err          ### File in which to store job error messages
#SBATCH --time=1-00:00:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1               ### Number of nodes needed for the job
#SBATCH --ntasks-per-node=8     ### Number of tasks to be launched per Node
#SBATCH --account=bgmp      ### Account used for job submission
#SBATCH --mail-user='jlee26@uoregon.edu'
#SBATCH --mail-type=END,FAIL
export OMP_NUM_THREADS=8
conda activate bgmp_py39

./demultiplex_r4.py