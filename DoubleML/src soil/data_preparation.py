import numpy as np
import pandas as pd
from util import normalize_df

# load dataframes from files
microbes_df = pd.read_csv("../data/soil/microbes.from_biom.tsv", sep='\t', index_col=0).drop(columns="9hr_late")
metabolites_df = pd.read_csv("../data/soil/metabolites.from_biom.tsv", sep='\t', index_col=0)

microbes_df.describe()

# apply log transformation
# first increase all values with 1
microbes_df += 1
metabolites_df += 1

microbes_df = np.log(microbes_df)
metabolites_df = np.log(metabolites_df)

# normalize dataframes
microbes_normalized = normalize_df(microbes_df)
metabolites_normalized = normalize_df(metabolites_df)
metabolites_normalized = metabolites_normalized.T.reindex(microbes_normalized.T.index).T

# save transformed data
microbes_normalized.to_csv("../data/soil/microbes_normalized.tsv", sep="\t", index=True)
metabolites_normalized.to_csv("../data/soil/metabolites_normalized.tsv", sep="\t", index=True)
