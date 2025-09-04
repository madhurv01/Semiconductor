import streamlit as st
import sys
import base64
sys.path.append('.') 
from analysis import load_data, get_llm_analysis_and_stream, create_html_report
from translations import LANG_STRINGS, DISTRICT_MAP_EN_KN, DISTRICT_MAP_KN_EN
import os

# --- Page Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if st.session_state.get("user_type") != "gov":
    st.error("ACCESS DENIED: This tool is available for Government Login only.")
    st.write("Please log out and sign in with government credentials from the main portal.")
    st.stop()

# --- NEW: Function to embed a dedicated background image with higher transparency ---
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
        /* --- THIS IS THE KEY CHANGE --- */
        /* Style for containers to make them more transparent */
        [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {{
            background: rgba(10, 25, 47, 0.45); /* Much more transparent */
            backdrop-filter: blur(5px); /* Reduced blur to see image better */
            -webkit-backdrop-filter: blur(5px);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(0, 168, 232, 0.2);
            margin-bottom: 20px;
        }}
        /* Enhance text readability with a stronger shadow */
        h1, h2, h3, p, .st-emotion-cache-1yy083c, .st-emotion-cache-1629p8f, .st-emotion-cache-1njjmv6, .st-emotion-cache-1r6slb0, .st-emotion-cache-1hg5474, .st-emotion-cache-1q8dd3i {{
             text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image 'site.jpg' not found. Please add it to the 'images' folder.")

# --- Call the function to set the background ---
add_page_bg("images/site.jpg")

# --- Main Application Code ---
lang = st.session_state.get('lang', 'en')

st.title("Site Analysis Tool")
st.markdown("---")

st.subheader(LANG_STRINGS['lang_label'][lang])
selected_lang_display = st.radio(
    label="Language",
    options=['English', 'ಕನ್ನಡ'],
    index=0 if lang == 'en' else 1,
    horizontal=True,
    label_visibility="collapsed"
)
st.session_state['lang'] = 'en' if selected_lang_display == 'English' else 'kn'
lang = st.session_state['lang'] 

rainfall_data, boilers_data, roads_data = load_data()

if all(df is not None for df in [rainfall_data, boilers_data, roads_data]):
    st.header(LANG_STRINGS['site_selection_header'][lang])
    st.info(LANG_STRINGS['site_selection_info'][lang])

    available_districts_en = [dist for dist in sorted(rainfall_data['District'].unique()) if dist in DISTRICT_MAP_EN_KN]
    
    if lang == 'kn':
        display_districts = [DISTRICT_MAP_EN_KN[dist] for dist in available_districts_en]
    else:
        display_districts = available_districts_en

    col1, col2 = st.columns([1, 2])
    with col1:
        selected_district_display = st.selectbox(
            label=LANG_STRINGS['district_label'][lang],
            options=display_districts
        )
        analyze_button = st.button(LANG_STRINGS['analyze_button'][lang], type="primary", use_container_width=True)

    if lang == 'kn':
        district_en = next((k for k, v in DISTRICT_MAP_EN_KN.items() if v == selected_district_display), selected_district_display)
    else:
        district_en = selected_district_display

    if analyze_button:
        display_name = selected_district_display
        with col2:
            st.header(LANG_STRINGS['report_header'][lang].format(district=display_name))
            
            def stream_handler():
                full_report_text = ""
                placeholder = st.empty()
                for chunk in get_llm_analysis_and_stream(district_en, rainfall_data, boilers_data, roads_data, language=lang):
                    if chunk == "<STOP_AND_CLEAR>":
                        full_report_text = ""
                    else:
                        full_report_text += chunk
                    placeholder.markdown(full_report_text + " ▌")
                placeholder.markdown(full_report_text)
                return full_report_text

            llm_report = stream_handler()

            if llm_report:
                st.success(LANG_STRINGS['success_message'][lang])
                st.markdown("---")
                html_report_str = create_html_report(llm_report, lang, district_en)
                
                if html_report_str:
                    st.download_button(
                        label="📄 Download Report as HTML",
                        data=html_report_str,
                        file_name=f"Feasibility_Report_{district_en.replace(' ', '_')}.html",
                        mime="text/html"
                    )
            else:
                pass
else:
    st.error(LANG_STRINGS['data_load_error'][lang])