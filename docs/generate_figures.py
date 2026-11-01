"""Reproduire les figures du README avec le CSV et l'OLS du projet.

Exécution depuis la racine : python docs/generate_figures.py
Les valeurs affichées sont calculées, jamais saisies à la main.
"""
from pathlib import Path
import hashlib
import json
import platform
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from linearmodel.ordinary_least_squares import OrdinaryLeastSquares

DATA = ROOT / "eCO2mix_RTE_Annuel-Definitif_2020.csv"
ASSETS = ROOT / "docs" / "assets"
FEATURES = ["Fioul", "Charbon", "Gaz", "Nucléaire", "Eolien", "Solaire", "Hydraulique", "Pompage", "Bioénergies"]
PRODUCTION = [f for f in FEATURES if f != "Pompage"]
NAVY, TEAL, ORANGE, GREY = "#182B49", "#0B8A8F", "#D27A36", "#667085"
CMAP = LinearSegmentedColormap.from_list("density", ["#DBEEEE", TEAL, NAVY])
FR_MONTHS = {1:"janv.", 2:"févr.", 3:"mars", 4:"avr.", 5:"mai", 6:"juin", 7:"juil.", 8:"août", 9:"sept.", 10:"oct.", 11:"nov.", 12:"déc."}

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "text.color": NAVY, "axes.labelcolor": GREY, "axes.edgecolor": "#D0D5DD",
    "xtick.color": GREY, "ytick.color": GREY,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 13,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "svg.fonttype": "none", "svg.hashsalt": "linearmodel-readme", "savefig.facecolor": "white",
})

def fmt(x, digits=1):
    return f"{x:,.{digits}f}".replace(",", " ").replace(".", ",")

def figure(title, subtitle, metrics):
    fig = plt.figure(figsize=(15, 8.1))
    fig.text(.06, .94, title, fontsize=23, fontweight="bold", va="top")
    fig.text(.06, .887, subtitle, fontsize=10.7, color=GREY, va="top")
    for x, (value, label) in zip([.06, .38, .7], metrics):
        fig.text(x, .808, value, fontsize=26, fontweight="bold", color=TEAL)
        fig.text(x, .774, label, fontsize=9.4, color=GREY)
    return fig

def save(fig, name):
    fig.savefig(ASSETS / f"{name}.png", dpi=180)
    fig.savefig(ASSETS / f"{name}.svg", metadata={"Date": None})
    plt.close(fig)

