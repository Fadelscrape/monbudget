import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
import os
from datetime import datetime, date

# ─────────────────────────────────────────────
# 1. CONFIG PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MonBudget 💜",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# 2. CSS CUSTOM — THÈME BLANC TECHNIQUE / FINTECH
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg:      #f4f6fb;
    --bg2:     #eef1f8;
    --surface: #ffffff;
    --surface2:#f0f2f9;
    --blue:    #2563eb;
    --indigo:  #4f46e5;
    --teal:    #0891b2;
    --green:   #059669;
    --amber:   #d97706;
    --red:     #dc2626;
    --text:    #0f172a;
    --muted:   #64748b;
    --border:  #e2e8f0;
    --border2: rgba(37,99,235,0.15);
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stApp"] {
    background: #f4f6fb !important;
    color: #0f172a !important;
    font-family: 'Outfit', sans-serif !important;
}

#MainMenu, footer { display: none !important; }
header { visibility: hidden !important; }
[data-testid="stDeployButton"] { display: none !important; }
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
header button,
header svg {
    visibility: visible !important;
    display: flex !important;
}

[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    box-shadow: 2px 0 12px rgba(0,0,0,0.04) !important;
}
[data-testid="stSidebar"] * { color: #0f172a !important; }

input, textarea, select,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
    font-family: 'Outfit', sans-serif !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,0.15) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #2563eb, #4f46e5) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(37,99,235,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.35) !important;
}

/* Bouton masquer actif */
.masque-actif .stButton > button {
    background: linear-gradient(135deg, #f59e0b, #d97706) !important;
    box-shadow: 0 4px 15px rgba(217,119,6,0.3) !important;
}

[data-testid="stTabs"] [role="tablist"] {
    background: #f0f2f9 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
}
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: #64748b !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #2563eb !important;
    color: #ffffff !important;
    border-bottom: none !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
}

.kpi-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 4px rgba(15,23,42,0.06);
    margin-bottom: 1rem;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2563eb, #4f46e5, #0891b2);
    border-radius: 20px 20px 0 0;
}
.kpi-label {
    font-size: 0.78rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.7rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.2;
}
.kpi-sub {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 0.3rem;
}

