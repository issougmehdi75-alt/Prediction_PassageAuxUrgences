"""Figures Plotly : une seule palette, validée daltonisme (bleu = observé, orange = prévu)."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

# ── Palette (rôles, pas couleurs décoratives) ──
BLEU = "#2a78d6"        # série 1 : historique / modèle mis en avant
BLEU_CLAIR = "#86b6ef"  # autres modèles
ORANGE = "#eb6834"      # série 2 : prévision
ORANGE_BANDE = "rgba(235,104,52,0.16)"
BLEU_BANDE = "rgba(42,120,214,0.10)"
GRIS_BASELINE = "#c3c2b7"
ENCRE = "#0b0b0b"
ENCRE_2 = "#52514e"
MUET = "#898781"
GRILLE = "#e1e0d9"
SURFACE = "#ffffff"
FONT = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'

MOIS_FR = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]


JOURS_FR = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."]


def mois_fr(d: pd.Timestamp) -> str:
    return f"{MOIS_FR[d.month - 1]} {d.year}"


def jour_fr(d: pd.Timestamp) -> str:
    return f"{JOURS_FR[d.dayofweek]} {d:%d/%m/%Y}"


def _axe_dates(fig: go.Figure, dates: pd.Series, mensuel: bool) -> None:
    """Graduations en français (Plotly n'affiche que l'anglais par défaut)."""
    if mensuel:
        d = pd.Series(pd.to_datetime(dates)).drop_duplicates().sort_values()
        pas = max(1, -(-len(d) // 7))  # ≤ 7 graduations
        ticks = d.iloc[::pas]
        marge = pd.Timedelta(days=12)
        fig.update_xaxes(tickvals=list(ticks), ticktext=[mois_fr(x) for x in ticks], hoverformat="%m/%Y",
                         range=[d.iloc[0] - marge, d.iloc[-1] + marge], tickangle=0)
    else:
        fig.update_xaxes(tickformat="%d/%m", hoverformat="%d/%m/%Y")


def _base(fig: go.Figure, titre: str | None, hauteur: int, y_titre: str = "Passages") -> go.Figure:
    fig.update_layout(
        title=dict(text=titre, x=0, xanchor="left", font=dict(size=15, color=ENCRE)) if titre else None,
        height=hauteur, margin=dict(l=8, r=8, t=48 if titre else 16, b=8),
        plot_bgcolor=SURFACE, paper_bgcolor=SURFACE,
        font=dict(family=FONT, size=12, color=ENCRE_2),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="white", bordercolor=GRILLE, font=dict(family=FONT, color=ENCRE)),
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1,
                    font=dict(size=12, color=ENCRE_2), bgcolor="rgba(0,0,0,0)"),
        separators=", ",
    )
    fig.update_xaxes(showgrid=False, linecolor=GRIS_BASELINE, tickfont=dict(color=MUET), ticks="")
    fig.update_yaxes(showgrid=True, gridcolor=GRILLE, zeroline=False, tickfont=dict(color=MUET),
                     title=dict(text=y_titre, font=dict(color=MUET, size=12)), tickformat=",d")
    return fig


def figure_historique(df: pd.DataFrame, mensuel: bool, titre: str | None = None, hauteur: int = 300) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["ds"], y=df["y"], name="Observé", mode="lines+markers" if mensuel else "lines",
        line=dict(color=BLEU, width=2), marker=dict(size=8, color=BLEU, line=dict(color="white", width=2)),
        fill="tozeroy" if mensuel else None, fillcolor=BLEU_BANDE,
        hovertemplate="%{y:,.0f} passages<extra></extra>",
    ))
    if not mensuel and len(df) >= 28:  # tendance lisible sous le bruit journalier
        mm = df["y"].rolling(28, center=True).mean()
        fig.add_trace(go.Scatter(x=df["ds"], y=mm, name="Moyenne mobile 28 j",
                                 line=dict(color=ENCRE, width=1.5),
                                 hovertemplate="moy. 28 j : %{y:,.0f}<extra></extra>"))
        fig.data[0].line.width = 1
        fig.data[0].line.color = BLEU_CLAIR
    if mensuel:
        lo, hi = df["y"].min(), df["y"].max()
        fig.update_yaxes(range=[lo - (hi - lo) * 0.6, hi + (hi - lo) * 0.3])
    _axe_dates(fig, df["ds"], mensuel)
    if not mensuel:
        fig.update_xaxes(tickformat="%m/%Y", dtick="M2")
    return _base(fig, titre, hauteur)


def figure_prevision(hist: pd.DataFrame, fc: pd.DataFrame, mensuel: bool, hauteur: int = 460) -> go.Figure:
    """Historique (bleu) + prévision (orange) + bande d'incertitude 95 % (orange clair)."""
    if not mensuel:  # ne garder que les dernières semaines pour que la prévision reste lisible
        hist = hist.tail(max(42, 3 * len(fc)))
    fig = go.Figure()
    # pont visuel entre dernier point observé et première prévision
    x_band = list(fc["ds"]) + list(fc["ds"][::-1])
    y_band = list(fc["yhat_upper"]) + list(fc["yhat_lower"][::-1])
    fig.add_trace(go.Scatter(x=x_band, y=y_band, fill="toself", fillcolor=ORANGE_BANDE, mode="lines",
                             line=dict(width=0), name="Intervalle 95 %", hoverinfo="skip"))
    fig.add_trace(go.Scatter(
        x=hist["ds"], y=hist["y"], name="Observé", mode="lines+markers" if mensuel else "lines",
        line=dict(color=BLEU, width=2 if mensuel else 1.5),
        marker=dict(size=7, color=BLEU, line=dict(color="white", width=1.5)),
        hovertemplate="observé : %{y:,.0f}<extra></extra>",
    ))
    pont_x = [hist["ds"].iloc[-1], fc["ds"].iloc[0]]
    pont_y = [hist["y"].iloc[-1], fc["yhat"].iloc[0]]
    fig.add_trace(go.Scatter(x=pont_x, y=pont_y, mode="lines", line=dict(color=ORANGE, width=2, dash="dot"),
                             showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(
        x=fc["ds"], y=fc["yhat"], name="Prévision", mode="lines+markers",
        line=dict(color=ORANGE, width=2.5), marker=dict(size=8 if mensuel else 6, color=ORANGE,
                                                        line=dict(color="white", width=1.5)),
        customdata=fc[["yhat_lower", "yhat_upper"]].to_numpy(),
        hovertemplate="prévu : %{y:,.0f}  [%{customdata[0]:,.0f} – %{customdata[1]:,.0f}]<extra></extra>",
    ))
    x0 = hist["ds"].iloc[-1]
    fig.add_shape(type="line", x0=x0, x1=x0, y0=0, y1=1, yref="paper",
                  line=dict(color=MUET, width=1, dash="dash"))
    fig.add_annotation(x=x0, y=1, yref="paper", text="dernière observation", showarrow=False,
                       xanchor="right", yanchor="top", xshift=-6, font=dict(color=MUET, size=11))
    _axe_dates(fig, pd.concat([hist["ds"], fc["ds"]]), mensuel)
    return _base(fig, None, hauteur)


def figure_comparaison(resultats: list[dict], plancher: float | None, mis_en_avant: str,
                       metrique: str = "MAE", hauteur: int = 360) -> go.Figure:
    """Barres horizontales triées : baselines en gris, modèles en bleu, modèle retenu en bleu foncé."""
    lignes = sorted(resultats, key=lambda r: r[metrique], reverse=True)  # meilleur en haut
    noms = [r["modele"] for r in lignes]
    vals = [r[metrique] for r in lignes]
    couleurs = [BLEU if r["modele"] == mis_en_avant else (GRIS_BASELINE if r["baseline"] else BLEU_CLAIR)
                for r in lignes]
    fig = go.Figure(go.Bar(
        y=noms, x=vals, orientation="h", marker=dict(color=couleurs, cornerradius=4),
        text=[f"{v:,.1f}" for v in vals], textposition="outside", cliponaxis=False,
        textfont=dict(color=ENCRE_2, size=12),
        hovertemplate="%{y}<br>" + metrique + " = %{x:.2f}<extra></extra>",
    ))
    if plancher is not None:
        fig.add_shape(type="line", x0=plancher, x1=plancher, y0=-0.5, y1=len(noms) - 0.5,
                      line=dict(color=ENCRE, width=1.5, dash="dash"))
        fig.add_annotation(x=plancher, y=len(noms) - 0.5, text=f"plancher théorique {plancher:.1f}",
                           showarrow=False, yanchor="bottom", xanchor="center",
                           font=dict(color=ENCRE, size=11))
    _base(fig, None, hauteur, y_titre="")
    fig.update_layout(hovermode="closest", bargap=0.35, showlegend=False)
    fig.update_xaxes(showgrid=True, gridcolor=GRILLE, title=dict(text=f"{metrique} (passages / jour) — plus bas = meilleur",
                                                                 font=dict(color=MUET, size=12)),
                     range=[0, max(vals) * 1.15], tickformat=",d")
    fig.update_yaxes(showgrid=False, tickfont=dict(color=ENCRE, size=12), title=None)
    return fig