def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(DATA, sep=";")
    raw["horodatage"] = pd.to_datetime(raw["Date"] + " " + raw["Heures"], errors="coerce")
    for col in ["Consommation", *FEATURES]:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    clean = raw.dropna(subset=["horodatage", "Consommation", *FEATURES]).sort_values("horodatage").copy()
    assert len(clean) > len(FEATURES) + 1
    delta = clean["horodatage"].diff().dropna().dt.total_seconds()
    assert (delta == 1800).all(), "Le pas attendu de 30 minutes a changé ; vérifier les agrégations."
    daily = clean.set_index("horodatage")["Consommation"].resample("D").agg(["mean", "min", "max"])/1000
    means = clean[PRODUCTION].mean().sort_values()/1000
    demand_mean = float(clean["Consommation"].mean()/1000)
    demand_max = float(clean["Consommation"].max()/1000)
    fig = figure("Électricité en France | panorama 2020", "Données RTE présentes dans l’archive · observations de puissance au pas de 30 minutes", [
        (fmt(len(clean), 0), "OBSERVATIONS COMPLÈTES"),
        (fmt(demand_mean)+" GW", "DEMANDE MOYENNE"),
        (fmt(demand_max)+" GW", "POINTE OBSERVÉE"),
    ])
    ax = fig.add_axes([.065, .19, .53, .47])
    ax.set_title("Une demande qui varie au fil de l’année", loc="left", pad=17)
    ax.fill_between(daily.index, daily["min"], daily["max"], color=TEAL, alpha=.12, linewidth=0, label="Minimum–maximum de chaque jour")
    ax.plot(daily.index, daily["mean"], color=TEAL, linewidth=1.7, label="Moyenne quotidienne")
    ax.set_ylabel("Puissance appelée (GW)"); ax.set_xlabel("Date en 2020")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: FR_MONTHS[mdates.num2date(x).month]))
    ax.set_xlim(daily.index.min(), daily.index.max())
    ax.grid(axis="y", color="#E9EDF2", linewidth=.7);ax.set_axisbelow(True)
    ax.legend(loc="upper right", fontsize=8.7, frameon=False)
    bx = fig.add_axes([.735, .19, .205, .47])
    bx.set_title("Production par filière", loc="left", pad=17)
    labels = ["Éolien" if c=="Eolien" else c for c in means.index]
    bars = bx.barh(labels, means.values, color=[TEAL if c=="Nucléaire" else "#9AAABD" for c in means.index], height=.62)
    for b, value in zip(bars, means.values):
        bx.text(value+.35, b.get_y()+b.get_height()/2, fmt(value), va="center", fontsize=9.5, color=NAVY)
    bx.set_xlim(0, means.max()*1.22);bx.set_xlabel("Puissance moyenne (GW)")
    bx.grid(axis="x", color="#E9EDF2", linewidth=.7);bx.set_axisbelow(True)
    bx.spines["left"].set_visible(False);bx.tick_params(axis="y", length=0, pad=8)
    fig.text(.06, .085, "Source : eCO2mix_RTE_Annuel-Definitif_2020.csv · 1er janvier – 31 décembre 2020.", color=GREY, fontsize=9.1)
    fig.text(.06, .059, "Filières : moyennes des puissances renseignées ; pompage et échanges physiques exclus du panneau de droite. GW = 1 000 MW.", color=GREY, fontsize=8.8)
    save(fig, "rte_panorama_2020")

    X = clean[FEATURES].to_numpy(dtype=float)
    y = clean["Consommation"].to_numpy(dtype=float)
    model = OrdinaryLeastSquares(intercept=True)
    fit_return = model.fit(X, y)
    assert fit_return is None
    fitted = model.predict(X)
    residuals = y - fitted
    r2 = float(model.determination_coefficient(X, y))
    rmse = float(np.sqrt(np.mean(residuals**2)))
    mae = float(np.mean(np.abs(residuals)))
    fig = figure("OLS | diagnostic de l’ajustement", "La classe OrdinaryLeastSquares du projet est ajustée et évaluée sur les mêmes 17 568 observations de 2020", [
        (fmt(r2, 3), "R² SUR LES DONNÉES D’AJUSTEMENT"),
        (fmt(rmse/1000, 2)+" GW", "RACINE DE L’ERREUR QUADRATIQUE MOYENNE"),
        (fmt(mae/1000, 2)+" GW", "ERREUR ABSOLUE MOYENNE"),
    ])
    ax = fig.add_axes([.065, .19, .375, .47]);bx = fig.add_axes([.585, .19, .375, .47])
    observed, predicted, errors = y/1000, fitted/1000, residuals/1000
    ax.set_title("Valeurs observées et ajustées", loc="left", pad=17)
    density = ax.hexbin(observed, predicted, gridsize=60, mincnt=1, cmap=CMAP, linewidths=0)
    lo=min(observed.min(), predicted.min());hi=max(observed.max(), predicted.max())
    ax.plot([lo, hi], [lo, hi], color=ORANGE, linestyle="--", linewidth=1.3, label="Égalité observé = ajusté")
    ax.set_xlabel("Consommation observée (GW)");ax.set_ylabel("Consommation ajustée (GW)")
    ax.legend(loc="upper left", fontsize=8.7, frameon=False)
    cb=fig.colorbar(density, ax=ax, fraction=.045, pad=.035);cb.set_label("Observations par cellule", fontsize=8.6);cb.ax.tick_params(labelsize=8.5)
    bx.set_title("Les résidus révèlent les écarts du modèle", loc="left", pad=17)
    density=bx.hexbin(predicted, errors, gridsize=60, mincnt=1, cmap=CMAP, linewidths=0)
    bx.axhline(0, color=ORANGE, linestyle="--", linewidth=1.3, label="Résidu nul")
    bx.set_xlabel("Consommation ajustée (GW)");bx.set_ylabel("Résidu observé − ajusté (GW)")
    bx.legend(loc="upper right", fontsize=8.7, frameon=False)
    cb=fig.colorbar(density, ax=bx, fraction=.045, pad=.035);cb.set_label("Observations par cellule", fontsize=8.6);cb.ax.tick_params(labelsize=8.5)
    for a in (ax,bx):
        a.grid(color="#E9EDF2", linewidth=.55);a.set_axisbelow(True)
    fig.text(.06, .085, "Modèle : constante + 9 variables de production/pompage. Source : CSV RTE fourni, du 1er janvier au 31 décembre 2020.", color=GREY, fontsize=9.1)
    fig.text(.06, .059, "Lecture : ajustement descriptif contemporain, sans test indépendant ni interprétation causale ; ces scores ne mesurent pas une capacité de prévision.", color=GREY, fontsize=8.8)
    save(fig, "ols_diagnostic_2020")
    metrics={
        "source":DATA.name,"source_sha256":hashlib.sha256(DATA.read_bytes()).hexdigest(),
        "raw_rows":len(raw),"complete_rows":len(clean),"interval_minutes":30,
        "period_start":str(clean["horodatage"].min()),"period_end":str(clean["horodatage"].max()),
        "target":"Consommation","source_power_unit":"MW","display_power_unit":"GW",
        "mean_demand_MW":demand_mean*1000,"max_demand_MW":demand_max*1000,
        "mean_production_MW":{k:float(v) for k,v in clean[PRODUCTION].mean().items()},
        "ols_features":FEATURES,"ols_intercept":True,"evaluation":"in_sample",
        "ols_r2":r2,"ols_rmse_MW":rmse,"ols_mae_MW":mae,
        "ols_coefficients":model.get_coefficients().tolist(),
        "fit_returns_none":fit_return is None,
        "versions":{"python":platform.python_version(),"numpy":np.__version__,"pandas":pd.__version__,"matplotlib":matplotlib.__version__},
        "generated_files":["docs/assets/rte_panorama_2020.png","docs/assets/rte_panorama_2020.svg","docs/assets/ols_diagnostic_2020.png","docs/assets/ols_diagnostic_2020.svg"],
    }
    (ROOT/"docs"/"figure_metrics.json").write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in metrics.items() if k in ("raw_rows","complete_rows","ols_r2","ols_rmse_MW","ols_mae_MW","versions")},ensure_ascii=True))

if __name__=="__main__":
    main()
