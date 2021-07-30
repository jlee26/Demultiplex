# Assignment the First

## Part 1
1. Be sure to upload your Python script.


| File name | label |
|---|---|
| 1294_S1_L008_R1_001.fastq.gz | read1 |
| 1294_S1_L008_R2_001.fastq.gz | index1 |
| 1294_S1_L008_R3_001.fastq.gz | index2 |
| 1294_S1_L008_R4_001.fastq.gz | read2 |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    2. ```A good quality score cutoff would be a high quality score to ensure the probability that the base is incorrect is low. Rather than taking the average of the quality scores for the index and determining if this value is below the cutoff, comparing individual quality score value to the cutoff may be better. This is to ensure any low quality score outliers are found. If the quality score is averaged, these low quality score outliers may go unoticed. The sequenced bases of the indexes should be highly confident, therefore we do not want low quality scores to go unoticed.```
    3. ```Your answer here```
    
## Part 2
1. Define the problem
```The problem is that the index hopping can ```
2. Describe output
```There will be a total of 52 output files: two 24 fastq files for the barcodes for read1 and read2, two index-hopping fastq files for read1 and read2, and two unknown or poor quality score fastq file for read1 and read2. There will also be another text file that reports number of matched index pairs, number of index-hoppings, and number of unknown indexes.```
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
``````
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
