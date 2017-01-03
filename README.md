# PSI-Clustering-Junction

The next scripts have been developed for generating PSI (Percent Spliced Index) values of junctions clusters. This pipleine is adpated for using STAR.

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
- **rpkm.tab**: normalizated rpkm values from the read counts
