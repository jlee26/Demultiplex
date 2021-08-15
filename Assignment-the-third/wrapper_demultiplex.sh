#!/bin/bash
#SBATCH --partition=bgmp        ### Partition
#SBATCH --job-name=demult_%j      ### Job Name
#SBATCH --output=demult_%j.out         ### File in which to store job output
#SBATCH --error=demult_%j.err          ### File in which to store job error messages
#SBATCH --time=1-00:00:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1               ### Number of nodes needed for the job
#SBATCH --ntasks-per-node=8     ### Number of tasks to be launched per Node
#SBATCH --account=bgmp      ### Account used for job submission
#SBATCH --mail-user='jlee26@uoregon.edu'
#SBATCH --mail-type=END,FAIL
export OMP_NUM_THREADS=8
conda activate bgmp_py39

# ##test
# /usr/bin/time -v ./demultiplex.py -i /projects/bgmp/shared/2017_sequencing/indexes.txt -r1 /projects/bgmp/jlee26/bioinformatics/Bi622/demultiplex/unit_test_r1.fastq.gz -r2 /projects/bgmp/jlee26/bioinformatics/Bi622/demultiplex/unit_test_r2.fastq.gz -r3 /projects/bgmp/jlee26/bioinformatics/Bi622/demultiplex/unit_test_r3.fastq.gz -r4 /projects/bgmp/jlee26/bioinformatics/Bi622/demultiplex/unit_test_r4.fastq.gz -c 30

/usr/bin/time -v ./demultiplex.py -i /projects/bgmp/shared/2017_sequencing/indexes.txt -r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -r3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -r4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -c 30
