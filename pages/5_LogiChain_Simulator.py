import streamlit as st
import pandas as pd
import sys
from geopy.distance import geodesic
sys.path.append('.') # Allows importing from the root directory
from analysis import create_html_report
from translations import DISTRICT_MAP_EN_KN
import google.generativeai as genai

# --- Page Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if st.session_state.get("user_type") != "gov":
    st.error("ACCESS DENIED: This tool is available for Government Login only.")
    st.stop()

# --- Load Logistics Datasets ---
@st.cache_data
def load_logistics_data():
    try:
        df_districts = pd.read_csv("data/karnataka_district_coords.csv")
        df_hubs = pd.read_csv("data/logistics_hubs.csv")
        return df_districts, df_hubs
    except FileNotFoundError:
        return None, None

districts_df, hubs_df = load_logistics_data()

# --- AI Analysis Function ---
@st.cache_data
def get_logistics_analysis(district_name, seaport_dist, airport_dist, chemical_dist):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception:
        st.error("Failed to configure AI Model. Have you added your GEMINI_API_KEY to secrets?")
        return None

    prompt = f"""
    **Role:** You are a senior supply chain analyst for a global semiconductor firm, specializing in site selection logistics.

    **Objective:** Provide a concise risk and viability assessment for a new semiconductor fab in **{district_name}, Karnataka**.

    **Input Data (Calculated Distances to Critical Hubs):**
    - **Distance to nearest major Seaport (New Mangalore Port):** {seaport_dist:.0f} km
    - **Distance to nearest international Airport (Kempegowda Intl, BLR):** {airport_dist:.0f} km
    - **Distance to nearest Chemical Hub (Mangalore):** {chemical_dist:.0f} km

    **Your Task (Generate a Markdown Report):**
    1.  **Overall Assessment:** In one sentence, classify the logistical viability as 'Excellent', 'Good', 'Moderate', or 'Challenging'.
    2.  **Key Strengths:** Identify the biggest logistical advantage of this location (e.g., "Excellent proximity to the international airport is ideal for high-value, low-volume components and urgent spare parts.").
    3.  **Primary Risks & Bottlenecks:** Identify the most significant risk (e.g., "The extensive road journey from the seaport presents a major risk for the initial transport of heavy, sensitive lithography equipment and a recurring cost for raw material import.").
    4.  **Logistical Viability Score:** Conclude with a "Logistical Viability Score" on a scale of 1 to 10 (1=High Risk, 10=Low Risk) and a one-sentence justification.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred while communicating with the AI model: {e}")
        return None

# --- Page UI ---
st.title("⛓️ LogiChain - Supply Chain Risk Simulator")
st.markdown("---")
st.info("This tool assesses the logistical viability of a potential fab site by analyzing its distance to critical supply chain hubs.")

if districts_df is None or hubs_df is None:
    st.error("Logistics datasets not found. Please run `generate_logistics_data.py` first.")
else:
    lang = st.session_state.get('lang', 'en')
    
    if lang == 'kn':
        available_districts_en = [dist for dist in sorted(districts_df['district'].unique()) if dist in DISTRICT_MAP_EN_KN]
        display_districts = [DISTRICT_MAP_EN_KN.get(dist, dist) for dist in available_districts_en]
    else:
        display_districts = sorted(districts_df['district'].unique())

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Select a District")
        selected_district_display = st.selectbox(
            "Select a district to simulate its supply chain:",
            display_districts,
            label_visibility="collapsed"
        )
        analyze_button = st.button("Analyze Supply Chain", type="primary", use_container_width=True)

    if lang == 'kn':
        district_en = next((k for k, v in DISTRICT_MAP_EN_KN.items() if v == selected_district_display), selected_district_display)
    else:
        district_en = selected_district_display

    # --- Analysis & Map Output ---
    if analyze_button:
        # Get coordinates
        district_coords = districts_df[districts_df['district'] == district_en][['latitude', 'longitude']].iloc[0]
        seaport_coords = hubs_df[hubs_df['hub_type'] == 'Seaport'][['latitude', 'longitude']].iloc[0]
        airport_coords = hubs_df[hubs_df['hub_type'] == 'Airport'][['latitude', 'longitude']].iloc[0]
        chemical_coords = hubs_df[hubs_df['hub_type'] == 'Chemical Hub'][['latitude', 'longitude']].iloc[0]

        # Calculate distances
        seaport_dist = geodesic(tuple(district_coords), tuple(seaport_coords)).kilometers
        airport_dist = geodesic(tuple(district_coords), tuple(airport_coords)).kilometers
        chemical_dist = geodesic(tuple(district_coords), tuple(chemical_coords)).kilometers

        # Prepare map data
        map_df = pd.DataFrame({
            'name': [f"Fab Site: {district_en}", 'Seaport', 'Airport', 'Chemical Hub'],
            'lat': [district_coords.latitude, seaport_coords.latitude, airport_coords.latitude, chemical_coords.latitude],
            'lon': [district_coords.longitude, seaport_coords.longitude, airport_coords.longitude, chemical_coords.longitude],
        })

        with col1:
            st.subheader("Logistical Map")
            st.map(map_df)

        with col2:
            st.subheader(f"AI-Generated Risk Report for {selected_district_display}")
            with st.spinner("AI is analyzing logistical data..."):
                analysis_report = get_logistics_analysis(district_en, seaport_dist, airport_dist, chemical_dist)
            
            if analysis_report:
                st.markdown(analysis_report)
                
                st.markdown("---")
                html_bytes = create_html_report(analysis_report, lang, district_en)
                if html_bytes:
                    st.download_button(
                        label="📄 Download Report as HTML",
                        data=html_bytes,
                        file_name=f"LogiChain_Report_{district_en.replace(' ', '_')}.html",
                        mime="text/html"
                    )