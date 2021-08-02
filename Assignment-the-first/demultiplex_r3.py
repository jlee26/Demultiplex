#!/usr/bin/env python

import numpy as np
import Bioinfo
import gzip
import matplotlib.pyplot as plt
# %matplotlib inline

# file_r1 = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz"
# file_r2 = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz"
file_r3 = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz"
# file_r4 = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz"
# dict_files = {
#     "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz": ["read 1",1],
#     "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz": ["index 1",2],
#     "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz": ["index 2",3],
#     "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz": ["read 2",4]}

# tfile_r1 = "./unit_test_r1.fastq.gz"
# tfile_r2 = "./unit_test_r2.fastq.gz"
# tfile_r3 = "./unit_test_r3.fastq.gz"
# tfile_r4 = "./unit_test_r4.fastq.gz"
# dict_files = {
#     "./unit_test_r1.fastq.gz": ["read 1",1],
#     "./unit_test_r2.fastq.gz": ["index 1",2],
#     "./unit_test_r3.fastq.gz": ["index 2",3],
#     "./unit_test_r4.fastq.gz": ["read 2",4]}


# for file_name, ri in dict_files.items():
    ### Reading in file and creating an array of the quality scores at each position for all reads to calculate the average
dict_tot = {}
with gzip.open(file_r3, "rb") as fr1:
    num_seq = 0
    count = 0
    for line in fr1:
        line = line[:-1]
        if count % 4 == 3:
            num_seq += 1
            seq_len = len(line)
            tot = 0
            for i in range(len(line)):
                if i in dict_tot.keys():
                    dict_tot[i] += line[i] - 33
                else:
                    dict_tot[i] = line[i] - 33
        count += 1

dict_ave = {}    
for base, tot in dict_tot.items():
    ave = tot/num_seq
    dict_ave[base] = ave

print("Number of records: ", num_seq) #number of lines
print("Number of bases: ",seq_len) #legth of the sequence
print("Total number of lines: ",count)

x = range(len(dict_ave))
plt.figure()
plt.bar(x, dict_ave.values())
plt.title("The average quality scores for each position for Index 2")
plt.xlabel("Position")
plt.ylabel("Mean")
plt.savefig("index2.png")
