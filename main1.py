# ====================================================
# Community Energy Land Allocation Dashboard
# ====================================================

import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Configure the page to use a wide layout
st.set_page_config(layout="wide")

# ----------------------------------------------------
# 1. Load Data
# ----------------------------------------------------
FILE_PATH = r"C:\Users\HP\Downloads\land_data_samarjeet.csv"

@st.cache_data
def load_data(path):
    try:
        if path.endswith('.csv'):
            df = pd.read_csv(path, sep=None, engine='python', encoding='utf-8-sig')
        else:
            df = pd.read_excel(path)
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error(f"❌ Error: The file was not found at {path}. Please check the file path.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        return pd.DataFrame()

df_original = load_data(FILE_PATH)
if df_original.empty:
    st.stop()

df = df_original.copy()
st.success(f"**File loaded successfully! Columns found:** `{', '.join(df.columns)}`")

# ----------------------------------------------------
# 2. Sidebar Controls
# ----------------------------------------------------
st.sidebar.title("⚙️ Settings")

# --- Map Settings Section ---
st.sidebar.subheader("Map Settings")
map_style = st.sidebar.selectbox(
    "Choose Map Style",
    options=["open-street-map", "carto-positron", "satellite-streets", "stamen-terrain"]
)
# --- Dropdown to control map color ---
color_choice = st.sidebar.selectbox(
    "Color Map Points By:",
    options=["Score", "FuelPovertyIndex", "SolarIrradiance", "GridDistance", "Energy_kWh"]
)

st.sidebar.subheader("Filter by Availability")
if 'AvailableFrom' in df.columns:
    df['AvailableFrom'] = pd.to_datetime(df['AvailableFrom'], format='%Y', errors='coerce')
    df.dropna(subset=['AvailableFrom'], inplace=True)
    show_available_only = st.sidebar.checkbox("✅ Show currently available land only", value=True)
    if show_available_only:
        df = df[df['AvailableFrom'].dt.date <= pd.Timestamp('today').date()]
else:
    st.sidebar.info("ℹ️ 'AvailableFrom' column not found.")

st.sidebar.subheader("Adjust Scoring Weights")
score_components = {
    "Social": {"column": "FuelPovertyIndex", "weight": 0.4, "formula": lambda col: col},
    "Technical": {"column": "SolarIrradiance", "weight": 0.3, "formula": lambda col: col},
    "Economic": {"column": "GridDistance", "weight": 0.2, "formula": lambda col: np.where(col > 0, (1 / col) * 1000, 0)},
    "Fairness": {"column": "ExistingProjects", "weight": 0.1, "formula": lambda col: 5 - col}
}

active_weights = {}
df["Score"] = 0
for name, comp in score_components.items():
    if comp["column"] in df.columns:
        weight = st.sidebar.slider(f"{name} Weight", 0.0, 1.0, comp["weight"], 0.05)
        active_weights[name] = weight
    else:
        st.sidebar.warning(f"⚠️ Missing '{comp['column']}'. '{name}' score is 0.")
        active_weights[name] = 0

wsum = sum(active_weights.values())
if wsum > 0:
    for name in active_weights:
        active_weights[name] /= wsum

for name, weight in active_weights.items():
    comp = score_components[name]
    if comp["column"] in df.columns and weight > 0:
        df["Score"] += weight * comp["formula"](df[comp["column"]])

# Energy & Impact Estimates
PANEL_EFFICIENCY = 0.15
HOUSEHOLD_CONSUMPTION = 3600
CARBON_FACTOR = 0.233

# Always initialize the columns to avoid errors
df["Energy_kWh"] = 0
df["Households"] = 0
df["CO2_tons"] = 0

if "SolarIrradiance" in df.columns and "Area_m2" in df.columns:
    df["Energy_kWh"] = df["Area_m2"] * df["SolarIrradiance"] * PANEL_EFFICIENCY
    df["Households"] = df["Energy_kWh"] / HOUSEHOLD_CONSUMPTION
    df["CO2_tons"] = (df["Energy_kWh"] * CARBON_FACTOR) / 1000
else:
    st.warning("⚠️ 'SolarIrradiance' or 'Area_m2' column not found. Energy impacts will be zero.")

# ----------------------------------------------------
# 5. Dashboard Layout
# ----------------------------------------------------
st.title("🌍 Community Energy Land Allocation Dashboard")
st.markdown("Identify and rank land parcels for community energy projects.")

c1, c2, c3 = st.columns(3)
c1.metric("⚡ Total Potential Energy (GWh)", f"{df['Energy_kWh'].sum()/1e6:.2f}")
c2.metric("🏡 Households Supported", f"{int(df['Households'].sum()):,}")
c3.metric("🌱 CO₂ Savings (tons/year)", f"{int(df['CO2_tons'].sum()):,}")

st.subheader("📊 Top Ranked Land Parcels")

base_table_cols = ["ID", "Zone", "Score", "Energy_kWh", "Households", "CO2_tons"]
if 'AvailableFrom' in df.columns:
    base_table_cols.append('AvailableFrom')

display_df = df.sort_values("Score", ascending=False).head(10).copy()
cols_to_show = [col for col in base_table_cols if col in display_df.columns]

if 'AvailableFrom' in cols_to_show:
    display_df['AvailableFrom'] = display_df['AvailableFrom'].dt.strftime('%Y')

st.dataframe(display_df[cols_to_show], hide_index=True)

st.subheader(f"🗺️ Map of Land Parcels (Colored by: {color_choice})")
if not df.empty and "Latitude" in df.columns and "Longitude" in df.columns:
    map_hover_cols = {"Score": ':.2f'}
    if "Households" in df.columns: map_hover_cols["Households"] = ':.1f'
    if "CO2_tons" in df.columns: map_hover_cols["CO2_tons"] = ':.2f'
    if 'AvailableFrom' in df.columns: map_hover_cols['AvailableFrom'] = True

    fig = px.scatter_mapbox(
        df, lat="Latitude", lon="Longitude",
        size="Area_m2",
        color=color_choice,
        color_continuous_scale="Viridis",
        hover_name="ID" if "ID" in df.columns else None,
        hover_data=map_hover_cols,
        zoom=10, height=600, center={"lat": 53.38, "lon": -1.47}
    )
    fig.update_layout(mapbox_style=map_style, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No land parcels to display or missing coordinate columns.")

# ----------------------------------------------------
# 6. Download Button
# ----------------------------------------------------
st.subheader("⬇️ Download Results")
st.download_button(
    label="Download Ranked Results as CSV",
    data=df.sort_values("Score", ascending=False).to_csv(index=False),
    file_name="ranked_land_parcels.csv",
    mime="text/csv"
)