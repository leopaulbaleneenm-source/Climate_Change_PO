import pandas as pd
import matplotlib.pyplot as plt

from packages.mining import reindex_clim_on_year, compute_diff
from packages.plotting import actu_year_vs_plot, plot_rr_nrm, plot_threshold, plot_data


def climatology(
    sr: pd.Series,
    start: str,
    end: str,
    variable: str,
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
    plot_data(
        sr_clim_median,
        "Normal",
        f"{variable} normal ({method}) in Rivesaltes computed from {start_year} to {end_year}",
        f"{method}_norm_{variable}_{start_year}_{end_year}"
    )
    # Computing mean method
    method = "mean"
    sr_clim_mean = sr_clim.groupby(dayofyear).mean()
    plot_data(
        sr_clim_mean,
        "Normal",
        f"{variable} normal ({method}) in Rivesaltes computed from {start_year} to {end_year}",
        f"{method}_norm_{variable}_{start_year}_{end_year}"
    )

    return sr_clim_median, sr_clim_mean


def quantiles(
    sr : pd.Series,
    title : str,
    ylabel : str,
    img_path : str
):

    sr_daily = sr.resample("D").mean()
    dayofyear = sr_daily.index.dayofyear
    dic_quantiles = {}
    
    sr_q10 = sr_daily.groupby(dayofyear).quantile(0.10)
    sr_q25 = sr_daily.groupby(dayofyear).quantile(0.25)
    sr_q50 = sr_daily.groupby(dayofyear).quantile(0.50)
    sr_q75 = sr_daily.groupby(dayofyear).quantile(0.75)
    sr_q90 = sr_daily.groupby(dayofyear).quantile(0.90)
    sr_max = sr_daily.groupby(dayofyear).max()
    sr_min = sr_daily.groupby(dayofyear).min()
    
    dic_quantiles["Q10"] = sr_q10
    dic_quantiles["Q25"] = sr_q25
    dic_quantiles["Q50"] = sr_q50
    dic_quantiles["Q75"] = sr_q75
    dic_quantiles["Q90"] = sr_q90
    dic_quantiles["Max"] = sr_max
    dic_quantiles["Min"] = sr_min

    plt.figure(figsize=(12, 6))
    plt.plot(sr_q10.index, sr_q10, label="Q10", linestyle="--", color="lightgreen")
    plt.plot(sr_q25.index, sr_q25, label="Q25", linestyle="--", color="green")
    plt.plot(sr_q50.index, sr_q50, label="Median", color="blue")
    plt.plot(sr_q75.index, sr_q75, label="Q75", linestyle="--", color="orange")
    plt.plot(sr_q90.index, sr_q90, label="Q90", linestyle="--", color="red")
    plt.plot(sr_max.index, sr_max, label="Max", color="black")
    plt.plot(sr_min.index, sr_min, label="Min", color="black")
    plt.fill_between(sr_min.index, sr_min, sr_max, color="lightgray", alpha=0.3)
    plt.legend()
    plt.title(f"{title}")
    plt.xlabel("Date")
    plt.ylabel(f"{ylabel}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(
        f"figs/{img_path}.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()
    
    return dic_quantiles


def thresholds (
    variable: str,
    months : list,
    months_letter : str,
    first_sr : pd.Series,
    second_sr : pd.Series,
    threshold : int,
    periods : list,
    study_sign : str
):
    """
    Computes and plots the frequency of days exceeding or below a given temperature threshold
    for two different periods and specified months.
    
    Args:
        months (list): List of month numbers to consider (e.g., [6, 7, 8] for June, July, August).
        months_letter (str): String representation of the months (e.g., "JJA").
        first_sr (pd.Series): Temperature series for the first period.
        second_sr (pd.Series): Temperature series for the second period.
        threshold (int): Temperature threshold to evaluate (°C).
        data_type (str): Type of temperature data ("maximal" or "minimal").
        periods (list): List containing two strings representing the periods (e.g., ["1997-2010", "2011-2024"]).
        study_sign (str): Sign to study, either ">" or "<".
    """
    
    if variable == "temperature" or "minimal temperature" or "maximal temperature":
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
    plot_threshold(
        variable,
        unit,
        count,
        months_letter,
        threshold,
        periods,
        study_sign
    )
    
    
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
        f"figs/temp/norm_{time_range_climato}_{year}_year.png",
        dpi=300,
        bbox_inches="tight"
    )
    
    # Plotting compared to quantiles
    actu_year_vs_plot(
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

        plot_rr_nrm(
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
        
        plot_rr_nrm(
            sr_climato,
            frst_year,
            last_year,
            freq,
            method
        )
        
    return sr_climato