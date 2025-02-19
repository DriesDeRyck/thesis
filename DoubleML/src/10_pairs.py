from math import sqrt, floor, ceil
from tqdm import tqdm
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import clone
from scipy import stats
import matplotlib.pyplot as plt
from plots import multiple_scatterplots

n_largest = 9

correlation_df = pd.read_csv("./data/correlation_filtered.tsv", sep='\t', index_col=0)
# use absolute values for highest positive and negative correlations
absolute_values = correlation_df.abs()

indexes = absolute_values.stack().nlargest(n_largest**2).index.tolist()

rows = [i[0] for i in indexes]
cols = [i[1] for i in indexes]

idx = pd.MultiIndex.from_arrays([rows, cols])
values = correlation_df.stack().reindex(idx).values

highest_correlations = pd.DataFrame(columns=['microbe', 'metabolite', 'correlation', 'rank'])
for i in range(len(values)):
    microbe = indexes[i][1]
    metabolite = indexes[i][0]
    correlation = values[i]
    if correlation == 1:
        continue
    if microbe in highest_correlations['microbe'].values or metabolite in highest_correlations['metabolite'].values:
        # microbe or metabolite is already in a filtered pair, so skip this one
        continue
    else:
        # add row to dataframe
        highest_correlations = pd.concat([highest_correlations,
            pd.DataFrame([[microbe, metabolite, correlation, i]], columns=highest_correlations.columns)],
            ignore_index=True
        )
    # stop after n_largest values are found
    if highest_correlations.shape[0] >= n_largest:
        break

print(highest_correlations.head(n_largest))
# highest_correlations.to_csv("../data/soil/highest_correlations.tsv", sep='\t')

# Do DoubleML on highest correlations
from doubleml import DoubleMLData, DoubleMLPLR

# read dataframes from files
microbes_normalized = pd.read_csv("./data/microbes_normalized.tsv", sep='\t', index_col=0)
metabolites_normalized = pd.read_csv("./data/metabolites_normalized.tsv", sep='\t', index_col=0)

# use transposed dataframe such that each row is a sample from the dataset
microbes_T = microbes_normalized.T
metabolites_T = metabolites_normalized.T
# metabolites_T = metabolites_T.reindex(microbes_T.index)


for index, row in tqdm(highest_correlations.iterrows()):
    outcome = row['metabolite']
    treatment = row['microbe']
    # add metabolite of interest to microbe dataframe
    joined_data = pd.concat([metabolites_T[outcome], microbes_T], axis=1)
    cofounders = microbes_T.columns.drop(treatment)

    # make DML Data frame
    dml_data = DoubleMLData(joined_data,
                            y_col=outcome,
                            d_cols=treatment,
                            x_cols=list(cofounders))

    learner = RandomForestRegressor(n_estimators=500, max_features='sqrt', max_depth=5)
    ml_l_bonus = clone(learner)
    ml_m_bonus = clone(learner)

    obj_dml_plr = DoubleMLPLR(dml_data, ml_l_bonus, ml_m_bonus)
    obj_dml_plr.fit()
    # print(obj_dml_plr)
    coefficient = obj_dml_plr.coef[0]
    pvalue = obj_dml_plr.pval[0]

    highest_correlations.at[index, 'coefficient'] = float(coefficient)
    highest_correlations.at[index, 'pvalue'] = float(pvalue)

highest_correlations.to_csv("./data/highest_correlations.tsv", sep='\t')

print(highest_correlations[['microbe', 'metabolite', 'correlation', 'coefficient', 'pvalue']])


def plot_correlations(microbe_data, metabolite_data, highest_correlations, file_name):
    fig, axs = plt.subplots(round(sqrt(n_largest)), ceil(sqrt(n_largest)), figsize=(20, 20))

    for i, row in enumerate(highest_correlations.iterrows()):
        treatment_name = row[1]['microbe']
        outcome_name = row[1]['metabolite']
        correlation = row[1]['correlation']
        coefficient = row[1]['coefficient']
        treatment_data = microbe_data[treatment_name]
        outcome_data = metabolite_data[outcome_name]

        ax = axs.reshape(-1)[i]

        color = 'tab:red'
        ax.set_xlabel('samples')
        ax.set_xticklabels([])
        ax.set_ylabel(treatment_name, color=color)
        ax.plot(treatment_data, color=color)
        ax.tick_params(axis='y', labelcolor=color)

        ax2 = ax.twinx()  # instantiate a second Axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel(outcome_name, color=color)  # we already handled the x-label with ax1
        ax2.plot(outcome_data, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        ax.set_title(f"Correlation: {round(float(correlation), 4)}, Coefficient: {round(coefficient, 4)} ")

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(f"./figures/{file_name}.png")


highest_correlations = pd.read_csv("./data/highest_correlations.tsv", sep='\t', index_col=0)
microbes_df = pd.read_csv("./data/microbes_normalized.tsv", sep='\t', index_col=0).T
metabolites_df = pd.read_csv("./data/metabolites_normalized.tsv", sep='\t', index_col=0).T
metabolites_df = metabolites_df.reindex(microbes_df.index)

plot_correlations(microbes_df, metabolites_df, highest_correlations, "10_pairs")
multiple_scatterplots(microbes_df, metabolites_df, highest_correlations, "scatter_plots", n_largest)