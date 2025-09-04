import streamlit as st
import pandas as pd
import sys
import base64
sys.path.append('.') # Allows importing from the root directory
from analysis import create_html_report # Re-using the HTML report generator
from translations import DISTRICT_MAP_EN_KN
import google.generativeai as genai

# --- Page Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if st.session_state.get("user_type") != "gov":
    st.error("ACCESS DENIED: This tool is available for Government Login only.")
    st.stop()

# --- NEW: Function to embed a background video ---
def add_bg_video():
    video_path = "videos/water_bg.mp4"
    try:
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
        video_b64 = base64.b64encode(video_bytes).decode()
        
        st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
            background: none; /* Remove default background */
        }}
        .stApp {{
            background: #0E1117; /* Fallback color */
        }}
        #bg-video {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            object-fit: cover;
            z-index: -1;
            opacity: 0.3; /* Make it subtle */
        }}
        /* Add some glassmorphism to the input/output containers for readability */
        [data-testid="stVerticalBlock"] {{
            background: rgba(10, 25, 47, 0.5);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(0, 168, 232, 0.2);
            margin-bottom: 20px;
        }}
        </style>
        <video autoplay muted loop id="bg-video">
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        </video>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Background video 'water_bg.mp4' not found. Please add it to the 'videos' folder.")

# --- Load the Water Dataset (cached for performance) ---
@st.cache_data
def load_water_data():
    try:
        df = pd.read_csv("data/karnataka_water_sources.csv")
        return df
    except FileNotFoundError:
        return None

water_df = load_water_data()

# --- AI Analysis Function (Bilingual) ---
@st.cache_data
def get_water_analysis(source_data_tuple, district_name, language='en'):
    source_data = dict(source_data_tuple)
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception:
        st.error("Failed to configure AI Model.")
        return None

    prompt = f"""
    **Role:** You are a senior water purification engineer for the semiconductor industry.
    **Objective:** Analyze the provided raw water source data for a new fab in {district_name}.
    **UPW Requirements:** TDS < 0.001 ppm, pH = 7.0.
    **Raw Water Source Data:**
    - Source: {source_data['source_name']} ({source_data['source_type']})
    - Distance: {source_data['distance_from_center_km']} km
    - TDS: {source_data['total_dissolved_solids_ppm']} ppm
    - pH Level: {source_data['ph_level']}
    - Hardness: {source_data['hardness_mg_L']} mg/L
    - Turbidity: {source_data['turbidity_ntu']} NTU
    - Silica: {source_data['silica_mg_L']} mg/L
    **Your Task (Generate a Markdown Report):**
    1.  **Initial Quality Assessment:** Classify the raw water quality as 'Excellent', 'Good', 'Moderate', or 'Poor'.
    2.  **Key Challenges:** Identify the top 2-3 purification challenges.
    3.  **Recommended Purification Train:** List the essential technologies required.
    4.  **Feasibility Score:** Conclude with a "Purification Feasibility Score" from 1 to 10 and a justification.
    """
    
    try:
        english_report = model.generate_content(prompt).text
        if language == 'kn' and english_report:
            translation_prompt = f"Translate the following technical report for '{district_name}' accurately into formal Kannada, retaining Markdown formatting:\n\n---\n\n{english_report}"
            kannada_report = model.generate_content(translation_prompt).text
            return kannada_report
        return english_report
    except Exception as e:
        st.error(f"An error occurred with the AI model: {e}")
        return None

# --- Page UI ---

# Call the function to set the background video at the very top
add_bg_video()

st.title("💧 AquaMetric - Water Source & Purity Analyzer")
st.markdown("---")
st.info("This tool analyzes the nearest major water source for a selected district and uses AI to assess the feasibility of purifying it to Ultra-Pure Water (UPW) standards required for semiconductor manufacturing.")

if water_df is None:
    st.error("Water source dataset not found. Please run `generate_water_data.py` first.")
else:
    lang = st.session_state.get('lang', 'en')
    selected_lang_display = st.radio(
        label="Select Language",
        options=['English', 'ಕನ್ನಡ'],
        index=0 if lang == 'en' else 1,
        horizontal=True
    )
    st.session_state['lang'] = 'en' if selected_lang_display == 'English' else 'kn'
    lang = st.session_state['lang']

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
        district_en = next((k for k, v in DISTRICT_MAP_EN_KN.items() if v == selected_district_display), selected_district_display)
    else:
        district_en = selected_district_display

    if analyze_button:
        source_info = water_df[water_df['district'] == district_en].iloc[0]
        
        with col2:
            st.subheader(f"Analysis for {selected_district_display}")
            with st.spinner("AI is analyzing the water quality data..."):
                source_info_tuple = tuple(source_info.to_dict().items())
                analysis_report = get_water_analysis(source_info_tuple, selected_district_display, language=lang)

            if analysis_report:
                st.markdown(analysis_report)
                st.markdown("---")
                html_bytes = create_html_report(analysis_report, lang, district_en)
                if html_bytes:
                    st.download_button(
                        label="📄 Download Report as HTML",
                        data=html_bytes,
                        file_name=f"AquaMetric_Report_{district_en.replace(' ', '_')}.html",
                        mime="text/html"
                    )