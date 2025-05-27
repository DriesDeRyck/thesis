import numpy as np
import pandas as pd


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
    df = df.loc[:, (zero_ratios <= threshold)]           # keep columns where zero_ratio is below threshold
    return df

def clr(microbes: pd.DataFrame, metabolites: pd.DataFrame):
    pass