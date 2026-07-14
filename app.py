import streamlit as st
import numpy as np
import pickle
import os
import plotly.graph_objects as go
import base64
import random

# ---------- CONFIG ----------
st.set_page_config(page_title="Arogya Plan", page_icon="🍃", layout="wide")

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")
BG_PATH = os.path.join(BASE_DIR, "assets", "images", "bg1.png")

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except Exception:
        return None

model = load_model()
if model is None:
    st.error("❌ Model failed to load")
    st.stop()

# ---------- BACKGROUND (optional image, kept dark either way) ----------
def get_base64_image(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

bg = get_base64_image(BG_PATH)

if bg:
    st.markdown(f"""
    <style>
    .stApp {{
        background: url("data:image/png;base64,{bg}") no-repeat center center fixed;
        background-size: cover;
    }}
    .stApp::before {{
        content:"";
        position:fixed;
        inset:0;
        background:rgba(0,0,0,0.82);
        z-index:-1;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------- DAZN-STYLE THEME ----------
# Palette: near-black surfaces, pure-black app bg, signature neon yellow accent,
# bold condensed/uppercase headers, sharp-edged cards with thin hairline borders.
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;600;700;900&display=swap');

:root{
    --dazn-black:#0a0a0a;
    --dazn-surface:#141414;
    --dazn-surface-2:#1c1c1c;
    --dazn-yellow:#f9f900;
    --dazn-yellow-dim:#c7c700;
    --dazn-grey:#8a8a8a;
    --dazn-border:rgba(255,255,255,0.08);
}

html, body, .stApp, [class*="css"] {
    background-color: var(--dazn-black) !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}

/* Kill Streamlit's default top padding for a tighter, app-like feel */
.block-container{
    padding-top: 1.5rem !important;
}

/* Labels */
label, .stRadio label, .stSelectbox label, .stNumberInput label {
    color: #ffffff !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

div[role="radiogroup"] label,
div[role="radiogroup"] p,
.stRadio label {
    color: #ffffff !important;
    opacity: 1 !important;
}

/* Inputs */
.stNumberInput input, .stSelectbox > div > div {
    background-color: var(--dazn-surface) !important;
    color: #ffffff !important;
    border: 1px solid var(--dazn-border) !important;
    border-radius: 4px !important;
}

/* Radio pills -> DAZN-style tab selectors */
div[role="radiogroup"] {
    gap: 6px;
}
div[role="radiogroup"] > label {
    background: var(--dazn-surface);
    border: 1px solid var(--dazn-border);
    border-radius: 4px;
    padding: 6px 14px !important;
}

/* Buttons */
.stButton > button {
    background: var(--dazn-yellow);
    color: #0a0a0a !important;
    border-radius: 4px;
    padding: 12px 24px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    border: none;
    width: 100%;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background: #ffffff;
    color: #0a0a0a !important;
    transform: scale(1.01);
}

/* Section headers */
h1, h2, h3 {
    font-family: 'Archivo Black', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 0.02em;
}

/* Meal / content Cards -> DAZN match-card style */
.card{
    background: var(--dazn-surface);
    padding: 22px;
    border-radius: 6px;
    margin-bottom: 15px;
    border-left: 4px solid var(--dazn-yellow);
    border-top: 1px solid var(--dazn-border);
    border-right: 1px solid var(--dazn-border);
    border-bottom: 1px solid var(--dazn-border);
}

.meal-head{
    font-family: 'Archivo Black', sans-serif;
    font-size: 20px;
    font-weight: 900;
    color: #ffffff !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.meal-text{
    font-size: 17px;
    font-weight: 600;
    color: #d8d8d8 !important;
    line-height: 2;
}

/* Metrics -> DAZN stat-tile style */
[data-testid="stMetric"] {
    background: var(--dazn-surface);
    border: 1px solid var(--dazn-border);
    border-top: 3px solid var(--dazn-yellow);
    border-radius: 4px;
    padding: 16px;
    text-align:center;
}
[data-testid="stMetricLabel"] {
    color: var(--dazn-grey) !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="stMetricValue"] {
    color: var(--dazn-yellow) !important;
    font-size: 34px !important;
    font-weight: 900 !important;
    font-family: 'Archivo Black', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ---------- HEADER (DAZN-style black bar + yellow wordmark) ----------
st.markdown("""
<div style="
text-align:center;
padding:26px 20px;
margin-bottom:25px;
background:#0a0a0a;
border-bottom: 3px solid #f9f900;
">
<h1 style="
font-family:'Archivo Black',sans-serif;
font-size:46px;
font-weight:900;
color:#f9f900;
margin:0;
letter-spacing:0.03em;">
AROGYA<span style="color:#ffffff;">PLAN</span>
</h1>
<p style="color:#8a8a8a;font-size:14px;margin-top:8px;text-transform:uppercase;letter-spacing:0.15em;font-weight:700;">
Your Personal Nutrition Coverage
</p>
</div>
""", unsafe_allow_html=True)

# ---------- INPUT ----------
if not st.session_state.submitted:

    st.markdown("""
    <h2 style="font-weight:900;margin-top:10px;margin-bottom:18px;color:#ffffff;">
    👤 Enter Your Details
    </h2>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.number_input("Age", 10, 100)
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        diet_pref = st.selectbox("Diet Preference", ["Veg", "Non-Veg"])

    with c2:
        height = st.number_input("Height (cm)", 100.0, 250.0)
        weight = st.number_input("Weight (kg)", 30.0, 200.0)
        region = st.selectbox("Food Style", ["South Indian", "North Indian"])

    with c3:
        activity = st.radio("Activity Level", ["Low", "Moderate", "High"], horizontal=True)
        goal = st.radio("Goal", ["Weight Loss", "Maintain", "Muscle Gain"], horizontal=True)
        budget = st.selectbox("Budget", ["Budget", "Premium"])

    sugar = st.number_input("Sugar Level", 50.0, 300.0)
    cholesterol = st.number_input("Cholesterol", 100.0, 400.0)

    if st.button("▶ GENERATE PLAN"):
        st.session_state.submitted = True
        st.session_state.data = {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "diet_pref": diet_pref,
            "region": region,
            "budget": budget,
            "activity": activity,
            "goal": goal,
            "sugar": sugar,
            "cholesterol": cholesterol
        }
        st.rerun()

# ---------- OUTPUT ----------
if st.session_state.submitted:

    d = st.session_state.data
    bmi = d["weight"] / ((d["height"] / 100) ** 2)

    gender_map = {"Male": 0, "Female": 1}
    activity_map = {"Low": 0, "Moderate": 1, "High": 2}
    goal_map = {"Weight Loss": 0, "Maintain": 1, "Muscle Gain": 2}

    input_data = np.array([[
        d["age"],
        gender_map[d["gender"]],
        d["height"],
        d["weight"],
        bmi,
        activity_map[d["activity"]],
        d["sugar"],
        d["cholesterol"],
        goal_map[d["goal"]]
    ]])

    pred = model.predict(input_data)[0]

    diet_names = {
        0: "Low Carb Diet",
        1: "Diabetic Diet",
        2: "Heart Healthy Diet",
        3: "Balanced Diet",
        4: "High Protein Diet"
    }

    diet_name = diet_names.get(pred, "Balanced Diet")

    st.markdown(f"""
    <div style="
    text-align:center;
    font-family:'Archivo Black',sans-serif;
    font-size:32px;
    font-weight:900;
    color:#f9f900;
    margin:15px 0;
    text-transform:uppercase;
    letter-spacing:0.03em;
    padding:16px;
    background:#141414;
    border-radius:6px;
    border:1px solid rgba(255,255,255,0.08);
    ">
    🥗 {diet_name}
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("BMI", f"{bmi:.2f}")
    c2.metric("Sugar", f'{d["sugar"]:.1f}')
    c3.metric("Cholesterol", f'{d["cholesterol"]:.1f}')

    # BMI Gauge (DAZN-tinted: black bg, yellow needle/number)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        title={"text": "BMI", "font": {"color": "#ffffff"}},
        number={"font": {"color": "#f9f900"}},
        gauge={
            "axis": {"range": [10, 50], "tickcolor": "#ffffff"},
            "bar": {"color": "#f9f900"},
            "bgcolor": "#141414",
            "bordercolor": "rgba(255,255,255,0.15)",
            "steps": [
                {"range": [10, 18], "color": "#1c2b3a"},
                {"range": [18, 25], "color": "#1c3a24"},
                {"range": [25, 30], "color": "#3a2f1c"},
                {"range": [30, 50], "color": "#3a1c1c"},
            ]
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)

    # Daily Plan Heading
    st.markdown("""
    <h2 style="color:#ffffff;font-weight:900;margin-top:20px;margin-bottom:15px;">
    🍽️ Your Daily Plan
    </h2>
    """, unsafe_allow_html=True)

    foods = {
        "Breakfast": {
            "Veg": ["🫐 Oats", "🥞 Dosa", "🥪 Veg Sandwich"],
            "Non-Veg": ["🥚 Eggs", "🍗 Chicken Sandwich", "🍳 Omelette"]
        },
        "Lunch": {
            "Veg": ["🍚 Rice + Dal", "🥗 Salad", "🫓 Roti + Curry"],
            "Non-Veg": ["🍗 Chicken Rice", "🐟 Fish Curry", "🍖 Egg Rice"]
        },
        "Dinner": {
            "Veg": ["🥣 Soup", "🫓 Roti + Paneer", "🍲 Khichdi"],
            "Non-Veg": ["🍗 Grilled Chicken", "🐟 Fish Fry", "🥚 Egg Curry"]
        },
        "Snacks": {
            "Veg": ["🥜 Nuts", "🍎 Apple"],
            "Non-Veg": ["🥚 Boiled Eggs", "🥜 Nuts"]
        },
        "Drinks": {
            "Veg": ["🥤 Buttermilk", "🍵 Green Tea"],
            "Non-Veg": ["🥤 Protein Shake", "🥛 Milk"]
        }
    }

    for meal in ["Breakfast", "Lunch", "Dinner"]:
        options = foods[meal][d["diet_pref"]]
        st.markdown(f"""
        <div class="card">
            <div class="meal-head">{meal}</div>
            <div class="meal-text">
                {options[0]} <br>
                {options[1]} <br>
                {options[2]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Snacks + Drinks
    snack = random.choice(foods["Snacks"][d["diet_pref"]])
    drink = random.choice(foods["Drinks"][d["diet_pref"]])

    cc1, cc2 = st.columns(2)

    with cc1:
        st.markdown(f"""
        <div class="card">
            <div class="meal-head">🥜 Snacks</div>
            <div class="meal-text">{snack}</div>
        </div>
        """, unsafe_allow_html=True)

    with cc2:
        st.markdown(f"""
        <div class="card">
            <div class="meal-head">🥤 Drink</div>
            <div class="meal-text">{drink}</div>
        </div>
        """, unsafe_allow_html=True)

    # Calories Graph
    st.markdown("""
    <h3 style="
    color:#f9f900;
    font-weight:900;
    margin-top:15px;
    margin-bottom:10px;
    ">
    📊 Daily Calories Overview
    </h3>
    """, unsafe_allow_html=True)

    calories_data = {
        "Breakfast": random.randint(250, 400),
        "Lunch": random.randint(450, 700),
        "Dinner": random.randint(350, 600),
        "Snacks": random.randint(100, 250)
    }

    fig_cal = go.Figure()
    fig_cal.add_trace(go.Bar(
        x=list(calories_data.keys()),
        y=list(calories_data.values()),
        text=list(calories_data.values()),
        textposition="outside",
        marker=dict(
            color="#f9f900",
            line=dict(color="#ffffff", width=1)
        )
    ))

    fig_cal.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#141414",
        font=dict(color="white", size=14),
        title=dict(
            text="Estimated Calories Per Meal",
            font=dict(size=20, color="white", family="Archivo Black, sans-serif")
        ),
        xaxis=dict(title="Meals", showgrid=False),
        yaxis=dict(title="Calories", gridcolor="rgba(255,255,255,0.08)"),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig_cal, use_container_width=True)

    if st.button("🔄 TRY AGAIN"):
        st.session_state.submitted = False
        st.rerun()