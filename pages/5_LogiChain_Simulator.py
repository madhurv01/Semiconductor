import streamlit as st
import pandas as pd
import sys
import base64
from geopy.distance import geodesic
sys.path.append('.') # Allows importing from the root directory
from analysis import create_html_report
from translations import DISTRICT_MAP_EN_KN, LANG_STRINGS
import google.generativeai as genai

# --- Page Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if st.session_state.get("user_type") != "gov":
    st.error("ACCESS DENIED: This tool is available for Government Login only.")
    st.stop()

# --- NEW: Function to embed a dedicated background image for this page ---
def add_page_bg(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string});
            background-size: cover;
            background-position: center;
        }}
        /* Style for containers to make them glass-like and readable */
        [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {{
            background: rgba(10, 25, 47, 0.45); /* Highly transparent */
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(0, 168, 232, 0.2);
            margin-bottom: 20px;
        }}
        /* Enhance text readability with a stronger shadow */
        h1, h2, h3, h4, p, .st-emotion-cache-1yy083c, .st-emotion-cache-1629p8f, .st-emotion-cache-1njjmv6, .st-emotion-cache-1r6slb0, .st-emotion-cache-1hg5474, .st-emotion-cache-1q8dd3i {{
             text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image 'log.jpg' not found. Please add it to the 'images' folder.")

# --- Call the function to set the background ---
add_page_bg("images/log.jpg")

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

# --- AI Analysis Function (Bilingual) ---
@st.cache_data
def get_logistics_analysis(district_name_en, seaport_dist, airport_dist, chemical_dist, language='en'):
    district_name_display = DISTRICT_MAP_EN_KN.get(district_name_en, district_name_en) if language == 'kn' else district_name_en
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception:
        st.error("Failed to configure AI Model.")
        return None

    prompt = f"""
    **Role:** You are a senior supply chain analyst for a global semiconductor firm.
    **Objective:** Provide a concise risk and viability assessment for a new fab in **{district_name_en}, Karnataka**.
    **Input Data:**
    - **Distance to nearest major Seaport (New Mangalore Port):** {seaport_dist:.0f} km
    - **Distance to nearest international Airport (Kempegowda Intl, BLR):** {airport_dist:.0f} km
    - **Distance to nearest Chemical Hub (Mangalore):** {chemical_dist:.0f} km
    **Your Task (Generate a Markdown Report):**
    1.  **Overall Assessment:** Classify the logistical viability as 'Excellent', 'Good', 'Moderate', or 'Challenging'.
    2.  **Key Strengths:** Identify the biggest logistical advantage.
    3.  **Primary Risks & Bottlenecks:** Identify the most significant risk.
    4.  **Logistical Viability Score:** Conclude with a "Logistical Viability Score" on a scale of 1 to 10 (1=High Risk, 10=Low Risk) and a justification.
    """
    
    try:
        english_report = model.generate_content(prompt).text
        if language == 'kn' and english_report:
            translation_prompt = f"Translate the following technical report for '{district_name_display}' accurately into formal Kannada, retaining Markdown formatting:\n\n---\n\n{english_report}"
            kannada_report = model.generate_content(translation_prompt).text
            return kannada_report
        return english_report
    except Exception as e:
        st.error(f"An error occurred with the AI model: {e}")
        return None

# --- Page UI ---
lang = st.session_state.get('lang', 'en')

st.title(LANG_STRINGS['logichain_title'][lang])
st.markdown("---")
st.info(LANG_STRINGS['logichain_info'][lang])

selected_lang_display = st.radio(
    label="Select Language",
    options=['English', 'ಕನ್ನಡ'],
    index=0 if lang == 'en' else 1,
    horizontal=True,
    label_visibility="collapsed"
)
st.session_state['lang'] = 'en' if selected_lang_display == 'English' else 'kn'
lang = st.session_state['lang']

if districts_df is None or hubs_df is None:
    st.error("Logistics datasets not found. Please run `generate_logistics_data.py` first.")
else:
    if lang == 'kn':
        available_districts_en = [dist for dist in sorted(districts_df['district'].unique()) if dist in DISTRICT_MAP_EN_KN]
        display_districts = [DISTRICT_MAP_EN_KN.get(dist, dist) for dist in available_districts_en]
    else:
        display_districts = sorted(districts_df['district'].unique())

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(LANG_STRINGS['logichain_select_district_header'][lang])
        selected_district_display = st.selectbox(
            LANG_STRINGS['logichain_select_district_label'][lang],
            display_districts,
            label_visibility="collapsed"
        )
        analyze_button = st.button(LANG_STRINGS['logichain_analyze_button'][lang], type="primary", use_container_width=True)

    if lang == 'kn':
        district_en = next((k for k, v in DISTRICT_MAP_EN_KN.items() if v == selected_district_display), selected_district_display)
    else:
        district_en = selected_district_display

    if analyze_button:
        district_coords = districts_df[districts_df['district'] == district_en][['latitude', 'longitude']].iloc[0]
        seaport_coords = hubs_df[hubs_df['hub_type'] == 'Seaport'][['latitude', 'longitude']].iloc[0]
        airport_coords = hubs_df[hubs_df['hub_type'] == 'Airport'][['latitude', 'longitude']].iloc[0]
        chemical_coords = hubs_df[hubs_df['hub_type'] == 'Chemical Hub'][['latitude', 'longitude']].iloc[0]

        seaport_dist = geodesic(tuple(district_coords), tuple(seaport_coords)).kilometers
        airport_dist = geodesic(tuple(district_coords), tuple(airport_coords)).kilometers
        chemical_dist = geodesic(tuple(district_coords), tuple(chemical_coords)).kilometers

        map_df = pd.DataFrame({
            'name': [f"Fab Site: {district_en}", 'Seaport', 'Airport', 'Chemical Hub'],
            'lat': [district_coords.latitude, seaport_coords.latitude, airport_coords.latitude, chemical_coords.latitude],
            'lon': [district_coords.longitude, seaport_coords.longitude, airport_coords.longitude, chemical_coords.longitude],
        })

        with col1:
            st.subheader(LANG_STRINGS['logichain_map_header'][lang])
            st.map(map_df)

        with col2:
            st.subheader(LANG_STRINGS['logichain_report_header'][lang].format(district=selected_district_display))
            with st.spinner(LANG_STRINGS['logichain_spinner'][lang]):
                analysis_report = get_logistics_analysis(district_en, seaport_dist, airport_dist, chemical_dist, language=lang)
            
            if analysis_report:
                st.markdown(analysis_report)
                
                st.markdown("---")
                html_bytes = create_html_report(analysis_report, lang, district_en)
                if html_bytes:
                    st.download_button(
                        label="📄 " + LANG_STRINGS['download_button'][lang].split(" ")[-1],
                        data=html_bytes,
                        file_name=f"LogiChain_Report_{district_en.replace(' ', '_')}.html",
                        mime="text/html"
                    )