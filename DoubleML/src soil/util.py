import numpy as np
import pandas as pd

def calculate_mean_std(dataframe: pd.DataFrame):
    return np.nanmean(dataframe), np.nanstd(dataframe)

def normalize_df(dataframe: pd.DataFrame):
    return (dataframe-np.nanmean(dataframe))/np.nanstd(dataframe)
