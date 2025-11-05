import calendar

import numpy as np
import pandas as pd


def open_data(
    path : str,
    var_name : str
    ):
    
    df = pd.read_csv(path, sep=';', encoding='utf-8')
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y%m%d%H")
    df = df.set_index("DATE")
    df = df.drop("POSTE", axis=1)
    
    sr = df[var_name].astype(str).str.replace(",", ".", regex=False).astype(float)
    dates_nan = sr[sr.isna()].index
    print(dates_nan)
    
    return sr


def reindex_clim_on_year(
    sr_current,
    sr_clim
    
):
    # Getting the climatology data and create a datetime index aligned on the actual year
    target_index = sr_current.index
    year = target_index[0].year

    clim = sr_clim.sort_index()

    if clim.index.max() == 366 and not calendar.isleap(year):
        vals = clim.values.copy()
        vals = np.delete(vals, 59)
        clim_for_year = pd.Series(vals, index=np.arange(1, 366))
    else:
        clim_for_year = clim.copy()

    days = target_index.dayofyear
    mapped_values = clim_for_year.loc[days].values
    sr_clim_on_dates = pd.Series(data=mapped_values, index=target_index)
    
    return sr_clim_on_dates


def compute_diff(
    sr_ref,
    sr_ex
):
    sr_diff = sr_ref - sr_ex
    
    average = sr_diff.mean().round(2)
    max_diff = sr_diff.max().round(2)
    min_diff = sr_diff.min().round(2)
    
    count_above = (sr_ref > sr_ex).sum()
    count_below = (sr_ref < sr_ex).sum()
    total_days = count_above + count_below
    
    above_txt = f"{count_above} days above over {total_days} days"
    below_txt = f"{count_below} days below over {total_days} days"
    
    avg_txt = f"Average difference: +{average} °C"
    max_diff_txt = f"Max difference: +{max_diff} °C"
    min_diff_txt = f"Min difference: {min_diff} °C"
    
    combined = f"{avg_txt}\n{max_diff_txt}\n{min_diff_txt}\n{above_txt}\n{below_txt}"
    
    return combined
