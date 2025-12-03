import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import packages.plotting as pltt

from packages.mining import reindex_clim_on_year, compute_diff

def climatology(
    sr: pd.Series,
    start: str,
    end: str,
    variable: str,
    folder
):
    """
    Computes climatology for a given variable over a specified period.

    Args:
        sr (pd.Series): initial pd.Series containing the time series data.
        start (str): start date of the climatology period (inclusive).
        end (str): end date of the climatology period (inclusive).
        variable (str): name of the variable for labeling purposes.

    Returns:
        Two pd.Series: climatology computed using median and mean methods.
    """
    start_year = start[:4]
    end_year = end[:4]
    
    if not isinstance(sr.index, pd.DatetimeIndex):
        raise TypeError("Serie index must be a DatetimeIndex")
    
    sr_clim = sr.loc[start:end]
    dayofyear = sr_clim.index.dayofyear
    
    # Computing median method
    method = "median"
    sr_clim_median = sr_clim.groupby(dayofyear).median()
    pltt.plot_data(
        sr_clim_median,
        "Normal",
        f"{variable} normal ({method} / {start_year}-{end_year})",
        f"{folder}/{method}_norm_{variable}_{start_year}_{end_year}"
    )
    # Computing mean method
    method = "mean"
    sr_clim_mean = sr_clim.groupby(dayofyear).mean()
    pltt.plot_data(
        sr_clim_mean,
        "Normal",
        f"{variable} normal ({method} / {start_year}-{end_year})",
        f"{folder}/{method}_norm_{variable}_{start_year}_{end_year}"
    )

    return sr_clim_median, sr_clim_mean


def quantiles(
    sr : pd.Series,
    type : str,
    title : str,
    ylabel : str,
    img_path : str,
    all : bool = True
):
    """
    This function computes and plots quantiles from a datasets. 

    Args:
        sr (pd.Series): pandas serie containing the data
        type (str): type of data used (eg: max, min, avg)
        title (str): title of the chart
        ylabel (str): name for the ylabel chart depending on the data type 
        img_path (str): path to storage the chart as a png image
        all (bool, optional): Depending on the data, can plot all the quantiles by True or
                            only mean/max/min with False. Defaults to True.

    Returns:
        Dictionnary containing the computed quantiles
    """

    if type == "avg":
        sr_daily = sr.resample("D").mean()
    elif type == "max":
        sr_daily = sr.resample("D").max()
    elif type == "min":
        sr_daily = sr.resample("D").min()

    dayofyear = sr_daily.index.dayofyear
    dic_quantiles = {}
    
    quantile_map = {
        "Q10": 0.10,
        "Q25": 0.25,
        "Q50": 0.50,
        "Q75": 0.75,
        "Q90": 0.90
    }
    for qname, qval in quantile_map.items():
        dic_quantiles[qname] = sr_daily.groupby(dayofyear).quantile(qval)
    
    dic_quantiles["Max"] = sr_daily.groupby(dayofyear).max()
    dic_quantiles["Min"] = sr_daily.groupby(dayofyear).min()

    # Number of days per year
    days_per_year = sr_daily.groupby(sr_daily.index.year).size()
    # Count year's number of days < 365
    need_fix = (days_per_year < 365).any()

    if need_fix:
        index_full = pd.Index(range(1, 366))
        for k in dic_quantiles:
            dic_quantiles[k] = dic_quantiles[k].reindex(index_full).interpolate()

    pltt.plot_quantiles(
        dic_quantiles,
        title,
        ylabel,
        img_path,
        all
    )
    
    return dic_quantiles


def quantile_max(
    sr,
    start_date,
    end_date,
    title
):
    """
    This function is quite similar to the quantiles function. 
    Improvments could be done by merging both functions.

    Args:
        sr (pd.Series): _description_
        start_date (str): _description_
        end_date (str): _description_
        title (str): _description_
    """
    sr_selected = sr.loc[start_date:end_date]
    sr_selected_d = sr_selected.resample("D").max()
    
    dayofyear = sr_selected_d.index.dayofyear
    sr_q50 = sr_selected_d.groupby(dayofyear).quantile(0.50)
    sr_max = sr_selected_d.groupby(dayofyear).max()
    sr_min = sr_selected_d.groupby(dayofyear).min()
    
    pltt.plot_quantiles_max(sr_q50, sr_max, sr_min, title)


