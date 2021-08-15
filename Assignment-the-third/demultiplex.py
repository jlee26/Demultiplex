#!/usr/bin/env python
import gzip
import re
import Bioinfo
import argparse
import os.path

### set up argparse
def get_args():
    parser = argparse.ArgumentParser(description="Files")
    parser.add_argument("-i", "--index_file", help="Specify the absolute pathway to the index information file.", required=True)
    parser.add_argument("-r1", "--r1_file", help="Specify the absolute pathway to the r1 file.", required=True)
    parser.add_argument("-r2", "--r2_file", help="Specify the absolute pathway to the r2 file.", required=True)
    parser.add_argument("-r3", "--r3_file", help="Specify the absolute pathway to the r3 file.", required=True)
    parser.add_argument("-r4", "--r4_file", help="Specify the absolute pathway to the r4 file.", required=True)
    parser.add_argument("-c", "--qscore_cutoff", help="Specify the cut-off value for the quality scores. The cut-off value will be compared to individual quality scores of the index1 and index2. Recommend 30.", required=True, type=int)
    return parser.parse_args()
args = get_args()

### Make barcode dictionary
#index_file = "/projects/bgmp/shared/2017_sequencing/indexes.txt"
dict_index = {} #key: index; value: index sequence
with open(args.index_file, "r") as f:
    next(f) #skip the header
    for line in f.readlines():
        tab_sep = line.strip().split("\t")
        dict_index[tab_sep[4]] = tab_sep[3] #col3: index; col4: index sequence
# #print(dict_index)



### Create writable files and open in dictionary (total of 52 files = 48 index-pairs + 2 index-hopped + 2 index-undet)
### 24 index-pairs * 2 (read1 & read2) = 48 files
### 1 index-hopped * 2 (read1 & read2) = 2 files
### 1 index-undet (contains low aulity and/or contains N) * 2 (read1 & read2) = 2 files
dict_openfiles = {
}
with open(args.index_file, "r") as rf:
    next(rf) #skip the header
    for line in rf.readlines():
        tab_sep = line.strip().split("\t") #col 4 contains the index sequence (matches to index1)
        dict_openfiles["r1_" + tab_sep[4]] = open(f"read1_{tab_sep[4]}.fastq", "w")
        dict_openfiles["r2_" + tab_sep[4]] = open(f"read2_{tab_sep[4]}.fastq", "w")

r1_hopped = open("./read1_index_hopped.fastq", "w")
r2_hopped = open("./read2_index_hopped.fastq", "w")
r1_undet = open("./read1_index_undetermined.fastq", "w")
r2_undet = open("./read2_index_undetermined.fastq", "w")

# ##tests
# dict_topenfiles = {
#     "tr1_AACAGCGA" : open("./test_read1_AACAGCGA.fastq", "w"),
#     "tr2_AACAGCGA" : open("./test_read2_AACAGCGA.fastq", "w"),
# }
# tr1_hopped = open("./test_read1_index_hopped.fastq", "w")
# tr2_hopped = open("./test_read2_index_hopped.fastq", "w")
# tr1_undet = open("./test_read1_undetermined.fastq", "w")
# tr2_undet = open("./test_read2_undetermined.fastq", "w")



### Open R1, R2, R3, and R4 files
#r1_file = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz"
#r2_file = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz"
#r3_file = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz"
#r4_file = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz"
r1 = gzip.open(args.r1_file, "rt")
r2 = gzip.open(args.r2_file, "rt")
r3 = gzip.open(args.r3_file, "rt")
r4 = gzip.open(args.r4_file, "rt")

# ##tests
# #tr1_file = "/projects/bgmp/jlee26/bioinformatics/Bi622/demultiplex/unit_test_r1.fastq.gz"
# #tr2_file = "/projects/bgmp/jlee26/bioinformatics/Bi622/demultiplex/unit_test_r2.fastq.gz"
# #tr3_file = "/projects/bgmp/jlee26/bioinformatics/Bi622/demultiplex/unit_test_r3.fastq.gz"
# #tr4_file = "/projects/bgmp/jlee26/bioinformatics/Bi622/demultiplex/unit_test_r4.fastq.gz"
# tr1 = gzip.open(args.r1_file, "rt")
# tr2 = gzip.open(args.r2_file, "rt")
# tr3 = gzip.open(args.r3_file, "rt")
# tr4 = gzip.open(args.r4_file, "rt")



