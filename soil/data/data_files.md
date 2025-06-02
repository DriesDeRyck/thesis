# Information about the data files

## Original biom files

The files ```microbes.biom``` and ```metabolites.biom``` were copied from
https://github.com/knightlab-analyses/multiomic-cooccurrences/tree/master/data/soils.

## TSV files

### Converting .biom to .tsv

The .biom files were converted to `microbes.from_biom.tsv` and `metabolites.from_biom.tsv` using
the following commands from the [biom-format package](http://biom-format.org/index.html):

```
biom convert -i microbes.biom -o microbes.from_biom.tsv --to-tsv
biom convert -i metabolites.biom -o metabolites.from_biom.tsv --to-tsv
```

### Cleaning the data

Before using the `microbes.from_biom.tsv` and `metabolites.from_biom.tsv` files, we
must clean them.
This includes removing the line that was generated during the .biom to .tsv conversion
that says `# Constructed from biom file`.\
It also includes removing a sample that was only present in the microbe file and
ordering the samples the same for both files.

These steps were done in the `data_clean.ipynb` notebook. The resulting files are
`microbes.tsv` and `metabolites.tsv`.

### Centered log-ratio transformations

Transforming the data with the centered log-ratio transformation is done in the
`clr.ipynb` notebook.