def thresholds (
    variable: str,
    months : list,
    first_sr : pd.Series,
    second_sr : pd.Series,
    threshold : int,
    study_sign : str
):
    """
    Computes and plots the frequency of days exceeding or below a given temperature threshold
    for two different periods and specified months.
    
    Args:
        months (list): List of month numbers to consider (e.g., [6, 7, 8] for June, July, August).
        first_sr (pd.Series): Temperature series for the first period.
        second_sr (pd.Series): Temperature series for the second period.
        threshold (int): Temperature threshold to evaluate (°C).
        data_type (str): Type of temperature data ("maximal" or "minimal").
        study_sign (str): Sign to study, either ">" or "<".
    """
    
    if months == [12, 1, 2]:
        months_letter="DJF"
    elif months == [3, 4, 5]:
        months_letter="MAM"
    elif months == [6, 7, 8]:
        months_letter="JJA"
    elif months == [9, 10, 11]:
        months_letter="SON"
    
    periods = [f"{first_sr.index.year.min()}-{first_sr.index.year.max()}",
               f"{second_sr.index.year.min()}-{second_sr.index.year.max()}"]
    
    if variable in ["temperature", "minimal temperature", "maximal temperature"]:
        unit = "°C"
    elif variable == "relative humidity":
        unit = "%"
    elif variable == "precipitation":
        unit = "mm"
    else:
        raise ValueError("Variable unit not defined")
    
    # List to store the counts
    count = []
    
    # Selecting the months
    sr_frst = first_sr[first_sr.index.month.isin(months)]
    sr_snd = second_sr[second_sr.index.month.isin(months)]
    
    if study_sign == ">":
        sr_freq_frst = sr_frst[sr_frst > threshold]
        sr_freq_snd = sr_snd[sr_snd > threshold]
        
    elif study_sign == "<":
        sr_freq_frst = sr_frst[sr_frst < threshold]
        sr_freq_snd = sr_snd[sr_snd < threshold]
    
    else:
        raise ValueError("Study sign must be either '>' or '<'")
    
    count_frst = sr_freq_frst.count()
    date_frst = sr_freq_frst.index.to_list()
    print(f"Numbre of days with {variable} {study_sign} {threshold}{unit} for {periods[0]} : {count_frst}")
    print(f"The corresponding dates are : {date_frst}")
    count.append(count_frst)
    
    count_snd = sr_freq_snd.count()
    date_snd = sr_freq_snd.index.to_list()
    print(f"Numbre of days with {variable} {study_sign} {threshold}{unit} for {periods[1]} : {count_snd}")
    print(f"The corresponding dates are : {date_snd}")
    count.append(count_snd)
    
    # Plotting the frequency comparison
    pltt.plot_threshold(
        variable,
        unit,
        count,
        months_letter,
        threshold,
        periods,
        study_sign
    )
    
    
