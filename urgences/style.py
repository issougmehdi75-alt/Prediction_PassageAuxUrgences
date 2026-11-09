"""CSS minimal : le thème global est dans .streamlit/config.toml."""

CSS = """
<style>
  .block-container { padding-top: 2.2rem; max-width: 1200px; }
  h1, h2, h3 { letter-spacing: -0.01em; }

  .hero {
    background: linear-gradient(120deg, #0d2847 0%, #1c5cab 100%);
    color: #ffffff; padding: 28px 34px; border-radius: 14px; margin-bottom: 22px;
  }
  .hero .eyebrow { font-size: .78rem; letter-spacing: .12em; text-transform: uppercase; opacity: .75; }
  .hero h1 { color: #ffffff; font-size: 2rem; font-weight: 750; margin: 6px 0 4px 0; padding: 0; }
  .hero p { margin: 0; opacity: .88; font-size: 1rem; }

  .carte {
    background: #ffffff; border: 1px solid #e1e0d9; border-radius: 12px;
    padding: 18px 22px; height: 100%; color: #0b0b0b;
  }
  .carte h4 { margin: 0 0 8px 0; font-size: 1rem; color: #0d2847; }
  .carte p, .carte li { color: #3d3c39; font-size: .93rem; line-height: 1.6; margin: 0; }

  .kpi { background: #ffffff; border: 1px solid #e1e0d9; border-radius: 12px; padding: 14px 18px; }
  .kpi .lbl { font-size: .8rem; color: #52514e; }
  .kpi .val { font-size: 1.7rem; font-weight: 700; color: #0b0b0b; line-height: 1.2; margin-top: 2px; }
  .kpi .sub { font-size: .78rem; color: #898781; margin-top: 2px; }

  .etape { background: #ffffff; border: 1px solid #e1e0d9; border-radius: 12px; padding: 16px; height: 100%; }
  .etape .num {
    display: inline-flex; width: 26px; height: 26px; border-radius: 50%; align-items: center;
    justify-content: center; background: #e8f0fb; color: #1c5cab; font-weight: 700; font-size: .85rem;
  }
  .etape .t { font-weight: 650; color: #0b0b0b; margin: 8px 0 4px 0; font-size: .92rem; }
  .etape .d { color: #52514e; font-size: .82rem; line-height: 1.5; }

  .note { border-left: 3px solid #2a78d6; background: #eef4fc; padding: 12px 16px;
          border-radius: 0 10px 10px 0; color: #0d2847; font-size: .92rem; margin: 6px 0 14px 0; }
  .note.alerte { border-left-color: #eda100; background: #fff7e6; color: #5c3d00; }

  .tag { display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: .75rem;
         font-weight: 600; margin-right: 6px; background: #e8f0fb; color: #1c5cab; }
  .tag.sim { background: #fff1e0; color: #8a4b00; }

  section[data-testid="stSidebar"] .sb-titre { font-size: 1.05rem; font-weight: 700; color: #ffffff; }
  section[data-testid="stSidebar"] .sb-sous { font-size: .82rem; color: #a9bdd6; }
  section[data-testid="stSidebar"] .sb-bloc { font-size: .85rem; line-height: 1.6; color: #d7e2ef; }
  section[data-testid="stSidebar"] .sb-bloc b { color: #ffffff; }
  .pied { text-align: center; color: #898781; font-size: .8rem; padding: 18px 0 4px 0; }
</style>
"""


def kpi(label: str, valeur: str, sous: str = "") -> str:
    return f'<div class="kpi"><div class="lbl">{label}</div><div class="val">{valeur}</div><div class="sub">{sous}</div></div>'


def nombre(x: float, dec: int = 0) -> str:
    """Format français : espace insécable pour les milliers, virgule décimale."""
    s = f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s