.prog-wrap { margin-bottom: 0.8rem; }
.prog-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.3rem;
    font-size: 0.85rem;
}
.prog-name { font-weight: 600; color: #0f172a; }
.prog-pct {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 20px;
}
.prog-bar-bg {
    background: #e2e8f0;
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
}
.prog-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    transition: width 0.6s ease;
}

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    border: 1px solid transparent;
}
.badge-purple { background: #ede9fe; color: #4338ca; border-color: #c4b5fd; }
.badge-green  { background: #d1fae5; color: #065f46; border-color: #6ee7b7; }
.badge-amber  { background: #fef3c7; color: #92400e; border-color: #fcd34d; }
.badge-red    { background: #fee2e2; color: #991b1b; border-color: #fca5a5; }

.expense-row {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.expense-row:hover {
    border-color: rgba(37,99,235,0.4);
    box-shadow: 0 2px 8px rgba(37,99,235,0.08);
}

.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin: 1rem 0 0.8rem;
    color: #0f172a;
}

.alert-over {
    background: #fee2e2; border: 1px solid #fca5a5;
    border-radius: 12px; padding: 0.8rem 1rem;
    color: #991b1b; font-size: 0.88rem; margin-bottom: 0.6rem;
}
.alert-warn {
    background: #fef3c7; border: 1px solid #fcd34d;
    border-radius: 12px; padding: 0.8rem 1rem;
    color: #92400e; font-size: 0.88rem; margin-bottom: 0.6rem;
}
.alert-ok {
    background: #d1fae5; border: 1px solid #6ee7b7;
    border-radius: 12px; padding: 0.8rem 1rem;
    color: #065f46; font-size: 0.88rem; margin-bottom: 0.6rem;
}

.logo-wrap { text-align: center; padding: 1.2rem 0 1rem; }
.logo-title { font-size: 1.5rem; font-weight: 900; color: #2563eb; }
.logo-sub { font-size: 0.75rem; color: #64748b; }

.tip-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 14px; padding: 1rem 1.2rem;
    margin-bottom: 0.8rem; position: relative;
    box-shadow: 0 1px 4px rgba(15,23,42,0.04);
}
.tip-card::before {
    content: ''; position: absolute;
    left: 0; top: 10%; bottom: 10%;
    width: 3px;
    background: linear-gradient(180deg, #2563eb, #4f46e5);
    border-radius: 999px;
}

.citation {
    text-align: center; font-style: italic;
    color: #64748b; font-size: 0.9rem;
    border-top: 1px solid #e2e8f0;
    padding-top: 1.5rem; margin-top: 2rem;
}

.js-plotly-plot .plotly { background: transparent !important; }
hr { border-color: #e2e8f0 !important; }

[data-testid="stCheckbox"] label { color: #0f172a !important; font-weight: 600 !important; }
[data-testid="stDateInput"] input { background: #ffffff !important; border: 1px solid #e2e8f0 !important; color: #0f172a !important; }
[data-testid="stNumberInput"] button { background: #f0f2f9 !important; border: none !important; color: #2563eb !important; }
[data-testid="stExpander"] { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 14px !important; }
[data-testid="stAlert"] { border-radius: 12px !important; }

@media (max-width: 768px) {
    .kpi-value { font-size: 1.3rem; }
    .kpi-card { padding: 1rem; }
}
@media (max-width: 640px) {
    [data-testid="column"] { width: 100% !important; min-width: 100% !important; flex: 1 1 100% !important; }
    .kpi-value { font-size: 1.1rem; }
    [data-testid="stTabs"] [role="tab"] { font-size: 0.72rem; padding: 0.3rem 0.4rem; }
    .prog-pct { font-size: 0.65rem; }
    .section-title { font-size: 1rem; }
}

/* ── Écran de connexion ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
.login-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    box-shadow: 0 8px 32px rgba(37,99,235,0.12), 0 2px 8px rgba(15,23,42,0.06);
    border: 1px solid #e2e8f0;
    animation: fadeIn 0.5s ease forwards;
    text-align: center;
}
.login-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0.5rem 0 0.3rem;
}
.login-sub {
    font-size: 0.88rem;
    color: #64748b;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}
.login-footer {
    text-align: center;
    font-size: 0.75rem;
    color: #94a3b8;
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid #f1f5f9;
}

/* ── Bouton déconnexion ── */
.btn-logout .stButton > button {
    background: rgba(239,68,68,0.1) !important;
    color: #ef4444 !important;
    border: 1px solid rgba(239,68,68,0.2) !important;
    box-shadow: none !important;
}
.btn-logout .stButton > button:hover {
    background: rgba(239,68,68,0.2) !important;
    transform: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. AUTHENTIFICATION
# ─────────────────────────────────────────────
try:
    MOT_DE_PASSE = st.secrets["auth"]["password"]
except Exception:
    MOT_DE_PASSE = "admin123"  # fallback local uniquement

if "authentifie" not in st.session_state:
    st.session_state.authentifie = False
if "tentatives" not in st.session_state:
    st.session_state.tentatives = 0


def afficher_ecran_connexion():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style="text-align:center;padding:2rem 0 1rem">
            <div style="font-size:2.8rem">💰</div>
            <div style="font-size:1.6rem;font-weight:900;color:#2563eb;line-height:1.1">MonBudget</div>
            <div style="font-size:0.8rem;color:#64748b;margin-top:0.3rem">Accès privé — Espace personnel</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="login-card">
            <div style="font-size:2.5rem;margin-bottom:0.5rem">🔒</div>
            <div class="login-title">Connexion requise</div>
            <div class="login-sub">
                Entrez votre mot de passe pour accéder<br>à votre espace financier personnel
            </div>
        </div>
        """, unsafe_allow_html=True)

        mdp_saisi = st.text_input(
            "Mot de passe",
            type="password",
            placeholder="••••••••",
            key="input_mdp",
            label_visibility="collapsed",
        )

        if st.button("🔓 Accéder à MonBudget", use_container_width=True, key="btn_login"):
            if mdp_saisi == MOT_DE_PASSE:
                st.session_state.authentifie = True
                st.session_state.tentatives  = 0
                st.rerun()
            else:
                st.session_state.tentatives += 1
                st.error("❌ Mot de passe incorrect. Réessayez.")
                if st.session_state.tentatives >= 3:
                    st.warning(
                        f"⚠️ {st.session_state.tentatives} tentative(s) échouée(s). "
                        "Vérifiez votre mot de passe."
                    )

        st.markdown(
            '<div class="login-footer">🔒 Vos données sont protégées et privées</div>',
            unsafe_allow_html=True,
        )


if not st.session_state.authentifie:
    afficher_ecran_connexion()
    st.stop()

# ─────────────────────────────────────────────
# 4. CONSTANTES
# ─────────────────────────────────────────────
DATA_FILE = "budget_data.json"

CATEGORIES = {
    "🏠 Loyer / Logement":   "#2563eb",
    "🍽️ Nourriture":         "#0891b2",
    "🚌 Transport":           "#059669",
    "💡 Factures & Charges": "#d97706",
    "🎓 Frais scolaires":    "#4f46e5",
    "💊 Santé":              "#dc2626",
    "🎉 Loisirs & Sorties":  "#7c3aed",
    "📦 Dépenses diverses":  "#64748b",
}

CITATIONS = [
    "\"Un budget, c'est dire à votre argent où aller, plutôt que de vous demander où il est passé.\" — Dave Ramsey",
    "\"Ne dépensez pas ce que vous n'avez pas encore gagné.\" — Sagesse populaire",
    "\"L'indépendance financière commence par un premier pas conscient.\" — T. Harv Eker",
    "\"Chaque franc économisé est un franc qui travaille pour vous.\" — Benjamin Franklin (adapté)",
    "\"Le secret de la richesse réside dans la discipline du quotidien.\" — Anonyme",
]

MOIS_FR = {
    1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril",
    5:"Mai", 6:"Juin", 7:"Juillet", 8:"Août",
    9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"
}

# ─────────────────────────────────────────────
# 4. HELPERS
# ─────────────────────────────────────────────
def next_month_key(key):
    yr, mo = map(int, key.split("-"))
    return f"{yr+1}-01" if mo == 12 else f"{yr}-{mo+1:02d}"

def empty_month():
    return {
        "revenus": [],
        "depenses": [],
        "epargne": {"transfere": False, "montant": 0},
        "dime_versements": [],
    }

def calc_enveloppes(revenu):
    return {
        "consommation": revenu * 0.70,
        "epargne":      revenu * 0.20,
        "dime":         revenu * 0.10,
    }

def total_par_categorie(depenses):
    totaux = {cat: 0.0 for cat in CATEGORIES}
    for d in depenses:
        cat = d.get("categorie", "")
        if cat in totaux:
            totaux[cat] += d.get("montant", 0.0)
    return totaux

def budget_cat_default(cat, enveloppe_conso):
    poids = {
        "🏠 Loyer / Logement":   0.35,
        "🍽️ Nourriture":         0.25,
        "🚌 Transport":           0.12,
        "💡 Factures & Charges": 0.10,
        "🎓 Frais scolaires":    0.08,
        "💊 Santé":              0.04,
        "🎉 Loisirs & Sorties":  0.04,
        "📦 Dépenses diverses":  0.02,
    }
    return enveloppe_conso * poids.get(cat, 0.05)

def fmt(valeur, decimales=0):
    if st.session_state.get("masquer", False):
        return "••••••"
    if decimales == 2:
        return f"{valeur:,.2f}"
    return f"{valeur:,.0f}"

# ─────────────────────────────────────────────
# 5. PERSISTANCE JSON + MIGRATION
# ─────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    migrated = False
    now = datetime.now()
    mois_key_now = f"{now.year}-{now.month:02d}"

    # ── Détection ancien format (pas de clé "historique") ──
    if "historique" not in data:
        migrated = True
        historique = {}

        old_revenus  = data.get("revenus", {})
        old_depenses = data.get("depenses", [])
        old_epargne  = data.get("epargne", {})
        old_dime     = data.get("dime", {})

        # Collecter tous les mois mentionnés
        all_months = set(old_revenus.keys())
        for d in old_depenses:
            m = d.get("mois")
            if m:
                all_months.add(m)
        all_months.add(mois_key_now)
        all_months.discard(None)

        for m in sorted(all_months):
            rev_amt = old_revenus.get(m, 0)
            rev_list = []
            if rev_amt > 0:
                rev_list = [{"montant": rev_amt, "source": "Revenu migré", "date": str(date.today())}]

            deps = [{k: v for k, v in d.items() if k != "mois"}
                    for d in old_depenses if d.get("mois") == m]

            ep = old_epargne.get(m, {})
            dm = old_dime.get(m, {})

            historique[m] = {
                "revenus":  rev_list,
                "depenses": deps,
                "epargne":  {"transfere": ep.get("transfere", False), "montant": ep.get("montant", 0)},
                "dime":     {"payee": dm.get("payee", False), "montant": dm.get("montant", 0)},
            }

        data = {
            "mois_actuel":    mois_key_now,
            "historique":     historique,
            "prets":          [],
            "objectif_epargne": data.get("objectif_epargne", 0),
        }

    # ── Valeurs par défaut ──
    data.setdefault("mois_actuel", mois_key_now)
    data.setdefault("historique", {})
    data.setdefault("prets", [])
    data.setdefault("objectif_epargne", 0)
    data.setdefault("dettes", [])

    # ── Migration dîme → versements ──
    for mois_k, mois_d in data["historique"].items():
        if "dime_versements" not in mois_d:
            dime_old = mois_d.get("dime", {})
            if dime_old.get("payee") and dime_old.get("montant", 0) > 0:
                mois_d["dime_versements"] = [{"montant": float(dime_old["montant"]), "date": mois_k + "-01", "note": "Migré"}]
            else:
                mois_d["dime_versements"] = []

    # Garantir que le mois actuel existe
    if data["mois_actuel"] not in data["historique"]:
        data["historique"][data["mois_actuel"]] = empty_month()

    return data, migrated

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─────────────────────────────────────────────
# 6. SESSION STATE
# ─────────────────────────────────────────────
if "data" not in st.session_state:
    loaded, was_migrated = load_data()
    st.session_state.data     = loaded
    st.session_state.migrated = was_migrated
else:
    was_migrated = False

if "masquer" not in st.session_state:
    st.session_state.masquer = False
if "confirm_nouveau_mois" not in st.session_state:
    st.session_state.confirm_nouveau_mois = False

data    = st.session_state.data
masquer = st.session_state.masquer

# ─────────────────────────────────────────────
# 7. MOIS ACTUEL ET VUE
# ─────────────────────────────────────────────
now         = datetime.now()
mois_actuel = data["mois_actuel"]
yr_act, mo_act = map(int, mois_actuel.split("-"))
mois_label_actuel = f"{MOIS_FR[mo_act]} {yr_act}"

mois_options = sorted(data["historique"].keys(), reverse=True)
if not mois_options:
    mois_options = [mois_actuel]

# Lecture du mois consulté (piloté par le selectbox via session_state)
mois_vue = st.session_state.get("mois_selectbox", mois_actuel)
if mois_vue not in mois_options:
    mois_vue = mois_actuel

est_archive = (mois_vue != mois_actuel)
yr_vue, mo_vue = map(int, mois_vue.split("-"))
mois_label_vue = f"{MOIS_FR[mo_vue]} {yr_vue}"

# Garantir que le mois consulté existe
if mois_vue not in data["historique"]:
    data["historique"][mois_vue] = empty_month()

mois_data = data["historique"][mois_vue]

# ─────────────────────────────────────────────
# 8. CALCULS PRINCIPAUX
# ─────────────────────────────────────────────
revenu_total  = sum(r["montant"] for r in mois_data.get("revenus", []))
enveloppes    = calc_enveloppes(revenu_total)
depenses_mois = mois_data.get("depenses", [])
totaux_cat    = total_par_categorie(depenses_mois)
total_depense = sum(totaux_cat.values())
reste         = enveloppes["consommation"] - total_depense

# Prêts (globaux)
prets            = data.get("prets", [])
prets_en_cours   = [p for p in prets if not p.get("rembourse")]
prets_rembourses = [p for p in prets if p.get("rembourse")]
total_prets_en_cours   = sum(p["montant"] for p in prets_en_cours)
total_prets_recuperes  = sum(p["montant"] for p in prets_rembourses)

today = date.today()

# Dettes (globales)
dettes = data.get("dettes", [])
for d in dettes:
    rem = sum(v["montant"] for v in d.get("versements", []))
    d["_rembourse"]   = rem
    d["_restant"]     = d["montant_total"] - rem
    d["_progression"] = (rem / d["montant_total"] * 100) if d["montant_total"] > 0 else 0
    d["_soldee"]      = d["_restant"] <= 0

dettes_en_cours      = [d for d in dettes if not d["_soldee"]]
dettes_soldees       = [d for d in dettes if d["_soldee"]]
total_dettes_restant = sum(d["_restant"] for d in dettes_en_cours)
total_dettes_rem     = sum(d["_rembourse"] for d in dettes_en_cours)

prochaine_echeance_dette = None
for _d in dettes_en_cours:
    try:
        _ech = date.fromisoformat(_d["date_echeance"])
        if prochaine_echeance_dette is None or _ech < prochaine_echeance_dette:
            prochaine_echeance_dette = _ech
    except (ValueError, KeyError):
        pass

# Dîme versements
dime_versements = mois_data.get("dime_versements", [])
dime_objectif   = enveloppes["dime"]
dime_paye_total = sum(v["montant"] for v in dime_versements)
dime_restante   = max(0, dime_objectif - dime_paye_total)
dime_complete   = dime_paye_total >= dime_objectif and dime_objectif > 0
dime_prog_pct   = min(100, (dime_paye_total / dime_objectif * 100)) if dime_objectif > 0 else 0

# ═══════════════════════════════════════════════
# 9. SIDEBAR
# ═══════════════════════════════════════════════
with st.sidebar:

    # ── Logo ──
    st.markdown("""
    <div class="logo-wrap">
        <div style="font-size:2.5rem">💰</div>
        <div class="logo-title">MonBudget</div>
        <div class="logo-sub">Règle 70 / 20 / 10</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Bouton Masquer / Révéler ──
    if masquer:
        st.markdown('<div class="masque-actif">', unsafe_allow_html=True)

    btn_label = "👁️ Révéler les montants" if masquer else "🙈 Masquer les montants"
    if st.button(btn_label, use_container_width=True, key="btn_masquer"):
        st.session_state.masquer = not masquer
        st.rerun()

    if masquer:
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Navigation mensuelle ──
    st.markdown("<div class='section-title'>📅 Navigation mensuelle</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#2563eb,#4f46e5);border-radius:12px;padding:0.7rem 1rem;
                margin-bottom:0.6rem;text-align:center">
        <div style="color:rgba(255,255,255,0.7);font-size:0.7rem;font-weight:600;letter-spacing:0.06em">MOIS ACTUEL</div>
        <div style="color:white;font-size:1.1rem;font-weight:700">{mois_label_actuel}</div>
    </div>
    """, unsafe_allow_html=True)

    def _fmt_mois(k):
        yr, mo = map(int, k.split("-"))
        lbl = f"{MOIS_FR[mo]} {yr}"
        return f"📍 {lbl} (actuel)" if k == mois_actuel else f"📂 {lbl}"

    st.selectbox(
        "Consulter un mois",
        options=mois_options,
        format_func=_fmt_mois,
        key="mois_selectbox",
        label_visibility="collapsed",
    )

    if est_archive:
        st.markdown(f"""
        <div style="background:#fef3c7;border:1px solid #fcd34d;border-radius:8px;padding:0.4rem 0.8rem;
                    text-align:center;font-size:0.8rem;color:#92400e;font-weight:600;margin-bottom:0.4rem">
            📂 Archivé — {mois_label_vue}
        </div>
        """, unsafe_allow_html=True)

    # ── Nouveau mois (uniquement si on est sur le mois actuel) ──
    if not est_archive:
        if not st.session_state.confirm_nouveau_mois:
            if st.button("➡️ Nouveau mois", use_container_width=True):
                st.session_state.confirm_nouveau_mois = True
                st.rerun()
        else:
            next_k = next_month_key(mois_actuel)
            next_yr, next_mo = map(int, next_k.split("-"))
            st.warning(f"⚠️ Créer {MOIS_FR[next_mo]} {next_yr} ?")
            cy, cn = st.columns(2)
            with cy:
                if st.button("✅ Oui", key="confirm_oui"):
                    if next_k not in data["historique"]:
                        data["historique"][next_k] = empty_month()
                    data["mois_actuel"] = next_k
                    save_data(data)
                    st.session_state.data = data
                    st.session_state.confirm_nouveau_mois = False
                    st.session_state.mois_selectbox = next_k
                    st.rerun()
            with cn:
                if st.button("❌ Non", key="confirm_non"):
                    st.session_state.confirm_nouveau_mois = False
                    st.rerun()

    st.markdown("---")

    # ── Revenus multiples ──
    st.markdown("<div class='section-title'>💰 Mes revenus du mois</div>", unsafe_allow_html=True)

    if not est_archive:
        new_mont   = st.number_input("Montant", min_value=0.0, step=500.0, format="%.0f",
                                     key="new_revenu_montant", label_visibility="collapsed")
        new_source = st.text_input("Source", placeholder="Salaire, Freelance, Vente...",
                                   key="new_revenu_source", label_visibility="collapsed")
        new_date   = st.date_input("Date reçu", value=date.today(),
                                   key="new_revenu_date", label_visibility="collapsed")

        if st.button("➕ Ajouter ce revenu", use_container_width=True):
            if new_mont > 0:
                mois_data["revenus"].append({
                    "montant": float(new_mont),
                    "source":  new_source.strip() or "Revenu",
                    "date":    str(new_date),
                })
                save_data(data)
                total_apres = sum(r["montant"] for r in mois_data["revenus"])
                st.success(f"✅ Revenu ajouté ! Total : {fmt(total_apres)}")
                for k in ["new_revenu_montant", "new_revenu_source", "new_revenu_date"]:
                    st.session_state.pop(k, None)
                st.rerun()
            else:
                st.error("⚠️ Le montant doit être supérieur à 0.")

    # Liste des revenus
    revenus_liste = mois_data.get("revenus", [])

    if revenus_liste:
        st.markdown(f"""
        <div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:12px;
                    padding:0.7rem 1rem;margin-bottom:0.5rem">
            <div style="font-size:0.72rem;color:#0891b2;font-weight:600;margin-bottom:0.2rem">
                💼 TOTAL REVENUS
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:1.3rem;font-weight:700;color:#0369a1">
                {fmt(revenu_total)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        for i, rev in enumerate(list(revenus_liste)):
            rc1, rc2 = st.columns([5, 1])
            with rc1:
                st.markdown(f"""
                <div style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;
                            padding:0.35rem 0.7rem;font-size:0.78rem;margin-bottom:0.2rem">
                    <span style="color:#64748b">{rev.get('date','?')}</span> ·
                    <span style="font-weight:600">{rev.get('source','Revenu')}</span> ·
                    <span style="color:#2563eb;font-family:'Space Mono',monospace">{fmt(rev.get('montant',0))}</span>
                </div>
                """, unsafe_allow_html=True)
            with rc2:
                if not est_archive:
                    if st.button("🗑️", key=f"del_rev_{i}", help="Supprimer ce revenu"):
                        mois_data["revenus"].pop(i)
                        save_data(data)
                        st.warning("🗑️ Revenu supprimé")
                        st.rerun()
    else:
        st.info("➕ Ajoute ton premier revenu du mois !")

    st.markdown("---")

    # ── Répartition 70/20/10 ──
    st.markdown("<div class='section-title'>📊 Répartition automatique</div>", unsafe_allow_html=True)

    for lbl, pct, val, color, icon in [
        ("Consommation", "70%", enveloppes["consommation"], "#2563eb", "🛒"),
        ("Épargne",      "20%", enveloppes["epargne"],      "#059669", "🏦"),
        ("Dîme",         "10%", enveloppes["dime"],         "#d97706", "🙏"),
    ]:
        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:0.7rem 1rem;
                    margin-bottom:0.5rem;border-left:3px solid {color};box-shadow:0 1px 3px rgba(15,23,42,0.04)">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <span style="font-size:0.85rem;color:#64748b">
                    {icon} {lbl} <span style="color:{color};font-weight:700">{pct}</span>
                </span>
                <span style="font-family:'Space Mono',monospace;font-size:0.9rem;color:{color};font-weight:700">
                    {fmt(val)}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Alerte prêts en cours ──
    if total_prets_en_cours > 0:
        st.markdown(f"""
        <div style="background:#fef3c7;border:1px solid #fcd34d;border-radius:10px;
                    padding:0.5rem 0.8rem;font-size:0.82rem;color:#92400e;margin-top:0.5rem">
            ⚠️ Prêts en cours : <strong>{fmt(total_prets_en_cours)}</strong>
        </div>
        """, unsafe_allow_html=True)

    if total_dettes_restant > 0:
        st.markdown(f"""
        <div style="background:#fee2e2;border:1px solid #fca5a5;border-radius:10px;
                    padding:0.5rem 0.8rem;font-size:0.82rem;color:#991b1b;margin-top:0.4rem">
            💳 Dettes restantes : <strong>{fmt(total_dettes_restant)}</strong>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem;color:#64748b;text-align:center'>Budget sauvegardé localement 🔒</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown('<div class="btn-logout">', unsafe_allow_html=True)
    if st.button("🚪 Se déconnecter", use_container_width=True, key="btn_logout"):
        st.session_state.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Notice migration ──
if st.session_state.get("migrated"):
    st.info("✅ Données migrées vers le nouveau format mensuel avec historique !")
    st.session_state.migrated = False

# ═══════════════════════════════════════════════
# 10. TABS PRINCIPALES
# ═══════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Dashboard", "💸 Dépenses", "🏦 Épargne", "🙏 Dîme", "💸 Prêts", "💳 Dettes", "💡 Conseils"
])

# ═══════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ═══════════════════════════════════════════════
with tab1:
    statut_masque = "🔒 Montants masqués" if masquer else "🔓 Montants visibles"
    h_col1, h_col2 = st.columns([7, 2])
    with h_col1:
        st.markdown(f"""
        <div style="font-size:1.6rem;font-weight:900;color:#0f172a;padding-top:0.3rem">
            Tableau de bord — <span style="color:#2563eb">{mois_label_vue}</span> 🚀
        </div>
        """, unsafe_allow_html=True)
    with h_col2:
        btn_label_main = "👁️ Révéler" if masquer else "🙈 Masquer"
        if st.button(btn_label_main, use_container_width=True, key="btn_masquer_main"):
            st.session_state.masquer = not masquer
            st.rerun()

    if est_archive:
        st.markdown(f"""
        <div style="background:#fef3c7;border:1px solid #fcd34d;border-radius:12px;padding:0.7rem 1rem;
                    margin-bottom:1rem;color:#92400e;font-weight:600;font-size:0.9rem">
            📂 Consultation archivée — données de {mois_label_vue}
        </div>
        """, unsafe_allow_html=True)

    # ── Alertes prêts en retard ──
    for p in prets_en_cours:
        try:
            echeance = date.fromisoformat(p["date_echeance"])
            if echeance < today:
                jours_retard = (today - echeance).days
                st.error(
                    f"🚨 **{p['emprunteur']}** devait rembourser {fmt(p['montant'])} "
                    f"le {p['date_echeance']} — en retard de **{jours_retard} jour(s)** !"
                )
        except (ValueError, KeyError):
            pass

    # ── KPI Cards ──
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">💵 Revenu total</div>
            <div class="kpi-value">{fmt(revenu_total)}</div>
            <div class="kpi-sub">Revenu net du mois</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">💸 Total dépensé</div>
            <div class="kpi-value" style="color:#dc2626">{fmt(total_depense)}</div>
            <div class="kpi-sub">Sur {fmt(enveloppes['consommation'])} alloués</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        reste_color = "#059669" if reste >= 0 else "#dc2626"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">✅ Reste disponible</div>
            <div class="kpi-value" style="color:{reste_color}">{fmt(reste)}</div>
            <div class="kpi-sub">{'Budget respecté 🎉' if reste >= 0 else '⚠️ Dépassement !'}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        nb_dep = len(depenses_mois)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📋 Transactions</div>
            <div class="kpi-value" style="color:#0891b2">{nb_dep}</div>
            <div class="kpi-sub">Dépenses ce mois</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📅 Mois</div>
            <div class="kpi-value" style="font-size:1rem;color:#4f46e5;line-height:1.4">{mois_label_vue}</div>
            <div class="kpi-sub">{'Actuel' if not est_archive else '📂 Archivé'}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Graphiques ──
    gc1, gc2 = st.columns(2)

    with gc1:
        st.markdown("<div class='section-title'>🥧 Répartition 70/20/10</div>", unsafe_allow_html=True)
        pie_vals   = [enveloppes["consommation"] or 70, enveloppes["epargne"] or 20, enveloppes["dime"] or 10]
        pie_annot  = "<b>••••••</b>" if masquer else f"<b>{revenu_total:,.0f}</b>"
        pie_text   = "label+percent"

        fig_pie = go.Figure(data=[go.Pie(
            labels=["🛒 Consommation (70%)", "🏦 Épargne (20%)", "🙏 Dîme (10%)"],
            values=pie_vals,
            hole=0.5,
            marker_colors=["#2563eb", "#059669", "#d97706"],
            textinfo=pie_text,
            textfont=dict(family="Outfit", size=11, color="#0f172a"),
        )])
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#0f172a", family="Outfit"),
            showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=280,
            annotations=[dict(
                text=pie_annot, x=0.5, y=0.5,
                font=dict(size=14, color="#2563eb", family="Space Mono"),
                showarrow=False,
            )],
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    with gc2:
        st.markdown("<div class='section-title'>📊 Dépenses par catégorie</div>", unsafe_allow_html=True)
        cats_with_dep = {k: v for k, v in totaux_cat.items() if v > 0}
        if cats_with_dep:
            bar_text = ["••••••" if masquer else f"{v:,.0f}" for v in cats_with_dep.values()]
            fig_bar = go.Figure(data=[go.Bar(
                x=list(cats_with_dep.values()),
                y=list(cats_with_dep.keys()),
                orientation="h",
                marker=dict(color=[CATEGORIES[c] for c in cats_with_dep], line=dict(width=0)),
                text=bar_text,
                textposition="outside",
                textfont=dict(family="Space Mono", size=10, color="#0f172a"),
            )])
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#0f172a", family="Outfit"),
                xaxis=dict(showgrid=True, gridcolor="rgba(226,232,240,0.8)", zeroline=False,
                           color="#64748b", showticklabels=not masquer),
                yaxis=dict(showgrid=False, color="#64748b"),
                margin=dict(t=20, b=20, l=20, r=80), height=280,
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown(
                "<div style='color:#64748b;text-align:center;padding:3rem'>Aucune dépense enregistrée</div>",
                unsafe_allow_html=True,
            )

    # ── Progression budgétaire ──
    st.markdown("<div class='section-title'>📈 Progression budgétaire</div>", unsafe_allow_html=True)

    alertes = []
    for cat, depense in totaux_cat.items():
        budget_c = budget_cat_default(cat, enveloppes["consommation"])
        if budget_c > 0:
            pct_use = (depense / budget_c) * 100
            if pct_use > 100:
                alertes.append(f"🔴 **{cat}** dépasse son budget ({pct_use:.0f}% utilisé)")
            elif pct_use > 85:
                alertes.append(f"🟡 **{cat}** proche du plafond ({pct_use:.0f}% utilisé)")

    for a in alertes:
        if "🔴" in a:
            st.markdown(f"<div class='alert-over'>{a}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-warn'>{a}</div>", unsafe_allow_html=True)

    pb_cols = st.columns(2)
    for i, (cat, color) in enumerate(CATEGORIES.items()):
        depense  = totaux_cat.get(cat, 0)
        budget_c = budget_cat_default(cat, enveloppes["consommation"])
        pct_display = (depense / budget_c * 100) if budget_c > 0 else 0
        pct_bar     = min(pct_display, 100)
        bar_color   = "#dc2626" if pct_display > 100 else ("#d97706" if pct_display > 80 else color)
        badge_bg    = "#fee2e2" if pct_display > 100 else ("#fef3c7" if pct_display > 80 else "#f0f2f9")
        badge_color = "#991b1b" if pct_display > 100 else ("#92400e" if pct_display > 80 else "#64748b")
        dep_txt     = fmt(depense)
        bud_txt     = fmt(budget_c)

        with pb_cols[i % 2]:
            st.markdown(f"""
            <div class="prog-wrap">
                <div class="prog-header">
                    <span class="prog-name">{cat}</span>
                    <span class="prog-pct" style="background:{badge_bg};color:{badge_color}">
                        {dep_txt} / {bud_txt}
                    </span>
                </div>
                <div class="prog-bar-bg">
                    <div class="prog-bar-fill" style="width:{pct_bar:.1f}%;background:{bar_color}"></div>
                </div>
                <div style="font-size:0.7rem;color:#64748b;margin-top:0.2rem">{pct_display:.1f}% utilisé</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Évolution des dépenses ──
    st.markdown("<div class='section-title'>📉 Évolution des dépenses du mois</div>", unsafe_allow_html=True)

    if depenses_mois:
        df_dep   = pd.DataFrame(depenses_mois)
        df_dep["date"] = pd.to_datetime(df_dep["date"])
        df_daily = df_dep.groupby("date")["montant"].sum().reset_index().sort_values("date")
        df_daily["cumul"] = df_daily["montant"].cumsum()

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_daily["date"], y=df_daily["cumul"],
            mode="lines+markers",
            line=dict(color="#2563eb", width=3, shape="spline"),
            marker=dict(size=7, color="#4f46e5", line=dict(width=2, color="#2563eb")),
            fill="tozeroy", fillcolor="rgba(37,99,235,0.08)",
            name="Cumul dépenses",
        ))
        fig_line.add_hline(
            y=enveloppes["consommation"], line_dash="dash",
            line_color="#dc2626", line_width=1.5,
            annotation_text="" if masquer else "Budget max",
            annotation_font_color="#dc2626",
        )
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#0f172a", family="Outfit"),
            xaxis=dict(showgrid=True, gridcolor="rgba(226,232,240,0.8)", color="#64748b"),
            yaxis=dict(showgrid=True, gridcolor="rgba(226,232,240,0.8)", color="#64748b",
                       showticklabels=not masquer),
            margin=dict(t=20, b=20, l=20, r=20), height=250, showlegend=False,
        )
        st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown(
            "<div style='color:#64748b;text-align:center;padding:2rem'>Aucune dépense pour construire le graphique</div>",
            unsafe_allow_html=True,
        )

    # ── Historique mensuel ──
    st.markdown("<div class='section-title'>📊 Historique mensuel (6 derniers mois)</div>", unsafe_allow_html=True)

    hist_keys = sorted(data["historique"].keys())[-6:]
    if len(hist_keys) > 1:
        hist_labels  = [f"{MOIS_FR[int(k.split('-')[1])]} {k.split('-')[0]}" for k in hist_keys]
        hist_revenus = [sum(r["montant"] for r in data["historique"][k].get("revenus", [])) for k in hist_keys]
        hist_dep     = [sum(d["montant"] for d in data["historique"][k].get("depenses", [])) for k in hist_keys]

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Bar(name="Revenus",  x=hist_labels, y=hist_revenus, marker_color="#2563eb"))
        fig_hist.add_trace(go.Bar(name="Dépenses", x=hist_labels, y=hist_dep,    marker_color="#dc2626"))
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#0f172a", family="Outfit"),
            xaxis=dict(color="#64748b"),
            yaxis=dict(color="#64748b", showticklabels=not masquer),
            barmode="group",
            margin=dict(t=20, b=20, l=20, r=20), height=250,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown(
            "<div style='color:#64748b;text-align:center;padding:2rem'>Pas encore assez de données pour l'historique</div>",
            unsafe_allow_html=True,
        )

# ═══════════════════════════════════════════════
# TAB 2 — DÉPENSES
# ═══════════════════════════════════════════════
with tab2:
    st.markdown(
        f"<div style='font-size:1.6rem;font-weight:900;margin-bottom:1rem;color:#0f172a'>"
        f"💸 Gestion des <span style='color:#2563eb'>Dépenses</span> — {mois_label_vue}</div>",
        unsafe_allow_html=True,
    )

    if est_archive:
        st.markdown("""
        <div style="background:#fef3c7;border:1px solid #fcd34d;border-radius:12px;padding:0.7rem 1rem;
                    margin-bottom:1rem;color:#92400e;font-weight:600;font-size:0.9rem">
            📂 Mode lecture — mois archivé. Modifications désactivées.
        </div>
        """, unsafe_allow_html=True)

    # ── Formulaire ajout (mois actuel uniquement) ──
    if not est_archive:
        if st.session_state.pop("reset_dep_form", False):
            st.session_state["dep_mont"] = 0.0
            st.session_state["dep_desc"] = ""
            st.session_state["dep_cat"]  = list(CATEGORIES.keys())[0]
            st.session_state["dep_date"] = date.today()
        with st.expander("➕ Ajouter une dépense", expanded=True):
            fa, fb = st.columns(2)
            with fa:
                dep_montant = st.number_input("💰 Montant", min_value=0.0, step=100.0, format="%.2f", key="dep_mont")
                dep_cat     = st.selectbox("🏷️ Catégorie", list(CATEGORIES.keys()), key="dep_cat")
            with fb:
                dep_desc = st.text_input("📝 Description", placeholder="Ex: Courses Carrefour", key="dep_desc")
                dep_date = st.date_input("📅 Date", key="dep_date")

            if st.button("➕ Ajouter la dépense", use_container_width=True):
                if dep_montant > 0:
                    mois_data["depenses"].append({
                        "id":          int(datetime.now().timestamp() * 1000),
                        "montant":     dep_montant,
                        "categorie":   dep_cat,
                        "description": dep_desc or "—",
                        "date":        str(dep_date),
                    })
                    save_data(data)
                    st.success(f"✅ Dépense de **{dep_montant:,.2f}** ajoutée !")
                    st.session_state["reset_dep_form"] = True
                    st.rerun()
                else:
                    st.error("⚠️ Le montant doit être supérieur à 0.")

    # ── Filtre catégorie ──
    st.markdown("<div class='section-title'>🔍 Filtre</div>", unsafe_allow_html=True)
    filtre_cat = st.selectbox("Catégorie", ["Toutes"] + list(CATEGORIES.keys()), key="f_cat")

    dep_filtrées = [
        d for d in mois_data.get("depenses", [])
        if filtre_cat == "Toutes" or d.get("categorie") == filtre_cat
    ]
    dep_filtrées.sort(key=lambda x: x.get("date", ""), reverse=True)

    total_filtre = sum(d["montant"] for d in dep_filtrées)
    st.markdown(
        f"<div style='font-size:0.85rem;color:#64748b;margin-bottom:0.8rem'>"
        f"{len(dep_filtrées)} transaction(s) — Total : "
        f"<b style='color:#2563eb'>{fmt(total_filtre)}</b></div>",
        unsafe_allow_html=True,
    )

    if dep_filtrées:
        for dep in dep_filtrées:
            cat     = dep.get("categorie", "📦 Dépenses diverses")
            col_cat = CATEGORIES.get(cat, "#64748b")
            dc1, dc2 = st.columns([6, 1])
            with dc1:
                st.markdown(f"""
                <div class="expense-row">
                    <span style="font-size:1.1rem">{cat.split()[0]}</span>
                    <div style="flex:1">
                        <div style="font-weight:600;font-size:0.9rem;color:#0f172a">{dep.get('description','—')}</div>
                        <div style="font-size:0.75rem;color:#64748b">
                            {dep.get('date','?')} · {cat[2:].strip() if ' ' in cat else cat}
                        </div>
                    </div>
                    <div style="font-family:'Space Mono',monospace;font-weight:700;
                                color:{col_cat};font-size:0.95rem;white-space:nowrap">
                        {fmt(dep.get('montant',0))}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with dc2:
                if not est_archive:
                    if st.button("🗑️", key=f"del_{dep['id']}", help="Supprimer"):
                        mois_data["depenses"] = [d for d in mois_data["depenses"] if d.get("id") != dep["id"]]
                        save_data(data)
                        st.rerun()
    else:
        st.markdown(
            "<div style='color:#64748b;text-align:center;padding:3rem'>Aucune dépense pour ce filtre 🌙</div>",
            unsafe_allow_html=True,
        )

# ═══════════════════════════════════════════════
# TAB 3 — ÉPARGNE
# ═══════════════════════════════════════════════
with tab3:
    st.markdown(
        "<div style='font-size:1.6rem;font-weight:900;margin-bottom:1rem;color:#0f172a'>"
        "🏦 Gestion de l'<span style='color:#059669'>Épargne</span></div>",
        unsafe_allow_html=True,
    )

    ep_data  = mois_data.get("epargne", {"transfere": False, "montant": 0})
    objectif = data.get("objectif_epargne", 0)
    cumul_ep = sum(
        data["historique"][k].get("epargne", {}).get("montant", 0)
        for k in data["historique"]
        if data["historique"][k].get("epargne", {}).get("transfere")
    )

    e1, e2 = st.columns(2)
    with e1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">💰 À épargner ce mois</div>
            <div class="kpi-value" style="color:#059669">{fmt(enveloppes['epargne'])}</div>
            <div class="kpi-sub">20% de {fmt(revenu_total)}</div>
        </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">🎯 Objectif total</div>
            <div class="kpi-value" style="color:#0891b2">{fmt(objectif)}</div>
            <div class="kpi-sub">Cumulé : {fmt(cumul_ep)}</div>
        </div>
        """, unsafe_allow_html=True)

    # Objectif personnalisable
    st.markdown("<div class='section-title'>🎯 Objectif d'épargne</div>", unsafe_allow_html=True)
    new_obj = st.number_input("Objectif total d'épargne", min_value=0.0, value=float(objectif), step=5000.0, format="%.2f")
    if st.button("💾 Mettre à jour l'objectif", key="save_obj"):
        data["objectif_epargne"] = new_obj
        save_data(data)
        st.success("✅ Objectif mis à jour !")
        st.rerun()

    if objectif > 0:
        pct_obj = min((cumul_ep / objectif) * 100, 100)
        st.markdown(f"""
        <div class="prog-wrap" style="margin-top:1rem">
            <div class="prog-header">
                <span class="prog-name">🏦 Progression vers l'objectif</span>
                <span class="prog-pct" style="background:#d1fae5;color:#065f46">{pct_obj:.1f}%</span>
            </div>
            <div class="prog-bar-bg" style="height:14px">
                <div class="prog-bar-fill" style="width:{pct_obj:.1f}%;background:linear-gradient(90deg,#059669,#0891b2)"></div>
            </div>
            <div style="font-size:0.78rem;color:#64748b;margin-top:0.3rem">{fmt(cumul_ep)} / {fmt(objectif)}</div>
        </div>
        """, unsafe_allow_html=True)

    # Statut du mois
    st.markdown("<div class='section-title'>✅ Statut du mois</div>", unsafe_allow_html=True)
    if not est_archive:
        transfere = st.checkbox(
            f"💸 Épargne transférée ce mois ({mois_label_vue}) ✅",
            value=ep_data.get("transfere", False),
            key="ep_check",
        )
        if transfere != ep_data.get("transfere", False):
            ep_data["transfere"] = transfere
            ep_data["montant"]   = enveloppes["epargne"]
            mois_data["epargne"] = ep_data
            save_data(data)
            if transfere:
                st.success(f"🎉 Épargne de {fmt(enveloppes['epargne'])} marquée comme transférée !")
            else:
                st.info("Épargne marquée comme non transférée.")
            st.rerun()
    else:
        statut_ep = "✅ Transférée" if ep_data.get("transfere") else "⏳ En attente"
        c_ep      = "#059669" if ep_data.get("transfere") else "#d97706"
        st.markdown(f"<span style='color:{c_ep};font-weight:600'>{statut_ep}</span>", unsafe_allow_html=True)

    # Historique
    st.markdown("<div class='section-title'>📋 Historique des épargnes</div>", unsafe_allow_html=True)
    for mois_k in sorted(data["historique"].keys(), reverse=True):
        ep  = data["historique"][mois_k].get("epargne", {})
        yr, mo = map(int, mois_k.split("-"))
        lbl_m  = f"{MOIS_FR.get(mo, mo)} {yr}"
        statut = "✅ Transférée" if ep.get("transfere") else "⏳ En attente"
        c_s    = "#059669" if ep.get("transfere") else "#d97706"
        m_txt  = fmt(ep.get("montant", 0))
        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:0.8rem 1rem;
                    margin-bottom:0.5rem;display:flex;justify-content:space-between;align-items:center;
                    box-shadow:0 1px 3px rgba(15,23,42,0.04)">
            <span style="font-weight:600;color:#0f172a">{lbl_m}</span>
            <span style="font-family:'Space Mono',monospace;color:#0891b2;font-weight:700">{m_txt}</span>
            <span style="color:{c_s};font-size:0.85rem;font-weight:600">{statut}</span>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# TAB 4 — DÎME
# ═══════════════════════════════════════════════
with tab4:
    st.markdown(
        "<div style='font-size:1.6rem;font-weight:900;margin-bottom:1rem;color:#0f172a'>"
        "🙏 Gestion de la <span style='color:#d97706'>Dîme</span></div>",
        unsafe_allow_html=True,
    )

    # Garantir la clé
    if "dime_versements" not in mois_data:
        mois_data["dime_versements"] = []

    # ── KPI Cards ──
    dk1, dk2, dk3, dk4 = st.columns(4)
    with dk1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">🎯 Objectif dîme</div>
            <div class="kpi-value" style="color:#d97706">{fmt(dime_objectif)}</div>
            <div class="kpi-sub">10% de {fmt(revenu_total)}</div>
        </div>
        """, unsafe_allow_html=True)
    with dk2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">✅ Total versé</div>
            <div class="kpi-value" style="color:#059669">{fmt(dime_paye_total)}</div>
            <div class="kpi-sub">{len(dime_versements)} versement(s)</div>
        </div>
        """, unsafe_allow_html=True)
    with dk3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">⏳ Reste à payer</div>
            <div class="kpi-value" style="color:#dc2626">{fmt(dime_restante)}</div>
            <div class="kpi-sub">{'Dîme complète 🎉' if dime_complete else 'À compléter'}</div>
        </div>
        """, unsafe_allow_html=True)
    with dk4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📈 Progression</div>
            <div class="kpi-value" style="color:#4f46e5">{dime_prog_pct:.0f}%</div>
            <div class="kpi-sub">Du mois en cours</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Badge statut ──
    if dime_complete:
        st.markdown('<span class="badge badge-green" style="font-size:0.9rem;padding:4px 14px">✅ Dîme complète</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="badge badge-amber" style="font-size:0.9rem;padding:4px 14px">⏳ En cours ({dime_prog_pct:.0f}%)</span>', unsafe_allow_html=True)

    # ── Barre de progression ──
    bar_color_dime = "#059669" if dime_complete else "#d97706"
    st.markdown(f"""
    <div class="prog-wrap" style="margin-top:1rem">
        <div class="prog-header">
            <span class="prog-name">🙏 Progression de la dîme</span>
            <span class="prog-pct" style="background:#fef3c7;color:#92400e">{fmt(dime_paye_total)} / {fmt(dime_objectif)}</span>
        </div>
        <div class="prog-bar-bg" style="height:16px">
            <div class="prog-bar-fill" style="width:{dime_prog_pct:.1f}%;background:{bar_color_dime}"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Formulaire ajout versement ──
    if not est_archive:
        st.markdown("<div class='section-title'>➕ Ajouter un versement de dîme</div>", unsafe_allow_html=True)
        dv1, dv2 = st.columns(2)
        with dv1:
            dv_montant = st.number_input("Montant versé", min_value=0.0, step=500.0, format="%.0f", key="dv_montant", label_visibility="collapsed")
            dv_note    = st.text_input("Note (ex: Église, pasteur...)", key="dv_note", placeholder="Note optionnelle")
        with dv2:
            dv_date = st.date_input("Date du versement", value=date.today(), key="dv_date")

        if st.button("🙏 Ajouter ce versement de dîme", use_container_width=True):
            if dv_montant > 0:
                mois_data["dime_versements"].append({
                    "montant": float(dv_montant),
                    "date":    str(dv_date),
                    "note":    dv_note.strip(),
                })
                save_data(data)
                new_total = sum(v["montant"] for v in mois_data["dime_versements"])
                if new_total >= dime_objectif > 0:
                    st.balloons()
                    st.success("🎉 Dîme du mois complète ! Que Dieu bénisse !")
                else:
                    st.success(f"✅ Versement de {fmt(dv_montant)} enregistré !")
                st.rerun()
            else:
                st.error("⚠️ Le montant doit être supérieur à 0.")

    # ── Historique versements du mois ──
    st.markdown("<div class='section-title'>📋 Versements du mois</div>", unsafe_allow_html=True)
    if dime_versements:
        for i, v in enumerate(dime_versements):
            vc1, vc2 = st.columns([6, 1])
            with vc1:
                note_txt = f" · {v['note']}" if v.get("note") else ""
                st.markdown(f"""
                <div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;
                            padding:0.5rem 0.9rem;font-size:0.85rem;margin-bottom:0.3rem;
                            display:flex;justify-content:space-between;align-items:center">
                    <span style="color:#64748b">{v.get('date','?')}{note_txt}</span>
                    <span style="font-family:'Space Mono',monospace;font-weight:700;color:#d97706">{fmt(v.get('montant',0))}</span>
                </div>
                """, unsafe_allow_html=True)
            with vc2:
                if not est_archive:
                    if st.button("🗑️", key=f"del_dv_{i}"):
                        mois_data["dime_versements"].pop(i)
                        save_data(data)
                        st.rerun()
        st.markdown(
            f"<div style='text-align:right;font-weight:700;color:#d97706;margin-top:0.3rem'>"
            f"Total : {fmt(dime_paye_total)}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.info("Aucun versement ce mois. Ajoutez votre premier versement de dîme !")

    # ── Historique mensuel ──
    st.markdown("<div class='section-title'>📊 Historique mensuel des dîmes</div>", unsafe_allow_html=True)
    for mois_k in sorted(data["historique"].keys(), reverse=True):
        mois_d_hist = data["historique"][mois_k]
        dv_hist  = mois_d_hist.get("dime_versements", [])
        total_h  = sum(v["montant"] for v in dv_hist)
        rev_h    = sum(r["montant"] for r in mois_d_hist.get("revenus", []))
        obj_h    = rev_h * 0.10
        comp_h   = total_h >= obj_h and obj_h > 0
        yr, mo   = map(int, mois_k.split("-"))
        lbl_m    = f"{MOIS_FR.get(mo, mo)} {yr}"
        statut_h = "✅ Complète" if comp_h else ("⏳ En cours" if total_h > 0 else "❌ Non versée")
        c_h      = "#059669" if comp_h else ("#d97706" if total_h > 0 else "#64748b")
        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:0.8rem 1rem;
                    margin-bottom:0.4rem;display:flex;justify-content:space-between;align-items:center;
                    box-shadow:0 1px 3px rgba(15,23,42,0.04)">
            <span style="font-weight:600;color:#0f172a">{lbl_m}</span>
            <span style="font-family:'Space Mono',monospace;color:#d97706;font-weight:700">{fmt(total_h)}</span>
            <span style="color:{c_h};font-size:0.85rem;font-weight:600">{statut_h}</span>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# TAB 5 — PRÊTS
# ═══════════════════════════════════════════════
with tab5:
    st.markdown(
        "<div style='font-size:1.6rem;font-weight:900;margin-bottom:1rem;color:#0f172a'>"
        "💸 Gestion des <span style='color:#4f46e5'>Prêts</span></div>",
        unsafe_allow_html=True,
    )

    # ── KPI Prêts ──
    prets_ce_mois     = [p for p in prets if p.get("date_pret", "").startswith(mois_vue)]
    total_prete_mois  = sum(p["montant"] for p in prets_ce_mois)

    kp1, kp2, kp3 = st.columns(3)
    with kp1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">💸 Prêté ce mois</div>
            <div class="kpi-value" style="color:#4f46e5">{fmt(total_prete_mois)}</div>
            <div class="kpi-sub">{len(prets_ce_mois)} prêt(s)</div>
        </div>
        """, unsafe_allow_html=True)
    with kp2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">⏳ En attente</div>
            <div class="kpi-value" style="color:#d97706">{fmt(total_prets_en_cours)}</div>
            <div class="kpi-sub">{len(prets_en_cours)} prêt(s)</div>
        </div>
        """, unsafe_allow_html=True)
    with kp3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">✅ Total récupéré</div>
            <div class="kpi-value" style="color:#059669">{fmt(total_prets_recuperes)}</div>
            <div class="kpi-sub">{len(prets_rembourses)} prêt(s)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Formulaire nouveau prêt ──
    st.markdown("<div class='section-title'>➕ Nouveau prêt</div>", unsafe_allow_html=True)

    if st.session_state.pop("_reset_pret_form", False):
        st.session_state["p_emprunteur"] = ""
        st.session_state["p_montant"]    = 0.0
        st.session_state["p_date_pret"]  = date.today()
        st.session_state["p_echeance"]   = date.today()
        st.session_state["p_note"]       = ""

    with st.expander("Enregistrer un nouveau prêt", expanded=False):
        pf1, pf2 = st.columns(2)
        with pf1:
            p_emprunteur = st.text_input("👤 Nom de l'emprunteur", key="p_emprunteur")
            p_montant    = st.number_input("💰 Montant prêté", min_value=0.0, step=500.0, format="%.0f", key="p_montant")
            p_date_pret  = st.date_input("📅 Date du prêt", value=date.today(), key="p_date_pret")
        with pf2:
            p_echeance = st.date_input("⏰ Date de remboursement prévue", key="p_echeance")
            p_note     = st.text_area("📝 Note / raison (optionnel)", key="p_note")

        if st.button("💸 Enregistrer le prêt", use_container_width=True):
            if p_emprunteur.strip() and p_montant > 0:
                data["prets"].append({
                    "id":                 f"pret_{int(datetime.now().timestamp() * 1000)}",
                    "emprunteur":         p_emprunteur.strip(),
                    "montant":            float(p_montant),
                    "date_pret":          str(p_date_pret),
                    "date_echeance":      str(p_echeance),
                    "rembourse":          False,
                    "date_remboursement": None,
                    "note":               p_note.strip(),
                })
                save_data(data)
                st.success(f"✅ Prêt de {fmt(p_montant)} à **{p_emprunteur}** enregistré !")
                st.session_state["_reset_pret_form"] = True
                st.rerun()
            else:
                st.error("⚠️ Veuillez renseigner le nom et un montant supérieur à 0.")

    # ── Prêts en cours ──
    st.markdown("<div class='section-title'>⏳ Prêts en cours</div>", unsafe_allow_html=True)

    if prets_en_cours:
        for p in prets_en_cours:
            try:
                echeance = date.fromisoformat(p["date_echeance"])
                delta    = (echeance - today).days
                if delta > 7:
                    status_color = "#059669"
                    status_txt   = f"✅ {delta} jours restants"
                elif delta >= 0:
                    status_color = "#d97706"
                    status_txt   = f"⚠️ {delta} jour(s) restant(s)"
                else:
                    status_color = "#dc2626"
                    status_txt   = f"🚨 En retard de {-delta} jour(s)"
            except (ValueError, KeyError):
                status_color = "#64748b"
                status_txt   = "Date inconnue"

            note_html = f'<div style="font-size:0.78rem;color:#64748b;margin-top:0.2rem">📝 {p["note"]}</div>' if p.get("note") else ""

            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:1rem 1.2rem;
                        margin-bottom:0.5rem;border-left:4px solid {status_color};
                        box-shadow:0 2px 8px rgba(15,23,42,0.06)">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem">
                    <div>
                        <div style="font-size:1rem;font-weight:700;color:#0f172a">{p['emprunteur']}</div>
                        <div style="font-family:'Space Mono',monospace;font-size:1.3rem;font-weight:700;
                                    color:#4f46e5;margin:0.15rem 0">{fmt(p['montant'])}</div>
                        <div style="font-size:0.78rem;color:#64748b">
                            📅 Prêté le {p['date_pret']} → Échéance {p['date_echeance']}
                        </div>
                        {note_html}
                    </div>
                    <div style="color:{status_color};font-size:0.82rem;font-weight:600;
                                text-align:right;white-space:nowrap">{status_txt}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            bc1, bc2 = st.columns(2)
            with bc1:
                if st.button("✅ Marquer remboursé", key=f"rembourse_{p['id']}"):
                    for pr in data["prets"]:
                        if pr["id"] == p["id"]:
                            pr["rembourse"]          = True
                            pr["date_remboursement"] = str(today)
                            break
                    save_data(data)
                    st.success(f"✅ Remboursement de **{p['emprunteur']}** enregistré !")
                    st.rerun()
            with bc2:
                if st.button("🗑️ Supprimer", key=f"del_pret_{p['id']}"):
                    data["prets"] = [pr for pr in data["prets"] if pr["id"] != p["id"]]
                    save_data(data)
                    st.rerun()
    else:
        st.markdown(
            "<div style='color:#64748b;text-align:center;padding:2rem'>✅ Aucun prêt en cours</div>",
            unsafe_allow_html=True,
        )

    # ── Prêts remboursés ──
    if prets_rembourses:
        st.markdown("<div class='section-title'>✅ Prêts remboursés</div>", unsafe_allow_html=True)
        for p in sorted(prets_rembourses, key=lambda x: x.get("date_remboursement", ""), reverse=True):
            st.markdown(f"""
            <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:0.6rem 1rem;
                        margin-bottom:0.4rem;display:flex;justify-content:space-between;align-items:center;gap:0.5rem">
                <span style="font-weight:600;color:#0f172a">{p['emprunteur']}</span>
                <span style="font-family:'Space Mono',monospace;color:#059669;font-weight:700">{fmt(p['montant'])}</span>
                <span style="font-size:0.78rem;color:#64748b;white-space:nowrap">
                    remboursé le {p.get('date_remboursement','?')}
                </span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align:right;font-weight:700;color:#059669;margin-top:0.5rem'>"
            f"Total récupéré : {fmt(total_prets_recuperes)}</div>",
            unsafe_allow_html=True,
        )

# ═══════════════════════════════════════════════
# TAB 6 — DETTES
# ═══════════════════════════════════════════════
with tab6:
    st.markdown(
        "<div style='font-size:1.6rem;font-weight:900;margin-bottom:1rem;color:#0f172a'>"
        "💳 Gestion des <span style='color:#dc2626'>Dettes</span></div>",
        unsafe_allow_html=True,
    )

    # ── Alertes échéances ──
    for _ad in dettes_en_cours:
        try:
            _ech_d = date.fromisoformat(_ad["date_echeance"])
            _delta_d = (_ech_d - today).days
            if _delta_d < 0:
                st.error(f"🚨 Dette envers **{_ad['creancier']}** en retard de {-_delta_d} jour(s) ! Reste : {fmt(_ad['_restant'])}")
            elif _delta_d <= 7:
                st.warning(f"⚠️ **{_ad['creancier']}** : échéance dans {_delta_d} jour(s) ! Reste : {fmt(_ad['_restant'])}")
        except (ValueError, KeyError):
            pass

    # ── KPI Cards ──
    kd1, kd2, kd3, kd4 = st.columns(4)
    with kd1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">💳 Total dû</div>
            <div class="kpi-value" style="color:#dc2626">{fmt(sum(d['montant_total'] for d in dettes_en_cours))}</div>
            <div class="kpi-sub">Dettes en cours</div>
        </div>
        """, unsafe_allow_html=True)
    with kd2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">✅ Total remboursé</div>
            <div class="kpi-value" style="color:#059669">{fmt(total_dettes_rem)}</div>
            <div class="kpi-sub">Sur dettes en cours</div>
        </div>
        """, unsafe_allow_html=True)
    with kd3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📋 Dettes en cours</div>
            <div class="kpi-value" style="color:#4f46e5">{len(dettes_en_cours)}</div>
            <div class="kpi-sub">{len(dettes_soldees)} soldée(s)</div>
        </div>
        """, unsafe_allow_html=True)
    with kd4:
        proch_txt = prochaine_echeance_dette.strftime("%d/%m/%Y") if prochaine_echeance_dette else "—"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📅 Prochaine échéance</div>
            <div class="kpi-value" style="font-size:1.1rem;color:#d97706">{proch_txt}</div>
            <div class="kpi-sub">Date limite</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Formulaire nouvelle dette ──
    st.markdown("<div class='section-title'>➕ Nouvelle dette</div>", unsafe_allow_html=True)
    if st.session_state.pop("_reset_dette_form", False):
        for _k in ["nd_creancier","nd_montant","nd_echeance","nd_note"]:
            st.session_state.pop(_k, None)

    with st.expander("Enregistrer une nouvelle dette", expanded=False):
        ndf1, ndf2 = st.columns(2)
        with ndf1:
            nd_creancier = st.text_input("👤 Créancier (à qui je dois ?)", key="nd_creancier")
            nd_montant   = st.number_input("💰 Montant total dû", min_value=0.0, step=500.0, format="%.0f", key="nd_montant")
        with ndf2:
            nd_echeance = st.date_input("📅 Date d'échéance", key="nd_echeance")
            nd_note     = st.text_area("📝 Note / raison", key="nd_note")

        if st.button("➕ Enregistrer la dette", use_container_width=True):
            if nd_creancier.strip() and nd_montant > 0:
                data["dettes"].append({
                    "id":            f"dette_{int(datetime.now().timestamp() * 1000)}",
                    "creancier":     nd_creancier.strip(),
                    "montant_total": float(nd_montant),
                    "date_creation": str(today),
                    "date_echeance": str(nd_echeance),
                    "note":          nd_note.strip(),
                    "versements":    [],
                })
                save_data(data)
                st.success(f"✅ Dette de {fmt(nd_montant)} envers **{nd_creancier}** enregistrée !")
                st.session_state["_reset_dette_form"] = True
                st.rerun()
            else:
                st.error("⚠️ Renseignez le créancier et un montant supérieur à 0.")

    # ── Dettes en cours ──
    st.markdown("<div class='section-title'>⏳ Dettes en cours</div>", unsafe_allow_html=True)

    if dettes_en_cours:
        for d in dettes_en_cours:
            try:
                ech_d  = date.fromisoformat(d["date_echeance"])
                delta_d = (ech_d - today).days
                if delta_d > 7:
                    sc, st_txt = "#059669", f"✅ {delta_d} jours restants"
                elif delta_d >= 0:
                    sc, st_txt = "#d97706", f"⚠️ {delta_d} jour(s) restant(s)"
                else:
                    sc, st_txt = "#dc2626", f"🚨 En retard de {-delta_d} j"
            except (ValueError, KeyError):
                sc, st_txt = "#64748b", "Date inconnue"

            prog_d = d["_progression"]
            bar_c  = "#dc2626" if prog_d < 30 else ("#d97706" if prog_d < 70 else "#059669")
            note_h = f'<div style="font-size:0.78rem;color:#64748b;margin-top:0.2rem">📝 {d["note"]}</div>' if d.get("note") else ""

            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:1rem 1.2rem;
                        margin-bottom:0.5rem;border-left:4px solid {sc};box-shadow:0 2px 8px rgba(15,23,42,0.06)">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem">
                    <div style="flex:1">
                        <div style="font-size:1rem;font-weight:700;color:#0f172a">{d['creancier']}</div>
                        <div style="font-family:'Space Mono',monospace;font-size:1.2rem;font-weight:700;color:#dc2626;margin:0.1rem 0">
                            Reste : {fmt(d['_restant'])}
                        </div>
                        <div style="font-size:0.78rem;color:#64748b">
                            Total : {fmt(d['montant_total'])} · Remboursé : {fmt(d['_rembourse'])} · Échéance : {d['date_echeance']}
                        </div>
                        {note_h}
                        <div style="margin-top:0.5rem">
                            <div style="background:#e2e8f0;border-radius:999px;height:8px;overflow:hidden">
                                <div style="width:{min(prog_d,100):.1f}%;height:100%;border-radius:999px;background:{bar_c}"></div>
                            </div>
                            <div style="font-size:0.7rem;color:#64748b;margin-top:0.2rem">{prog_d:.1f}% remboursé</div>
                        </div>
                    </div>
                    <div style="color:{sc};font-size:0.8rem;font-weight:600;text-align:right;white-space:nowrap">{st_txt}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Versements déjà faits
            if d.get("versements"):
                with st.expander(f"📋 {len(d['versements'])} versement(s) enregistré(s)", expanded=False):
                    for v in d["versements"]:
                        vn = f" · {v['note']}" if v.get("note") else ""
                        st.markdown(
                            f"<div style='font-size:0.82rem;color:#64748b;padding:0.2rem 0'>"
                            f"📅 {v.get('date','?')}{vn} — "
                            f"<b style='color:#059669'>{fmt(v.get('montant',0))}</b></div>",
                            unsafe_allow_html=True,
                        )

            # Mini-formulaire versement
            st.markdown(f"<div style='font-size:0.85rem;font-weight:600;color:#64748b;margin-top:0.4rem'>💸 Ajouter un versement</div>", unsafe_allow_html=True)
            vc1, vc2 = st.columns([2, 1])
            with vc1:
                v_mont = st.number_input("Montant", min_value=0.0, step=500.0, format="%.0f",
                                         key=f"v_{d['id']}", label_visibility="collapsed")
                v_note_d = st.text_input("Note versement", key=f"n_{d['id']}", placeholder="Note (optionnel)")
            with vc2:
                v_date_d = st.date_input("Date", value=date.today(), key=f"d_{d['id']}", label_visibility="collapsed")

            if st.button("💸 Ajouter versement", key=f"btn_{d['id']}"):
                if v_mont > 0:
                    for _det in data["dettes"]:
                        if _det["id"] == d["id"]:
                            _det["versements"].append({
                                "montant": float(v_mont),
                                "date":    str(v_date_d),
                                "note":    v_note_d.strip(),
                            })
                            break
                    save_data(data)
                    new_rem = sum(v["montant"] for v in next(x for x in data["dettes"] if x["id"] == d["id"])["versements"])
                    if d["montant_total"] - new_rem <= 0:
                        st.success(f"🎉 Dette envers **{d['creancier']}** entièrement soldée !")
                    else:
                        st.success(f"✅ Versement de {fmt(v_mont)} enregistré !")
                    st.rerun()
                else:
                    st.error("⚠️ Montant invalide.")

            st.markdown("<hr style='margin:0.8rem 0;border-color:#f1f5f9'>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div style='color:#64748b;text-align:center;padding:2rem'>✅ Aucune dette en cours. Bravo !</div>",
            unsafe_allow_html=True,
        )

    # ── Dettes soldées ──
    if dettes_soldees:
        st.markdown("<div class='section-title'>✅ Dettes soldées</div>", unsafe_allow_html=True)
        for d in sorted(dettes_soldees, key=lambda x: x.get("date_echeance", ""), reverse=True):
            st.markdown(f"""
            <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:0.6rem 1rem;
                        margin-bottom:0.4rem;display:flex;justify-content:space-between;align-items:center">
                <span style="font-weight:600;color:#0f172a">{d['creancier']}</span>
                <span style="font-family:'Space Mono',monospace;color:#059669;font-weight:700">{fmt(d['montant_total'])}</span>
                <span style="font-size:0.78rem;color:#64748b">soldée ✅</span>
            </div>
            """, unsafe_allow_html=True)

    if st.button("🗑️ Supprimer une dette soldée", key="del_dettes_soldees"):
        data["dettes"] = [d for d in data["dettes"] if not (d["montant_total"] - sum(v["montant"] for v in d.get("versements",[])) <= 0)]
        save_data(data)
        st.rerun()

# ═══════════════════════════════════════════════
# TAB 7 — CONSEILS
# ═══════════════════════════════════════════════
with tab7:
    st.markdown(
        "<div style='font-size:1.6rem;font-weight:900;margin-bottom:1rem;color:#0f172a'>"
        "💡 <span style='color:#2563eb'>Conseils Intelligents</span></div>",
        unsafe_allow_html=True,
    )

    pct_utilise  = (total_depense / enveloppes["consommation"] * 100) if enveloppes["consommation"] > 0 else 0
    jours_ecoules = now.day
    rythme_ideal  = (jours_ecoules / 30) * 100

    tips = []

    if revenu_total == 0:
        tips.append(("⚠️", "Commencez par saisir votre revenu",
                     "Renseignez votre revenu mensuel dans la barre latérale pour activer tous les calculs automatiques.", "#d97706"))
    elif pct_utilise > 100:
        tips.append(("🔴", "Budget dépassé !",
                     f"Vous avez dépensé {pct_utilise:.1f}% de votre budget consommation. Identifiez les catégories en dépassement.", "#dc2626"))
    elif pct_utilise > rythme_ideal + 15:
        tips.append(("🟡", "Rythme de dépenses élevé",
                     f"À {jours_ecoules}j dans le mois, vous avez consommé {pct_utilise:.1f}% du budget (idéalement {rythme_ideal:.0f}%). Ralentissez !", "#d97706"))
    elif pct_utilise < rythme_ideal - 20 and jours_ecoules > 10:
        tips.append(("🟢", "Excellent contrôle budgétaire !",
                     f"Bravo ! Seulement {pct_utilise:.1f}% utilisé pour {jours_ecoules} jours. Continuez ainsi !", "#059669"))
    else:
        tips.append(("✅", "Budget bien maîtrisé",
                     f"Vous êtes dans la moyenne : {pct_utilise:.1f}% du budget utilisé au {jours_ecoules}ème jour.", "#059669"))

    conseils_cat = {
        "🍽️ Nourriture":         "Planifiez vos repas en avance et préparez vos courses avec une liste stricte.",
        "🎉 Loisirs & Sorties":  "Cherchez des activités gratuites ou à prix réduit pour le reste du mois.",
        "🚌 Transport":           "Explorez le covoiturage ou les transports en commun pour réduire vos coûts.",
        "📦 Dépenses diverses":  "Différenciez les besoins des envies. Attendez 48h avant tout achat impulsif.",
        "🏠 Loyer / Logement":   "Vérifiez si vous pouvez renégocier votre loyer ou trouver des économies d'énergie.",
        "💡 Factures & Charges": "Comparez les offres fournisseurs et adoptez des gestes éco-responsables.",
        "🎓 Frais scolaires":    "Cherchez des bourses, aides étudiantes ou matériels de seconde main.",
        "💊 Santé":              "Privilégiez les médicaments génériques et vérifiez vos remboursements.",
    }

    for cat, depense in totaux_cat.items():
        budget_c = budget_cat_default(cat, enveloppes["consommation"])
        if budget_c > 0 and depense > budget_c:
            surplus = depense - budget_c
            conseil = conseils_cat.get(cat, "Réduisez vos dépenses dans cette catégorie.")
            tips.append(("💡", f"{cat} : surplus de {fmt(surplus)}", conseil, "#4f46e5"))

    ep_mois   = mois_data.get("epargne", {})

    if not ep_mois.get("transfere") and revenu_total > 0:
        tips.append(("🏦", "Épargne non encore transférée",
                     f"N'oubliez pas de transférer vos {fmt(enveloppes['epargne'])} d'épargne ce mois ! Payez-vous en premier.", "#0891b2"))

    if not dime_complete and revenu_total > 0:
        tips.append(("🙏", "Dîme non encore complète",
                     f"Pensez à compléter votre dîme de {fmt(dime_objectif)} ({dime_prog_pct:.0f}% versé). La générosité attire l'abondance.", "#d97706"))

    prets_en_retard = [p for p in prets_en_cours if p.get("date_echeance", "9999") < str(today)]
    if prets_en_retard:
        tips.append(("🚨", f"{len(prets_en_retard)} prêt(s) en retard !",
                     "Relancez vos emprunteurs. Un suivi régulier favorise le remboursement.", "#dc2626"))

    if len(depenses_mois) > 15:
        tips.append(("📊", "Bonne habitude de suivi",
                     "Vous suivez régulièrement vos dépenses. C'est la clé d'une saine gestion financière !", "#059669"))
    elif len(depenses_mois) < 3 and jours_ecoules > 5:
        tips.append(("📝", "Pensez à saisir vos dépenses",
                     "Un bon suivi financier nécessite d'enregistrer toutes vos dépenses, même les petites.", "#64748b"))

    for icon, titre, contenu, color in tips:
        st.markdown(f"""
        <div class="tip-card" style="border-left:3px solid {color}">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem">
                <span style="font-size:1.2rem">{icon}</span>
                <span style="font-weight:700;color:{color}">{titre}</span>
            </div>
            <div style="color:#475569;font-size:0.9rem;line-height:1.5">{contenu}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Résumé du mois ──
    st.markdown("<div class='section-title'>📊 Résumé du mois</div>", unsafe_allow_html=True)
    rs1, rs2, rs3 = st.columns(3)
    card_style = "background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:1rem;text-align:center;box-shadow:0 1px 4px rgba(15,23,42,0.06)"

    with rs1:
        note_budget = "🟢 Excellent" if pct_utilise < 80 else ("🟡 Attention" if pct_utilise < 100 else "🔴 Dépassé")
        note_color  = "#059669" if pct_utilise < 80 else ("#d97706" if pct_utilise < 100 else "#dc2626")
        st.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:0.8rem;color:#64748b;margin-bottom:0.3rem">BUDGET</div>
            <div style="font-size:1.2rem;font-weight:700;color:{note_color}">{note_budget}</div>
            <div style="font-size:0.75rem;color:#64748b">{pct_utilise:.1f}% utilisé</div>
        </div>
        """, unsafe_allow_html=True)

    with rs2:
        note_ep = "✅ Transférée" if ep_mois.get("transfere") else "⏳ À faire"
        c_ep    = "#059669" if ep_mois.get("transfere") else "#d97706"
        st.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:0.8rem;color:#64748b;margin-bottom:0.3rem">ÉPARGNE</div>
            <div style="font-size:1.2rem;font-weight:700;color:{c_ep}">{note_ep}</div>
            <div style="font-size:0.75rem;color:#64748b">{fmt(enveloppes['epargne'])}</div>
        </div>
        """, unsafe_allow_html=True)

    with rs3:
        note_dime = "✅ Complète" if dime_complete else f"⏳ {dime_prog_pct:.0f}%"
        c_dime    = "#059669" if dime_complete else "#d97706"
        st.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:0.8rem;color:#64748b;margin-bottom:0.3rem">DÎME</div>
            <div style="font-size:1.2rem;font-weight:700;color:{c_dime}">{note_dime}</div>
            <div style="font-size:0.75rem;color:#64748b">{fmt(enveloppes['dime'])}</div>
        </div>
        """, unsafe_allow_html=True)

    # Citation du jour
    import hashlib
    citation_idx = int(hashlib.md5(str(now.date()).encode()).hexdigest(), 16) % len(CITATIONS)
    st.markdown(f'<div class="citation">{CITATIONS[citation_idx]}</div>', unsafe_allow_html=True)