def thresholds_serie(
    variable: str,
    months : list,
    list_sr : list,
    threshold : int,
    study_sign : str
):
    """
    Computes and plots the frequency of days exceeding or below a given temperature threshold
    for two different periods and specified months.
    
    Args:
        months (list): List of month numbers to consider (e.g., [6, 7, 8] for June, July, August).
        first_sr (pd.Series): Temperature series for the first period.
        second_sr (pd.Series): Temperature series for the second period.
        threshold (int): Temperature threshold to evaluate (°C).
        data_type (str): Type of temperature data ("maximal" or "minimal").
        study_sign (str): Sign to study, either ">" or "<".
    """
    
    dic_count = {}
    
    if variable in ["temperature", "minimal temperature", "maximal temperature"]:
        unit = "°C"
    elif variable == "relative humidity":
        unit = "%"
    elif variable == "precipitation":
        unit = "mm"
    else:
        raise ValueError("Variable unit not defined")
    
    # Seasons definition
    seasons = {
        (12, 1, 2): "DJF",
        (3, 4, 5): "MAM",
        (6, 7, 8): "JJA",
        (9, 10, 11): "SON",
    }
    
    months_letter = None
    for mlist, label in seasons.items():
        if set(months) == set(mlist):
            months_letter = label
            break

    if months_letter is None:
        months_letter = str(months)
        
    for sr in list_sr:
        
        period = f"{sr.index.year.min()}-{sr.index.year.max()}"

        # Selecting the months
        sr_months = sr[sr.index.month.isin(months)]
    
        if study_sign == ">":
            sr_freq = sr_months[sr_months > threshold]
        elif study_sign == "<":
            sr_freq = sr_months[sr_months < threshold]
        else:
            raise ValueError("Study sign must be either '>' or '<'")
    
        count = sr_freq.count()
        date = sr_freq.index.to_list()
        print(f"Numbre of days with {variable} {study_sign} {threshold}{unit} for {period} : {count}")
        print(f"The corresponding dates are : {date}")
        
        dic_count[period] = count
    
    # Plotting the frequency comparison
    pltt.plot_threshold_serie(
        variable,
        unit,
        dic_count,
        months_letter,
        threshold,
        study_sign
    )
    
    return dic_count
    
    
def year_vs_climato(
    sr: pd.Series,
    sr_climato: pd.Series,
    dic_quantiles,
    time_range_climato:str,
    start: str,
    end: str = None,
):
    """_summary_

    Args:
        sr (pd.Series): _description_
        sr_climato (pd.Series): _description_
        time_range_climato (_type_): corresponds to the period used to compute the climatology.
        Can be "1990-2019" or "1960-1989".
        end (str, optional): _description_. Defaults to None.
    """

    # Getting the actual year data
    year = start[:4]
    sr_actu_year = sr.loc[start:end]
    sr_actu_year_d = sr_actu_year.resample("D").mean()
    
    sr_clim_on_dates = reindex_clim_on_year(
        sr_actu_year_d,
        sr_climato
        )
    
    dic_quantiles_on_dates = {}
    for key in dic_quantiles:
        dic_quantiles_on_dates[key] = reindex_clim_on_year(
            sr_actu_year_d,
            dic_quantiles[key]
            )
    
    # Computing differences
    all_diff = compute_diff(
        sr_actu_year_d,
        sr_clim_on_dates
    )
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        sr_actu_year_d.index,
        sr_actu_year_d,
        label=f"{year} temperature",
        color="red"
        ) 
    ax.plot(
        sr_clim_on_dates.index,
        sr_clim_on_dates,
        label=f"Normal-{time_range_climato}",
        color="blue"
        ) 

    ax.set_title(f"Comparison between {year} temperature and {time_range_climato} normal at Rivesaltes station") 
    ax.set_xlabel("Date") 
    ax.set_ylabel("Temperature (°C)") 
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.5))
    ax.grid(True) 
    ax.legend() 
    plt.tight_layout() 

    valid = sr_actu_year_d.notna() & sr_clim_on_dates.notna()  # éviter NaN lors du remplissage
    ax.fill_between(sr_actu_year_d.index, 
                    sr_actu_year_d, sr_clim_on_dates, 
                    where=(valid & (sr_actu_year_d > sr_clim_on_dates)), 
                    interpolate=True, color="red", alpha=0.3
                    )
    ax.fill_between(sr_actu_year_d.index, 
                    sr_actu_year_d, sr_clim_on_dates, 
                    where=(valid & (sr_actu_year_d <= sr_clim_on_dates)), 
                    interpolate=True, color="blue", alpha=0.2
                    )

    if year == "2025":
        ax.text(
            0.72, 0.035,
            all_diff,
            transform=ax.transAxes,
            va="bottom",
            ha="left",
            fontsize=10,
            bbox=dict(facecolor="white", alpha=1, edgecolor="red")  
        )
    else:
        ax.text(
            0.45, 0.035,
            all_diff,
            transform=ax.transAxes,
            va="bottom",
            ha="left",
            fontsize=10,
            bbox=dict(facecolor="white", alpha=1, edgecolor="red")  
        )

    plt.savefig(
        f"figs/temp/clim_vs_year/norm_{time_range_climato}_{year}_year.png",
        dpi=300,
        bbox_inches="tight"
    )
    
    # Plotting compared to quantiles
    pltt.actu_year_vs_plot(
        dic_quantiles_on_dates,
        sr_actu_year_d,
        time_range_climato,
        year
    )
    
    
