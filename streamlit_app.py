# ============================================================
#   🏥 Prévision des Passages aux Urgences — Hôpital Mohamed V
#   Auteur : Issoug El Mehdi & Bado Ange Yipene Cenacle 
#   Modèles : Prophet (mensuel) | MLP (journalier)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="🏥 Urgences — Prévision Passages",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #f0f4f8; }
    [data-testid="stSidebar"] { background-color: #1e3a5f !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    [data-testid="stSidebar"] .sidebar-content { background-color: #1e3a5f !important; }
    [data-testid="stSidebarNav"] { background-color: #1e3a5f !important; }
    .main-title {
        background: linear-gradient(135deg, #1e3a5f 0%, #2980b9 100%);
        color: white; padding: 30px 40px; border-radius: 16px;
        text-align: center; margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(41,128,185,0.35);
    }
    .main-title h1 { font-size: 2.4rem; margin: 0; font-weight: 800; }
    .main-title p  { font-size: 1.05rem; margin: 8px 0 0 0; opacity: 0.9; }
    .metric-card {
        background: white; border-radius: 12px; padding: 20px 24px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #2980b9; margin-bottom: 12px;
    }
    .metric-card h3 { color: #2980b9; font-size: 1rem; margin: 0 0 4px 0; }
    .metric-card h2 { color: #1e3a5f; font-size: 2rem; margin: 0; font-weight: 700; }
    .metric-card small { color: #7f8c8d; font-size: 0.82rem; }
    .info-box {
        background: #eaf4fb; border: 1.5px solid #2980b9;
        border-radius: 10px; padding: 16px 20px; margin: 14px 0;
        color: #1e3a5f; font-size: 0.95rem;
    }
    .warning-box {
        background: #fef9e7; border: 1.5px solid #f39c12;
        border-radius: 10px; padding: 14px 18px; margin: 10px 0;
        color: #7d6608; font-size: 0.92rem;
    }
    .success-box {
        background: #eafaf1; border: 1.5px solid #27ae60;
        border-radius: 10px; padding: 14px 18px; margin: 10px 0;
        color: #1e8449; font-size: 0.92rem;
    }
    .section-header {
        background: white; border-radius: 10px; padding: 14px 22px;
        margin: 20px 0 14px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-top: 4px solid #2980b9; font-size: 1.15rem;
        font-weight: 700; color: #1e3a5f;
    }
    .result-highlight {
        background: linear-gradient(135deg,#1e3a5f,#2980b9);
        color:white; border-radius:14px; padding:28px 34px;
        text-align:center; margin:18px 0;
        box-shadow:0 6px 20px rgba(41,128,185,0.3);
    }
    .result-highlight .big-num { font-size:3.5rem; font-weight:900; }
    .result-highlight .interval { font-size:1.1rem; opacity:0.88; margin-top:6px; }
    .sidebar-block {
        background: rgba(255,255,255,0.12); border-radius: 10px;
        padding: 14px; margin-bottom: 14px; color: white !important;
        font-size: 0.88rem; line-height: 1.7;
        border: 1px solid rgba(255,255,255,0.15);
    }
    .sidebar-block b { color: #7ecfff !important; }
    .sidebar-block code {
        background: rgba(255,255,255,0.18); border-radius: 4px;
        padding: 1px 5px; color: #ffe08a !important; font-size: 0.82rem;
    }
    .stButton > button {
        background: linear-gradient(135deg,#1e3a5f,#2980b9);
        color:white; border:none; border-radius:10px;
        padding:12px 28px; font-size:1.05rem; font-weight:700;
        width:100%; transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(41,128,185,0.45);
    }
    .perf-table {
        width:100%; border-collapse:collapse; margin-top:10px;
        font-size:0.9rem; color:#1e3a5f;
    }
    .perf-table th { background:#1e3a5f; color:white; padding:9px 14px; text-align:left; }
    .perf-table td { padding:8px 14px; border-bottom:1px solid #dde3ea; }
    .perf-table tr:nth-child(even) { background:#f0f4f8; }
    .perf-table tr:first-child td { font-weight:700; color:#27ae60; }
    .intro-card {
        background:white; border-radius:14px; padding:24px 28px;
        box-shadow:0 4px 18px rgba(0,0,0,0.08); margin-bottom:18px;
        border-top: 4px solid #2980b9;
    }
    .intro-card h3 { color:#1e3a5f; margin:0 0 10px 0; font-size:1.15rem; }
    .intro-card p  { color:#4a4a4a; margin:0; line-height:1.7; font-size:0.95rem; }
    .badge {
        display:inline-block; padding:4px 14px; border-radius:20px;
        font-size:0.82rem; font-weight:700; margin:3px;
    }
    .badge-blue  { background:#d6eaf8; color:#1e3a5f; }
    .badge-green { background:#d5f5e3; color:#1e8449; }
    .badge-gold  { background:#fef9e7; color:#9a7d0a; border:1px solid #f39c12; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:16px 0 10px 0;">
        <div style="font-size:3rem;">🏥</div>
        <div style="font-size:1.1rem; font-weight:800; color:#7ecfff; margin-top:4px;">
            Hôpital Mohamed V
        </div>
        <div style="font-size:0.82rem; color:#cce4ff; margin-top:2px;">Meknès — Urgences</div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.2); margin:10px 0 16px 0;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-block">
        <b>🎯 Objectif</b><br>
        Prédire le nombre de passages aux urgences pour anticiper les besoins en personnel et ressources médicales.
    </div>
    <div class="sidebar-block">
        <b>🤖 Modèles utilisés</b><br>
        • <b>Prophet</b> (Facebook/Meta) — prévision mensuelle<br>
        • <b>MLP</b> (Réseau de neurones) — prévision journalière ⭐ MAE = 7
    </div>
    <div class="sidebar-block">
        <b>📊 Évaluation</b><br>
        • Intervalles de confiance à <b>95%</b><br>
        • Erreur <b>MAE</b> affichée<br>
        • Fiabilité estimée en <b>%</b>
    </div>
    <div class="sidebar-block">
        <b>📁 Format fichier Excel</b><br>
        Colonne A : <code>Date</code><br>
        Colonne B : <code>Nombre de passages</code><br><br>
        ✅ Exemples valides :<br>
        &nbsp;• <code>2024-01-01</code> / <code>245</code><br>
        &nbsp;• <code>Janvier 2024</code> / <code>7340</code><br><br>
        ❌ Éviter :<br>
        &nbsp;• Plus de 2 colonnes<br>
        &nbsp;• Cellules fusionnées
    </div>
    <div class="sidebar-block">
        <b>🏆 Performances des modèles</b><br><br>
        🥇 MLP &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MAE = <b>7</b><br>
        🥈 Prophet &nbsp;&nbsp;&nbsp;&nbsp;MAE = Excellent<br>
        🥉 XGBoost &nbsp;&nbsp;&nbsp;MAE = Très bon<br>
        4️⃣ LSTM/GRU &nbsp;MAE = Bon<br>
        5️⃣ SARIMA &nbsp;&nbsp;&nbsp;&nbsp;MAE = Moyen
    </div>
    <div style="text-align:center; color:#aacce0; font-size:0.78rem; margin-top:10px;">
        👨‍💼 Issoug El Mehdi & Bado Ange Yipene Cenacle<br>
        Projet Séries Temporelles 2024–2025
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  NAVIGATION
# ─────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "intro"

col_nav1, col_nav2, col_nav3 = st.columns([1,1,4])
with col_nav1:
    if st.button("📖  Introduction", use_container_width=True):
        st.session_state.page = "intro"
with col_nav2:
    if st.button("🔮  Prédiction", use_container_width=True):
        st.session_state.page = "prediction"

st.markdown("---")

# ══════════════════════════════════════════════
#  PAGE 1 — INTRODUCTION
# ══════════════════════════════════════════════
if st.session_state.page == "intro":

    st.markdown("""
    <div class="main-title">
        <h1>🏥 Prévision des Passages aux Urgences</h1>
        <p>🏛️ Hôpital Mohamed V — Meknès &nbsp;|&nbsp; Outil d'aide à la décision médicale</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="intro-card">
            <h3>🎯 Objectif du projet</h3>
            <p>
            Ce projet vise à <b>prédire le nombre quotidien et mensuel de passages aux urgences</b>
            de l'Hôpital Mohamed V de Meknès, à l'aide de modèles de séries temporelles avancés.<br><br>
            L'outil aide les équipes médicales à <b>anticiper les pics d'affluence</b>,
            optimiser les ressources humaines et améliorer la prise en charge des patients.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="intro-card">
            <h3>📊 Données utilisées</h3>
            <p>
            • <b>Source :</b> Registres de l'Hôpital Mohamed V, Meknès<br>
            • <b>Période :</b> Janvier 2024 — 2025<br>
            • <b>Granularité :</b> Données mensuelles (désagrégées en journalier)<br>
            • <b>Variable cible :</b> Nombre de passages aux urgences<br><br>
            <span class="badge badge-blue">Séries temporelles</span>
            <span class="badge badge-green">Deep Learning</span>
            <span class="badge badge-gold">Statistiques</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔄 Pipeline du projet</div>', unsafe_allow_html=True)
    p1, p2, p3, p4, p5 = st.columns(5)
    steps = [
        ("1️⃣", "Chargement & Prétraitement", "Nettoyage, format long, désagrégation mensuelle → journalière"),
        ("2️⃣", "Analyse statistique", "Stationnarité (ADF, KPSS, PP), ACF/PACF, différenciation"),
        ("3️⃣", "Modèles statistiques", "Prophet mensuel & journalier, SARIMA + GARCH"),
        ("4️⃣", "Machine Learning", "XGBoost, LightGBM, MLP avec feature engineering temporel"),
        ("5️⃣", "Deep Learning", "RNN, LSTM, GRU avec optimisation Optuna"),
    ]
    for col, (num, title, desc) in zip([p1,p2,p3,p4,p5], steps):
        with col:
            st.markdown(f"""
            <div style="background:white; border-radius:12px; padding:18px 14px;
                        text-align:center; box-shadow:0 3px 12px rgba(0,0,0,0.07);
                        height:180px; border-bottom:4px solid #2980b9;">
                <div style="font-size:1.8rem;">{num}</div>
                <div style="font-weight:700; color:#1e3a5f; margin:8px 0 6px 0;
                            font-size:0.88rem;">{title}</div>
                <div style="color:#7f8c8d; font-size:0.78rem; line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🏆 Comparaison des modèles testés</div>', unsafe_allow_html=True)
    st.markdown("""
    <table class="perf-table">
        <tr><th>Modèle</th><th>Type</th><th>MAE Journalier</th><th>Points forts</th><th>Limites</th><th>Rang</th></tr>
        <tr>
            <td>🥇 MLP</td><td>Réseau de neurones</td><td><b>≈ 7</b> ⭐</td>
            <td>Excellent avec feature engineering, rapide</td>
            <td>Pas de mémoire séquentielle</td><td>1er</td>
        </tr>
        <tr>
            <td>🥈 Prophet</td><td>Statistique bayésien</td><td>Excellent (mensuel)</td>
            <td>Gère tendances et saisonnalité automatiquement</td>
            <td>Moins adapté au journalier fin</td><td>2e</td>
        </tr>
        <tr>
            <td>🥉 XGBoost</td><td>Gradient Boosting</td><td>Très bon</td>
            <td>Rapide, interprétable, robuste</td>
            <td>Pas de mémoire temporelle</td><td>3e</td>
        </tr>
        <tr>
            <td>4️⃣ LightGBM</td><td>Gradient Boosting</td><td>≈ 47</td>
            <td>Très rapide, léger</td>
            <td>Moins précis que MLP ici</td><td>4e</td>
        </tr>
        <tr>
            <td>5️⃣ LSTM / GRU</td><td>Deep Learning RNN</td><td>Bon</td>
            <td>Mémoire longue, séquentiel</td>
            <td>Nécessite beaucoup de données</td><td>5e</td>
        </tr>
        <tr>
            <td>6️⃣ SARIMA+GARCH</td><td>Statistique classique</td><td>≈ 100</td>
            <td>Interprétable, intervalles de confiance</td>
            <td>Linéaire uniquement, lent</td><td>6e</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">📊 Visualisation des performances</div>', unsafe_allow_html=True)
    modeles  = ["MLP ⭐", "XGBoost", "LightGBM", "LSTM", "GRU", "SARIMA"]
    mae_vals = [7, 22, 47, 55, 58, 100]
    colors   = ["#27ae60","#2980b9","#3498db","#8e44ad","#9b59b6","#e74c3c"]
    fig_cmp = go.Figure(go.Bar(
        x=modeles, y=mae_vals, marker=dict(color=colors),
        text=[f"MAE ≈ {v}" for v in mae_vals], textposition="outside"
    ))
    fig_cmp.update_layout(
        title="MAE des modèles — plus c'est bas, mieux c'est ✅",
        xaxis_title="Modèle", yaxis_title="MAE (erreur absolue moyenne)",
        plot_bgcolor="white", height=370,
        yaxis=dict(showgrid=True, gridcolor="#ecf0f1"),
        font=dict(family="Arial"),
        annotations=[dict(
            x="MLP ⭐", y=7, text="🏆 Meilleur",
            showarrow=True, arrowhead=2, ax=0, ay=-40,
            font=dict(color="#27ae60", size=13)
        )]
    )
    st.plotly_chart(fig_cmp, use_container_width=True)

    st.markdown('<div class="section-header">🔬 Résultats des tests statistiques</div>', unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    for col, (test, stat, pval, conclusion) in zip([t1,t2,t3], [
        ("ADF (Augmented Dickey-Fuller)", "Stat < Valeur critique", "p < 0.05", "✅ Stationnaire après différenciation"),
        ("KPSS", "Stat < Valeur critique", "p > 0.05", "✅ Stationnaire confirmé"),
        ("Phillips-Perron", "Stat < Valeur critique", "p < 0.05", "✅ Cohérent avec ADF"),
    ]):
        with col:
            st.markdown(f"""
            <div style="background:white; border-radius:12px; padding:18px;
                        box-shadow:0 3px 10px rgba(0,0,0,0.07); border-top:3px solid #2980b9;">
                <div style="font-weight:700; color:#1e3a5f; font-size:0.9rem;">{test}</div>
                <div style="color:#7f8c8d; font-size:0.82rem; margin:6px 0;">{stat} | {pval}</div>
                <div style="color:#27ae60; font-weight:700; font-size:0.88rem;">{conclusion}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box" style="margin-top:18px;">
    📌 <b>Conclusion :</b> La série est <b>non-stationnaire à l'origine</b> mais devient stationnaire après
    une différenciation d'ordre 1 (d=1). Une composante saisonnière hebdomadaire (S=7) a été détectée.
    Le modèle <b>MLP</b> avec feature engineering temporel (encodage cyclique jour/mois, lags)
    donne les meilleures performances avec <b>MAE ≈ 7 passages/jour</b>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_cta, _ = st.columns([1,2])
    with col_cta:
        if st.button("🔮  Accéder à la Prédiction →", use_container_width=True):
            st.session_state.page = "prediction"
            st.rerun()

# ══════════════════════════════════════════════
#  PAGE 2 — PRÉDICTION
# ══════════════════════════════════════════════
elif st.session_state.page == "prediction":

    st.markdown("""
    <div class="main-title">
        <h1>🔮 Prévision des Passages aux Urgences</h1>
        <p>Chargez vos données Excel et obtenez vos prédictions en quelques secondes</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""<div class="metric-card">
            <h3>🤖 Modèle Mensuel</h3><h2>Prophet</h2>
            <small>Bayésien — Facebook/Meta</small></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="metric-card">
            <h3>⭐ Modèle Journalier</h3><h2>MLP</h2>
            <small>Réseau de neurones — MAE ≈ 7</small></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="metric-card">
            <h3>🎯 Confiance</h3><h2>95%</h2>
            <small>Intervalle de prédiction</small></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="metric-card">
            <h3>📈 Visualisation</h3><h2>Plotly</h2>
            <small>Courbes interactives & zoom</small></div>""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-header">🔀 Type de prévision</div>', unsafe_allow_html=True)
    mode = st.radio("", ["📅  Prévision MENSUELLE", "📆  Prévision JOURNALIÈRE"], horizontal=True)
    is_monthly = "MENSUELLE" in mode

    # ── Lecture Excel ──
    def lire_excel(uploaded_file, granularity="monthly"):
        try:
            df_raw = pd.read_excel(uploaded_file, header=None)
        except Exception as e:
            return None, f"❌ Impossible de lire le fichier Excel : {e}"

        df_raw = df_raw.dropna(how="all", axis=1).dropna(how="all", axis=0)

        if df_raw.shape[1] < 2:
            return None, "❌ Le fichier doit contenir 2 colonnes : **Date** et **Nombre de passages**."

        df_raw = df_raw.iloc[:, :2].copy()
        df_raw.columns = ["date_raw", "y_raw"]

        mask_numeric = df_raw["y_raw"].astype(str).str.strip().str.replace(",",".",regex=False).str.match(r"^\d+\.?\d*$")
        df_raw = df_raw[mask_numeric].copy()

        if df_raw.empty:
            return None, "❌ Aucune valeur numérique trouvée dans la colonne Passages."

        df_raw["date_raw"] = df_raw["date_raw"].astype(str).str.strip()
        parsed_dates = pd.Series([pd.NaT] * len(df_raw), dtype="datetime64[ns]", index=df_raw.index)
        for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d", "%B %Y", "%b %Y"]:
            mask_na = parsed_dates.isna()
            if not mask_na.any():
                break
            attempt = pd.to_datetime(df_raw.loc[mask_na, "date_raw"], format=fmt, errors="coerce")
            parsed_dates[mask_na] = attempt.values
        still_na = parsed_dates.isna()
        if still_na.any():
            attempt = pd.to_datetime(df_raw.loc[still_na, "date_raw"], errors="coerce")
            parsed_dates[still_na] = attempt.values

        df_raw["ds"] = parsed_dates

        if df_raw["ds"].isna().sum() == len(df_raw):
            return None, "❌ La colonne de dates n'est pas reconnue. Utilisez : 01/01/2024 ou 2024-01-01."

        df_raw["y"] = pd.to_numeric(
            df_raw["y_raw"].astype(str).str.replace(",",".",regex=False), errors="coerce"
        )

        df_clean = df_raw[["ds","y"]].dropna().sort_values("ds").reset_index(drop=True)

        if len(df_clean) < 6:
            return None, f"❌ Seulement {len(df_clean)} lignes valides. Minimum 6 requis."

        if granularity == "monthly":
            df_clean["ds"] = df_clean["ds"].apply(lambda d: d.replace(day=1))

        return df_clean, None

    def generer_exemple_excel(is_monthly):
        if is_monthly:
            dates = pd.date_range("2024-01-01", periods=17, freq="MS")
            vals  = [7340,6850,7120,7400,7600,7250,7800,7500,7300,7650,7100,7900,7200,7450,7600,7350,7550]
            label = "Mois"
        else:
            dates = pd.date_range("2024-01-01", periods=60, freq="D")
            np.random.seed(42)
            vals  = np.random.randint(220,280,60).tolist()
            label = "Date"
        df_ex = pd.DataFrame({label: [d.strftime("%Y-%m-%d") for d in dates], "Passages": vals})
        out = BytesIO()
        with pd.ExcelWriter(out, engine="openpyxl") as w:
            df_ex.to_excel(w, index=False, sheet_name="Données")
        out.seek(0)
        return out

    # ── Prophet ──
    def predict_monthly(df, n_months):
        from prophet import Prophet
        from sklearn.metrics import mean_absolute_error
        model = Prophet(
            yearly_seasonality=True, weekly_seasonality=False,
            daily_seasonality=False, interval_width=0.95,
            changepoint_prior_scale=0.3
        )
        model.fit(df)
        future = model.make_future_dataframe(periods=n_months, freq="MS")
        forecast_full = model.predict(future)
        last_date = df["ds"].max()
        forecast  = forecast_full[forecast_full["ds"] > last_date].head(n_months)
        in_sample = forecast_full[forecast_full["ds"] <= last_date]
        mae = mean_absolute_error(df["y"].values, in_sample["yhat"].values[:len(df)])
        return forecast[["ds","yhat","yhat_lower","yhat_upper"]].reset_index(drop=True), mae

    # ── MLP ──
    def predict_daily_mlp(df, n_days):
        from sklearn.neural_network import MLPRegressor
        from sklearn.preprocessing import MinMaxScaler
        from sklearn.metrics import mean_absolute_error

        df = df.copy().sort_values("ds").reset_index(drop=True)

        def make_features(dates, y_series=None, history_y=None, idx=None):
            rows = []
            for i, d in enumerate(dates):
                d = pd.Timestamp(d)
                feat = {
                    "dayofweek":  d.dayofweek,
                    "dayofmonth": d.day,
                    "month":      d.month,
                    "quarter":    d.quarter,
                    "dayofyear":  d.dayofyear,
                    "dow_sin":    np.sin(2*np.pi*d.dayofweek/7),
                    "dow_cos":    np.cos(2*np.pi*d.dayofweek/7),
                    "month_sin":  np.sin(2*np.pi*d.month/12),
                    "month_cos":  np.cos(2*np.pi*d.month/12),
                }
                if y_series is not None:
                    base_idx = idx if idx is not None else i
                    for lag in [1,2,3,7,14]:
                        li = base_idx - lag
                        feat[f"lag_{lag}"] = float(y_series[li]) if li >= 0 else np.nan
                    for w in [7,14]:
                        li = base_idx - w
                        feat[f"roll_{w}"] = float(np.mean(y_series[max(0,li):base_idx])) if base_idx > 0 else np.nan
                elif history_y is not None:
                    for lag in [1,2,3,7,14]:
                        li = len(history_y) - lag
                        feat[f"lag_{lag}"] = float(history_y[li]) if li >= 0 else np.nan
                    for w in [7,14]:
                        feat[f"roll_{w}"] = float(np.mean(history_y[-w:])) if len(history_y) >= w else float(np.mean(history_y))
                rows.append(feat)
            return pd.DataFrame(rows).bfill().ffill().fillna(0)

        y_arr  = df["y"].values
        X      = make_features(df["ds"], y_series=y_arr)
        y      = y_arr
        split  = max(int(len(df)*0.85), len(df)-30)
        X_tr, y_tr   = X.iloc[:split], y[:split]
        X_val, y_val = X.iloc[split:], y[split:]

        scaler_X = MinMaxScaler()
        scaler_y = MinMaxScaler()
        X_tr_s   = scaler_X.fit_transform(X_tr)
        X_val_s  = scaler_X.transform(X_val)
        y_tr_s   = scaler_y.fit_transform(y_tr.reshape(-1,1)).ravel()

        model = MLPRegressor(
            hidden_layer_sizes=(128,64,32), activation="relu",
            max_iter=1000, random_state=42, early_stopping=True,
            validation_fraction=0.1, learning_rate_init=0.001, n_iter_no_change=20
        )
        model.fit(X_tr_s, y_tr_s)

        val_preds_s = model.predict(X_val_s)
        val_preds   = scaler_y.inverse_transform(val_preds_s.reshape(-1,1)).ravel()
        mae        = mean_absolute_error(y_val, val_preds)
        resid_std  = np.std(y_val - val_preds)

        history_y = list(y_arr)
        last_date = pd.Timestamp(df["ds"].max())
        future_preds, future_lower, future_upper = [], [], []

        for i in range(n_days):
            next_date = last_date + pd.Timedelta(days=i+1)
            row   = make_features([next_date], history_y=history_y)
            row_s = scaler_X.transform(row)
            pred_s = model.predict(row_s)[0]
            pred   = float(scaler_y.inverse_transform([[pred_s]])[0][0])
            pred   = max(0, pred)
            future_preds.append(pred)
            future_lower.append(max(0, pred - 1.96*resid_std))
            future_upper.append(pred + 1.96*resid_std)
            history_y.append(pred)

        future_dates = [last_date + pd.Timedelta(days=i+1) for i in range(n_days)]
        return pd.DataFrame({
            "ds": future_dates, "yhat": future_preds,
            "yhat_lower": future_lower, "yhat_upper": future_upper
        }), mae

    # ── Graphique — FIX add_vline ──
    def plot_forecast(df_hist, df_fc, is_monthly, mae):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_hist["ds"], y=df_hist["y"], mode="lines+markers",
            name="📊 Historique", line=dict(color="#1e3a5f", width=2.5),
            marker=dict(size=5)
        ))
        fig.add_trace(go.Scatter(
            x=list(df_fc["ds"]) + list(df_fc["ds"][::-1]),
            y=list(df_fc["yhat_upper"]) + list(df_fc["yhat_lower"][::-1]),
            fill="toself", fillcolor="rgba(41,128,185,0.12)",
            line=dict(color="rgba(0,0,0,0)"), name="🔵 IC 95%"
        ))
        fig.add_trace(go.Scatter(
            x=df_fc["ds"], y=df_fc["yhat"], mode="lines+markers",
            name="🔮 Prévisions", line=dict(color="#e74c3c", width=3, dash="dot"),
            marker=dict(size=7, symbol="diamond")
        ))
        fig.add_trace(go.Scatter(
            x=df_fc["ds"], y=df_fc["yhat_upper"], mode="lines",
            name="⬆️ Borne haute", line=dict(color="#27ae60", dash="dash", width=1.5)
        ))
        fig.add_trace(go.Scatter(
            x=df_fc["ds"], y=df_fc["yhat_lower"], mode="lines",
            name="⬇️ Borne basse", line=dict(color="#e67e22", dash="dash", width=1.5)
        ))

        # ✅ FIX : utiliser add_shape + add_annotation au lieu de add_vline
        # add_vline plante avec pandas >= 2.0 car Plotly essaie d'additionner
        # des entiers à un pd.Timestamp en interne → TypeError
        last_x = str(df_hist["ds"].max().date())
        fig.add_shape(
            type="line",
            x0=last_x, x1=last_x,
            y0=0, y1=1, yref="paper",
            line=dict(dash="dash", color="gray", width=1.5)
        )
        fig.add_annotation(
            x=last_x, y=0.98, yref="paper",
            text="  Fin historique",
            showarrow=False, xanchor="left",
            font=dict(color="gray", size=11)
        )

        granularity = "mois" if is_monthly else "jours"
        fig.update_layout(
            title=f"🏥 Prévisions — MAE ≈ {mae:.0f} patients/{granularity}",
            xaxis_title="Date", yaxis_title="Nombre de passages",
            hovermode="x unified", plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", y=-0.22, x=0), height=480,
            xaxis=dict(showgrid=True, gridcolor="#ecf0f1"),
            yaxis=dict(showgrid=True, gridcolor="#ecf0f1"),
        )
        return fig

    # ── Étape 1 : Upload ──
    st.markdown('<div class="section-header">📁 Étape 1 — Charger vos données</div>', unsafe_allow_html=True)
    format_msg = (
        "**Format mensuel :** Colonne A = Mois (ex: `2024-01-01` ou `Janvier 2024`) | Colonne B = Nombre de passages"
        if is_monthly else
        "**Format journalier :** Colonne A = Date (ex: `2024-01-01`) | Colonne B = Nombre de passages"
    )
    with st.expander("📖 Format attendu du fichier Excel", expanded=True):
        st.markdown(format_msg)
        col_dl, _ = st.columns([1,3])
        with col_dl:
            st.download_button(
                "⬇️ Télécharger un exemple Excel",
                data=generer_exemple_excel(is_monthly),
                file_name=f"exemple_{'mensuel' if is_monthly else 'journalier'}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    uploaded = st.file_uploader(
        f"📤 Déposez votre fichier Excel ({'données mensuelles' if is_monthly else 'données journalières'})",
        type=["xlsx","xls"]
    )

    if uploaded is not None:
        df_data, err = lire_excel(uploaded, "monthly" if is_monthly else "daily")
        if err:
            st.markdown(f'<div class="warning-box">{err}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="success-box">✅ <b>{len(df_data)}</b> enregistrements chargés — '
                f'de <b>{df_data["ds"].min().strftime("%d/%m/%Y")}</b> '
                f'à <b>{df_data["ds"].max().strftime("%d/%m/%Y")}</b></div>',
                unsafe_allow_html=True
            )

            with st.expander("🔍 Aperçu des données"):
                df_show = df_data.copy()
                df_show["ds"] = df_show["ds"].dt.strftime("%d/%m/%Y")
                df_show.columns = ["Date","Passages"]
                st.dataframe(df_show, use_container_width=True, height=200)

            fig_h = go.Figure()
            fig_h.add_trace(go.Scatter(
                x=df_data["ds"], y=df_data["y"], mode="lines+markers",
                line=dict(color="#1e3a5f", width=2), marker=dict(size=5),
                fill="tozeroy", fillcolor="rgba(30,58,95,0.08)"
            ))
            fig_h.update_layout(
                title="📈 Historique des passages", xaxis_title="Date",
                yaxis_title="Passages", plot_bgcolor="white", height=300
            )
            st.plotly_chart(fig_h, use_container_width=True)

            # ── Étape 2 : Plage ──
            st.markdown('<div class="section-header">📅 Étape 2 — Plage de prévision</div>', unsafe_allow_html=True)
            last_date = df_data["ds"].max()
            if is_monthly:
                n_periods  = st.slider("Nombre de mois à prédire", 1, 24, 6)
                first_pred = last_date + pd.DateOffset(months=1)
                last_pred  = last_date + pd.DateOffset(months=n_periods)
            else:
                n_periods  = st.slider("Nombre de jours à prédire", 1, 90, 14)
                first_pred = last_date + pd.Timedelta(days=1)
                last_pred  = last_date + pd.Timedelta(days=n_periods)

            st.markdown(f"""
            <div class="info-box">
            📅 Les prévisions iront du <b>{first_pred.strftime('%d/%m/%Y')}</b>
            au <b>{last_pred.strftime('%d/%m/%Y')}</b>
            ({n_periods} {'mois' if is_monthly else 'jours'})
            </div>
            """, unsafe_allow_html=True)

            # ── Étape 3 : Lancer ──
            st.markdown('<div class="section-header">🚀 Étape 3 — Générer les prévisions</div>', unsafe_allow_html=True)
            col_btn, _ = st.columns([1,3])
            with col_btn:
                run = st.button("🔮 Générer les prévisions", use_container_width=True)

            if run:
                with st.spinner("🧠 Entraînement du modèle… quelques secondes…"):
                    try:
                        if is_monthly:
                            model_name = "Prophet (Facebook/Meta)"
                            fc_df, mae = predict_monthly(df_data, n_periods)
                        else:
                            model_name = "MLP — Réseau de neurones (scikit-learn)"
                            fc_df, mae = predict_daily_mlp(df_data, n_periods)

                        st.markdown("---")
                        st.markdown(
                            f'<div class="success-box">✅ <b>Modèle :</b> {model_name} &nbsp;|&nbsp; '
                            f'<b>MAE ≈ {mae:.0f}</b> passages/{"mois" if is_monthly else "jour"} &nbsp;|&nbsp; '
                            f'<b>IC 95%</b></div>',
                            unsafe_allow_html=True
                        )

                        n_show = min(n_periods, 4)
                        cols_r = st.columns(n_show)
                        for i, (_, row) in enumerate(fc_df.head(n_show).iterrows()):
                            with cols_r[i]:
                                dlabel    = row["ds"].strftime("%b %Y") if is_monthly else row["ds"].strftime("%d/%m")
                                certitude = max(0, int(100 - (mae/row["yhat"]*100))) if row["yhat"] > 0 else 0
                                st.markdown(f"""
                                <div class="metric-card">
                                    <h3>📅 {dlabel}</h3>
                                    <h2>{row['yhat']:.0f}</h2>
                                    <small>[{row['yhat_lower']:.0f} – {row['yhat_upper']:.0f}]<br>
                                    Fiabilité : <b>{certitude}%</b></small>
                                </div>""", unsafe_allow_html=True)

                        if n_periods == 1:
                            r = fc_df.iloc[0]
                            certitude = max(0, int(100 - (mae/r["yhat"]*100))) if r["yhat"] > 0 else 0
                            st.markdown(f"""
                            <div class="result-highlight">
                                <div>🔮 Prévision</div>
                                <div class="big-num">{r['yhat']:.0f} patients</div>
                                <div class="interval">📉 {r['yhat_lower']:.0f} &nbsp;|&nbsp; 📈 {r['yhat_upper']:.0f}</div>
                                <div class="interval">🎯 Fiabilité : {certitude}%</div>
                            </div>""", unsafe_allow_html=True)

                        # ✅ Graphique — maintenant sans erreur
                        st.plotly_chart(plot_forecast(df_data, fc_df, is_monthly, mae), use_container_width=True)

                        # Tableau
                        df_disp = fc_df.copy()
                        df_disp["ds"]         = df_disp["ds"].dt.strftime("%B %Y" if is_monthly else "%d/%m/%Y")
                        df_disp["yhat"]       = df_disp["yhat"].round(0).astype(int)
                        df_disp["yhat_lower"] = df_disp["yhat_lower"].round(0).astype(int)
                        df_disp["yhat_upper"] = df_disp["yhat_upper"].round(0).astype(int)
                        df_disp["Fiabilité"]  = df_disp["yhat"].apply(
                            lambda v: f"{max(0,int(100-mae/v*100))}%" if v > 0 else "N/A"
                        )
                        df_disp.columns = ["Date","Prévision","Borne basse (95%)","Borne haute (95%)","Fiabilité"]
                        st.dataframe(df_disp, use_container_width=True)

                        # Export Excel
                        out = BytesIO()
                        with pd.ExcelWriter(out, engine="openpyxl") as w:
                            df_disp.to_excel(w, index=False, sheet_name="Prévisions")
                            df_data.rename(columns={"ds":"Date","y":"Passages"}).to_excel(
                                w, index=False, sheet_name="Historique"
                            )
                        out.seek(0)
                        st.download_button(
                            "📥 Télécharger les prévisions (Excel)", data=out,
                            file_name=f"previsions_urgences_{'mensuel' if is_monthly else 'journalier'}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                    except Exception as e:
                        st.error(f"❌ Erreur lors de la prévision : {e}")
    else:
        st.markdown("""
        <div class="info-box">
        📤 <b>En attente de votre fichier Excel…</b><br>
        Déposez votre fichier ci-dessus ou téléchargez d'abord l'exemple pour voir le format attendu.
        </div>""", unsafe_allow_html=True)

# ─── Footer ───
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#7f8c8d; font-size:0.85rem; padding:10px 0;">
🏥 Hôpital Mohamed V — Meknès &nbsp;|&nbsp;
Développé par <b>Issoug El Mehdi & Bado Ange Yipene Cenacle </b> &nbsp;|&nbsp;
Modèles : Prophet · MLP &nbsp;|&nbsp;
🔒 Usage interne uniquement
</div>
""", unsafe_allow_html=True)