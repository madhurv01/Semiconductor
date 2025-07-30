import streamlit as st
# The import for the analysis function name has changed
from analysis import load_data, get_llm_analysis_and_stream, create_html_report 
from translations import LANG_STRINGS, DISTRICT_MAP_EN_KN, DISTRICT_MAP_KN_EN
import base64
import os

# ... (get_base64_of_bin_file and set_page_background functions remain the same) ...
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_page_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''<style>.stApp {{ background-image: url("data:image/png;base64,{bin_str}"); background-size: cover; }}</style>'''
    st.markdown(page_bg_img, unsafe_allow_html=True)


if 'lang' not in st.session_state:
    st.session_state['lang'] = 'en'

st.set_page_config(page_title="LLM Semiconductor Analytics", layout="wide")

background_image_path = 'images/background.png'
if os.path.exists(background_image_path):
    set_page_background(background_image_path)

lang = st.session_state['lang']
st.title(LANG_STRINGS['title'][lang])
st.caption(LANG_STRINGS['caption'][lang])
st.sidebar.header(LANG_STRINGS['sidebar_header'][lang])
selected_lang_display = st.sidebar.radio(
    label=LANG_STRINGS['lang_label'][lang],
    options=['English', 'ಕನ್ನಡ'],
    index=0 if lang == 'en' else 1,
    horizontal=True
)
st.session_state['lang'] = 'en' if selected_lang_display == 'English' else 'kn'
st.sidebar.markdown("---")

# Data loading is now cached
rainfall_data, boilers_data, roads_data = load_data()

if all(df is not None for df in [rainfall_data, boilers_data, roads_data]):
    st.sidebar.header(LANG_STRINGS['site_selection_header'][lang])
    st.sidebar.info(LANG_STRINGS['site_selection_info'][lang])

    available_districts_en = [dist for dist in sorted(rainfall_data['District'].unique()) if dist in DISTRICT_MAP_EN_KN]
    
    if lang == 'kn':
        display_districts = [DISTRICT_MAP_EN_KN[dist] for dist in available_districts_en]
    else:
        display_districts = available_districts_en

    selected_district_display = st.sidebar.selectbox(label=LANG_STRINGS['district_label'][lang], options=display_districts)
    district_en = DISTRICT_MAP_KN_EN[selected_district_display] if lang == 'kn' else selected_district_display

    if st.sidebar.button(LANG_STRINGS['analyze_button'][lang], type="primary"):
        display_name = selected_district_display
        st.header(LANG_STRINGS['report_header'][lang].format(district=display_name))

        # --- THIS IS THE KEY CHANGE ---
        # Use st.write_stream to display the report as it's generated
        
        # A special generator to handle the streaming logic
        def stream_handler():
            full_report_text = ""
            placeholder = st.empty()
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
            st.error(LANG_STRINGS['error_message'][lang])
else:
    st.error(LANG_STRINGS['data_load_error'][lang])