def precip_climato(
    sr_ini,
    start,
    end,
    freq,
    method
):
    """
    Computes the precipitation climatology over a given period.
    
    Args:
        sr_ini (pd.Series): Initial precipitation series with datetime index.
        start (str): Start date of the climatology period (inclusive).
        end (str): End date of the climatology period (inclusive).
        freq (str): Resampling frequency (e.g., 'D' for daily, 'M' for monthly).
        method (str): Method to compute climatology ('mean', 'median', etc.).
        
    Returns:
        pd.Series: Climatology series resampled to the specified frequency.
    """
    sr_tdy = sr_ini.loc[start:end]
    frst_year = start[:4]
    last_year = end[:4]
    
    
    if freq == "D":
        sr_stdy_d = sr_tdy.resample("D").sum()
        
        if method == "mean":
            dayofyear = sr_stdy_d.index.dayofyear
            sr_climato = sr_stdy_d.groupby(dayofyear).mean()
        if method == "median":
            dayofyear = sr_stdy_d.index.dayofyear
            sr_climato = sr_stdy_d.groupby(dayofyear).median()

        pltt.plot_rr_nrm(
            sr_climato,
            frst_year,
            last_year,
            freq,
            method
        )
        
    elif freq == "M":
        sr_stdy_m = sr_tdy.resample("ME").sum()
        
        if method == "mean":
            sr_climato = sr_stdy_m.groupby(sr_stdy_m.index.month).mean()
        if method == "median":
            sr_climato = sr_stdy_m.groupby(sr_stdy_m.index.month).median()
        
        pltt.plot_rr_nrm(
            sr_climato,
            frst_year,
            last_year,
            freq,
            method
        )
        
    return sr_climato


def clim_ma(
    sr,
    var_name,
    ma_range,
    method,
    start_range,
    end_range,
    folder = None,
    plot = True
):
    """
    Produces a normal based on a moving average method <=> Ti for i day is equal to the average of T[i-n;i-1], 
    Ti and T[i+1;i+n] where n is the max number of days taken before and after the i day. Smoothes the normal.

    Args:
        sr (pd.series): pandas series containing the values
        ma_range (int): numbers of days used to compute the moving average (equal to 2n+1)
        method (str): can be mean or median
        start_range (str): first date time to compute the normal
        end_range (str): last date time to compute the normal
        folder (str): folder to store the image
        
    Returns:
        pd.series: contaning the normal indexes on 366 days
    """
    sr_range = sr.loc[start_range:end_range]
    
    start_year = start_range[:4]
    end_year = end_range[:4]
    
    # Extracting each day
    day = sr_range.index.dayofyear
    if method == "mean":
        sr_day = sr_range.groupby(day).apply(np.mean)
    elif method == "median":
        sr_day = sr_range.groupby(day).apply(np.median)
        
    # Risk for limit days (as 1 or 365) to not be able to have an average
    # Wrap-around of the calendar to do the average for 1 with 364/364/365 and 2/3/4
    # It creates a continuity: 365 is followed by 1
    sr_extended = pd.concat(
        [sr_day, sr_day, sr_day], 
        ignore_index=True
        )
    
    # Applying the moving average
    if method == "mean":
        sr_smoothed = sr_extended.rolling(
            window=ma_range, 
            center=True, 
            min_periods=1
            ).mean()
    elif method == "median":
        sr_smoothed = sr_extended.rolling(
            window=ma_range, 
            center=True, 
            min_periods=1
            ).median()
    
    # Extracting the central part = smooth climatology
    n = len(sr_day)
    sr_clim = sr_smoothed[n : 2*n].reset_index(drop=True)
    
    if folder is not None:
        if plot == True:
            pltt.plot_data(
                sr_clim,
                "Normal",
                f"Moving average ({ma_range} days) {method} normal {var_name} ({start_year}-{end_year})",
                f"{folder}/ma_{ma_range}days_{method}_norm_{start_year}_{end_year}"
            )
    
    return sr_clim


