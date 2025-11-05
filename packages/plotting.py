import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(
    sr: pd.Series,
    var_name: str,
    var_call: str,
    img_title: str,  
    yaxe_precistion: bool = False,
    ):

    plt.figure(figsize=(10, 5)) 
    plt.plot(
        sr.index,
        sr,
        label=var_name,
        color="blue"
        ) 
    plt.title(f"{var_call} at Rivesaltes station") 
    plt.xlabel("Date") 
    if "temperature" in var_call:
        plt.ylabel("Temperature (°C)") 
    elif "precipitation" in var_call:
        plt.ylabel("Precipitation (mm)")
        plt.ylim(0,35)
       
    
    if yaxe_precistion:
        plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(0.5))
        
    plt.grid(True) 
    plt.legend() 
    plt.tight_layout() 
    
    if "temperature" in var_call:
        plt.savefig(
            f"figs/temp/{img_title}.png",
            dpi=300,
            bbox_inches="tight"
        )
    elif "precipitation" in var_call:
        plt.savefig(
            f"figs/precip/{img_title}.png",
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