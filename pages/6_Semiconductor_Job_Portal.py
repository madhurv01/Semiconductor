import streamlit as st
from googleapiclient.discovery import build
import os

# --- Page Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if not st.session_state.get("logged_in"):
    st.error("Please log in from the main portal to access this page.")
    st.stop()

# --- Google Search API Function ---
@st.cache_data(ttl=3600) # Cache results for 1 hour to avoid excessive API calls
def search_jobs(job_type, experience):
    """Performs a targeted Google search for semiconductor jobs."""
    try:
        # Load secrets for the API
        api_key = st.secrets["GOOGLE_API_KEY"]
        search_engine_id = st.secrets["SEARCH_ENGINE_ID"]
    except (KeyError, FileNotFoundError):
        st.error("Search API credentials not found. The administrator needs to configure the secrets.")
        return None

    # Build the search query
    query = f'"{job_type}" semiconductor engineer jobs in India {experience} years experience'

    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(
            q=query,
            cx=search_engine_id,
            num=10 # Get top 10 results
        ).execute()
        return res.get('items', [])
    except Exception as e:
        st.error(f"An error occurred while searching for jobs: {e}")
        return None

# --- Page UI ---
st.title("🛰️ Semiconductor Job Portal")
st.markdown("---")
st.info("Find real-time job openings in the Indian semiconductor industry from top hiring platforms.")

# --- User Input Form ---
with st.form("job_search_form"):
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        job_type = st.selectbox("Select Job Type", ["Hardware", "Software", "VLSI Design", "Chip Design", "Verification", "Firmware"])
    
    with col2:
        experience = st.number_input("Experience in Years", min_value=0, max_value=30, value=0, step=1)
        
    with col3:
        st.write("") # Spacer
        st.write("") # Spacer
        submitted = st.form_submit_button("Search for Jobs", use_container_width=True)

# --- Display Results ---
if submitted:
    with st.spinner(f"Searching for {job_type} jobs with {experience} years experience..."):
        job_results = search_jobs(job_type, experience)

    st.markdown("---")
    st.subheader(f"Search Results ({len(job_results) if job_results else 0} found)")

    if not job_results:
        st.warning("No job openings found matching your criteria. Try broadening your search.")
    else:
        for item in job_results:
            st.markdown(f"""
            <div class="job-card">
                <h4><a href="{item['link']}" target="_blank">{item['title']}</a></h4>
                <p style="color: #00A8E8; font-weight: bold;">{item['displayLink']}</p>
                <p>{item['snippet'].replace('...', '')}</p>
                <a href="{item['link']}" target="_blank" class="apply-button">Apply Now &rarr;</a>
            </div>
            """, unsafe_allow_html=True)

# --- CSS for Job Cards ---
st.markdown("""
<style>
.job-card {
    border-radius: 10px;
    border: 1px solid #2C2C2C;
    padding: 20px;
    margin-bottom: 20px;
    transition: all 0.3s ease-in-out;
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