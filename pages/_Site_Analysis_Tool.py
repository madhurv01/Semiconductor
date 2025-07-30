import streamlit as st
import sys
sys.path.append('.') 

# --- THIS IS THE CORRECTED IMPORT LINE ---
from analysis import load_data, get_llm_analysis_and_stream, create_html_report
from translations import LANG_STRINGS, DISTRICT_MAP_EN_KN, DISTRICT_MAP_KN_EN
import os

# --- Page Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if st.session_state.get("user_type") != "gov":
    st.error("ACCESS DENIED: This tool is available for Government Login only.")
    st.write("Please log out and sign in with government credentials from the main portal.")
    st.stop()

# --- Main Application Code ---
lang = st.session_state.get('lang', 'en')

st.title("Site Analysis Tool")
st.markdown("---")

# Language selection
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

# Load data (cached)
rainfall_data, boilers_data, roads_data = load_data()

if all(df is not None for df in [rainfall_data, boilers_data, roads_data]):
    st.header(LANG_STRINGS['site_selection_header'][lang])
    st.info(LANG_STRINGS['site_selection_info'][lang])

    available_districts_en = [dist for dist in sorted(rainfall_data['District'].unique()) if dist in DISTRICT_MAP_EN_KN]
    
    if lang == 'kn':
        display_districts = [DISTRICT_MAP_EN_KN[dist] for dist in available_districts_en]
    else:
        display_districts = available_districts_en

    col1, col2 = st.columns([1,2])
    with col1:
        selected_district_display = st.selectbox(
            label=LANG_STRINGS['district_label'][lang],
            options=display_districts
        )
        analyze_button = st.button(LANG_STRINGS['analyze_button'][lang], type="primary", use_container_width=True)

    if lang == 'kn':
        district_en = DISTRICT_MAP_KN_EN[selected_district_display]
    else:
        district_en = selected_district_display

    if analyze_button:
        display_name = selected_district_display
        with col2:
            st.header(LANG_STRINGS['report_header'][lang].format(district=display_name))

            # --- THIS IS THE CORRECTED LOGIC USING THE STREAMING FUNCTION ---
            def stream_handler():
                full_report_text = ""
                placeholder = st.empty()
                # Calling the new function name
                for chunk in get_llm_analysis_and_stream(district_en, rainfall_data, boilers_data, roads_data, language=lang):
                    if chunk == "<STOP_AND_CLEAR>":
                        full_report_text = "" # Reset for translation
                    else:
                        full_report_text += chunk
                    placeholder.markdown(full_report_text + " ▌") # Add a blinking cursor effect
                placeholder.markdown(full_report_text) # Show final report
                return full_report_text

            llm_report = stream_handler()

            if llm_report:
                st.success(LANG_STRINGS['success_message'][lang])
                st.markdown("---")
                html_report_str = create_html_report(llm_report, lang, district_en)
                if html_report_str:
                    st.download_button(
                        label=LANG_STRINGS['download_button'][lang],
                        data=html_report_str,
                        file_name=f"Feasibility_Report_{district_en.replace(' ', '_')}.html",
                        mime="text/html"
                    )
            else:
                # Error is now handled within the analysis function itself
                pass
else:
    st.error(LANG_STRINGS['data_load_error'][lang])