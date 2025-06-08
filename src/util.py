import os
import numpy as np
import pandas as pd
from src.evaluate import _edge_roc_curve
from pathlib import Path


def calculate_mean_std(dataframe: pd.DataFrame):
    return np.nanmean(dataframe), np.nanstd(dataframe)


def normalize_df(dataframe: pd.DataFrame):
    # subtracts mean of whole dataframe and divides by std of whole dataframe (for absolute values?)
    return (dataframe - np.nanmean(dataframe)) / np.nanstd(dataframe)


def normalize_per_column(dataframe: pd.DataFrame):
    """
    Subtracts mean of each column and divides by std of each column (for relative values)
    :param dataframe:
    :return: normalized dataframe
    """
    return (dataframe - dataframe.mean()) / dataframe.std()


def drop_const_columns(df: pd.DataFrame):
    """
    Removes all columns in a dataframe whose std is zero (value is constant for whole column).
    :param df: original dataframe
    :return: dataframe without constant columns
    """
    constant = df.loc[:, (df.std() < np.finfo(np.float64).eps)]  # filter on std smaller than machine precision
    return df.drop(constant.columns.tolist(), axis=1)


def drop_sparse_columns(df: pd.DataFrame, threshold: float):
    """
    Remove all columns with higher ratio of zero values than threshold.
    :param df: original dataframe
    :param threshold: float in range [0, 1]
    :return: dataframe without sparse columns
    """
    nr_rows = df.shape[0]
    zero_ratios = (df == 0).sum(axis=0) / nr_rows
    df = df.loc[:, (zero_ratios <= threshold)]  # keep columns where zero_ratio is below threshold
    return df


def isfloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def clr(dataframe: pd.DataFrame):
    """
    :param dataframe: a pandas dataframe containing compositional data with each column representing a different sample
    :return: clr transformed dataframe
    """
    return np.log(dataframe) - np.log(dataframe).mean(axis=0)


def read_ini_file(config, file='settings.ini', automl=False):
    config.read(file)

    seed = int(config['general']['seed'])
    learner = config['general']['learner']

    if (learner not in ['rf', 'lr', 'boost', 'xgboost']) and (automl is False):
        raise (ValueError("Learner must be 'lr', 'rf', 'boost' or 'xgboost'"))
    elif learner != 'automl' and automl is True:
        raise (ValueError("Learner must be 'automl'"))

    learner_settings = {}
    # Check if custom values are specified
    if learner in config:
        for setting in config[learner]:
            learner_settings[setting] = config[learner][setting]
            if learner_settings[setting].isdigit():
                learner_settings[setting] = int(learner_settings[setting])
            elif isfloat(learner_settings[setting]):
                learner_settings[setting] = float(learner_settings[setting])

    return seed, learner, learner_settings

def _roc_curve(name, ranks, edges, k_max=100, axis=1):
    # if _edges_roc_curve has been calculated before, load from files
    if os.path.exists(os.path.join('./results/roc/', name)):
        res = [pd.read_csv(os.path.join('./results/roc/', name, f'{name}_0.tsv'), sep='\t', index_col=0),
               pd.read_csv(os.path.join('./results/roc/', name, f'{name}_1.tsv'), sep='\t', index_col=0),
               pd.read_csv(os.path.join('./results/roc/', name, f'{name}_2.tsv'), sep='\t', index_col=0),
               ]
    # else do calculation (takes some time)
    else:
        res = _edge_roc_curve(ranks, edges, k_max, axis=axis)
        Path(os.path.join('./results/roc/', name)).mkdir(parents=True, exist_ok=False)
        for i in range(len(res)):
            res[i].to_csv(os.path.join('./results/roc/', name, f'{name}_{str(i)}.tsv'), sep='\t', index=True)
    return res