def clim_ma_compa(
    sr,
    range_ma,
    method,
    start_range,
    end_range,
    folder = None
):
    
    dic_nrms = {}
    start, stop, step = range_ma
    
    for ndays in range(start, stop, step):
        sr_clim = clim_ma(
            sr,
            ndays,
            method,
            start_range,
            end_range,
            folder,
            False
            )
        dic_nrms[ndays] = sr_clim
    
    return (dic_nrms)


def ma_quantiles(
    sr,
    ma_range,
    type,
    start_range,
    end_range,
    title,
    ylabel,
    folder,
    all = True
):
    """
    Compute moving-average climatological quantiles using the same wrap-around logic
    as clim_ma().

    Args:
        sr (pd.Series): time series data
        ma_range (int): moving average window (must be odd ideally)
        type (str): "avg", "max", "min" (same as quantiles())
        start_range (str): beginning of period
        end_range (str): end of period
        folder (str): folder to save plots
        quantiles (list): quantiles to compute
        plot (bool): produce plot or not

    Returns:
        dict of pd.Series: smoothed quantiles indexed 1..366
    """

    sr_range = sr.loc[start_range:end_range]
    start_year = start_range[:4]
    end_year = end_range[:4]

    if type == "avg":
        sr_daily = sr_range.resample("D").mean()
    elif type == "max":
        sr_daily = sr_range.resample("D").max()
    elif type == "min":
        sr_daily = sr_range.resample("D").min()

    dayofyear = sr_daily.index.dayofyear

    # --- Raw quantiles per day ---
    dic_q = {}

    qnames = ["Q10", "Q25", "Q50", "Q75", "Q90"]
    qvalues = [0.10, 0.25, 0.50, 0.75, 0.90]

    for qname, qval in zip(qnames, qvalues):
        dic_q[qname] = sr_daily.groupby(dayofyear).quantile(qval)

    # Add Min/Max
    dic_q["Min"] = sr_daily.groupby(dayofyear).min()
    dic_q["Max"] = sr_daily.groupby(dayofyear).max()

    # --- Wrap-around extension (same as clim_ma) ---
    dic_ext = {}
    for key, serie in dic_q.items():
        dic_ext[key] = pd.concat([serie, serie, serie], ignore_index=True)

    # --- Rolling window smoothing ---
    dic_smooth = {}
    for key, serie in dic_ext.items():
        dic_smooth[key] = (
            serie.rolling(
                window=ma_range,
                center=True,
                min_periods=1
            ).mean()
        )

    # --- Extract central part (+ reset index 1..366) ---
    n = len(dic_q[qnames[0]])  # number of days = 365 or 366
    dic_final = {}
    for key, serie in dic_smooth.items():
        dic_final[key] = serie[n:2*n].reset_index(drop=True)
        dic_final[key].index = range(1, len(dic_final[key])+1)

    img_path = (
        f"{folder}/ma_{ma_range}days_quantiles_{start_year}_{end_year}"
    )

    # Transform keys for plotting function (needs strings)
    dic_plot = {str(k): v for k, v in dic_final.items()}

    pltt.plot_quantiles(
        dic_plot,
        title,
        ylabel,
        img_path,
        all
    )

    return dic_final


def season_box(
    sr_list : list,
    months,
    y_label,
    title,
    folder
):
        
    dic_sr = {}
    for sr in sr_list:
        period = f"{sr.index.year.min()}-{sr.index.year.max()}"
        sr_m = sr[sr.index.month.isin(months)]
        sr_grouped = [sr_m[sr_m.index.month == m] for m in months]
        
        if folder == "precip":
            total = sr_m.sum()
            cumul_m = [g.sum() for g in sr_grouped]
        else:
            total = None
            cumul_m = None   
            
        dic_sr[period] = {
            "series": sr_grouped,
            "total": total,
            "cumul_m": cumul_m
    }
    
    pltt.season_box_plot(dic_sr, months, y_label, title, folder)

    return None