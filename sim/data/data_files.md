# Information about the data files

## Original biom files
The files ```table.rel.microbes.0.biom``` and ```table.rel.metabolites.0.biom``` were copied from
https://github.com/knightlab-analyses/multiomic-cooccurrences/tree/88dc584109708accf3c36a697d990c46cf7b6c2f/results/benchmark_output/CF_small_benchmark.

## TSV files
### Converting .biom to .tsv
The .biom files were converted to `microbes.from_biom.tsv` and `metabolites.from_biom.tsv` using
the following commands from the [biom-format package](http://biom-format.org/index.html): 
```
biom convert -i microbes.biom -o microbes.from_biom.tsv --to-tsv
biom convert -i metabolites.biom -o metabolites.from_biom.tsv --to-tsv
```
This command places a header line (`# Constructed from biom file`) in the `.tsv` 
files, which was removed for further usage.

### Centered log-ratio transformations
Transforming the data