import streamlit as st
from googleapiclient.discovery import build
import os
import sys
import base64
sys.path.append('.') # Allows importing from the root directory
from translations import LANG_STRINGS

# --- Page Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if not st.session_state.get("logged_in"):
    st.error("Please log in from the main portal to access this page.")
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
        [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"], [data-testid="stForm"] {{
            background: rgba(10, 25, 47, 0.45); /* Highly transparent */
            backdrop-filter: blur(5px);
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
        st.warning("Background image 'job.jpg' not found. Please add it to the 'images' folder.")

# --- Call the function to set the background ---
add_page_bg("images/job.jpg")


# --- Google Search API Function ---
@st.cache_data(ttl=3600) # Cache results for 1 hour
def search_jobs(job_type, experience, language_code='en'):
    """Performs a targeted Google search for semiconductor jobs."""
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        search_engine_id = st.secrets["SEARCH_ENGINE_ID"]
    except (KeyError, FileNotFoundError):
        st.error("Search API credentials not found. The administrator needs to configure the secrets.")
        return None

    query = f'"{job_type}" semiconductor engineer jobs in India {experience} years experience'
    if language_code == 'kn':
        query = f'"{job_type}" ಸೆಮಿಕಂಡಕ್ಟರ್ ಇಂಜಿನಿಯರ್ ಉದ್ಯೋಗಗಳು ಭಾರತದಲ್ಲಿ {experience} ವರ್ಷಗಳ ಅನುಭವ'

    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(
            q=query,
            cx=search_engine_id,
            num=10
        ).execute()
        return res.get('items', [])
    except Exception as e:
        st.error(f"An error occurred while searching for jobs: {e}")
        return None

# --- Page UI ---
lang = st.session_state.get('lang', 'en')

st.title(LANG_STRINGS['job_portal_title'][lang])
st.markdown("---")
st.info(LANG_STRINGS['job_portal_info'][lang])

# --- User Input Form ---
with st.form("job_search_form"):
    col1, col2, col3 = st.columns([2, 1, 1])
    
    job_type_options = LANG_STRINGS['job_types'][lang]
    
    with col1:
        job_type_display = st.selectbox(LANG_STRINGS['job_type_label'][lang], job_type_options)
    
    with col2:
        experience = st.number_input(LANG_STRINGS['experience_label'][lang], min_value=0, max_value=30, value=0, step=1)
        
    with col3:
        st.write("") # Spacer
        st.write("") # Spacer
        submitted = st.form_submit_button(LANG_STRINGS['search_button'][lang], use_container_width=True)

if lang == 'kn':
    job_type_index = job_type_options.index(job_type_display)
    job_type_for_search = LANG_STRINGS['job_types']['kn'][job_type_index]
else:
    job_type_for_search = job_type_display

# --- Display Results ---
if submitted:
    with st.spinner(LANG_STRINGS['spinner_text_jobs'][lang].format(job_type=job_type_display, experience=experience)):
        job_results = search_jobs(job_type_for_search, experience, lang)

    st.markdown("---")
    st.subheader(LANG_STRINGS['results_header'][lang].format(count=len(job_results) if job_results else 0))

    if not job_results:
        st.warning(LANG_STRINGS['no_results_warning'][lang])
    else:
        for item in job_results:
            st.markdown(f"""
            <div class="job-card">
                <h4><a href="{item['link']}" target="_blank">{item['title']}</a></h4>
                <p style="color: #00A8E8; font-weight: bold;">{item['displayLink']}</p>
                <p>{item['snippet'].replace('...', '')}</p>
                <a href="{item['link']}" target="_blank" class="apply-button">{LANG_STRINGS['apply_button_text'][lang]}</a>
            </div>
            """, unsafe_allow_html=True)

# --- CSS for Job Cards (different from the background CSS) ---
st.markdown("""
<style>
.job-card {
    border-radius: 10px;
    border: 1px solid #2C2C2C;
    padding: 20px;
    margin-bottom: 20px;
    transition: all 0.3s ease-in-out;
    background: rgba(10, 25, 47, 0.45); /* Make job cards also glass-like */
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
}
.job-card:hover {
    border-color: #00A8E8;
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 168, 232, 0.2);
}
.job-card a {
    text-decoration: none;
    color: #FFFFFF;
}
.job-card h4 a:hover {
    color: #00A8E8;
}
.apply-button {
    display: inline-block;
    padding: 8px 15px;
    border: 1px solid #00A8E8;
    border-radius: 5px;
    color: #00A8E8;
    margin-top: 10px;
    font-weight: bold;
}
.apply-button:hover {
    background-color: rgba(0, 168, 232, 0.7);
    color: white;
}
</style>
""", unsafe_allow_html=True)