### Initialize variables
counter_lines = 0
counter_undet = 0
counter_matched = 0
counter_hopped = 0
check_counter_rev_comp_but_nobarcode = 0
qscore_cutoff = args.qscore_cutoff

dict_counter = {}
for index, d in enumerate(dict_index.items()):
    dict_counter[d[0]] = 0

### demultiplex code
while True:
    if counter_lines % 4 == 0:
        header = r1.readline()
        # ##tests
        # header = tr1.readline()
        if header == "":
            break
        else:
            header = r2.readline().strip()
            header = r3.readline().strip()
            header = r4.readline().strip()
            header = re.match("[^\s]+", header)
            header = header.group(0)
            r1_seq = r1.readline().strip()
            r2_seq = r4.readline().strip()
            i1_seq = r2.readline().strip()
            i2_seq = r3.readline().strip()
            plus = r1.readline().strip()
            plus = r2.readline().strip()
            plus = r3.readline().strip()
            plus = r4.readline().strip()
            r1_qscore = r1.readline().strip()
            r2_qscore = r4.readline().strip()
            i1_qscore = r2.readline().strip()
            i2_qscore = r3.readline().strip()
            header = header + "-" + i1_seq + "-" + i2_seq
            # ##tests
            # header = tr2.readline().strip()
            # header = tr3.readline().strip()
            # header = tr4.readline().strip()
            # header = re.match("[^\s]+", header)
            # header = header.group(0)
            # r1_seq = tr1.readline().strip()
            # r2_seq = tr4.readline().strip()
            # i1_seq = tr2.readline().strip()
            # i2_seq = tr3.readline().strip()
            # plus = tr1.readline().strip()
            # plus = tr2.readline().strip()
            # plus = tr3.readline().strip()
            # plus = tr4.readline().strip()
            # r1_qscore = tr1.readline().strip()
            # r2_qscore = tr4.readline().strip()
            # i1_qscore = tr2.readline().strip()
            # i2_qscore = tr3.readline().strip()
            # header = header + "-" + i1_seq + "-" + i2_seq
            if Bioinfo.validate_base_seq(i1_seq) == False or Bioinfo.validate_base_seq(i2_seq) == False: ##index1 or index2 sequence contains non DNA letters (N)
                counter_undet += 1
                r1_undet.write(header + "\n" + r1_seq + "\n" + plus + "\n" + r1_qscore + "\n")
                r2_undet.write(header + "\n" + r2_seq + "\n" + plus + "\n" + r2_qscore + "\n")
                # ##test
                # tr1_undet.write(header + "\n" + r1_seq + "\n" + plus + "\n" + r1_qscore + "\n")
                # tr2_undet.write(header + "\n" + r2_seq + "\n" + plus + "\n" + r2_qscore + "\n")
            else:
                for n in range(len(i1_qscore)):
                    if Bioinfo.convert_phred(i1_qscore[n]) > qscore_cutoff and Bioinfo.convert_phred(i2_qscore[n]) > qscore_cutoff: #index1 and index2 have good quality scores
                        if Bioinfo.rev_comp(i1_seq) == i2_seq: #index1 is reverse compliment of index2
                            if i1_seq in dict_index.keys(): #index1 is the barcode
                                counter_matched += 1
                                i1_seqname = "r1_" + i1_seq
                                i2_seqname = "r2_" + i1_seq
                                # ##tests
                                # i1_seqname = "tr1_" + i1_seq
                                # i2_seqname = "tr2_" + i1_seq
                                dict_openfiles.get(i1_seqname).write(header + "\n" + r1_seq + "\n" + plus + "\n" + r1_qscore + "\n")
                                dict_openfiles.get(i2_seqname).write(header + "\n" + r2_seq + "\n" + plus + "\n" + r2_qscore + "\n")
                                if i1_seq in dict_counter.keys():
                                    dict_counter[i1_seq] += 1
                                    break
                                # ##tests
                                # dict_topenfiles.get(i1_seqname).write(header + "\n" + r1_seq + "\n" + plus + "\n" + r1_qscore + "\n")
                                # dict_topenfiles.get(i2_seqname).write(header + "\n" + r2_seq + "\n" + plus + "\n" + r2_qscore + "\n")
                            else: #the index sequences are reverse compliment, but they're not one of the given barcodes
                                counter_undet += 1
                                check_counter_rev_comp_but_nobarcode += 1
                                r1_undet.write(header + "\n" + r1_seq + "\n" + plus + "\n" + r1_qscore + "\n")
                                r2_undet.write(header + "\n" + r2_seq + "\n" + plus + "\n" + r2_qscore + "\n")
                                # ##tests
                                # tr1_undet.write(header + "\n" + r1_seq + "\n" + plus + "\n" + r1_qscore + "\n")
                                # tr2_undet.write(header + "\n" + r2_seq + "\n" + plus + "\n" + r2_qscore + "\n")
                            break
                        else:
                            counter_hopped += 1
                            r1_hopped.write(header + "\n" + r1_seq + "\n" + plus + "\n" + r1_qscore + "\n")
                            r2_hopped.write(header + "\n" + r2_seq + "\n" + plus + "\n" + r2_qscore + "\n")
                            # ##tests
                            # tr1_hopped.write(header + "\n" + r1_seq + "\n" + plus + "\n" + r1_qscore + "\n")
                            # tr2_hopped.write(header + "\n" + r2_seq + "\n" + plus + "\n" + r2_qscore + "\n")
                            break
                    else:
                        counter_undet += 1
                        r1_undet.write(header + "\n" + r1_seq + "\n" + plus + "\n" + r1_qscore + "\n")
                        r2_undet.write(header + "\n" + r2_seq + "\n" + plus + "\n" + r2_qscore + "\n")
                        # ##tests
                        # tr1_undet.write(header + "\n" + r1_seq + "\n" + plus + "\n" + r1_qscore + "\n")
                        # tr2_undet.write(header + "\n" + r2_seq + "\n" + plus + "\n" + r2_qscore + "\n")
                        break
    counter_lines += 4        

