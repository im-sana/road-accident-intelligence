import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import json
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Road Accident Risk & Safety Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Academic BI Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a6496;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #f8f9fa;
        border-left: 4px solid #1a6496;
        padding: 1rem;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .kpi-card-danger {
        border-left-color: #e74c3c;
    }
    .kpi-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        color: #7f8c8d;
        font-weight: 600;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin-top: 0.2rem;
    }
    .kpi-subtitle {
        font-size: 0.8rem;
        color: #95a5a6;
    }
</style>
""", unsafe_allow_html=True)

# Set Matplotlib / Seaborn aesthetic
sns.set_style("whitegrid")
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'figure.dpi': 100,
    'axes.titlesize': 11,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8
})
SEV_COLORS = {'Slight': '#3498db', 'Serious': '#f39c12', 'Fatal': '#e74c3c'}

# --- DATA LOADERS (CACHED) ---
@st.cache_data
def load_kpis():
    with open('outputs/kpis.json', 'r') as f:
        return json.load(f)

@st.cache_data
def load_risk_summary():
    with open('outputs/risk_summary.json', 'r') as f:
        return json.load(f)

@st.cache_data
def load_data():
    df = pd.read_csv('data/cleaned_road_accidents.csv', low_memory=False)
    df['Accident Date'] = pd.to_datetime(df['Accident Date'], errors='coerce')
    df['Year'] = df['Year'].astype(int)
    for col in ['Number_of_Casualties', 'Number_of_Vehicles', 'Speed_limit', 'Latitude', 'Longitude']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# Load cached data
try:
    kpis = load_kpis()
    risk_summary = load_risk_summary()
    df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading project data files: {e}")
    data_loaded = False

if data_loaded:
    # --- 1. HEADER ---
    st.markdown('<div class="main-header">Road Accident Risk & Safety Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Data-driven analysis of accident patterns, risk factors and safety insights</div>', unsafe_allow_html=True)

    # Sidebar Filter Controls
    st.sidebar.header("🔍 Filter Options")
    selected_year = st.sidebar.selectbox("Select Year", ["All Years (2021-2022)", 2021, 2022])
    selected_severity = st.sidebar.multiselect("Select Severity", ["Slight", "Serious", "Fatal"], default=["Slight", "Serious", "Fatal"])
    selected_area = st.sidebar.radio("Area Filter", ["All Areas", "Urban", "Rural"])

    # Filter dataframe
    filtered_df = df.copy()
    if selected_year != "All Years (2021-2022)":
        filtered_df = filtered_df[filtered_df['Year'] == int(selected_year)]
    if selected_severity:
        filtered_df = filtered_df[filtered_df['Accident_Severity'].isin(selected_severity)]
    if selected_area != "All Areas":
        filtered_df = filtered_df[filtered_df['Urban_or_Rural_Area'] == selected_area]

    st.sidebar.markdown("---")
    st.sidebar.info(f"**Filtered Records:** {len(filtered_df):,} / {len(df):,}")

    # --- 2. KPI CARDS ---
    st.markdown("### 📊 Key Performance Indicators (KPIs)")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Accidents</div>
            <div class="kpi-value">{kpis['total_accidents']:,}</div>
            <div class="kpi-subtitle">2021: {kpis['year_2021_accidents']:,} | 2022: {kpis['year_2022_accidents']:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Casualties</div>
            <div class="kpi-value">{kpis['total_casualties']:,}</div>
            <div class="kpi-subtitle">Avg {kpis['avg_casualties_per_accident']} per accident</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card kpi-card-danger">
            <div class="kpi-title">Serious + Fatal Rate</div>
            <div class="kpi-value">{kpis['serious_fatal_rate_pct']}%</div>
            <div class="kpi-subtitle">{kpis['serious_fatal_count']:,} total severe incidents</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Year-over-Year Change</div>
            <div class="kpi-value">{kpis['yoy_change_2021_to_2022_pct']}%</div>
            <div class="kpi-subtitle">2021 → 2022 accident trend</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 3. TREND & SEVERITY ANALYSIS ---
    st.markdown("### 📈 Trend & Severity Analysis")
    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.subheader("Monthly Accident Trend")
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_series = filtered_df.groupby('Month').size().reindex(month_order).fillna(0)
        
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.plot(month_order, monthly_series.values, marker='o', color='#1a6496', linewidth=2, markersize=5)
        ax.fill_between(month_order, monthly_series.values, alpha=0.15, color='#1a6496')
        ax.set_ylabel("Accident Count")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        plt.tight_layout()
        st.pyplot(fig)

    with col_t2:
        st.subheader("Accident Severity Distribution")
        sev_counts = filtered_df['Accident_Severity'].value_counts()
        sev_order = ['Slight', 'Serious', 'Fatal']
        sev_vals = [sev_counts.get(s, 0) for s in sev_order]
        
        fig, ax = plt.subplots(figsize=(6, 3.5))
        wedges, texts, autotexts = ax.pie(
            sev_vals, labels=sev_order, autopct='%1.1f%%',
            colors=[SEV_COLORS[s] for s in sev_order], startangle=140,
            pctdistance=0.75, wedgeprops=dict(edgecolor='white', linewidth=1.5)
        )
        for t in autotexts: t.set_fontsize(8)
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")

    # --- 4. RISK FACTOR EXPLORER ---
    st.markdown("### ⚡ Risk Factor Analysis")
    factor = st.selectbox(
        "Select Factor to Analyze:",
        ["Time_Period", "Speed_limit", "Road_Surface_Conditions", "Light_Conditions", "Weather_Conditions", "Road_Type", "Vehicle_Type"]
    )

    f_col1, f_col2 = st.columns(2)

    with f_col1:
        st.subheader(f"Accident Count by {factor.replace('_', ' ')}")
        sub = filtered_df[filtered_df[factor] != 'Unknown'].copy()
        top_cats = sub[factor].value_counts().head(8).index
        sub = sub[sub[factor].isin(top_cats)]
        
        grp_count = sub.groupby([factor, 'Accident_Severity']).size().unstack(fill_value=0)
        for s in ['Slight', 'Serious', 'Fatal']:
            if s not in grp_count.columns: grp_count[s] = 0
        grp_count = grp_count.loc[grp_count.sum(axis=1).sort_values(ascending=False).index]

        fig, ax = plt.subplots(figsize=(6, 4))
        grp_count[['Slight', 'Serious', 'Fatal']].plot(
            kind='bar', stacked=True, color=[SEV_COLORS[s] for s in ['Slight', 'Serious', 'Fatal']],
            ax=ax, edgecolor='white', width=0.65
        )
        ax.set_xlabel('')
        ax.set_ylabel("Accidents")
        ax.set_xticklabels(grp_count.index, rotation=35, ha='right')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        plt.tight_layout()
        st.pyplot(fig)

    with f_col2:
        st.subheader(f"Serious + Fatal Rate (%) by {factor.replace('_', ' ')}")
        grp_risk = sub.groupby(factor).agg(
            total=('Accident_Severity', 'count'),
            serious_fatal=('Accident_Severity', lambda x: ((x == 'Fatal') | (x == 'Serious')).sum())
        )
        grp_risk['rate'] = (grp_risk['serious_fatal'] / grp_risk['total'] * 100).round(2)
        grp_risk = grp_risk[grp_risk['total'] >= 50].sort_values('rate', ascending=False).head(8)

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.barh(grp_risk.index[::-1], grp_risk['rate'][::-1], color='#e74c3c', edgecolor='white', height=0.55)
        for bar, val in zip(bars, grp_risk['rate'][::-1].values):
            ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, f"{val:.1f}%", va='center', fontsize=8, fontweight='bold')
        ax.set_xlabel("Serious + Fatal Rate (%)")
        ax.set_xlim(0, max(grp_risk['rate'].max() * 1.25, 10))
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("---")

    # --- 5. GEOGRAPHIC VIEW ---
    st.markdown("### 🗺️ Geographic Distribution View")
    st.caption("ℹ️ *Note: Scatter map displays recorded accident occurrence locations across the UK mainland, not exposure-adjusted risk rates.*")
    
    geo_df = filtered_df.dropna(subset=['Latitude', 'Longitude'])
    if len(geo_df) > 5000:
        # Subsample for ultra-fast performance on low-spec computers
        geo_sample = geo_df.sample(5000, random_state=42)
    else:
        geo_sample = geo_df

    st.map(geo_sample[['Latitude', 'Longitude']].rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}), zoom=5)

    st.markdown("---")

    # --- 6. KEY INSIGHTS ---
    st.markdown("### 💡 Key Academic Insights")
    
    ins_col1, ins_col2 = st.columns(2)
    with ins_col1:
        st.info("**Insight 1: Afternoon Volume vs. Night Severity**\nAfternoon (12-16:59) drives total accident volume, but **Night hours carry the highest Serious+Fatal rate (19.8%)** due to darkness, fatigue, and speed.")
        st.info("**Insight 2: Rural Road Fatality Risk**\nRural accidents account for ~35% of volume but exhibit a **20.2% Serious+Fatal rate** (vs 11.4% in Urban areas) due to higher speeds and longer EMS response times.")
        st.info("**Insight 3: High Speed Limit Impact**\n60-70 mph speed zones show Serious+Fatal rates above **20.8%**, compared to **11.9%** in 30 mph urban zones.")

    with ins_col2:
        st.warning("**Insight 4: Motorcycle Vulnerability**\nMotorcyclists experience Serious+Fatal rates between **22.5% and 28.4%** across all collision types due to lack of protective frames.")
        st.warning("**Insight 5: Adverse Surface Grip Loss**\nFrost/ice (17.5% severe) and flooded roads (22.2% severe) carry significantly higher injury severity than dry road surfaces (14.2% severe).")
        st.warning("**Insight 6: YoY Accident Volume Change**\nAccidents decreased by **11.70%** from 2021 (163,553) to 2022 (144,419). Reporting completeness across police forces should be verified.")

    st.markdown("---")

    # --- 7. RECOMMENDED ACTIONS ---
    st.markdown("### 🎯 Evidence-Based Recommended Actions")
    
    rec_data = [
        {"Priority": "🔴 HIGH", "Recommended Action": "Rural High-Speed Road Safety Audits", "Data Basis": "60-70 mph rural roads show >20% Serious+Fatal rate", "Target Stakeholder": "Transport Authorities"},
        {"Priority": "🔴 HIGH", "Recommended Action": "Night-time Speed & Impairment Enforcement", "Data Basis": "Night exhibits highest Serious+Fatal rate (19.8%)", "Target Stakeholder": "Traffic Police"},
        {"Priority": "🔴 HIGH", "Recommended Action": "Winter Gritting Prioritization", "Data Basis": "Frost/ice and flood surfaces show elevated severe rates", "Target Stakeholder": "Highways Maintenance"},
        {"Priority": "🟡 MEDIUM", "Recommended Action": "Motorcycle Safety & Blind-Spot Campaign", "Data Basis": "Motorcycles show up to 28.4% Serious+Fatal rate", "Target Stakeholder": "Road Safety Agencies"},
        {"Priority": "🟡 MEDIUM", "Recommended Action": "Afternoon Peak Speed Harmonization", "Data Basis": "15:00-18:00 represents peak hourly volume", "Target Stakeholder": "Urban Traffic Control"},
        {"Priority": "🟢 LOW", "Recommended Action": "Rural Emergency Response Optimization", "Data Basis": "High rural fatality proportion linked to response times", "Target Stakeholder": "Emergency Medical Services"}
    ]
    st.table(pd.DataFrame(rec_data))

    st.markdown("---")
    st.caption("Road Accident Risk & Safety Intelligence Dashboard | Built for BCA Academic Project Demonstration | Data Source: UK STATS19 (2021-2022)")
