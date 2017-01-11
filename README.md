# Junckie

Junckie is a collection of scripts for the calculation of PSI (Proportion Spliced Index) values of junctions clusters. This pipeline is adpated for using STAR (https://github.com/alexdobin/STAR).

### 1. Format STAR output

This pipeline uses the SJ.out.tab files generated with STAR. It is necessary to specify to the next code the path to the STAR samples, with each execution in a separated folder. Also, is necesary a gtf annotation of the transcriptome:

```
format_STAR_output.sh <path_to_STAR_samples> <gtf_annotation>
```
This script generates two files, with the samples in the columns and the junctions in the rows:
- **readCounts.tab**: all the unique read counts computed with STAR. Per junction we obtain the overlap with genes and the type of the junction:
  - 1: Fully annotated junction
  - 2: Junction overlapping with known exons, but new connection
  - 3: Alternative donor site
  - 4: Alternative acceptor site
  - 5: Novel junction, neither donor nor acceptor site is annotated
- **rpkm.tab**: normalizated rpkm values from the read counts. For the following steps we will just use the readCounts file

### 2. Clustering

For computing the PSI of the junctions, we propose to do it according to the relative inclusion of the nearby junctions. In order to achieve this, we can calculate clusters of our junctions using LeafCutter (https://github.com/davidaknowles/leafcutter).

First, we need to split the readCounts file in .junc files (one per sample). The next script will generate this files in the same provided path and the corresponding index file (index_juncfiles.txt):

```
python Split_in_juncfiles.py <path_to_STAR_samples>/readCounts.tab
```

Now we are ready for running LeafCutter. Here we show an example of execution, but there are several options in the github website for tuning the execution. It's necessary to provide the previous generated index_juncfiles.txt file:

```
python leafcutter-master/clustering/leafcutter_cluster.py -p 0.01 -j <path_to_STAR_samples>/index_juncfiles.txt -o <output_path_LeafCutter>
```

### 3. PSI Calculation

The next script calculate the PSI inclusion of each junction in relation to the clusters. It returns a sigle file with all the PSI values together, removing those clusters with NA values

```
python Get_PSI.py <output_path_LeafCutter> <path_to_STAR_samples>/readCounts.tab
```