with open("./report.md", "w") as wf:
    wf.write("# Demultiplex Reports" + "\n")
    wf.write("| | Undetermined | Index Hopping | Matched | Index(es) are reverse complimented but not found in the list of barcodes (These records are included in the undetermined files) |" + "\n")
    wf.write("| ------ | :------: | :------: | :------: | :------: |" + "\n")
    wf.write(f"| Number of records: | {counter_undet} | {counter_hopped} | {counter_matched} | {check_counter_rev_comp_but_nobarcode} |" + "\n")
    wf.write(f"| Percent: | {counter_undet/(counter_undet + counter_hopped + counter_matched)*100} | {counter_hopped/(counter_undet + counter_hopped + counter_matched)*100} | {counter_matched/(counter_undet + counter_hopped + counter_matched)*100} | {check_counter_rev_comp_but_nobarcode/(counter_undet + counter_hopped + counter_matched)*100} |" + "\n" + "\n")
    
    wf.write("### Number of records for each bucket" + "\n")
    wf.write("| Bucket | Count | Percent |" + "\n")
    wf.write("| :----: | :----: | :----: |" + "\n")
    count_total_match = 0
    count_percent_match = 0
    for index, dic in enumerate(dict_counter.items()):
        wf.write(f"| {dic[0]} | {dic[1]} | {(dic[1]/counter_matched)*100} |" + "\n")
        count_total_match += dic[1]
        count_percent_match += (dic[1]/counter_matched)*100
    wf.write(f"| Total: | {count_total_match} | {count_percent_match} |" + "\n" + "\n")

    
    
    wf.write("### Distribution of Nucleotides for Read 1, Read 2, Index 1, and Index 2" + "\n")

    images = ["index1.png", "index2.png", "read1.png", "read2.png"]
    for n in range(len(images)):
        if os.path.isfile(f"/projects/bgmp/jlee26/bioinformatics/Bi622/Demultiplex/Assignment-the-third/{images[n]}") == True:
            wf.write(f"![alt text](https://github.com/jlee26/Demultiplex/blob/master/Assignment-the-first/{images[n]})" + "\n")
        else:
            wf.write(f"Note: No graph provided. Make sure {images[n]} is located in the correct directory!")



### Close open files
dict_closefiles = {}
for i, values in enumerate(dict_openfiles.items()):
    values[1].close() #closing all 48 index-pair files

r1_hopped.close()
r2_hopped.close()
r1_undet.close()
r2_undet.close()

r1.close()
r2.close()
r3.close()
r4.close()

# ##tests
# for i, values in enumerate(dict_topenfiles.items()):
#     values[1].close() #closing all 48 index-pair files

# tr1_hopped.close()
# tr2_hopped.close()
# tr1_undet.close()
# tr2_undet.close()

# tr1.close()
# tr2.close()
# tr3.close()
# tr4.close()