"""
================================================================================
  🔴 CRIMEWATCH — Urban Crime Intelligence System
================================================================================
  Syllabus mapping:
    Unit 1 · Data Visualization   → 3D analytics, maps, trends
    Unit 2 · Streamlit Web App    → Every page · filters · widgets · state
    Unit 3 · Image Processing     → Evidence Lab (30+ CCTV/forensic operations)
    Unit 4 · Text Analysis        → Report Intelligence (classification + search)
================================================================================
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import HeatMap, MarkerCluster, Fullscreen
from streamlit_folium import st_folium
import cv2
from PIL import Image, ImageEnhance
import io, re, string, json, warnings
from datetime import datetime
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

from theme import inject_css, apply_theme, kpi_card, section, CHART_COLORS

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="CrimeWatch · Intelligence System",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ================================================================================
# DATA LOADING
# ================================================================================
@st.cache_data
def load_crime():
    return pd.read_csv("data/crime_data.csv")

@st.cache_data
def load_reports():
    return pd.read_csv("data/reports.csv")

@st.cache_data
def load_facts():
    with open("data/city_facts.json") as f:
        return json.load(f)

df_raw = load_crime()
reports_df = load_reports()
city_facts = load_facts()

# ================================================================================
# SIDEBAR
# ================================================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 14px 0 8px 0;'>
        <div style='font-family: Playfair Display, serif; font-weight: 900;
                    font-size: 2.15rem; line-height: 1;
                    background: linear-gradient(180deg, #F5F5F4 0%, #DC2626 100%);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            CRIMEWATCH
        </div>
        <div style='font-family: JetBrains Mono, monospace; font-size: 0.65rem;
                    color: #DC2626; letter-spacing: 0.3em; margin-top: 4px; font-weight: 700;'>
            URBAN INTELLIGENCE SYSTEM
        </div>
        <div style='margin-top: 10px;'>
            <span class='blink-dot'></span>
            <span style='font-family: JetBrains Mono, monospace; font-size: 0.65rem;
                         color: #DC2626; letter-spacing: 0.15em; font-weight: 700;'>LIVE · CLASSIFIED</span>
        </div>
    </div>
    <hr style='border-color: #27272A; margin: 12px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("**🧭 NAVIGATION**")
    page = st.radio(
        "Page",
        ["🎯 Command Center", "🗺️ Crime Atlas", "📊 3D Analytics",
         "🖼️ Evidence Lab", "📝 Report Intelligence", "ℹ️ About"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: #27272A;'>", unsafe_allow_html=True)

    # Filters
    st.markdown("**🎛️ FILTERS**")
    year_range = st.slider("Year", int(df_raw.Year.min()), int(df_raw.Year.max()),
                           (int(df_raw.Year.min()), int(df_raw.Year.max())))
    crime_filter = st.multiselect("Crime Types", sorted(df_raw.Crime_Type.unique()),
                                   default=sorted(df_raw.Crime_Type.unique()))
    severity_filter = st.multiselect("Severity",
                                      sorted(df_raw.Severity.unique()),
                                      default=sorted(df_raw.Severity.unique()))

    st.markdown("<hr style='border-color: #27272A;'>", unsafe_allow_html=True)
    st.markdown("**📚 MADE BY:-**")
    st.markdown("""
    <div style='font-family: JetBrains Mono, monospace; font-size: 0.9rem; line-height: 2; font-weight: 700;'>
    <span style='color:#10B981;'>●</span> VISHAL SHARMA<br>
    <span style='color:#10B981;'>●</span> VAIBHAV SAHU<br>
    <span style='color:#10B981;'>●</span> VINNER<br>
    </div>
    """, unsafe_allow_html=True)

    now = datetime.now().strftime("%d %b %Y · %H:%M")
    st.markdown(f"""
    <hr style='border-color: #27272A; margin: 12px 0;'>
    <div style='font-family: JetBrains Mono, monospace; font-size: 0.54rem;
                color: #57534E; text-align: center; line-height: 1.9; letter-spacing: 0.15em;'>
    DATA · {df_raw.City.nunique()} CITIES<br>
    {df_raw.Year.min()}–{df_raw.Year.max()} · {len(df_raw):,} RECORDS<br>
    ━━━━━━━━━━━━━━━━━<br>
    {now}
    </div>
    """, unsafe_allow_html=True)

# Apply filters
df = df_raw[
    df_raw.Year.between(*year_range) &
    df_raw.Crime_Type.isin(crime_filter) &
    df_raw.Severity.isin(severity_filter)
].copy()

# ================================================================================
# HERO
# ================================================================================
st.markdown('<div class="classified-strip">⚠ CLASSIFIED · FOR AUTHORIZED PERSONNEL ONLY · CLEARANCE LEVEL 3 ⚠</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="hero">CRIMEWATCH</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">URBAN CRIME INTELLIGENCE · DETECT · ANALYZE · PREVENT</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-divider"></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ================================================================================
# ROUTING
# ================================================================================

# ================================================================================
# PAGE: COMMAND CENTER
# ================================================================================
if page == "🎯 Command Center":
    latest = df[df.Year == df.Year.max()] if len(df) else df

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(220,38,38,0.15), rgba(153,27,27,0.05));
                border: 1px solid #27272A; border-left: 4px solid #DC2626;
                border-radius: 4px; padding: 22px 26px; margin-bottom: 20px;'>
        <div style='font-family: JetBrains Mono, monospace; font-size: 0.68rem;
                    color: #DC2626; letter-spacing: 0.28em; margin-bottom: 8px; font-weight: 700;'>
            ◆ SYSTEM OVERVIEW ◆
        </div>
        <div style='font-family: Playfair Display, serif; font-weight: 900; font-size: 2rem;
                    color: #F5F5F4; line-height: 1.2;'>
            Real-time Urban Crime Intelligence Platform
        </div>
        <div style='font-family: Inter; color: #A8A29E; margin-top: 8px; font-size: 0.92rem;'>
            Monitoring <b style='color:#F5F5F4;'>{df_raw.City.nunique()} cities</b> ·
            <b style='color:#F5F5F4;'>{len(df_raw):,} records</b> ·
            <b style='color:#F5F5F4;'>{df_raw.Crime_Type.nunique()} crime categories</b> ·
            <b style='color:#F5F5F4;'>{df_raw.Year.min()}–{df_raw.Year.max()}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    k = st.columns(6)
    kpi_card(k[0], "Total Cases", f"{df.Cases.sum():,}", "📋", "#DC2626")
    kpi_card(k[1], "Cities", df.City.nunique(), "🏙️", "#F59E0B")
    kpi_card(k[2], "Arrests", f"{df.Arrests.sum():,}", "🚔", "#FBBF24")
    kpi_card(k[3], "Resolution", f"{df.Resolution_Rate.mean()*100:.1f}%", "✓", "#10B981")
    kpi_card(k[4], "Avg Response", f"{df.Response_Time_Min.mean():.0f} min", "⏱️", "#991B1B")
    kpi_card(k[5], "Critical", f"{(df.Severity=='Critical').sum():,}", "🚨", "#DC2626")

    # Features
    section("MODULES")
    fc = st.columns(3)
    features = [
        ("🗺️", "CRIME ATLAS", "Interactive hotspot maps with Folium, heatmaps, and city-level choropleths.", "#DC2626"),
        ("📊", "3D ANALYTICS", "Three-dimensional crime frequency bars, histograms, and trend surfaces.", "#F59E0B"),
        ("🖼️", "EVIDENCE LAB", "30+ image forensic tools for CCTV enhancement, segmentation, and feature detection.", "#FBBF24"),
        ("📝", "REPORT INTELLIGENCE", "Auto-classify crime reports with ML (Naive Bayes, LogReg, SVM) + similarity search.", "#991B1B"),
        ("📈", "TREND FORECAST", "Temporal patterns, seasonal analysis, and year-over-year comparisons.", "#DC2626"),
        ("🎯", "CASE TRACKING", "Severity-based triage, resolution rates, and response time monitoring.", "#F59E0B"),
    ]
    for i, (ic, t, d, c) in enumerate(features):
        with fc[i % 3]:
            st.markdown(f"""
            <div class='feature-tile fade-in' style='border-top: 3px solid {c}; margin-bottom: 12px;'>
                <span class='feature-icon'>{ic}</span>
                <div class='feature-title'>{t}</div>
                <div class='feature-desc'>{d}</div>
            </div>
            """, unsafe_allow_html=True)

    # Top crime cities chart
    section("⚠ HIGHEST CRIME CITIES", "blood")
    if len(df):
        city_tot = df.groupby('City').agg(Cases=('Cases','sum'), Pop=('Population_M','first')).reset_index()
        city_tot['Per_Capita'] = city_tot['Cases'] / city_tot['Pop']
        city_tot = city_tot.sort_values('Cases', ascending=False).head(15)
        fig = px.bar(city_tot, x='City', y='Cases', color='Cases',
                     color_continuous_scale=[[0,"#450A0A"],[0.5,"#991B1B"],[1,"#DC2626"]],
                     title=f"TOP 15 CITIES BY TOTAL CASES · {df.Year.min()}–{df.Year.max()}")
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    # Crime breakdown
    section("CRIME BREAKDOWN", "amber")
    cb1, cb2 = st.columns([3, 2])
    with cb1:
        ct = df.groupby('Crime_Type').Cases.sum().reset_index().sort_values('Cases', ascending=True)
        fig = px.bar(ct, x='Cases', y='Crime_Type', orientation='h',
                     color='Cases', color_continuous_scale=[[0,"#44403C"],[1,"#DC2626"]],
                     title="CASES BY CRIME TYPE")
        st.plotly_chart(apply_theme(fig), use_container_width=True)
    with cb2:
        sev = df.groupby('Severity').Cases.sum().reset_index()
        sev_order = ["Low", "Medium", "High", "Critical"]
        sev['Severity'] = pd.Categorical(sev.Severity, categories=sev_order, ordered=True)
        sev = sev.sort_values('Severity')
        colors = ["#57534E", "#F59E0B", "#991B1B", "#DC2626"]
        fig = go.Figure(go.Pie(labels=sev.Severity, values=sev.Cases, hole=0.6,
                                marker=dict(colors=colors, line=dict(color="#151519", width=2))))
        fig.update_layout(title="SEVERITY DISTRIBUTION")
        fig.add_annotation(text=f"<b>{df.Cases.sum():,}</b>", x=0.5, y=0.5,
                          showarrow=False, font=dict(size=24, color="white", family="Oswald"))
        st.plotly_chart(apply_theme(fig), use_container_width=True)

# ================================================================================
# PAGE: CRIME ATLAS
# ================================================================================
elif page == "🗺️ Crime Atlas":
    section("🗺️ CRIME ATLAS · GEOSPATIAL INTELLIGENCE")

    if not len(df):
        st.warning("No data matches current filters")
    else:
        city_agg = df.groupby(['City','Lat','Lon','State']).agg(
            Cases=('Cases','sum'), Arrests=('Arrests','sum'),
            Resolution=('Resolution_Rate','mean')).reset_index()

        k = st.columns(4)
        kpi_card(k[0], "Cities", len(city_agg), "🏙️", "#DC2626")
        kpi_card(k[1], "Hotspots", (city_agg.Cases > city_agg.Cases.median()).sum(), "🔴", "#F59E0B")
        kpi_card(k[2], "States", df.State.nunique(), "🗺️", "#FBBF24")
        kpi_card(k[3], "Total Cases", f"{city_agg.Cases.sum():,}", "📋", "#991B1B")

        atlas_tabs = st.tabs(["🔴 HOTSPOT MAP", "🔥 HEATMAP", "📍 CLUSTERS", "📊 STATE CHOROPLETH"])

        with atlas_tabs[0]:
            sel_metric = st.selectbox("Metric", ["Cases", "Arrests"], key="am1")
            m = folium.Map(location=[22.5, 79], zoom_start=5, tiles="CartoDB dark_matter")
            Fullscreen().add_to(m)
            mx = city_agg[sel_metric].max()
            for _, r in city_agg.iterrows():
                rad = 6 + (r[sel_metric]/mx) * 30
                ratio = r[sel_metric]/mx
                col = "#DC2626" if ratio > 0.66 else ("#F59E0B" if ratio > 0.33 else "#FBBF24")
                popup = f"""
                <div style='font-family: Inter; min-width: 200px;'>
                    <h4 style='color: #DC2626; margin: 0 0 6px 0;'>{r.City}</h4>
                    <b>State:</b> {r.State}<br>
                    <b>Total Cases:</b> {r.Cases:,}<br>
                    <b>Arrests:</b> {r.Arrests:,}<br>
                    <b>Resolution:</b> {r.Resolution*100:.1f}%
                </div>"""
                folium.CircleMarker(
                    [r.Lat, r.Lon], radius=rad,
                    popup=folium.Popup(popup, max_width=260),
                    tooltip=f"{r.City} · {r[sel_metric]:,}",
                    color=col, fill=True, fillColor=col, fillOpacity=0.65, weight=2
                ).add_to(m)
            st_folium(m, width=1400, height=580, returned_objects=[])

        with atlas_tabs[1]:
            st.markdown('<div class="info-box">🔥 Heatmap intensity = case density. Darker/redder = more crime.</div>', unsafe_allow_html=True)
            mh = folium.Map(location=[22.5, 79], zoom_start=5, tiles="CartoDB dark_matter")
            hd = [[r.Lat, r.Lon, r.Cases] for _, r in city_agg.iterrows()]
            HeatMap(hd, radius=32, blur=22,
                    gradient={0.2: '#FBBF24', 0.5: '#F59E0B', 0.8: '#991B1B', 1.0: '#DC2626'}).add_to(mh)
            st_folium(mh, width=1400, height=580, returned_objects=[])

        with atlas_tabs[2]:
            mc = folium.Map(location=[22.5, 79], zoom_start=5, tiles="CartoDB dark_matter")
            cluster = MarkerCluster().add_to(mc)
            for _, r in df.groupby(['City','Lat','Lon']).Cases.sum().reset_index().iterrows():
                folium.Marker([r.Lat, r.Lon],
                              popup=f"<b>{r.City}</b><br>Cases: {r.Cases:,}",
                              tooltip=r.City,
                              icon=folium.Icon(color='red', icon='info-sign')).add_to(cluster)
            st_folium(mc, width=1400, height=580, returned_objects=[])

        with atlas_tabs[3]:
            state_agg = df.groupby('State').Cases.sum().reset_index().sort_values('Cases', ascending=False)
            fig = px.bar(state_agg, x='State', y='Cases', color='Cases',
                         color_continuous_scale=[[0,"#57534E"],[0.5,"#F59E0B"],[1,"#DC2626"]],
                         title="CASES BY STATE")
            st.plotly_chart(apply_theme(fig), use_container_width=True)

# ================================================================================
# PAGE: 3D ANALYTICS
# ================================================================================
elif page == "📊 3D Analytics":
    section("📊 3D ANALYTICS")

    if not len(df):
        st.warning("No data matches filters")
    else:
        k = st.columns(4)
        kpi_card(k[0], "Total Cases", f"{df.Cases.sum():,}", "📋", "#DC2626")
        kpi_card(k[1], "Peak Year", int(df.groupby('Year').Cases.sum().idxmax()), "📈", "#F59E0B")
        kpi_card(k[2], "Peak Month", int(df.groupby('Month').Cases.sum().idxmax()), "📅", "#FBBF24")
        kpi_card(k[3], "Top Crime", df.groupby('Crime_Type').Cases.sum().idxmax(), "⚠️", "#991B1B")

        viz_tabs = st.tabs(["🎯 3D BARS", "📊 3D HEATMAP", "🌐 3D SCATTER", "🏔️ 3D SURFACE", "🎬 ANIMATED"])

        with viz_tabs[0]:
            c1, c2 = st.columns([1, 3])
            with c1:
                yr3d = st.slider("Year", int(df.Year.min()), int(df.Year.max()), int(df.Year.max()), key="y3")
                cm = st.selectbox("Colormap", ["Reds", "YlOrRd", "inferno", "magma"], key="cm3")
                st.markdown('<div class="info-box">🎯 Each bar = city/crime combination for the selected year.</div>', unsafe_allow_html=True)
            with c2:
                yd = df[df.Year == yr3d].groupby(['City','Crime_Type']).Cases.sum().reset_index()
                pivot = yd.pivot(index='City', columns='Crime_Type', values='Cases').fillna(0)
                # show top 12 cities only
                top_cities = pivot.sum(axis=1).nlargest(12).index
                pivot = pivot.loc[top_cities]
                if len(pivot):
                    fig = plt.figure(figsize=(14, 8), facecolor='#151519')
                    ax = fig.add_subplot(111, projection='3d')
                    ax.set_facecolor('#151519')
                    xp, yp = np.meshgrid(np.arange(pivot.shape[1]), np.arange(pivot.shape[0]), indexing="xy")
                    xp = xp.ravel(); yp = yp.ravel()
                    dz = pivot.values.ravel()
                    colors = plt.get_cmap(cm)(dz / max(dz.max(), 1))
                    ax.bar3d(xp, yp, 0, 0.8, 0.8, dz, color=colors, alpha=0.9, edgecolor='#DC2626', linewidth=0.3)
                    ax.set_xticks(np.arange(pivot.shape[1]))
                    ax.set_xticklabels(pivot.columns, rotation=50, ha='right', color='white', fontsize=8)
                    ax.set_yticks(np.arange(pivot.shape[0]))
                    ax.set_yticklabels(pivot.index, color='white', fontsize=8)
                    ax.set_zlabel('Cases', color='white', fontsize=10)
                    ax.set_title(f'CRIME FREQUENCY · TOP 12 CITIES × CRIME TYPE · {yr3d}',
                                 color='white', fontsize=13, pad=20, fontweight='bold')
                    ax.tick_params(colors='white')
                    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
                        pane.fill = False
                        pane.set_edgecolor('#27272A')
                    plt.tight_layout()
                    st.pyplot(fig)

        with viz_tabs[1]:
            heat = df.groupby(['Year','Month']).Cases.sum().reset_index()
            heat_pivot = heat.pivot(index='Month', columns='Year', values='Cases').fillna(0)
            fig = plt.figure(figsize=(13, 7), facecolor='#151519')
            ax = fig.add_subplot(111, projection='3d')
            ax.set_facecolor('#151519')
            xp, yp = np.meshgrid(np.arange(heat_pivot.shape[1]), np.arange(heat_pivot.shape[0]), indexing="xy")
            xp = xp.ravel(); yp = yp.ravel()
            dz = heat_pivot.values.ravel()
            colors = plt.cm.inferno(dz / max(dz.max(), 1))
            ax.bar3d(xp, yp, 0, 0.85, 0.85, dz, color=colors, alpha=0.88, edgecolor='#F59E0B', linewidth=0.2)
            ax.set_xticks(np.arange(heat_pivot.shape[1]))
            ax.set_xticklabels(heat_pivot.columns, color='white', fontsize=9)
            ax.set_yticks(np.arange(heat_pivot.shape[0]))
            ax.set_yticklabels(heat_pivot.index, color='white', fontsize=8)
            ax.set_zlabel('Cases', color='white', fontsize=10)
            ax.set_title('TEMPORAL HEATMAP · YEAR × MONTH', color='white', fontsize=13, fontweight='bold')
            ax.tick_params(colors='white')
            for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
                pane.fill = False
            plt.tight_layout()
            st.pyplot(fig)

        with viz_tabs[2]:
            scatter_df = df.groupby(['City','Lat','Lon']).agg(
                Cases=('Cases','sum'), Arrests=('Arrests','sum'),
                Resolution=('Resolution_Rate','mean'), Pop=('Population_M','first')).reset_index()
            fig = go.Figure(data=[go.Scatter3d(
                x=scatter_df.Pop, y=scatter_df.Cases, z=scatter_df.Resolution*100,
                mode='markers+text',
                text=scatter_df.City,
                textposition='top center',
                textfont=dict(size=9, color='white'),
                marker=dict(
                    size=np.clip(scatter_df.Arrests / scatter_df.Arrests.max() * 30 + 5, 5, 35),
                    color=scatter_df.Cases,
                    colorscale='Reds', showscale=True,
                    colorbar=dict(title="Cases"),
                    opacity=0.85, line=dict(color='white', width=0.5)
                ),
                hovertemplate='<b>%{text}</b><br>Pop: %{x:.1f}M<br>Cases: %{y:,}<br>Resolution: %{z:.1f}%<extra></extra>'
            )])
            fig.update_layout(
                title="3D SCATTER · POPULATION × CASES × RESOLUTION RATE",
                scene=dict(
                    xaxis=dict(title="Pop (M)", backgroundcolor="#151519", gridcolor="#27272A", color="white"),
                    yaxis=dict(title="Cases", backgroundcolor="#151519", gridcolor="#27272A", color="white"),
                    zaxis=dict(title="Resolution %", backgroundcolor="#151519", gridcolor="#27272A", color="white"),
                    bgcolor="#151519"
                ),
                paper_bgcolor="#151519", font=dict(color="white", family="Inter"), height=660
            )
            st.plotly_chart(fig, use_container_width=True)

        with viz_tabs[3]:
            top_ct = df.groupby('Crime_Type').Cases.sum().nlargest(8).index
            surf = df[df.Crime_Type.isin(top_ct)].groupby(['Year','Crime_Type']).Cases.sum().reset_index()
            surf_pivot = surf.pivot(index='Year', columns='Crime_Type', values='Cases').fillna(0)
            fig = go.Figure(data=[go.Surface(
                z=surf_pivot.values, x=surf_pivot.columns, y=surf_pivot.index,
                colorscale='Inferno',
                contours=dict(z=dict(show=True, usecolormap=True, highlightcolor="#DC2626", project_z=True))
            )])
            fig.update_layout(
                title="CRIME SURFACE · TYPE × YEAR",
                scene=dict(
                    xaxis=dict(title="Crime Type", backgroundcolor="#151519", gridcolor="#27272A", color="white"),
                    yaxis=dict(title="Year", backgroundcolor="#151519", gridcolor="#27272A", color="white"),
                    zaxis=dict(title="Cases", backgroundcolor="#151519", gridcolor="#27272A", color="white"),
                    bgcolor="#151519"
                ),
                paper_bgcolor="#151519", font=dict(color="white"), height=660
            )
            st.plotly_chart(fig, use_container_width=True)

        with viz_tabs[4]:
            st.markdown('<div class="info-box">🎬 Press ▶ to watch crime patterns evolve over years.</div>', unsafe_allow_html=True)
            anim = df.groupby(['Year','City']).Cases.sum().reset_index()
            top_cit = anim.groupby('City').Cases.sum().nlargest(15).index
            anim = anim[anim.City.isin(top_cit)].sort_values('Cases', ascending=True)
            fig = px.bar(anim, x='Cases', y='City', orientation='h',
                         animation_frame='Year', color='Cases',
                         color_continuous_scale=[[0,"#57534E"],[0.5,"#F59E0B"],[1,"#DC2626"]],
                         range_x=[0, anim.Cases.max() * 1.05],
                         title="🏁 ANIMATED RACE · CRIME CASES BY CITY",
                         height=640)
            st.plotly_chart(apply_theme(fig), use_container_width=True)

# ================================================================================
# PAGE: EVIDENCE LAB
# ================================================================================
elif page == "🖼️ Evidence Lab":
    section("🖼️ EVIDENCE LAB · FORENSIC IMAGE ANALYSIS")
    st.markdown('<div class="info-box">📸 Upload CCTV footage, evidence photos, or use a demo image. Apply 30+ forensic operations.</div>', unsafe_allow_html=True)

    uc = st.columns([2, 1, 1])
    with uc[0]:
        uploaded = st.file_uploader("Upload Evidence", type=['png','jpg','jpeg','bmp','webp'])
    with uc[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        demo_cctv = st.button("🎥 Demo: CCTV Scene")
    with uc[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        demo_night = st.button("🌃 Demo: Night Shot")

    img_bytes = None
    if uploaded:
        img_bytes = uploaded.read()
    elif demo_cctv or 'demo_cctv' in st.session_state:
        if demo_cctv:
            # Synthetic "CCTV" style image
            demo = np.ones((400, 600, 3), dtype=np.uint8) * 40
            # Ground
            demo[300:, :] = [60, 55, 50]
            # Add rectangles (buildings)
            for i, x in enumerate([50, 200, 380]):
                h = np.random.randint(100, 200)
                cv2.rectangle(demo, (x, 300-h), (x+120, 300), (80+i*15, 75+i*10, 70+i*8), -1)
                for wy in range(300-h+15, 295, 20):
                    for wx in range(x+10, x+115, 18):
                        cv2.rectangle(demo, (wx, wy), (wx+8, wy+10), (220, 210, 140), -1)
            # Simulated person (blob)
            cv2.circle(demo, (400, 270), 12, (180, 150, 120), -1)
            cv2.rectangle(demo, (392, 280), (408, 320), (90, 60, 100), -1)
            # Add noise (CCTV grain)
            noise = np.random.randint(-25, 25, demo.shape, dtype=np.int16)
            demo = np.clip(demo.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            # Timestamp overlay
            cv2.putText(demo, "CAM 04 // 2024-08-15 23:47:12", (15, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (230, 230, 230), 1)
            cv2.rectangle(demo, (15, 370), (140, 390), (0, 0, 0), -1)
            cv2.putText(demo, "REC", (25, 385),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 220), 2)
            cv2.circle(demo, (80, 380), 4, (0, 0, 220), -1)
            b = io.BytesIO()
            Image.fromarray(demo).save(b, format='PNG')
            st.session_state['demo_cctv'] = b.getvalue()
        img_bytes = st.session_state.get('demo_cctv')
    elif demo_night or 'demo_night' in st.session_state:
        if demo_night:
            demo = np.ones((400, 600, 3), dtype=np.uint8) * 15
            # Street gradient
            for y in range(200, 400):
                c = int(15 + (y-200) * 0.3)
                demo[y, :] = [c, c, c+5]
            # Streetlight pools
            for px_ in [150, 450]:
                for y in range(200, 400):
                    for x in range(max(0,px_-80), min(600, px_+80)):
                        dist = np.sqrt((x-px_)**2 + (y-180)**2)
                        if dist < 100:
                            boost = int(80 * (1 - dist/100))
                            demo[y, x] = np.clip(demo[y, x] + [boost, boost-5, boost-15], 0, 255)
            # Figures in shadow
            cv2.rectangle(demo, (290, 250), (310, 330), (45, 42, 48), -1)
            cv2.circle(demo, (300, 240), 10, (55, 50, 55), -1)
            # Heavy noise
            noise = np.random.randint(-30, 30, demo.shape, dtype=np.int16)
            demo = np.clip(demo.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            cv2.putText(demo, "LOW LIGHT // ENHANCE", (15, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
            b = io.BytesIO()
            Image.fromarray(demo).save(b, format='PNG')
            st.session_state['demo_night'] = b.getvalue()
        img_bytes = st.session_state.get('demo_night')

    if img_bytes:
        pil = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        img = np.array(pil)

        section("📋 EVIDENCE PROPERTIES")
        pc = st.columns(6)
        kpi_card(pc[0], "Width", f"{img.shape[1]}px", "↔️", "#DC2626")
        kpi_card(pc[1], "Height", f"{img.shape[0]}px", "↕️", "#F59E0B")
        kpi_card(pc[2], "Channels", img.shape[2] if len(img.shape) == 3 else 1, "🎨", "#FBBF24")
        kpi_card(pc[3], "Pixels", f"{img.shape[0]*img.shape[1]:,}", "⬛", "#991B1B")
        kpi_card(pc[4], "Dtype", str(img.dtype), "🔢", "#DC2626")
        kpi_card(pc[5], "Mean", f"{img.mean():.0f}", "📊", "#F59E0B")

        section("🔬 FORENSIC OPERATIONS", "amber")
        cat = st.radio("Category", [
            "📐 Transformations", "🎛️ Filtering", "✨ Enhancement",
            "✂️ Segmentation", "🔍 Feature Detection", "😀 Face Detection"
        ], horizontal=True)

        processed = img.copy()
        op_name = "Original"

        if cat == "📐 Transformations":
            op = st.selectbox("Op", ["Grayscale","Rotation","Resize","Flip","Crop","HSV","LAB","YCrCb"])
            op_name = op
            if op == "Grayscale":
                processed = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            elif op == "Rotation":
                a = st.slider("Angle", -180, 180, 45)
                (h, w) = img.shape[:2]
                M = cv2.getRotationMatrix2D((w//2, h//2), a, 1.0)
                processed = cv2.warpAffine(img, M, (w, h))
            elif op == "Resize":
                s = st.slider("Scale %", 10, 200, 50)
                processed = cv2.resize(img, (int(img.shape[1]*s/100), int(img.shape[0]*s/100)))
            elif op == "Flip":
                d = st.radio("Direction", ["Horizontal","Vertical","Both"], horizontal=True)
                code = 1 if d == "Horizontal" else (0 if d == "Vertical" else -1)
                processed = cv2.flip(img, code)
            elif op == "Crop":
                h, w = img.shape[:2]
                x1 = st.slider("Left", 0, w-1, 0)
                y1 = st.slider("Top", 0, h-1, 0)
                x2 = st.slider("Right", x1+1, w, w)
                y2 = st.slider("Bottom", y1+1, h, h)
                processed = img[y1:y2, x1:x2]
            elif op == "HSV":
                processed = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            elif op == "LAB":
                processed = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
            elif op == "YCrCb":
                processed = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)

        elif cat == "🎛️ Filtering":
            op = st.selectbox("Op", ["Gaussian Blur","Median Blur","Bilateral","Sharpen","Emboss","Custom Kernel","Motion Blur","Denoise"])
            op_name = op
            if op == "Gaussian Blur":
                k = st.slider("Kernel", 1, 51, 15, step=2)
                processed = cv2.GaussianBlur(img, (k, k), 0)
            elif op == "Median Blur":
                k = st.slider("Kernel", 1, 25, 5, step=2)
                processed = cv2.medianBlur(img, k)
            elif op == "Bilateral":
                d = st.slider("Diameter", 5, 25, 9)
                processed = cv2.bilateralFilter(img, d, 75, 75)
            elif op == "Sharpen":
                i = st.slider("Intensity", 1, 10, 5)
                kernel = np.array([[0,-1,0],[-1,i,-1],[0,-1,0]])
                processed = cv2.filter2D(img, -1, kernel)
            elif op == "Emboss":
                kernel = np.array([[-2,-1,0],[-1,1,1],[0,1,2]])
                processed = cv2.filter2D(img, -1, kernel)
            elif op == "Custom Kernel":
                st.markdown("**3×3 Kernel:**")
                rows = []
                for i in range(3):
                    ck = st.columns(3)
                    r = []
                    for j in range(3):
                        v = ck[j].number_input(f"[{i},{j}]", -5.0, 5.0,
                                                1.0 if i==1 and j==1 else 0.0, 0.1, key=f"k{i}{j}")
                        r.append(v)
                    rows.append(r)
                processed = cv2.filter2D(img, -1, np.array(rows))
            elif op == "Motion Blur":
                size = st.slider("Size", 3, 25, 9)
                kernel = np.zeros((size, size))
                kernel[size // 2, :] = 1.0 / size
                processed = cv2.filter2D(img, -1, kernel)
            elif op == "Denoise":
                h_val = st.slider("Strength", 1, 30, 10)
                processed = cv2.fastNlMeansDenoisingColored(img, None, h_val, h_val, 7, 21)

        elif cat == "✨ Enhancement":
            op = st.selectbox("Op", ["Brightness","Contrast","Saturation","Hist Equalization","CLAHE","Gamma","Unsharp Mask","Sepia"])
            op_name = op
            if op == "Brightness":
                f = st.slider("Factor", 0.1, 3.0, 1.5)
                processed = np.array(ImageEnhance.Brightness(pil).enhance(f))
            elif op == "Contrast":
                f = st.slider("Factor", 0.1, 3.0, 1.5)
                processed = np.array(ImageEnhance.Contrast(pil).enhance(f))
            elif op == "Saturation":
                f = st.slider("Factor", 0.0, 3.0, 1.5)
                processed = np.array(ImageEnhance.Color(pil).enhance(f))
            elif op == "Hist Equalization":
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                processed = cv2.equalizeHist(gray)
            elif op == "CLAHE":
                c = st.slider("Clip", 1.0, 10.0, 2.0)
                lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=c, tileGridSize=(8,8))
                l = clahe.apply(l)
                processed = cv2.cvtColor(cv2.merge([l,a,b]), cv2.COLOR_LAB2RGB)
            elif op == "Gamma":
                g = st.slider("Gamma", 0.1, 3.0, 1.0)
                table = np.array([((i/255.0)**(1.0/g))*255 for i in np.arange(256)]).astype("uint8")
                processed = cv2.LUT(img, table)
            elif op == "Unsharp Mask":
                amt = st.slider("Amount", 0.1, 3.0, 1.5)
                blur = cv2.GaussianBlur(img, (9, 9), 10)
                processed = cv2.addWeighted(img, 1+amt, blur, -amt, 0)
            elif op == "Sepia":
                kernel = np.array([[0.272,0.534,0.131],[0.349,0.686,0.168],[0.393,0.769,0.189]])
                processed = cv2.transform(img, kernel)
                processed = np.clip(processed, 0, 255).astype(np.uint8)

        elif cat == "✂️ Segmentation":
            op = st.selectbox("Op", ["Binary Thresh","Adaptive Thresh","Otsu","K-Means Colors","HSV Mask"])
            op_name = op
            if op == "Binary Thresh":
                t = st.slider("Thresh", 0, 255, 127)
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                _, processed = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)
            elif op == "Adaptive Thresh":
                bs = st.slider("Block", 3, 51, 11, step=2)
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                  cv2.THRESH_BINARY, bs, 2)
            elif op == "Otsu":
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                _, processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            elif op == "K-Means Colors":
                k = st.slider("K", 2, 12, 5)
                Z = img.reshape((-1, 3)).astype(np.float32)
                crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
                _, lb, ct = cv2.kmeans(Z, k, None, crit, 10, cv2.KMEANS_RANDOM_CENTERS)
                processed = np.uint8(ct)[lb.flatten()].reshape(img.shape)
            elif op == "HSV Mask":
                hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
                h1 = st.slider("H min", 0, 179, 0)
                h2 = st.slider("H max", 0, 179, 179)
                s1 = st.slider("S min", 0, 255, 50)
                s2 = st.slider("S max", 0, 255, 255)
                v1 = st.slider("V min", 0, 255, 50)
                v2 = st.slider("V max", 0, 255, 255)
                mask = cv2.inRange(hsv, np.array([h1,s1,v1]), np.array([h2,s2,v2]))
                processed = cv2.bitwise_and(img, img, mask=mask)

        elif cat == "🔍 Feature Detection":
            op = st.selectbox("Op", ["Canny","Sobel","Laplacian","Contours","Harris Corners","ORB Keypoints"])
            op_name = op
            if op == "Canny":
                t1 = st.slider("T1", 0, 500, 100)
                t2 = st.slider("T2", 0, 500, 200)
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                processed = cv2.Canny(gray, t1, t2)
            elif op == "Sobel":
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
                sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
                processed = np.uint8(np.clip(np.sqrt(sx**2+sy**2), 0, 255))
            elif op == "Laplacian":
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                processed = np.uint8(np.clip(np.abs(cv2.Laplacian(gray, cv2.CV_64F)), 0, 255))
            elif op == "Contours":
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                _, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                processed = img.copy()
                cv2.drawContours(processed, contours, -1, (220, 38, 38), 2)
                st.success(f"🔍 Detected **{len(contours)}** objects")
            elif op == "Harris Corners":
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32)
                dst = cv2.cornerHarris(gray, 2, 3, 0.04)
                dst = cv2.dilate(dst, None)
                processed = img.copy()
                processed[dst > 0.01 * dst.max()] = [245, 158, 11]
            elif op == "ORB Keypoints":
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                orb = cv2.ORB_create(nfeatures=500)
                kp = orb.detect(gray, None)
                processed = cv2.drawKeypoints(img, kp, None, color=(220, 38, 38),
                                              flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                st.success(f"🔍 Detected **{len(kp)}** ORB keypoints")

        elif cat == "😀 Face Detection":
            op_name = "Face Detection"
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            try:
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
                sf = st.slider("Scale Factor", 1.05, 2.0, 1.1, 0.05)
                mn = st.slider("Min Neighbors", 1, 10, 5)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=sf, minNeighbors=mn)
                processed = img.copy()
                detect_eyes = st.checkbox("Detect eyes too", True)
                for (x, y, w, h) in faces:
                    cv2.rectangle(processed, (x, y), (x+w, y+h), (220, 38, 38), 3)
                    cv2.putText(processed, "SUSPECT", (x, y-8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (220, 38, 38), 2)
                    if detect_eyes:
                        eyes = eye_cascade.detectMultiScale(gray[y:y+h, x:x+w])
                        for (ex, ey, ew, eh) in eyes:
                            cv2.rectangle(processed, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (245, 158, 11), 2)
                st.success(f"😀 Detected **{len(faces)}** face(s)")
            except Exception as e:
                st.warning(f"Face detection unavailable: {e}")

        # Before / After
        section("🔍 BEFORE & AFTER")
        b_cols = st.columns(2)
        with b_cols[0]:
            st.markdown("**📥 ORIGINAL**")
            st.image(img, use_container_width=True)
        with b_cols[1]:
            st.markdown(f"**✨ {op_name.upper()}**")
            if len(processed.shape) == 2:
                st.image(processed, use_container_width=True, clamp=True)
            else:
                st.image(processed, use_container_width=True)

        # Download
        if len(processed.shape) == 3:
            out_pil = Image.fromarray(processed.astype(np.uint8))
        else:
            out_pil = Image.fromarray(processed.astype(np.uint8))
        buf = io.BytesIO()
        out_pil.save(buf, format='PNG')
        st.download_button("💾 DOWNLOAD EVIDENCE", buf.getvalue(), f"evidence_{op_name}.png", "image/png")

        # Histograms
        section("📊 PIXEL INTENSITY ANALYSIS", "amber")
        h1, h2 = st.columns(2)
        colors = ('#DC2626', '#10B981', '#3B82F6')
        with h1:
            fig, ax = plt.subplots(figsize=(8, 3.6), facecolor='#151519')
            ax.set_facecolor('#151519')
            for i, c in enumerate(colors):
                hist = cv2.calcHist([img], [i], None, [256], [0, 256])
                ax.plot(hist, color=c, alpha=0.85, linewidth=1.5, label=['R','G','B'][i])
                ax.fill_between(range(256), hist.flatten(), alpha=0.2, color=c)
            ax.set_title('ORIGINAL RGB', color='white', fontweight='bold')
            ax.tick_params(colors='white')
            ax.legend(facecolor='#151519', edgecolor='#27272A', labelcolor='white')
            ax.grid(color='#27272A')
            for s in ax.spines.values():
                s.set_edgecolor('#3F3F46')
            st.pyplot(fig)
        with h2:
            fig2, ax2 = plt.subplots(figsize=(8, 3.6), facecolor='#151519')
            ax2.set_facecolor('#151519')
            if len(processed.shape) == 3:
                for i, c in enumerate(colors):
                    hist = cv2.calcHist([processed], [i], None, [256], [0, 256])
                    ax2.plot(hist, color=c, alpha=0.85, linewidth=1.5, label=['R','G','B'][i])
                    ax2.fill_between(range(256), hist.flatten(), alpha=0.2, color=c)
                ax2.legend(facecolor='#151519', edgecolor='#27272A', labelcolor='white')
            else:
                hist = cv2.calcHist([processed], [0], None, [256], [0, 256])
                ax2.plot(hist, color='#DC2626', linewidth=1.5)
                ax2.fill_between(range(256), hist.flatten(), alpha=0.3, color='#DC2626')
            ax2.set_title(f'PROCESSED · {op_name}', color='white', fontweight='bold')
            ax2.tick_params(colors='white')
            ax2.grid(color='#27272A')
            for s in ax2.spines.values():
                s.set_edgecolor('#3F3F46')
            st.pyplot(fig2)
    else:
        st.markdown("""
        <div style='text-align: center; padding: 80px 20px; background: #151519;
                    border: 2px dashed #27272A; border-radius: 4px;'>
            <div style='font-size: 4rem; opacity: 0.3;'>🎥</div>
            <div style='font-family: Oswald; font-weight: 700; font-size: 2rem; color: #57534E;
                       letter-spacing: 0.1em; text-transform: uppercase;'>NO EVIDENCE LOADED</div>
            <div style='font-family: JetBrains Mono, monospace; font-size: 0.7rem;
                       color: #3F3F46; margin-top: 10px; letter-spacing: 0.2em; text-transform: uppercase;'>
                UPLOAD OR USE DEMO ABOVE
            </div>
        </div>
        """, unsafe_allow_html=True)

# ================================================================================
# PAGE: REPORT INTELLIGENCE
# ================================================================================
elif page == "📝 Report Intelligence":
    section("📝 REPORT INTELLIGENCE · NLP PIPELINE")

    tt = st.tabs([
        "🧹 NORMALIZATION", "🏷️ CLASSIFY", "🔍 SIMILAR CASES",
        "📚 CASE SEARCH", "💭 SENTIMENT", "📈 N-GRAMS", "☁️ WORD CLOUD"
    ])

    # NORMALIZATION
    with tt[0]:
        st.markdown("**Processing & Normalization Pipeline for Crime Reports**")
        default = ("The SUSPECT (age ~35, wearing RED jacket) stole a mobile phone at 14:30 PM!!! "
                   "Contact officer.raj@police.in for details. Case #FIR-2024-00847. "
                   "Location: https://maps.google.com/?q=Mumbai. 3 witnesses identified.")
        text = st.text_area("Crime Report", default, height=130, key="norm_in")

        n = st.columns(3)
        with n[0]:
            lc = st.checkbox("Lowercase", True)
            re_em = st.checkbox("Remove Emails", True)
            re_url = st.checkbox("Remove URLs", True)
        with n[1]:
            re_num = st.checkbox("Remove Numbers", True)
            re_p = st.checkbox("Remove Punctuation", True)
            re_case = st.checkbox("Remove Case IDs", True)
        with n[2]:
            re_sw = st.checkbox("Remove Stopwords", True)
            re_ws = st.checkbox("Collapse Spaces", True)
            stem_words = st.checkbox("Simple Stemming", False)

        steps = [("Original", text)]
        p = text
        if lc: p = p.lower(); steps.append(("Lowercase", p))
        if re_url: p = re.sub(r'http\S+|www\.\S+', '', p); steps.append(("Remove URLs", p))
        if re_em: p = re.sub(r'\S+@\S+', '', p); steps.append(("Remove Emails", p))
        if re_case: p = re.sub(r'#\S+|fir[-\s]*\d+[-\s]*\d+', '', p); steps.append(("Remove Case IDs", p))
        if re_num: p = re.sub(r'\d+', '', p); steps.append(("Remove Numbers", p))
        if re_p: p = p.translate(str.maketrans('','', string.punctuation)); steps.append(("Remove Punct", p))
        if re_ws: p = re.sub(r'\s+', ' ', p).strip(); steps.append(("Collapse Spaces", p))
        if re_sw:
            sw = {'the','is','it','a','an','of','and','by','at','to','in','on','for','has','have',
                  'be','with','from','as','or','that','this','these','those','i','you','we','they',
                  'he','she','will','was','were','are','am','been','being','do','does','did'}
            p = ' '.join([w for w in p.split() if w.lower() not in sw])
            steps.append(("Remove Stopwords", p))
        if stem_words:
            def stem(w):
                for s in ['ing','ed','ly','s']:
                    if w.endswith(s) and len(w) > len(s)+2:
                        return w[:-len(s)]
                return w
            p = ' '.join([stem(w) for w in p.split()])
            steps.append(("Stemming", p))

        section("🔧 PIPELINE STEPS", "amber")
        for i, (lbl, txt) in enumerate(steps):
            st.markdown(f"""
            <div class='case-card'>
                <div class='case-id'>STEP {i+1:02d}</div>
                <div class='case-headline'>{lbl}</div>
                <div class='case-meta' style='color:#A8A29E; font-family: Inter;'>
                    {txt[:240]}{'…' if len(txt)>240 else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # CLASSIFY
    with tt[1]:
        st.markdown("**Crime Report Classification · 3 ML Models**")

        mc = st.radio("Model", ["Naive Bayes","Logistic Regression","Linear SVM"], horizontal=True)
        model_map = {
            "Naive Bayes": MultinomialNB(),
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Linear SVM": LinearSVC()
        }
        pipe = Pipeline([('tfidf', TfidfVectorizer(ngram_range=(1,2))), ('clf', model_map[mc])])

        try:
            X_tr, X_te, y_tr, y_te = train_test_split(
                reports_df.Report, reports_df.Crime_Type,
                test_size=0.3, random_state=42, stratify=reports_df.Crime_Type)
        except ValueError:
            X_tr, X_te, y_tr, y_te = train_test_split(
                reports_df.Report, reports_df.Crime_Type,
                test_size=0.3, random_state=42)
        pipe.fit(X_tr, y_tr)
        preds = pipe.predict(X_te)
        acc = accuracy_score(y_te, preds)
        f1 = f1_score(y_te, preds, average='weighted')
        pipe.fit(reports_df.Report, reports_df.Crime_Type)

        cc = st.columns(4)
        kpi_card(cc[0], "Training", len(reports_df), "📚", "#DC2626")
        kpi_card(cc[1], "Accuracy", f"{acc*100:.0f}%", "🎯", "#10B981")
        kpi_card(cc[2], "F1 Score", f"{f1:.2f}", "📈", "#F59E0B")
        kpi_card(cc[3], "Classes", reports_df.Crime_Type.nunique(), "🏷️", "#FBBF24")

        ui = st.text_area("✍️ Enter new report:",
                          "Two masked men entered the bank wielding handguns and demanded all cash from the tellers before fleeing on motorcycles.",
                          height=100)
        if st.button("🏷️ CLASSIFY REPORT"):
            pred = pipe.predict([ui])[0]
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #DC2626, #991B1B);
                        padding: 22px; border-radius: 4px; text-align: center; margin: 18px 0;'>
                <div style='font-family: JetBrains Mono, monospace; color: rgba(255,255,255,0.8);
                            font-size: 0.66rem; letter-spacing: 0.25em;'>◆ PREDICTED CRIME CATEGORY ◆</div>
                <div style='font-family: Oswald; font-weight: 700; color: white; font-size: 3rem;
                            letter-spacing: 0.1em; margin-top: 6px;'>{pred.upper()}</div>
            </div>
            """, unsafe_allow_html=True)

            if hasattr(pipe.named_steps['clf'], 'predict_proba'):
                probs = pipe.predict_proba([ui])[0]
                classes = pipe.classes_
                pdf = pd.DataFrame({'Category':classes, 'Probability':probs}).sort_values('Probability', ascending=True)
                fig = px.bar(pdf, x='Probability', y='Category', orientation='h',
                             color='Probability',
                             color_continuous_scale=[[0,"#44403C"],[1,"#DC2626"]],
                             title="CLASSIFICATION CONFIDENCE")
                st.plotly_chart(apply_theme(fig), use_container_width=True)

        section("🎯 CONFUSION MATRIX", "amber")
        cm = confusion_matrix(y_te, preds, labels=sorted(reports_df.Crime_Type.unique()))
        labels_cm = sorted(reports_df.Crime_Type.unique())
        fig_cm = px.imshow(cm, x=labels_cm, y=labels_cm, text_auto=True, aspect="auto",
                           color_continuous_scale=[[0,"#27272A"],[1,"#DC2626"]],
                           title=f"CONFUSION MATRIX · {mc}",
                           labels=dict(x="Predicted", y="Actual"))
        st.plotly_chart(apply_theme(fig_cm), use_container_width=True)

    # SIMILARITY
    with tt[2]:
        st.markdown("**Find Similar Past Cases · Cosine Similarity**")
        query = st.text_area("📝 Enter case description:",
                             "Thief stole wallet from victim on public transit during morning rush",
                             height=90)
        if query:
            vec = TfidfVectorizer()
            dv = vec.fit_transform(reports_df.Report)
            qv = vec.transform([query])
            sims = cosine_similarity(qv, dv)[0]
            res = sorted(enumerate(sims), key=lambda x: -x[1])

            section("🏆 MATCHING CASES", "amber")
            for rank, (i, sc) in enumerate(res[:8]):
                if sc > 0:
                    col = "#10B981" if sc > 0.3 else ("#F59E0B" if sc > 0.15 else "#57534E")
                    bw = min(sc*100, 100)
                    rep = reports_df.iloc[i]
                    st.markdown(f"""
                    <div class='case-card' style='border-left-color:{col};'>
                        <div style='display:flex; justify-content: space-between; align-items: center;'>
                            <div class='case-id'>CASE #{i+1:03d} · MATCH {sc:.3f}</div>
                            <span class='badge' style='background: {col};'>{rep.Crime_Type.upper()}</span>
                        </div>
                        <div class='case-headline' style='margin-top:6px;'>{rep.Report}</div>
                        <div style='background:#1F1F26; border-radius:3px; height:4px; margin-top:8px;'>
                            <div style='background:linear-gradient(to right,{col},#DC2626);
                                       width:{bw}%; height:4px; border-radius:3px;'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # SEARCH
    with tt[3]:
        st.markdown("**TF-IDF Ranked Search Across Case Database**")
        q = st.text_input("🔍 Search", "stolen mobile phone on street")
        if q:
            vec = TfidfVectorizer()
            dv = vec.fit_transform(reports_df.Report)
            qv = vec.transform([q])
            sims = cosine_similarity(qv, dv)[0]
            res = sorted(enumerate(sims), key=lambda x: -x[1])
            section("RESULTS", "amber")
            for rank, (i, sc) in enumerate(res[:10]):
                if sc > 0:
                    col = "#DC2626" if sc > 0.3 else ("#F59E0B" if sc > 0.15 else "#57534E")
                    rep = reports_df.iloc[i]
                    st.markdown(f"""
                    <div class='case-card' style='border-left-color:{col};'>
                        <div style='display:flex; justify-content: space-between;'>
                            <div class='case-id'>#{rank+1:02d} · SCORE {sc:.3f}</div>
                            <span class='badge'>{rep.Crime_Type.upper()}</span>
                        </div>
                        <div class='case-headline'>{rep.Report}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # SENTIMENT
    with tt[4]:
        st.markdown("**Sentiment · Severity Indicator for Reports**")
        severe = {'attack','attacked','violent','armed','gun','weapon','beaten','injured',
                  'killed','murder','assault','threatening','stabbed','brutally','severe',
                  'ruthless','blood','dangerous','critical','emergency','deadly','victim','brutal'}
        minor = {'minor','small','lost','misplaced','petty','verbal','light','warning',
                 'resolved','recovered','returned','handled','nothing','stable','peaceful'}

        ss = st.selectbox("Sample", ["Custom"] + reports_df.Report.tolist())
        if ss == "Custom":
            text_s = st.text_area("Report",
                                   "Armed attackers brutally beat victim leaving him with severe life-threatening injuries",
                                   height=100)
        else:
            text_s = ss
            st.text_area("Report", text_s, height=100, disabled=True)

        words = re.findall(r'\b\w+\b', text_s.lower())
        sev_hits = [w for w in words if w in severe]
        min_hits = [w for w in words if w in minor]
        score = (len(sev_hits) - len(min_hits)) / max(len(words), 1)
        if score > 0.01:
            label, color = "HIGH SEVERITY 🚨", "#DC2626"
        elif score < -0.01:
            label, color = "LOW SEVERITY ✓", "#10B981"
        else:
            label, color = "MODERATE ⚠️", "#F59E0B"

        sc = st.columns(4)
        kpi_card(sc[0], "Severity", label, "💭", color)
        kpi_card(sc[1], "Severe Words", len(sev_hits), "🚨", "#DC2626")
        kpi_card(sc[2], "Minor Words", len(min_hits), "✓", "#10B981")
        kpi_card(sc[3], "Score", f"{score:+.3f}", "📊", color)

        if sev_hits or min_hits:
            st.markdown(f"""
            <div class='info-box' style='border-left-color:{color};'>
                <b>Severe markers:</b> {", ".join(set(sev_hits)) if sev_hits else "—"}<br>
                <b>Minor markers:</b> {", ".join(set(min_hits)) if min_hits else "—"}
            </div>
            """, unsafe_allow_html=True)

    # N-GRAMS
    with tt[5]:
        st.markdown("**N-Gram Analysis of Crime Reports Corpus**")
        ng = st.radio("N-Gram", ["Unigrams (1)","Bigrams (2)","Trigrams (3)"], horizontal=True, index=1)
        n_val = {"Unigrams (1)":1,"Bigrams (2)":2,"Trigrams (3)":3}[ng]

        all_text = " ".join(reports_df.Report.tolist())
        cl = re.sub(r'[^\w\s]', '', all_text.lower())
        try:
            vec = CountVectorizer(ngram_range=(n_val, n_val), stop_words='english' if n_val > 1 else None)
            mat = vec.fit_transform([cl])
            ngs = vec.get_feature_names_out()
            counts = mat.toarray()[0]
            ndf = pd.DataFrame({'N-Gram':ngs,'Count':counts}).sort_values('Count', ascending=False).head(20)
            if len(ndf):
                fig = px.bar(ndf, x='Count', y='N-Gram', orientation='h', color='Count',
                             color_continuous_scale=[[0,"#44403C"],[1,"#DC2626"]],
                             title=f"TOP 20 {ng.upper()} · ALL REPORTS")
                fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
                st.plotly_chart(apply_theme(fig), use_container_width=True)
        except Exception:
            st.info("Try another n-gram setting.")

    # WORD CLOUD
    with tt[6]:
        st.markdown("**Word Cloud · Most Frequent Terms in Crime Corpus**")
        all_text = " ".join(reports_df.Report.tolist())
        cleaned = re.sub(r'[^\w\s]', ' ', all_text.lower())
        stopwords = set(['the','is','a','an','of','and','to','in','for','on','with','at','by','from',
                         'as','or','that','this','it','has','have','been','was','were','are','be'])
        words = [w for w in cleaned.split() if w not in stopwords and len(w) > 2]
        freq = Counter(words).most_common(50)

        if freq:
            import random
            random.seed(42)
            mx = freq[0][1]
            fig = go.Figure()
            cmap = ["#DC2626","#F59E0B","#FBBF24","#991B1B","#EAB308","#A16207"]
            for i, (word, count) in enumerate(freq):
                size = 10 + (count / mx) * 40
                x = random.uniform(-50, 50)
                y = random.uniform(-30, 30)
                fig.add_annotation(x=x, y=y, text=word, showarrow=False,
                                   font=dict(size=size, color=cmap[i % len(cmap)], family="Oswald"),
                                   opacity=0.7 + (count/mx) * 0.3)
            fig.update_layout(
                xaxis=dict(visible=False, range=[-60, 60]),
                yaxis=dict(visible=False, range=[-40, 40]),
                paper_bgcolor="#151519", plot_bgcolor="#151519",
                height=500, margin=dict(t=40, b=10, l=10, r=10),
                title=dict(text="CRIME CORPUS · WORD CLOUD",
                          font=dict(color="white", family="Oswald", size=18))
            )
            st.plotly_chart(fig, use_container_width=True)

# ================================================================================
# PAGE: ABOUT
# ================================================================================
elif page == "ℹ️ About":
    section("ℹ️ ABOUT CRIMEWATCH")

    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(220,38,38,0.12), rgba(0,0,0,0.3));
                border: 1px solid #27272A; border-left: 4px solid #DC2626;
                border-radius: 4px; padding: 24px 28px;'>
        <div class='stamp' style='margin-bottom: 14px;'>CLASSIFIED · CASE FILE</div>
        <div style='font-family: Playfair Display, serif; font-weight: 900; font-size: 2.4rem;
                    color: #F5F5F4; line-height: 1.1;'>
            Urban Crime Intelligence System
        </div>
        <div style='font-family: Inter; color: #A8A29E; font-size: 1rem; margin-top: 10px; line-height: 1.7;'>
            CrimeWatch is a production-grade intelligence platform integrating the four units
            of the Python data science curriculum. Every module serves a real investigative purpose —
            mapping crime hotspots, enhancing grainy CCTV footage, triaging reports by ML classification,
            and analyzing temporal patterns to forecast hotspots.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    section("🛠️ TECHNOLOGY STACK", "amber")
    tc = st.columns(4)
    techs = [
        ("Framework", "Streamlit 1.28+", "🎛️", "#DC2626"),
        ("Data", "Pandas · NumPy", "📊", "#F59E0B"),
        ("Plotting", "Matplotlib · Plotly", "📈", "#FBBF24"),
        ("Maps", "Folium", "🗺️", "#991B1B"),
        ("Image", "OpenCV · Pillow", "🖼️", "#DC2626"),
        ("ML/NLP", "scikit-learn", "🤖", "#F59E0B"),
        ("Typography", "Google Fonts", "🔤", "#FBBF24"),
        ("Storage", "CSV · JSON", "💾", "#991B1B"),
    ]
    for i, (lbl, val, ic, c) in enumerate(techs):
        tc[i % 4].markdown(f"""
        <div class='kpi-card' style='--kpi-accent:{c}; margin-bottom: 10px;'>
            <div class='kpi-label'>{lbl}</div>
            <div class='kpi-value' style='font-size: 1.3rem;'>{val}</div>
            <div class='kpi-icon'>{ic}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; padding: 30px; font-family: JetBrains Mono, monospace;
                font-size: 0.62rem; color: #3F3F46; letter-spacing: 0.24em; margin-top: 24px;'>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br>
    CRIMEWATCH · URBAN INTELLIGENCE · 2026<br>
    STREAMLIT · PLOTLY · FOLIUM · OPENCV · SCIKIT-LEARN<br>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    </div>
    """, unsafe_allow_html=True)

# ================================================================================
# FOOTER
# ================================================================================
st.markdown('<div class="hero-divider" style="margin-top: 40px;"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align: center; padding: 14px 0; font-family: JetBrains Mono, monospace;
            font-size: 0.65rem; color: #3F3F46; letter-spacing: 0.22em;'>
🔴 CRIMEWATCH · URBAN CRIME INTELLIGENCE · 2026<br>
{df_raw.City.nunique()} CITIES · {len(df_raw):,} RECORDS · {df_raw.Crime_Type.nunique()} CATEGORIES
</div>
""", unsafe_allow_html=True)
