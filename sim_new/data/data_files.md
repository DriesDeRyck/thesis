# Information about the data files

## Original files

The files ```rel.microbes.tsv``` and ```rel.metab.biom``` were copied from
https://github.com/knightlab-analyses/multiomic-cooccurrences/tree/master/results/benchmark_output/CF_sims/data.
## TSV files

### Cleaning the data

Before using the `rel.microbes.tsv` and `rel.metab.biom` files, they
must be cleaned.
This includes removing the line that was generated during the .biom to .tsv conversion
that says `# Constructed from biom file`. It also includes making sure that the columns 
are ordered equally.


These steps were done in the `data_clean.ipynb` notebook. 

The resulting files are:
- `microbes.tsv` and 
- `metabolites.tsv`

### Centered log-ratio transformations

Transforming the data with the centered log-ratio transformation is done in the
`clr.ipynb` notebook.

The resulting files are:

- `clr_microbes.tsv`
- `clr_microbes_min.tsv`
- `clr_microbes_sc.tsv`
- `clr_microbes_sc_min.tsv`
- `clr_metabolites.tsv`
- `clr_metabolites_min.tsv`
- `clr_metabolites_sc.tsv`
- `clr_metabolites_sc_min.tsv`

### Subset files
Creating the subsets of the relative simulation data is done in the 
`subsets.ipynb` notebook.

The resulting files are:

- `microbes.subset20.tsv`
- `microbes.subset100.tsv`
- `microbes.subset500.tsv`
- `metabolites.subset100.tsv`
- `metabolites.subset500.tsv`
- `metabolites.subset20.tsv`
