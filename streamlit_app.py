# ============================================================
#   Prévision des passages aux urgences — Hôpital Mohamed V, Meknès
#   Auteurs : Issoug El Mehdi & Bado Ange Yipene Cenacle
#   Modèles : Prophet (mensuel) · MLP (journalier)
# ============================================================

from __future__ import annotations

import hashlib
import json
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from urgences import graphiques as G
from urgences.donnees import FICHIER_JOURNALIER, FICHIER_MENSUEL, charger_exemple, lire_excel
from urgences.prevision import prevoir_journalier, prevoir_mensuel
from urgences.style import CSS, kpi, nombre

RACINE = Path(__file__).resolve().parent
METRIQUES = RACINE / "results" / "metriques.json"
CFG_PLOT = {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"]}

st.set_page_config(page_title="Urgences — Prévision des passages", page_icon="🏥", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Cache
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def metriques_projet() -> dict | None:
    return json.loads(METRIQUES.read_text(encoding="utf-8")) if METRIQUES.exists() else None


@st.cache_data(show_spinner=False)
def exemple(granularite: str) -> pd.DataFrame:
    return charger_exemple(granularite)


@st.cache_data(show_spinner=False)
def lire_upload(contenu: bytes, granularite: str):
    return lire_excel(BytesIO(contenu), granularite)


@st.cache_data(show_spinner=False, max_entries=20)
def calculer_prevision(df: pd.DataFrame, n: int, mensuel: bool):
    return prevoir_mensuel(df, n) if mensuel else prevoir_journalier(df, n)


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="sb-titre">🏥 Hôpital Mohamed V</div><div class="sb-sous">Service des urgences — Meknès</div>',
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown(
        """<div class="sb-bloc">
        <b>Objectif</b><br>Anticiper l'affluence aux urgences pour planifier le personnel et les ressources.<br><br>
        <b>Modèles</b><br>• Prophet — prévision mensuelle<br>• MLP — prévision journalière<br><br>
        <b>Évaluation</b><br>Erreurs mesurées hors-échantillon (backtest à origine glissante) et comparées
        à des modèles naïfs de référence.<br><br>
        <b>Fichier Excel attendu</b><br>Colonne A : date (<code>2024-01-01</code>, <code>01/01/2024</code>,
        <code>Janvier 2024</code>)<br>Colonne B : nombre de passages
        </div>""",
        unsafe_allow_html=True,
    )
    st.divider()
    st.caption("Issoug El Mehdi & Bado Ange Yipene Cenacle · Projet Séries Temporelles 2024–2025")


# ══════════════════════════════════════════════
#  PAGE 1 — INTRODUCTION
# ══════════════════════════════════════════════
def page_introduction() -> None:
    m = metriques_projet()
    st.markdown(
        """<div class="hero"><div class="eyebrow">Outil d'aide à la décision</div>
        <h1>Prévision des passages aux urgences</h1>
        <p>Hôpital Mohamed V — Meknès · séries temporelles, apprentissage automatique</p></div>""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown(
            """<div class="carte"><h4>🎯 Objectif</h4><p>
            Prévoir le nombre de passages aux urgences, <b>par mois</b> et <b>par jour</b>, afin d'anticiper
            les pics d'affluence, ajuster les plannings du personnel et dimensionner les ressources.</p></div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """<div class="carte"><h4>📊 Données</h4><p>
            <span class="tag">réel</span> Totaux <b>mensuels</b> de passages, janvier 2024 → mai 2025 (17 mois).<br>
            <span class="tag sim">simulé</span> Série <b>journalière</b> obtenue en répartissant aléatoirement chaque
            total mensuel sur ses jours (la somme par mois est conservée).</p></div>""",
            unsafe_allow_html=True,
        )

    if m is None:
        st.warning("Fichier results/metriques.json absent : lancez `python scripts/evaluer_modeles.py`.")
        return

    dm, dj = m["donnees"]["mensuel"], m["donnees"]["journalier"]
    bj = m["backtest_journalier"]
    mlp = next(r for r in bj if r["modele"] == "MLP")
    naif_s = next(r for r in bj if r["modele"].startswith("Naïf saisonnier"))
    gain = (1 - mlp["MAE"] / naif_s["MAE"]) * 100

    st.write("")
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi("Historique mensuel", f"{dm['n']} mois", f"moyenne {nombre(dm['moyenne'])} passages / mois"), unsafe_allow_html=True)
    k2.markdown(kpi("Historique journalier (simulé)", f"{dj['n']} jours", f"moyenne {nombre(dj['moyenne'])} passages / jour"), unsafe_allow_html=True)
    k3.markdown(kpi("Erreur MLP journalière", f"± {nombre(mlp['MAE'], 1)}", f"MAE hors-échantillon · MAPE {nombre(mlp['MAPE'], 1)} %"), unsafe_allow_html=True)
    k4.markdown(kpi("Gain vs modèle naïf", f"−{nombre(gain)} %", "d'erreur par rapport au « même jour J-7 »"), unsafe_allow_html=True)

    st.subheader("Série mensuelle observée")
    st.plotly_chart(G.figure_historique(exemple("mensuel"), mensuel=True, hauteur=300),
                    use_container_width=True, config=CFG_PLOT)

    st.subheader("Démarche")
    etapes = [
        ("Données", "Nettoyage des totaux mensuels ; simulation journalière documentée (scripts/simuler_journalier.py)."),
        ("Analyse statistique", "Tests ADF et KPSS, autocorrélations, choix de la différenciation."),
        ("Modélisation", "Baselines naïves, SARIMA, Prophet, Ridge, Gradient Boosting, MLP avec lags et encodage cyclique."),
        ("Évaluation", "Backtest à origine glissante : chaque modèle prévoit des périodes qu'il n'a jamais vues."),
    ]
    for col, (i, (t, d)) in zip(st.columns(4, gap="small"), enumerate(etapes, 1)):
        col.markdown(f'<div class="etape"><span class="num">{i}</span><div class="t">{t}</div><div class="d">{d}</div></div>',
                     unsafe_allow_html=True)

    # ── Comparaison des modèles ──
    st.subheader("Comparaison des modèles — prévision journalière")
    pj = m["protocole"]["journalier"]
    st.caption(f"Backtest : {pj['plis']} fenêtres successives de {pj['horizon']} jours "
               f"(les {pj['plis'] * pj['horizon']} derniers jours), prévision récursive à 1–{pj['horizon']} jours. "
               "Gris = modèles naïfs de référence.")
    plancher = m.get("plancher_journalier", {}).get("MAE")
    g1, g2 = st.columns([3, 2], gap="large")
    with g1:
        st.plotly_chart(G.figure_comparaison(bj, plancher, "MLP"), use_container_width=True, config=CFG_PLOT)
    with g2:
        tab = pd.DataFrame(bj)
        tab["modele"] = tab["modele"] + tab["baseline"].map({True: " (réf.)", False: ""})
        tab = tab[["modele", "MAE", "RMSE", "MAPE"]]
        st.dataframe(
            tab.rename(columns={"modele": "Modèle", "MAPE": "MAPE (%)"}), hide_index=True, use_container_width=True,
            column_config={c: st.column_config.NumberColumn(format="%.1f") for c in ["MAE", "RMSE", "MAPE (%)"]},
        )
    st.markdown(
        f"""<div class="note"><b>Lecture.</b> Le MLP, la régression Ridge et SARIMA obtiennent des erreurs très proches
        (MAE ≈ {nombre(mlp['MAE'], 1)} passages/jour) et réduisent l'erreur d'environ {nombre(gain)} % par rapport au modèle naïf.
        Le <b>plancher théorique</b> ({nombre(plancher, 1)}) est l'erreur d'un oracle qui connaîtrait la valeur moyenne exacte de
        chaque jour : l'écart restant est du bruit aléatoire introduit par la simulation, qu'aucun modèle ne peut prévoir.
        Les différences entre les meilleurs modèles sont donc faibles ; le MLP est conservé pour l'application.</div>""",
        unsafe_allow_html=True,
    )

    st.subheader("Comparaison des modèles — prévision mensuelle")
    bm = pd.DataFrame(m["backtest_mensuel"])
    pm = m["protocole"]["mensuel"]
    c1, c2 = st.columns([2, 3], gap="large")
    with c1:
        bm["Type"] = bm.pop("baseline").map({True: "référence", False: "modèle"})
        st.dataframe(
            bm[["modele", "MAE", "MAPE", "Type"]].rename(columns={"modele": "Modèle", "MAPE": "MAPE (%)"}),
            hide_index=True, use_container_width=True,
            column_config={"MAE": st.column_config.NumberColumn(format="%.0f"),
                           "MAPE (%)": st.column_config.NumberColumn(format="%.1f")},
        )
    with c2:
        st.markdown(
            f"""<div class="note alerte"><b>Avec {dm['n']} mois seulement</b>, l'évaluation porte sur
            {pm['plis']} prévisions à 1 mois : Prophet et la moyenne mobile sur 3 mois sont équivalents (≈ 3 % d'erreur).
            La saisonnalité annuelle de Prophet est désactivée tant que l'historique compte moins de 24 mois
            (elle ne peut pas être estimée sur moins de deux cycles). Prophet reste utile pour ses intervalles
            d'incertitude et deviendra plus pertinent avec un historique plus long.</div>""",
            unsafe_allow_html=True,
        )

    # ── Stationnarité ──
    st.subheader("Tests de stationnarité")
    df_st = pd.DataFrame(m["stationnarite"])
    df_st["Conclusion"] = df_st["stationnaire"].map({True: "✅ stationnaire", False: "❌ non stationnaire"})
    st.dataframe(
        df_st.rename(columns={"serie": "Série", "transformation": "Transformation", "n": "n",
                              "adf_stat": "ADF stat", "adf_p": "ADF p", "kpss_stat": "KPSS stat", "kpss_p": "KPSS p"})
        [["Série", "Transformation", "n", "ADF stat", "ADF p", "KPSS stat", "KPSS p", "Conclusion"]],
        hide_index=True, use_container_width=True,
        column_config={"ADF p": st.column_config.NumberColumn(format="%.4f"),
                       "KPSS p": st.column_config.NumberColumn(format="%.2f")},
    )
    acf = m["acf_journalier"]
    st.markdown(
        f"""<div class="note">ADF : H₀ = racine unitaire (p &lt; 0,05 → stationnaire). KPSS : H₀ = stationnaire
        (p &gt; 0,05 → stationnaire). Les p-values KPSS sont bornées à [0,01 ; 0,10] par la table de statsmodels.<br>
        La série journalière est non stationnaire en niveau (elle suit les variations des totaux mensuels) et le devient
        après une différenciation d'ordre 1. L'autocorrélation au lag 7 ({nombre(acf['7'], 2)}) est plus forte qu'au lag 1
        ({nombre(acf['1'], 2)}) : c'est l'effet « jour de la semaine » <b>introduit par l'hypothèse de simulation</b>,
        pas une observation sur données réelles.</div>""",
        unsafe_allow_html=True,
    )

    with st.expander("Limites et perspectives"):
        st.markdown(
            """
- **Données journalières simulées** : les performances journalières mesurent la capacité des modèles à retrouver
  la structure de la simulation. Elles devront être revalidées sur de vraies données journalières.
- **Historique mensuel court** (17 mois) : peu de points de test, saisonnalité annuelle non estimable.
- **Pas de variables explicatives** (météo, jours fériés, épidémies saisonnières, Ramadan…) : piste d'amélioration naturelle.
- L'exploration initiale incluait aussi XGBoost, LightGBM, LSTM et GRU ; ces résultats n'ont pas été conservés
  et ne sont donc pas présentés ici. Toutes les valeurs affichées sont recalculées par `scripts/evaluer_modeles.py`.
"""
        )
    st.caption(f"Métriques générées le {m['genere_le']} par scripts/evaluer_modeles.py")


# ══════════════════════════════════════════════
#  PAGE 2 — PRÉDICTION
# ══════════════════════════════════════════════
def page_prediction() -> None:
    st.markdown(
        """<div class="hero"><div class="eyebrow">Prévision interactive</div>
        <h1>Générer des prévisions</h1>
        <p>Utilisez les données du projet ou chargez votre propre fichier Excel.</p></div>""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        mode = st.segmented_control("Type de prévision", ["Mensuelle", "Journalière"], default="Mensuelle",
                                    key="mode")
    with c2:
        source = st.segmented_control("Source des données", ["Données du projet", "Mon fichier Excel"],
                                      default="Données du projet", key="source")
    mensuel = (mode or "Mensuelle") == "Mensuelle"
    gran = "mensuel" if mensuel else "journalier"
    unite, unite_s = ("mois", "mois") if mensuel else ("jours", "jour")

    # ── 1. Données ──
    st.subheader("1 · Données")
    df, avert = None, []
    if (source or "Données du projet") == "Données du projet":
        df = exemple(gran)
        if not mensuel:
            st.markdown('<div class="note alerte">Série journalière <b>simulée</b> à partir des totaux mensuels réels '
                        '(voir page Introduction).</div>', unsafe_allow_html=True)
    else:
        fichier_ex = FICHIER_MENSUEL if mensuel else FICHIER_JOURNALIER
        cc1, cc2 = st.columns([3, 1], vertical_alignment="bottom")
        with cc1:
            up = st.file_uploader(f"Fichier Excel — données {'mensuelles' if mensuel else 'journalières'} "
                                  "(colonne A : date, colonne B : passages)", type=["xlsx", "xls"])
        with cc2:
            st.download_button("Télécharger un exemple", fichier_ex.read_bytes(), file_name=fichier_ex.name,
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
        if up is None:
            st.info("En attente d'un fichier. Téléchargez l'exemple pour voir le format attendu.")
            return
        df, err, avert = lire_upload(up.getvalue(), gran)
        if err:
            st.error(err)
            return

    for a in avert:
        st.warning(a)

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi("Période", f"{len(df)} {unite}",
                    f"{df['ds'].min():%d/%m/%Y} → {df['ds'].max():%d/%m/%Y}"), unsafe_allow_html=True)
    k2.markdown(kpi(f"Moyenne / {unite_s}", nombre(df['y'].mean())), unsafe_allow_html=True)
    k3.markdown(kpi("Minimum", nombre(df['y'].min()), f"{df.loc[df['y'].idxmin(), 'ds']:%d/%m/%Y}"), unsafe_allow_html=True)
    k4.markdown(kpi("Maximum", nombre(df['y'].max()), f"{df.loc[df['y'].idxmax(), 'ds']:%d/%m/%Y}"), unsafe_allow_html=True)
    st.plotly_chart(G.figure_historique(df, mensuel, hauteur=280), use_container_width=True, config=CFG_PLOT)

    # ── 2. Horizon ──
    st.subheader("2 · Horizon de prévision")
    n = st.slider(f"Nombre de {unite} à prévoir", 1, 12 if mensuel else 60, 6 if mensuel else 14)
    debut = df["ds"].max() + (pd.DateOffset(months=1) if mensuel else pd.Timedelta(days=1))
    fin = df["ds"].max() + (pd.DateOffset(months=n) if mensuel else pd.Timedelta(days=n))
    st.caption(f"Prévisions du {debut:%d/%m/%Y} au {fin:%d/%m/%Y}.")

    # ── 3. Résultats ──
    cle = (gran, n, hashlib.md5(pd.util.hash_pandas_object(df).values.tobytes()).hexdigest())
    if st.button("Générer les prévisions", type="primary", icon="🔮"):
        with st.spinner("Évaluation hors-échantillon puis entraînement du modèle…"):
            try:
                st.session_state["resultat"] = (cle, calculer_prevision(df, n, mensuel))
            except Exception as e:
                st.session_state.pop("resultat", None)
                st.error(f"Erreur lors de la prévision : {e}")
                return

    # Les résultats restent affichés après un clic sur « Télécharger » (Streamlit relance le script).
    res = st.session_state.get("resultat")
    if res is None or res[0] != cle:
        return
    p = res[1]
    fc = p.previsions

    st.subheader("3 · Résultats")
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi(f"Total prévu ({n} {unite})", nombre(fc['yhat'].sum()), f"moyenne {nombre(fc['yhat'].mean())} / {unite_s}"),
                unsafe_allow_html=True)
    pic = fc.loc[fc["yhat"].idxmax()]
    k2.markdown(kpi("Pic prévu", nombre(pic['yhat']),
                    G.mois_fr(pic['ds']) if mensuel else G.jour_fr(pic['ds'])), unsafe_allow_html=True)
    if p.scores:
        gain = (1 - p.scores["MAE"] / p.scores_baseline["MAE"]) * 100
        k3.markdown(kpi("Erreur attendue (MAE)", f"± {nombre(p.scores['MAE'])}",
                        f"MAPE {nombre(p.scores['MAPE'], 1)} % · hors-échantillon"), unsafe_allow_html=True)
        k4.markdown(kpi(f"vs {p.nom_baseline}", f"{'−' if gain >= 0 else '+'}{nombre(abs(gain))} %",
                        f"d'erreur (MAE réf. {nombre(p.scores_baseline['MAE'])})"), unsafe_allow_html=True)
    else:
        k3.markdown(kpi("Erreur attendue", "n.d.", "historique trop court"), unsafe_allow_html=True)

    st.plotly_chart(G.figure_prevision(df, fc, mensuel), use_container_width=True, config=CFG_PLOT)
    st.caption(f"**Modèle :** {p.modele}. **Évaluation :** {p.protocole}. "
               "La zone orange est l'intervalle de prévision à 95 % ; elle s'élargit avec l'horizon.")

    tab = fc.copy()
    tab["Date"] = tab["ds"].map(G.mois_fr) if mensuel else tab["ds"].map(G.jour_fr)
    tab = tab.rename(columns={"yhat": "Prévision", "yhat_lower": "Borne basse 95 %", "yhat_upper": "Borne haute 95 %"})
    cols = ["Date", "Prévision", "Borne basse 95 %", "Borne haute 95 %"]
    tab[cols[1:]] = tab[cols[1:]].round().astype(int)
    st.dataframe(tab[cols], hide_index=True, use_container_width=True, height=min(400, 38 + 35 * len(tab)))

    out = BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        tab[cols].to_excel(w, index=False, sheet_name="Prévisions")
        df.assign(ds=df["ds"].dt.date).rename(columns={"ds": "Date", "y": "Passages"}).to_excel(
            w, index=False, sheet_name="Historique")
        ev = {"Modèle": p.modele, "Protocole d'évaluation": p.protocole}
        if p.scores:
            ev |= {f"{k} modèle": round(v, 2) for k, v in p.scores.items()}
            ev |= {f"{k} {p.nom_baseline}": round(v, 2) for k, v in p.scores_baseline.items()}
        pd.DataFrame(list(ev.items()), columns=["Élément", "Valeur"]).to_excel(w, index=False, sheet_name="Évaluation")
    st.download_button("Télécharger les prévisions (Excel)", out.getvalue(), icon="📥",
                       file_name=f"previsions_urgences_{gran}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ─────────────────────────────────────────────
#  Navigation
# ─────────────────────────────────────────────
nav = st.navigation(
    [st.Page(page_introduction, title="Introduction", icon="📖", default=True),
     st.Page(page_prediction, title="Prédiction", icon="🔮", url_path="prediction")],
    position="top",
)
nav.run()

st.markdown(
    '<div class="pied">Hôpital Mohamed V — Meknès · Issoug El Mehdi & Bado Ange Yipene Cenacle · '
    'Projet académique — les prévisions sont indicatives et ne remplacent pas le jugement des équipes.</div>',
    unsafe_allow_html=True,
)
