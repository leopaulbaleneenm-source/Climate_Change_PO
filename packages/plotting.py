import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap


def plot_data(
    sr: pd.Series,
    var_name: str,
    graph_title: str,
    path: str, 
    station: bool = True,
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

    if station == True:
        plt.title(f"{graph_title} at Rivesaltes station") 
    if station == False:
        plt.title(f"{graph_title} over Perpignan")

    plt.xlabel("Date") 
    if var_name == "Normal":
        plt.xticks(np.arange(0, 366, 30))
    
    var_call_lower = graph_title.lower()
    if "temperature" in var_call_lower:
        plt.ylabel("Temperature (°C)") 
        plt.yticks(np.arange(5, 27, 2.5))
    elif "precipitation" in var_call_lower:
        plt.ylabel("Precipitation (mm)")
    elif "humidity" in var_call_lower:
        plt.ylabel("Relative Humidity (%)")
       
    if yaxe_precision:
        plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(0.5))
        
    plt.grid(True) 
    plt.legend() 
    plt.tight_layout() 
    
    plt.savefig(
            f"figs/{path}.png",
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
        f"figs/temp/clim_vs_year/quantiles_{time_range_climato}_{year}_year.png",
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
    
    
def plot_threshold_serie(
    variable: str,
    unit: str,
    dic_count: dict,
    months_letter: str,
    threshold: str,
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
    
    periods = list(dic_count.keys())
    counts = list(dic_count.values())
    
    colors = ["#c7f7b3", "#ADD8E6", "#ffb3a7"]
    
    # --- Plot ---
    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(periods, counts, color=colors)

    ax.set_title(
        f"Number of days with {variable} {study_sign} {threshold}{unit} during {months_letter}",
        fontsize=12
    )
    ax.set_ylabel("Number of days")

    # Grid only horizontally
    ax.grid(axis="y", alpha=0.3)

    # --- Annotate bars ---
    for bar, val in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() / 2,
            f"{int(val)}",
            ha="center",
            va="center",
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


def plot_clim_ma_compa(
    dic_nrms : dict, 
    first_year,
    last_year,
    station : str = True
):
    
    plt.figure(figsize=(10, 5)) 
    
    for key, serie in dic_nrms.items():
        plt.plot(
            serie.index,
            serie.values,
            label=f"MA {key} jours"
        ) 
        
    plt.title(f"Comparison between different MA length to compute normal from {first_year} to {last_year}")

    plt.xlabel("Days") 
    plt.xticks(np.arange(0, 366, 30))
    
    plt.ylabel("Température (°C)") 
    
    plt.grid(True) 
    plt.legend(title="Number of days")
    plt.tight_layout() 
    
    img_title = f"compa_ma_lenght_{first_year}_{last_year}"
    
    if station == True:
        path = f"figs/temp/station/{img_title}.png"
    else:
        path = f"figs/temp/reanalysis/{img_title}.png"
    
    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight"
    )
    
    plt.show()


def plot_quantiles(
    dic_quantiles: dict,
    title : str,
    ylabel : str,
    img_path : str,
    all : bool = True 
):
    
    plt.figure(figsize=(12, 6))
    
    if all == True :
        plt.plot(dic_quantiles["Q10"].index, dic_quantiles["Q10"], label="Q10", linestyle="--", color="lightgreen")
        plt.plot(dic_quantiles["Q25"].index, dic_quantiles["Q25"], label="Q25", linestyle="--", color="green")
        plt.plot(dic_quantiles["Q75"].index, dic_quantiles["Q75"], label="Q75", linestyle="--", color="orange")
        plt.plot(dic_quantiles["Q90"].index, dic_quantiles["Q90"], label="Q90", linestyle="--", color="red")
    
    plt.plot(dic_quantiles["Q50"].index, dic_quantiles["Q50"], label="Median", color="blue")
    plt.plot(dic_quantiles["Max"].index, dic_quantiles["Max"], label="Max", color="black")
    plt.plot(dic_quantiles["Min"].index, dic_quantiles["Min"], label="Min", color="black")
    plt.fill_between(dic_quantiles["Min"].index, dic_quantiles["Min"], dic_quantiles["Max"], color="lightgray", alpha=0.3)
    
    plt.legend()
    plt.title(f"{title}")
    plt.xlabel("Date")
    plt.xticks(np.arange(0, 366, 30))
    plt.ylabel(f"{ylabel}")
    if type == "max":
        plt.yticks(np.arange(-5, 46, 5))
    if type == "min":
        plt.yticks(np.arange(-15, 31, 5))
    plt.grid(True)
    plt.tight_layout()
    
    plt.savefig(
        f"figs/{img_path}.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()
    
    
def plot_quantiles_max(
    sr_q50,
    sr_max,
    sr_min,
    title
):
    """
    Similar function to plot_quantiles (cf.computing package quantiles_max)

    Args:
        sr_q50 (pd.Series): _description_
        sr_max (pd.Series): _description_
        sr_min (pd.Series): _description_
        title (str): _description_
    """

    plt.figure(figsize=(12, 6))
    plt.plot(sr_q50.index, sr_q50, label="Median", color="blue")
    plt.plot(sr_max.index, sr_max, label="Max", color="black")
    plt.plot(sr_min.index, sr_min, label="Min", color="black")
    plt.fill_between(sr_min.index, sr_min, sr_max, color="lightgray", alpha=0.3, label="Min-Max")
    plt.legend()
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Max daily température (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.ylim(0, 45)
    plt.show()
    

def season_box_plot(
    dic_sr,
    months,
    y_label,
    title,
    folder 
):
    month_labels_map = {
        (12,1,2): ["Dec","Jan","Feb"],
        (3,4,5): ["Mar","Apr","May"],
        (6,7,8): ["Jun","Jul","Aug"],
        (9,10,11): ["Sep","Oct","Nov"]
    }
    
    labels = month_labels_map[months]
    save = "".join(labels).lower()

    n_months = len(months)
    n_series = len(dic_sr)
    
    plt.figure(figsize=(10, 6))
    
    base_positions = np.arange(1, n_months+1)
    
    # --- décalage horizontal pour chaque série ---
    width = 0.15
    total_width = width * n_series
    offsets = np.linspace(-total_width/2, total_width/2, n_series)
    
    # --- Colormap personnalisé vert → bleu → rouge ---
    custom_cmap = LinearSegmentedColormap.from_list(
        "green_blue_red", ["green", "blue", "red"]
    )
    
    legend_handles = []

    # --- Boxplots ---
    for i, (period, groups) in enumerate(dic_sr.items()):
        positions = base_positions + offsets[i]

        # Normaliser l’indice i pour obtenir une couleur entre 0 et 1
        color_value = i / (n_series - 1) if n_series > 1 else 0.5
        box_color = custom_cmap(color_value, 0.4)
        median_color = custom_cmap(color_value, 1.0)

        plt.boxplot(
            groups,
            positions=positions,
            widths=width,
            patch_artist=True,
            boxprops=dict(facecolor=box_color),
            medianprops=dict(color=median_color)
        )

        legend_handles.append(Patch(facecolor=box_color, label=period))

    plt.xticks(base_positions, labels)
    plt.xlabel("Month")
    plt.ylabel(y_label)
    plt.title(title)

    plt.legend(handles=legend_handles, loc="upper right")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(f"figs/{folder}/{save}_boxplot.png", dpi=300, bbox_inches="tight")
    plt.show()