# 🏥 Prévision des Passages aux Urgences
### Hôpital Mohamed V — Meknès

> **Outil d'aide à la décision médicale** pour anticiper le nombre de passages aux urgences, basé sur des modèles de séries temporelles avancés.

---

## 📋 Table des matières

- [Présentation du projet](#-présentation-du-projet)
- [Démonstration](#-démonstration)
- [Modèles utilisés](#-modèles-utilisés)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Format des données](#-format-des-données)
- [Structure du projet](#-structure-du-projet)
- [Performances](#-performances-des-modèles)
- [Auteur](#-auteur)

---

## 🎯 Présentation du projet

Ce projet a été développé dans le cadre d'un **projet de fin d'études en séries temporelles (2024–2025)**. Il vise à prédire le nombre quotidien et mensuel de passages aux urgences de l'Hôpital Mohamed V de Meknès, afin d'aider les équipes médicales à :

- 📈 **Anticiper les pics d'affluence**
- 👨‍⚕️ **Optimiser la planification du personnel**
- 🏥 **Améliorer la prise en charge des patients**
- 📦 **Gérer les ressources matérielles** en conséquence

L'application est construite avec **Streamlit** et propose une interface intuitive en 2 pages : une page d'introduction analytique et une page de prédiction interactive.

---

## 🖥️ Démonstration

### Page Introduction
- Présentation du projet et des données
- Pipeline complet du traitement (5 étapes)
- Tableau comparatif des 6 modèles testés
- Graphique des performances (MAE)
- Résultats des tests statistiques de stationnarité

### Page Prédiction
- Choix entre prévision **mensuelle** ou **journalière**
- Chargement d'un fichier Excel personnel
- Sélection de la plage de prédiction via un slider
- Affichage des résultats avec intervalles de confiance à **95%**
- Courbe interactive historique + prévisions (Plotly)
- Export des résultats en Excel

---

## 🤖 Modèles utilisés

### 📅 Prévision Mensuelle — Prophet (Facebook/Meta)

[Prophet](https://facebook.github.io/prophet/) est un modèle statistique bayésien développé par Meta, idéal pour les séries temporelles avec tendances et saisonnalités.

**Configuration :**
```python
Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    interval_width=0.95,
    changepoint_prior_scale=0.3
)
```

### 📆 Prévision Journalière — MLP (Réseau de neurones)

Un **MLPRegressor** (scikit-learn) avec feature engineering temporel avancé :

| Feature | Description |
|---|---|
| `lag_1, lag_2, lag_3` | Valeurs des 1, 2, 3 jours précédents |
| `lag_7, lag_14` | Valeurs J-7 et J-14 (saisonnalité hebdo) |
| `roll_7, roll_14` | Moyenne glissante sur 7 et 14 jours |
| `dow_sin, dow_cos` | Encodage cyclique du jour de la semaine |
| `month_sin, month_cos` | Encodage cyclique du mois |
| `dayofyear, quarter` | Position dans l'année |

**Architecture :**
```
Couches : (128 → 64 → 32) neurones — Activation : ReLU
Optimisation : Adam — Learning rate : 0.001
Early stopping : activé (patience = 20 itérations)
```

---

## ⚙️ Installation

### Prérequis

- Python **3.9+**
- pip

### Étapes

**1. Cloner le dépôt**
```bash
git clone https://github.com/votre-repo/prediction-urgences.git
cd prediction-urgences
```

**2. Créer un environnement virtuel** *(recommandé)*
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

**3. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**4. Lancer l'application**
```bash
streamlit run streamlit_app.py
```

L'application s'ouvre automatiquement sur `http://localhost:8501`

### Fichier `requirements.txt`

```
streamlit>=1.30.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
prophet>=1.1.5
scikit-learn>=1.3.0
openpyxl>=3.1.0
```

---

## 📖 Utilisation

### Étape 1 — Choisir le type de prévision

Sur la page **Prédiction**, sélectionnez :
- `📅 Prévision MENSUELLE` → utilise Prophet
- `📆 Prévision JOURNALIÈRE` → utilise MLP

### Étape 2 — Charger votre fichier Excel

Téléchargez d'abord le fichier exemple pour voir le format attendu, puis chargez votre propre fichier.

### Étape 3 — Choisir la plage

Utilisez le slider pour sélectionner le nombre de mois (1–24) ou de jours (1–90) à prédire. **Seules les dates futures** sont autorisées.

### Étape 4 — Générer et exporter

Cliquez sur **"🔮 Générer les prévisions"** et obtenez :
- Les prévisions avec intervalles de confiance à 95%
- La fiabilité estimée en %
- La courbe interactive historique + prédictions
- Un fichier Excel exportable

---

## 📁 Format des données

### Prévision mensuelle

| Mois | Passages |
|---|---|
| 2024-01-01 | 7340 |
| 2024-02-01 | 6850 |
| 2024-03-01 | 7120 |
| ... | ... |

Formats de date acceptés : `2024-01-01`, `01/01/2024`, `Janvier 2024`, `Jan 2024`

### Prévision journalière

| Date | Passages |
|---|---|
| 2024-01-01 | 245 |
| 2024-01-02 | 231 |
| 2024-01-03 | 258 |
| ... | ... |

### Règles importantes

- ✅ Exactement **2 colonnes** : Date + Nombre de passages
- ✅ Minimum **6 lignes** de données valides
- ✅ Les en-têtes sont détectés et ignorés automatiquement
- ❌ Pas de cellules fusionnées
- ❌ Pas de colonnes supplémentaires
- ❌ Pas de lignes vides au milieu des données

---

## 🗂️ Structure du projet

```
prediction-urgences/
│
├── streamlit_app.py          # Application principale Streamlit
├── requirements.txt          # Dépendances Python
├── README.md                 # Ce fichier
│
├── data/
│   ├── exemple_journalier.xlsx   # Exemple données journalières (60 jours)
│   └── exemple_mensuel.xlsx      # Exemple données mensuelles (17 mois)
│
└── notebook/
    └── Issoug_ElMehdi_Projet_TimeSeries_Hopital_v2.ipynb  # Analyse complète
```

---

## 📊 Performances des modèles

Résultats obtenus sur les données de l'Hôpital Mohamed V :

| Rang | Modèle | Type | MAE Journalier | Remarque |
|---|---|---|---|---|
| 🥇 1er | **MLP** | Réseau de neurones | **≈ 7** | ⭐ Meilleur modèle |
| 🥈 2e | **Prophet** | Statistique bayésien | Excellent | Idéal pour le mensuel |
| 🥉 3e | **XGBoost** | Gradient Boosting | ≈ 22 | Rapide et robuste |
| 4e | **LightGBM** | Gradient Boosting | ≈ 47 | Très léger |
| 5e | **LSTM / GRU** | Deep Learning | ≈ 55–58 | Manque de données |
| 6e | **SARIMA+GARCH** | Statistique classique | ≈ 100 | Linéaire uniquement |

### Tests de stationnarité

| Test | Résultat | Conclusion |
|---|---|---|
| ADF (Augmented Dickey-Fuller) | p < 0.05 | ✅ Stationnaire après différenciation |
| KPSS | p > 0.05 | ✅ Stationnaire confirmé |
| Phillips-Perron | p < 0.05 | ✅ Cohérent avec ADF |

> La série est **non-stationnaire à l'origine** mais devient stationnaire après une différenciation d'ordre 1 (d=1). Une composante saisonnière hebdomadaire (S=7) a été détectée.

---

## 🐛 Problèmes connus et solutions

### `TypeError: Addition/subtraction of integers and integer-arrays with Timestamp`

**Cause :** `plotly.add_vline()` est incompatible avec `pandas >= 2.0` car il tente d'additionner des entiers à un `pd.Timestamp` en interne.

**Solution appliquée :** Remplacement par `fig.add_shape()` + `fig.add_annotation()` avec `str(date.date())`.

### `NDFrame.fillna() got an unexpected keyword argument 'method'`

**Cause :** L'argument `method=` a été supprimé dans `pandas >= 2.0`.

**Solution appliquée :** Remplacement par `.bfill().ffill()`.

---

## 👨‍💼 Auteur

**Issoug El Mehdi**
**Bado Ange Yipene Cenacle** 
Projet Séries Temporelles — 2024–2025
Hôpital Mohamed V, Meknès

---

> 🔒 *Usage interne uniquement — Hôpital Mohamed V, Meknès*