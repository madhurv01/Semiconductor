import streamlit as st
import pandas as pd
import sys
sys.path.append('.') # Allows importing from the root directory

# --- THIS IS THE CORRECTED IMPORT LINE ---
from analysis import create_html_report # Re-using the HTML report generator
from translations import DISTRICT_MAP_EN_KN
import google.generativeai as genai

# --- Page Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if st.session_state.get("user_type") != "gov":
    st.error("ACCESS DENIED: This tool is available for Government Login only.")
    st.stop()

# --- Load the Water Dataset (cached for performance) ---
@st.cache_data
def load_water_data():
    try:
        df = pd.read_csv("data/karnataka_water_sources.csv")
        return df
    except FileNotFoundError:
        return None

water_df = load_water_data()

# --- AI Analysis Function ---
@st.cache_data # Cache the AI response for a given district to save API calls
def get_water_analysis(source_data_tuple, district_name):
    source_data = dict(source_data_tuple) # Convert tuple back to dict for processing
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception:
        st.error("Failed to configure AI Model. Have you added your GEMINI_API_KEY to secrets?")
        return None

    prompt = f"""
    **Role:** You are a senior water purification engineer for the semiconductor industry.
    **Objective:** Analyze the provided raw water source data and assess its suitability for producing Ultra-Pure Water (UPW) for a new semiconductor fab in {district_name}.
    **UPW Requirements:** TDS < 0.001 ppm, pH = 7.0. All other impurities must be removed.
    **Raw Water Source Data:**
    - Source: {source_data['source_name']} ({source_data['source_type']})
    - Distance: {source_data['distance_from_center_km']} km
    - TDS: {source_data['total_dissolved_solids_ppm']} ppm
    - pH Level: {source_data['ph_level']}
    - Hardness: {source_data['hardness_mg_L']} mg/L
    - Turbidity: {source_data['turbidity_ntu']} NTU
    - Silica: {source_data['silica_mg_L']} mg/L
    **Your Task (Generate a Markdown Report):**
    1.  **Initial Quality Assessment:** In one sentence, classify the raw water quality as 'Excellent', 'Good', 'Moderate', or 'Poor' for UPW purposes.
    2.  **Key Challenges:** Identify the top 2-3 challenges for purification (e.g., "High initial TDS will require a multi-stage reverse osmosis system.").
    3.  **Recommended Purification Train:** Briefly list the essential technologies required (e.g., Pre-treatment, Reverse Osmosis, Degasification, Ion Exchange, UV Sterilization).
    4.  **Feasibility Score:** Conclude with a "Purification Feasibility Score" on a scale of 1 to 10 (1=Extremely Difficult/Costly, 10=Very Feasible) and a one-sentence justification.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred while communicating with the AI model: {e}")
        return None

# --- Page UI ---
st.title("💧 AquaMetric - Water Source & Purity Analyzer")
st.markdown("---")
st.info("This tool analyzes the nearest major water source for a selected district and uses AI to assess the feasibility of purifying it to Ultra-Pure Water (UPW) standards required for semiconductor manufacturing.")

if water_df is None:
    st.error("Water source dataset not found. Please run `generate_water_data.py` first.")
else:
    lang = st.session_state.get('lang', 'en')
    
    if lang == 'kn':
        available_districts_en = [dist for dist in sorted(water_df['district'].unique()) if dist in DISTRICT_MAP_EN_KN]
        display_districts = [DISTRICT_MAP_EN_KN.get(dist, dist) for dist in available_districts_en]
    else:
        display_districts = sorted(water_df['district'].unique())

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Select a District")
        selected_district_display = st.selectbox(
            "Select a district to analyze its water source:",
            display_districts,
            label_visibility="collapsed"
        )
        analyze_button = st.button("Analyze Water Source", type="primary", use_container_width=True)

    if lang == 'kn':
        # Find the English key from the Kannada value
        district_en = next((k for k, v in DISTRICT_MAP_EN_KN.items() if v == selected_district_display), selected_district_display)
    else:
        district_en = selected_district_display

    if analyze_button:
        source_info = water_df[water_df['district'] == district_en].iloc[0]
        
        with col2:
            st.subheader(f"Analysis for {selected_district_display}")
            with st.spinner("AI is analyzing the water quality data..."):
                # Convert DataFrame row to a hashable tuple for caching
                source_info_tuple = tuple(source_info.to_dict().items())
                analysis_report = get_water_analysis(source_info_tuple, selected_district_display)

            if analysis_report:
                st.markdown(analysis_report)
                
                # --- THIS IS THE CORRECTED DOWNLOAD SECTION ---
                st.markdown("---")
                # Use the correct function: create_html_report
                html_bytes = create_html_report(analysis_report, lang, district_en)
                if html_bytes:
                    st.download_button(
                        label="📄 Download Report as HTML",
                        data=html_bytes,
                        file_name=f"AquaMetric_Report_{district_en.replace(' ', '_')}.html",
                        mime="text/html"
                    )