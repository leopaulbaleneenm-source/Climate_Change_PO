import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(
    sr: pd.Series,
    var_name: str,
    var_call: str,
    img_title: str,  
    yaxe_precision: bool = False, 
    season: str = None
    ):
    """
    Plots a time series data with appropriate labels and saves the figure.

    Args:
        sr (pd.Series): pd.Series containing the time series data to plot.
        var_name (str): the name of the variable given to the legend of the curve
        var_call (str): the start of the title of the graph
        img_title (str): the name of the image to be saved
        yaxe_precistion (bool, optional): parameter to increase the precision of the y axis.
            Defaults to False.
        season (str, optional): specify the season to adapt x-axis 
            ("DJF", "MAM", "JJA", "SON")
    """

    plt.figure(figsize=(10, 5)) 
    
    if season is not None:
        
        new_index = range(1, len(sr) + 1)
        plt.plot(new_index, sr, label=var_name, color="blue")
        
        # Defining index for the graph
        if season == "DJF":
            plt.xticks([1, 31, 62, 90], ["1 Dec", "1 Jan", "1 Feb", "28/29 Feb"])
        elif season == "MAM":
            plt.xticks([1, 31, 61, 92], ["1 Mar", "1 Apr", "1 May", "31 May"])
        elif season == "JJA":
            plt.xticks([1, 31, 61, 92], ["1 Jun", "1 Jul", "1 Aug", "31 Aug"])
        elif season == "SON":
            plt.xticks([1, 31, 61, 91], ["1 Sep", "1 Oct", "1 Nov", "30 Nov"])
    
    else:
        plt.plot(
            sr.index,
            sr,
            label=var_name,
            color="blue"
            ) 
    
    plt.title(f"{var_call} at Rivesaltes station") 

    plt.xlabel("Date") 
    
    var_call_lower = var_call.lower()
    if "temperature" in var_call_lower:
        plt.ylabel("Temperature (°C)") 
    elif "precipitation" in var_call_lower:
        plt.ylabel("Precipitation (mm)")
    elif "humidity" in var_call_lower:
        plt.ylabel("Relative Humidity (%)")
       
    if yaxe_precision:
        plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(0.5))
        
    plt.grid(True) 
    plt.legend() 
    plt.tight_layout() 
    
    if "temperature" in var_call_lower:
        plt.savefig(
            f"figs/temp/{img_title}.png",
            dpi=300,
            bbox_inches="tight"
        )
    elif "precipitation" in var_call_lower:
        plt.savefig(
            f"figs/precip/{img_title}.png",
            dpi=300,
            bbox_inches="tight"
        )
    elif "humidity" in var_call_lower:
        plt.savefig(
            f"figs/humidity/{img_title}.png",
            dpi=300,
            bbox_inches="tight"
        )
        

