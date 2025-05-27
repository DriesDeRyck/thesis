import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sbn
import scipy.stats as stats
from math import sqrt, ceil

from correlation_test import metabolites_df, microbes_df


def scatter_plot(treatment_data, outcome_data, treatment_name, outcome_name):
    # df = pd.DataFrame({treatment_name: treatment_data, outcome_name: outcome_data})
    rho, p_value = stats.spearmanr(treatment_data, outcome_data)

    plt.scatter(treatment_data, outcome_data)
    plt.plot(np.sort(treatment_data), np.sort(outcome_data), color='red')
    plt.title("Spearman correlation coefficient: {:.4f}".format(rho))
    plt.xlabel(treatment_name)
    plt.ylabel(outcome_name)
    plt.show()


def multiple_scatterplots(microbe_data, metabolite_data, highest_correlations, file_name, n_plots):
    fig, axs = plt.subplots(ceil(sqrt(n_plots)), ceil(sqrt(n_plots)), figsize=(20, 20))

    for i, row in enumerate(highest_correlations.iterrows()):
        treatment_name = row[1]['microbe']
        outcome_name = row[1]['metabolite']
        correlation = row[1]['correlation']
        coefficient = row[1]['coefficient']
        treatment_data = microbe_data[treatment_name]
        outcome_data = metabolite_data[outcome_name]

        ax = axs.reshape(-1)[i]

        color = ['tab:red', 'tab:blue']
        ax.set_xlabel(treatment_name, color=color[0])
        # ax.set_xticklabels([])
        ax.set_ylabel(outcome_name, color=color[1])
        # ax.set_yticklabels([])
        ax.scatter(treatment_data, outcome_data)

        ax.set_title(f"Correlation: {round(float(correlation), 4)}, Coefficient: {round(coefficient, 4)} ")

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(f"./figures/{file_name}.png")


def plot_single_correlation(treatment_data, outcome_data, treatment_name, outcome_name, correlation=None):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('samples')
    ax1.set_ylabel(treatment_name, color=color)
    ax1.plot(treatment_data, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Rotate x-axis labels vertically
    # ax1.tick_params(axis='x', labelrotation=90)

    ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel(outcome_name, color=color)  # we already handled the x-label with ax1
    ax2.plot(outcome_data, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    rho, p_value = stats.spearmanr(treatment_data, outcome_data)
    correlation = rho
    if correlation is not None:
        plt.title(f"Correlation: {round(float(rho), 4)}")
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(f"{treatment_name}-{outcome_name}.png")


if __name__ == "__main__":
    # %%
    treatment = '(2,3-dihydroxy-3-methylbutanoate)'
    outcome = '(2,5-diaminohexanoate)'

    treatment = 'rplo 1 (Cyanobacteria)'
    outcome = 'rplo 153 (Bacteroidetes)'

    #
    # treatment_val = ""
    # outcome_val = ""
    # for i in microbes_df.T[treatment].values:
    #     treatment_val += f"{i} "
    # for i in microbes_df.T[outcome].values:
    #     outcome_val += f"{i} "
    #
    # print(treatment_val)
    # print(outcome_val)
    # plot_single_correlation(metabolites_df.T[treatment], metabolites_df.T[outcome], treatment, outcome)
    # scatter_plot(metabolites_df.T[treatment], metabolites_df.T[outcome], treatment, outcome)
    scatter_plot(microbes_df.T[treatment], microbes_df.T[outcome], treatment, outcome)
