# Assignment the First

## Part 1
1. Be sure to upload your Python script.
Used the following command lines to look at the sequence to determine the indexes and reads:
zcat 1294_S1_L008_R1_001.fastq.gz | head
zcat 1294_S1_L008_R2_001.fastq.gz | head
zcat 1294_S1_L008_R3_001.fastq.gz | head
zcat 1294_S1_L008_R4_001.fastq.gz | head

| File name | label |
|---|---|
| 1294_S1_L008_R1_001.fastq.gz | read1 |
| 1294_S1_L008_R2_001.fastq.gz | index1 |
| 1294_S1_L008_R3_001.fastq.gz | index2 |
| 1294_S1_L008_R4_001.fastq.gz | read2 |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    2. ```A good quality score cutoff would be to use a high quality score to ensure that the probability of which the base is incorrect is low. To perform downstream analysis or to identify a sample, each individual quality score should be high to prevent high chances of incorrect nucleotide sequencing. For this case, rather than taking the average of the quality scores and determining if this value is below the cutoff, comparing individual quality score value to the cutoff is preferred. If the quality score is averaged, these low quality score outliers may be missed.```
    3. ```Index1 has 3,976,613 indexes with N base call. Command line: zcat 1294_S1_L008_R2_001.fastq.gz | sed -n '2~4p' | grep "N" | wc -l
    Index2 has 3,328,051 indexes with N base call. Command line: zcat 1294_S1_L008_R3_001.fastq.gz |
 sed -n '2~4p' | grep "N" | wc -l```
    
## Part 2
1. Define the problem
```The problem is that the index hopping can occur during RNA-seq lab, therefore, an algorithm should be made to determine if an index has properly ligated or if we can observe index hopping. The reads that have index hopping is placed in a separate file.```
2. Describe output
```There will be a total of 52 output files: 24 fastq files for the barcodes for read1 and read2, index-hopping fastq files for read1 and read2, and unknown or poor quality score fastq file for read1 and read2. There will also be another text file that reports the number of matched index pairs, number of index-hoppings, and number of unknown/poor quality indexes.```
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
```
0. Assign variables
counter_poor = 0
counter_
qscore_cutoff = 30

1. Make barcode dictionary and open (open()) files for each index for read1 and read2
a) open indexes.txt
b) for each line, take the index column and store as key, and take index sequence and store as value
c) open new file named read1_<bucket>.fastq
    Get the bucket from the key
d) open new file named read2_<bucket>.fastq
    Get the bucket from the key

2. Open read1_index_hopping.fastq, read2_index_hopping.fastq, read1_index_poor.fastq, and read2_index_poor.fastq

3. Open all four R1, R2, R3, and R4 files

4. In a loop, read each line (.readline()) of all 4 files (#3) and assign the line to variables
a) header = first line of the files that excludes all characters on and after the space
b) r1_seq = 2nd line of read1 file (R1)
c) r2_seq = 2nd line of read2 file (R4)
d) i1_seq = 2nd line of index1 file (R2)
e) i2_seq = 2nd line of index2 file (R3)
f) plus = 3rd line of the files
g) i1_qscore = 4th line of index1 file (R2)
h) i2_qscore = 4th line of index2 file (R3)

5. Check the i1_seq and i2_seq to see if there is N:
    
    True: write the following into read1_index_poor.fastq file:
            header-i1_seq-i2_seq
            r1_seq
            plus
            r1_qscore
          write the following into read2_index_poor.fastq file:
            header-i1_seq-i2_seq
            r2_seq
            plus
            r2_qscore
    counter_poor += 1
    False: check the i1_qscore and i2_qscore if it's lower than the qscore_cutoff
        a) convert i1_qscore and i2_qscore to quality score using a function that converts from ascii number to quality score
        True: write the following into read1_index_poor.fastq file:
            header-i1_seq-i2_seq
            r1_seq
            plus
            r1_qscore
          write the following into read2_index_poor.fastq file:
            header-i1_seq-i2_seq
            r2_seq
            plus
            r2_qscore
        counter_poor += 1
        False: check if i1_seq is reverse compliment and backwards from i2_seq by using a function
            True: look at the indexes.txt and find the bucket name and write the following into read1_<bucketname>.fastq file
                header-i1_seq-i2_seq
                r1_seq
                plus
                r1_qscore
                  write the following into read2_<bucketname>.fastq file
                header-i1_seq-i2_seq
                r2_seq
                plus
                r2_qscore
            counter_dual += 1
            False: write the following into read1_index_hopping.fastq
                header-i1_seq-i2_seq
                r1_seq
                plus
                r1_qscore
                  write the following into read2_index_hopping.fastq
                header-i1_seq-i2_seq
                r2_seq
                plus
                r2_qscore
            counter_hopped += 1

6. End for loop.

7. Report the values for counter_poor, counter_dual, and counter_hopped to new outputfile.txt. This is the total number of reads with unknown indexes, matched indexes, and hopped indexes.

8. Close all open files.
```
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
