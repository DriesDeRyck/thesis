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

def clr(dataframe: pd.DataFrame):
    """
    :param dataframe: a pandas dataframe containing compositional data with each column representing a different sample
    :return: clr transformed dataframe
    """
    return np.log(dataframe) - np.log(dataframe).mean(axis=0)

def read_ini_file(config, file='settings.ini'):
    config.read(file)

    seed = int(config['general']['seed'])
    learner = config['general']['learner']

    if learner not in ['rf', 'lr', 'boost']:
        raise (ValueError("Learner must be 'lr', 'rf' or 'boost'"))

    learner_settings = {}
    # Check if custom values are specified
    if learner in config:
        # match learner:
        #     case 'rf':
        #         if 'n_estimators' in config[learner]:
        #             learner_settings['n_estimators'] = int(config[learner]['n_estimators'])
        #         if 'max_depth' in config[learner]:
        #             learner_settings['max_depth'] = int(config[learner]['max_depth'])
        #         if 'max_features' in config[learner]:
        #             learner_settings['max_features'] = config[learner]['max_features']
        #             if learner_settings['n_estimators'].isdigit():
        #                 learner_settings['n_estimators'] = int(learner_settings['n_estimators'])
        #
        #     case 'boost':
        #         if 'n_iter_no_change' in config[learner]:
        #             try: learner_settings['n_iter_no_change'] = int(config[learner]['n_iter_no_change'])
        #             except: pass
        #
        #     case 'lr':
        #         learner_settings = {}
        for setting in config[learner]:
            learner_settings[setting] = config[learner][setting]
            if learner_settings[setting].isdigit():
                learner_settings[setting] = int(learner_settings[setting])

    return seed, learner, learner_settings