def actu_year_vs_plot(
    dic_quantiles,
    sr_actu_year,
    time_range_climato,
    year
    
):
    
    sr_q10 = dic_quantiles["Q10"]
    sr_q25 = dic_quantiles["Q25"]
    sr_q50 = dic_quantiles["Q50"]
    sr_q75 = dic_quantiles["Q75"]
    sr_q90 = dic_quantiles["Q90"]
    sr_max = dic_quantiles["Max"]
    sr_min = dic_quantiles["Min"]
    
    plt.figure(figsize=(12, 6))
    plt.plot(sr_q10.index, sr_q10, label="Q10", linestyle="--", color="lightgreen")
    plt.plot(sr_q25.index, sr_q25, label="Q25", linestyle="--", color="green")
    plt.plot(sr_q50.index, sr_q50, label="Median", color="black")
    plt.plot(sr_q75.index, sr_q75, label="Q75", linestyle="--", color="orange")
    plt.plot(sr_q90.index, sr_q90, label="Q90", linestyle="--", color="red")
    plt.plot(sr_max.index, sr_max, label="Max", color="black")
    plt.plot(sr_min.index, sr_min, label="Min", color="black")
    plt.plot(
        sr_actu_year.index,
        sr_actu_year,
        label="Actual Year",
        color="blue",
        linewidth=2
        )
    plt.fill_between(sr_min.index, sr_min, sr_max, color="lightgray", alpha=0.3)
    plt.legend()
    plt.title(f"Comparison between {year} temperature and {time_range_climato} quantiles at Rivesaltes station")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(
        f"figs/temp/quantiles_{time_range_climato}_{year}_year.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()
    
    
def plot_threshold(
    variable: str,
    unit: str,
    count: list,
    months_letter: str,
    threshold: str,
    periods: str,
    study_sign: str,     
):
    """
    Plots two bars representing the count of days meeting a temperature threshold
    for two different periods.

    Args:
        count (list): List containing the counts of days meeting the threshold for each period.
        months_letter (str): String representation of the months (e.g., "JJA").
        threshold (int): Temperature threshold to evaluate (°C).
        data_type (str): Type of temperature data ("maximal" or "minimal").
        periods (list): List containing two strings representing the periods (e.g., ["1997-2010", "2011-2024"]).
        study_sign (str): Sign to study, either ">" or "<".
    """
    
    plt.figure(figsize=(6, 5))
    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(periods, count, color=["lightblue", "salmon"])
    ax.set_title(f"Number of days with {variable} {study_sign} {threshold}{unit} during {months_letter}")
    ax.set_ylabel("Number of days")
    ax.grid(axis="y", alpha=0.3)

    # Annotate bars with their values
    ymax = max(count) if len(count) else 0
    for bar, val in zip(bars, count):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height / 2,
            f"{int(val)}",
            ha="center",
            va="bottom",
            fontsize=10,
            color="black"
        )
    plt.tight_layout()
    plt.show()
    
    
def plot_rr_nrm(
    sr_climato: pd.Series,
    frst_year: str,
    last_year: str,
    freq,
    method
):
    
    total = sr_climato.sum().round(2)
    total_txt = f"Total year: {total:.2f} mm"
    
    if freq == "D":
        fig, ax = plt.subplots(figsize=(10, 5)) 
        ax.plot(
            sr_climato.index,
            sr_climato,
            label="Normal",
            color="blue"
            ) 
        ax.set_title(f"Normal ({method}) precipitations (mm) in Rivesaltes computed from {frst_year} to {last_year}") 
        ax.set_xlabel("Date") 
        ax.set_ylabel("Precipitation (mm)")
        
        ax.text(
            0.45, 0.90,
            total_txt,
            transform=ax.transAxes,
            va="bottom",
            ha="left",
            fontsize=10,
            bbox=dict(facecolor="white", alpha=1, edgecolor="black")  
        )
            
        plt.grid(True) 
        plt.legend() 
        plt.tight_layout() 
    
        plt.savefig(
            f"figs/precip/norm_rr1_{frst_year}_{last_year}_daily.png",
            dpi=300,
            bbox_inches="tight"
        )
        
    elif freq == "M":
        sr_climato.index.name = "month"   # index = 1..12

        months_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        x = np.arange(1, 13)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(
            x,
            sr_climato.values,
            width=0.6,
            color="steelblue",
            edgecolor="black",
            linewidth=1.0
        )
        ax.set_xticks(x, months_labels, rotation=45)
        ax.set_title(f"Normal ({method}) precipitations (mm) in Rivesaltes computed from {frst_year} to {last_year}")
        ax.set_xlabel("Month")
        ax.set_ylabel("Precipitation (mm)")
        ax.set_ylim(0, 35)
        
        ax.text(
            0.45, 0.90,
            total_txt,
            transform=ax.transAxes,
            va="bottom",
            ha="left",
            fontsize=10,
            bbox=dict(facecolor="white", alpha=1, edgecolor="black")  
        )
        
        plt.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"figs/precip/norm_rr1_{frst_year}_{last_year}_monthly.png", dpi=300, bbox_inches="tight")
        plt.show()