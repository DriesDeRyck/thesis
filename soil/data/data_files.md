# Information about the data files

## Original biom files
The files ```microbes.biom``` and ```metabolites.biom``` were copied from 
https://github.com/knightlab-analyses/multiomic-cooccurrences/tree/master/data/soils.

## TSV files
### Converting to .tsv
The .biom files were converted to `microbes.from_biom.tsv` and `metabolites.from_biom.tsv` using
the following commands from the [biom-format package](http://biom-format.org/index.html): 
```
biom convert -i microbes.biom -o microbes.from_biom.tsv --to-tsv
biom convert -i metabolites.biom -o metabolites.from_biom.tsv --to-tsv
```
This command places a header line (`# Constructed from biom file`) in the `.tsv` 
files, which was removed for further usage.

### Centered log-ratio transformations
Transforming the data with the centered log-ratio transformation is done in the `clr.ipynb` file.
