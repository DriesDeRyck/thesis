import sys
import os.path
from pathlib import Path
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import pandas as pd
from doubleml import DoubleMLData, DoubleMLPLR
# from tqdm import tqdm
from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LassoCV, LinearRegression
from xgboost import XGBRegressor
from time import time
from util import read_ini_file
from argparse import ArgumentParser
from configparser import ConfigParser
from joblib import Parallel, delayed


def run_dml(microbe_file, metabolite_file, results_dir, learner, seed=4131):
    # read dataframes from files
    microbes_T = pd.read_csv(microbe_file, sep='\t', index_col=0).T
    metabolites_T = pd.read_csv(metabolite_file, sep='\t', index_col=0).T

    # get names of microbes and metabolites
    microbe_names = np.array(microbes_T.columns.sort_values())
    metabolite_names = np.array(metabolites_T.columns.sort_values())

    # calculate DML coefficient for each (microbe, metabolite) pair
    coefficient_matrix = pd.DataFrame(columns=microbe_names, index=metabolite_names, dtype=float)
    pvalues = pd.DataFrame(columns=microbe_names, index=metabolite_names, dtype=float)
    sensitivity_test = pd.DataFrame(columns=microbe_names, index=metabolite_names)

    def single_dml_calculation(microbe, metabolite, seed=4131):
        np.random.seed(seed)
        # print(np.random.rand())
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
    output = Parallel(n_jobs=-1)(delayed(single_dml_calculation)(i, j, seed) for j in metabolite_names for i in microbe_names)
    end = time()
    print("Time to run DML: ","{:.4f}".format(end - start), " seconds")
    #
    # coefficients_list = [pair[0] for pair in output]
    # pvalues_list = [pair[1] for pair in output]
    # sensitivity_list = [pair[4] for pair in output]

    for result in output:
        coefficient_matrix.at[result[3], result[2]] = float(result[0])
        pvalues.at[result[3], result[2]] = float(result[1])
        sensitivity_test.at[result[3], result[2]] = result[4]

    # print("{:.3f}".format(time() - end))

    coefficient_matrix.to_csv(os.path.join(results_dir, "coefficients.tsv"), sep='\t', index=True)
    pvalues.to_csv(os.path.join(results_dir, "pvalues.tsv"), sep='\t', index=True)
    sensitivity_test.to_csv(os.path.join(results_dir, "sensitivity_test.tsv"), sep='\t', index=True)


if __name__ == "__main__":
    # parse arguments
    argparser = ArgumentParser("Run DML")
    argparser.add_argument("microbes", type=str, help="path to microbe (.tsv) file (rows = microbes, colunms = samples)")
    argparser.add_argument("metabolites", type=str, help="path to metabolite (.tsv) file (rows = metabolites, colunms = samples)")
    argparser.add_argument("results", type=str, help="path to results directory (must not exist)")
    argparser.add_argument("config", type=str, help="path to config (.ini) file (see README for more info)")
    args = argparser.parse_args()
    microbe_file = args.microbes
    metabolite_file = args.metabolites
    results_dir = args.results
    config_file = args.config

    # parse config file
    config = ConfigParser()
    # try to open microbe, metabolite and config file
    try:
        with open(microbe_file, 'r') as f:
            pass
        with open(metabolite_file) as f:
            pass
        with open(config_file) as f:
            pass
    except Exception as e:
        print(f"Could not find files\n", type(e), e)
        exit(1)

    try:
        seed, learner_type, learner_settings = read_ini_file(config, file=config_file)
    except Exception as e:
        print("Could not parse settings file\n", type(e), e)
        exit(1)

    np.random.seed(seed)

    # try to construct learner with specified settings
    try:
        match learner_type:
            case 'lr':
                learner = LinearRegression()
            case 'rf':
                learner = RandomForestRegressor(**learner_settings)
            case 'boost':
                learner = GradientBoostingRegressor(**learner_settings)
            case 'xgboost':
                learner = XGBRegressor(**learner_settings)
            case _:
                raise Exception(f"Unknown learner type: {learner_type}")
    except Exception as e:
        print(f"Could not construct learner with settings: {learner_settings}\n", type(e), e)
        exit(1)

    # make sure results directory exists
    try:
        Path(results_dir).mkdir(parents=True, exist_ok=False)
    except Exception as e:
        print(f"Could not create results directory\n", type(e), e)
        exit(1)

    print(f"Running DML_parallel with seed {seed}, learner {learner_type}, and learner settings {learner_settings}\n")
    print(f"{type(learner)}: {learner.get_params()}\n")

    run_dml(microbe_file, metabolite_file, results_dir, learner, seed)

    # save settings together with results in results dir
    with open(os.path.join(results_dir, 'settings.ini'), 'w') as configfile:
        configfile.write(f"# Config file used with {microbe_file} and {metabolite_file}\n")
        config.write(configfile)

    exit(0)
