# README

## CLI COMMANDS

For src code:
working directory should have ./data/microbes.tsv and ./data/metabolites.tsv file

Example: (in YACHIDA_CRC_2019 directory):

```
python3 ../../../src/correlation_test.py
```

## Utils
#### Convert to and from .biom files
```
biom convert -i table.biom -o table.from_biom.tsv --to-tsv
biom convert -i table.txt -o table.from_txt_hdf5.biom --table-type="OTU table" --to-hdf5
```
#### Show head of .biom file with 10 rows and 8 columns
```
biom head -i inputfile.biom -n 10 -m 8