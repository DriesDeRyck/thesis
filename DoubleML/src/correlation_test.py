import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import ConstantInputWarning
from tqdm import tqdm

import warnings
# warnings.simplefilter("ignore", ConstantInputWarning)



# treatment = (2 ,'rplo 60 (Firmicutes)')
# outcome = 'myristate'
# outcome = 'urate'
#%%
# read dataframes from files
microbes_df = pd.read_csv("./data/microbes_normalized.tsv", sep='\t', index_col=0)
metabolites_df = pd.read_csv("./data/metabolites_normalized.tsv", sep='\t', index_col=0)

def create_correlation_matrix(microbes_df, metabolites_df):
    # get names of microbes and metabolites
    microbe_names = np.array(microbes_df.index.sort_values())
    metabolite_names = np.array(metabolites_df.index.sort_values())

    # calculate correlation for each (microbe, metabolite) pair
    correlation_matrix = pd.DataFrame(columns=microbe_names, index=metabolite_names)
    pvalues = pd.DataFrame(columns=microbe_names, index=metabolite_names)
    for microbe in tqdm(microbe_names):
        treatment = microbe
        treatment_abundances = microbes_df.T[treatment].to_numpy()
        treatment_data = [float(np_float) for np_float in treatment_abundances]

        correlation_column = pd.Series(index=metabolite_names)
        pvalue_column = pd.Series(index=metabolite_names)
        for idx, columns in metabolites_df.iterrows():
            name = idx
            outcome_abundances = metabolites_df.T[idx].to_numpy()
            outcome_data = [float(np_float) for np_float in outcome_abundances]
            rho, p_value = stats.spearmanr(treatment_data, outcome_data)
            correlation_column[name] = float(rho)
            pvalue_column[name] = float(p_value)
        correlation_matrix[microbe] = correlation_column
        pvalues[microbe] = pvalue_column

    return correlation_matrix, pvalues


def microbe_metabolite_correlation():
    correlation_matrix, pvalues = create_correlation_matrix(microbes_df, metabolites_df)

    correlation_matrix.to_csv("./data/correlation_matrix.tsv", sep='\t', index=True)
    pvalues.to_csv("./data/correlation_pvalues.tsv", sep='\t', index=True)

    plt.matshow(correlation_matrix, cmap='coolwarm')
    plt.savefig("./figures/correlation_matrix.png")

    print(f"pvalues mean: {np.nanmean(pvalues)}, pvalues std: {np.nanstd(pvalues)}")


def microbe_microbe_correlation():
    correlation_matrix, pvalues = create_correlation_matrix(microbes_df, microbes_df)
    correlation_matrix = correlation_matrix.where(pvalues < 0.01)
    # correlation_matrix = correlation_matrix.where(correlation_matrix < 1)
    print(correlation_matrix.stack().index[np.argmax(correlation_matrix.values)])

    correlation_matrix.to_csv("../data/micr_micr_corr.tsv", sep='\t', index=True)
    pvalues.to_csv("../data/micr_micr_pvalues.tsv", sep='\t', index=True)

    plt.matshow(correlation_matrix, cmap='coolwarm')
    plt.savefig("../figures/micr_micr_corr.png")

    print(f"pvalues mean: {np.nanmean(pvalues)}, pvalues std: {np.nanstd(pvalues)}")


def metabolite_metabolite_correlation():
    correlation_matrix, pvalues = create_correlation_matrix(metabolites_df, metabolites_df)
    correlation_matrix = correlation_matrix.where(pvalues < 0.01)
    # correlation_matrix = correlation_matrix.where(correlation_matrix < 1)
    print(correlation_matrix.stack().index[np.argmax(correlation_matrix.values)])

    correlation_matrix.to_csv("../data/meta_meta_corr.tsv", sep='\t', index=True)
    pvalues.to_csv("../data/meta_meta_pvalues.tsv", sep='\t', index=True)

    plt.matshow(correlation_matrix, cmap='coolwarm')
    plt.savefig("../figures/meta_meta_corr.png")

    print(f"pvalues mean: {np.nanmean(pvalues)}, pvalues std: {np.nanstd(pvalues)}")

#%%
if __name__ == "__main__":
    microbe_metabolite_correlation()
    # microbe_microbe_correlation()
    # metabolite_metabolite_correlation()
    # print(microbes_df.head())
    #
    # microbe_correlations = pd.read_csv('../data/micr_micr_corr.tsv', sep='\t', index_col=0)
    # print(microbe_correlations['rplo 153 (Bacteroidetes)'].loc['rplo 1 (Cyanobacteria)'])
    pass