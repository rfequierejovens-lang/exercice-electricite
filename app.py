from pathlib import Path

import pandas as pd
import streamlit as st

DOSSIER = Path(__file__).parent / "donnees"


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DOSSIER / "consommation_propre.csv")


def format_num(value: float | int, decimals: int = 1) -> str:
    return f"{value:,.{decimals}f}" if decimals > 0 else f"{value:,.0f}"


st.set_page_config(page_title="L'électricité dans 12 quartiers", page_icon="⚡", layout="wide")

st.title("L'électricité dans 12 quartiers")
st.caption("Analyse mensuelle de 12 quartiers sur 2024-2025. Données traitées et prêtes pour le diagnostic.")

# Données propres ; on ne refait pas le nettoyage dans le dashboard.
df = load_data()
df["annee"] = df["annee"].astype(int)

communes = sorted(df["commune"].unique())
annees = sorted(df["annee"].unique())

with st.sidebar:
    st.header("Filtres")
    communes_sel = st.multiselect(
        "Communes",
        communes,
        default=communes,
        help="Sélectionnez une ou plusieurs communes à analyser.",
    )
    annee_sel = st.selectbox("Année", annees, index=len(annees) - 1)

if not communes_sel:
    st.warning("Aucune commune n'est sélectionnée. Choisissez au moins une commune pour afficher les résultats.")
    st.stop()

filtered = df[(df["commune"].isin(communes_sel)) & (df["annee"] == annee_sel)].copy()

if filtered.empty:
    st.warning("Aucune donnée pour cette sélection. Merci de modifier les filtres.")
    st.stop()

consommation_totale = filtered["kwh"].sum()
kwh_par_abonne = filtered["kwh_par_abonne"].mean()
heures_moyennes = filtered["heures_courant"].mean()

st.subheader(f"Synthèse — {annee_sel}")
metrics = st.columns(3)
metrics[0].metric("Consommation totale", f"{consommation_totale / 1_000_000:,.2f} MWh")
metrics[1].metric("kWh par abonné", f"{kwh_par_abonne:,.1f}")
metrics[2].metric("Heures de courant", f"{heures_moyennes:,.1f} h/j")

with st.expander("Données filtrées", expanded=False):
    st.dataframe(filtered, use_container_width=True, hide_index=True)

# Onglets du dashboard
quartiers_tab, evolution_tab, chaleur_tab, coupures_tab, extremes_tab = st.tabs(
    ["Quartiers", "Évolution", "Chaleur ou courant", "Coupures", "Valeurs extrêmes"]
)

with quartiers_tab:
    top_quartiers = (
        filtered.groupby("quartier", as_index=False)["kwh_par_abonne"]
        .mean()
        .sort_values("kwh_par_abonne", ascending=False)
    )
    st.bar_chart(top_quartiers.set_index("quartier")["kwh_par_abonne"], use_container_width=True)
    best = top_quartiers.iloc[0]
    st.write(
        f"Le quartier le plus consommateur est {best['quartier']} avec {best['kwh_par_abonne']:.1f} kWh par abonné, "
        f"contre {top_quartiers['kwh_par_abonne'].mean():.1f} en moyenne sur la sélection."
    )

with evolution_tab:
    evolution = (
        filtered.pivot_table(index="mois", columns="commune", values="kwh_par_abonne", aggfunc="mean")
        .sort_index()
    )
    st.line_chart(evolution, use_container_width=True)
    if len(evolution.columns) > 0:
        st.write(
            f"La consommation par abonné varie entre {evolution.min().min():.1f} et {evolution.max().max():.1f} kWh selon la commune et le mois."
        )

with chaleur_tab:
    residentiel = filtered[filtered["type"] == "Résidentiel"].copy()
    if residentiel.empty:
        st.info("Aucune donnée résidentielle dans cette sélection.")
    else:
        st.scatter_chart(
            residentiel,
            x="heures_courant",
            y="kwh_par_abonne",
            color="commune",
        )
        corr_heures = residentiel["kwh_par_abonne"].corr(residentiel["heures_courant"])
        corr_temp = residentiel["kwh_par_abonne"].corr(residentiel["temperature_c"])
        st.write(
            f"Corrélation avec les heures de courant : {corr_heures:.2f}. "
            f"Corrélation avec la température : {corr_temp:.2f}."
        )

with coupures_tab:
    desc = (
        filtered.groupby("commune")["heures_courant"]
        .describe()[["25%", "50%", "75%"]]
        .rename(columns={"50%": "médiane", "25%": "Q1", "75%": "Q3"})
    )
    st.dataframe(desc, use_container_width=True)
    st.bar_chart(filtered.groupby("commune")["heures_courant"].mean())
    plus_court = filtered.loc[filtered["heures_courant"].idxmin()]
    st.write(
        f"La commune la plus impactée est {plus_court['commune']} avec {plus_court['heures_courant']:.1f} h/j, "
        f"soit la moyenne la plus faible parmi les données sélectionnées."
    )

with extremes_tab:
    top3 = filtered.nlargest(3, "kwh")[["mois", "quartier", "commune", "type", "kwh"]]
    st.dataframe(top3, use_container_width=True, hide_index=True)
    top1 = top3.iloc[0]
    st.write(
        f"Le pic de consommation est {top1['quartier']} en {top1['mois']} avec {top1['kwh']:,.0f} kWh, "
        f"dans la commune {top1['commune']}."
    )

st.markdown("### Conclusion")
residential = filtered[filtered["type"] == "Résidentiel"].copy()
if not residential.empty:
    corr_heures = residential["kwh_par_abonne"].corr(residential["heures_courant"])
    corr_temp = residential["kwh_par_abonne"].corr(residential["temperature_c"])
    st.markdown(
        f"La consommation suit les heures de courant, pas la chaleur : dans les quartiers résidentiels, la corrélation vaut {corr_heures:.2f} avec les heures de courant, contre {corr_temp:.2f} avec la température. "
        "Ainsi, les abonnés consomment davantage quand ils reçoivent plus d'électricité, pas quand il fait plus chaud. "
        "Une corrélation ne prouve pas la cause : elle indique une association, pas un lien unique ou direct entre les variables."
    )
else:
    st.markdown(
        "La consommation suit principalement les heures de courant dans les quartiers résidentiels, mais cette sélection ne contient pas de données résidentielle."
    )
