import sys
import os.path
from pathlib import Path
import numpy as np
import pandas as pd
from doubleml import DoubleMLData, DoubleMLPLR
import matplotlib.pyplot as plt
# from tqdm import tqdm
from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LassoCV, LinearRegression
from time import time

from joblib import Parallel, delayed

np.random.seed(3141)

if len(sys.argv) == 4:
    microbe_file = sys.argv[1]
    metabolite_file = sys.argv[2]
    results_dir = sys.argv[3]
else:
    microbe_file = "./data/microbes_normalized.tsv"
    metabolite_file = "./data/metabolites_normalized.tsv"
    results_dir = "./data/"

# read dataframes from files
microbes_normalized = pd.read_csv(microbe_file, sep='\t', index_col=0)
metabolites_normalized = pd.read_csv(metabolite_file, sep='\t', index_col=0)

# use transposed dataframe such that each row is a sample from the dataset
microbes_T = microbes_normalized.T
metabolites_T = metabolites_normalized.T
# %%
# get names of microbes and metabolites
microbe_names = np.array(microbes_normalized.index.sort_values())
metabolite_names = np.array(metabolites_normalized.index.sort_values())

# calculate DML coefficient for each (microbe, metabolite) pair
coefficient_matrix = pd.DataFrame(columns=microbe_names, index=metabolite_names, dtype=float)
pvalues = pd.DataFrame(columns=microbe_names, index=metabolite_names, dtype=float)

sensitivity_test = pd.DataFrame(columns=microbe_names, index=metabolite_names)


# %%
def single_dml_calculation(microbe, metabolite, seed=3141):
    np.random.seed(seed)
    outcome = metabolite
    joined_data = pd.concat([metabolites_T[outcome], microbes_T], axis=1)

    treatment = microbe
    # get column names of covariates
    cols = microbes_T.columns
    cols = cols.drop(treatment)

    # make DML Data frame
    dml_data = DoubleMLData(joined_data,
                            y_col=outcome,
                            d_cols=treatment,
                            x_cols=list(cols))

    learner = RandomForestRegressor(n_estimators=100, max_features='sqrt', max_depth=5)
    # learner = LinearRegression()  # trying Linear Regression to see if it speeds up calculation
    ml_l_bonus = clone(learner)
    ml_m_bonus = clone(learner)

    obj_dml_plr = DoubleMLPLR(dml_data, ml_l_bonus, ml_m_bonus)
    obj_dml_plr.fit()
    # print(obj_dml_plr)
    # print(obj_dml_plr.confint())
    obj_dml_plr.sensitivity_analysis()
    sensitivity_result = obj_dml_plr.sensitivity_params
    # print(obj_dml_plr.sensitivity_summary)
    # obj_dml_plr.sensitivity_plot()

    coefficient = obj_dml_plr.coef[0]
    pvalue = obj_dml_plr.pval[0]

    # coefficient_matrix.at[outcome, treatment] = float(coefficient)
    # pvalues.at[outcome, treatment] = float(pvalue)

    return [coefficient, pvalue, microbe, metabolite, sensitivity_result]


start = time()
output = Parallel(n_jobs=-1)(delayed(single_dml_calculation)(i, j) for j in metabolite_names for i in microbe_names)
end = time()
print("{:.4f}".format(end - start))
#
# coefficients_list = [pair[0] for pair in output]
# pvalues_list = [pair[1] for pair in output]
# sensitivity_list = [pair[4] for pair in output]

for result in output:
    coefficient_matrix.at[result[3], result[2]] = float(result[0])
    pvalues.at[result[3], result[2]] = float(result[1])
    sensitivity_test.at[result[3], result[2]] = result[4]

print("{:.3f}".format(time() - end))

# make sure results directory exists
Path(results_dir).mkdir(parents=True, exist_ok=True)

coefficient_matrix.to_csv(os.path.join(results_dir, "coefficient_matrix_parallel.tsv"), sep='\t', index=True)
pvalues.to_csv(os.path.join(results_dir, "pvalues_matrix.tsv"), sep='\t', index=True)
sensitivity_test.to_csv(os.path.join(results_dir, "sensitivity_test.tsv"), sep='\t', index=True)

# plt.matshow(coefficient_matrix, cmap='bwr')
# plt.savefig("./figures/coefficient_matrix.png")
