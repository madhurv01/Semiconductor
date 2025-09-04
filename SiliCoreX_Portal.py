import streamlit as st
import base64
import os
import streamlit.components.v1 as components
from supabase import create_client, Client
import bcrypt

# --- Page Configuration ---
st.set_page_config(
    page_title="SiliCoreX Portal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Define Authorized Government Users ---
AUTHORIZED_GOV_USERS = [
    "nishkalavr18@gmail.com",
    "naiksaniya21@gmail.com",
    "lpniranjan555@gmail.com",
    "sireesha@vvce.ac.in",
    "madhurvwork@gmail.com"
]

# --- Function to load and apply CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- NEW: Function to embed a background video for the portal ---
def add_portal_bg_video():
    video_path = "videos/portal_bg.mp4"
    try:
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
        video_b64 = base64.b64encode(video_bytes).decode()
        
        st.markdown(f"""
        <style>
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
            z-index: -2;
            opacity: 0.6; /* Highlighted visibility */
        }}
        </style>
        <video autoplay muted loop id="bg-video">
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        </video>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Portal background video 'portal_bg.mp4' not found. Please add it to the 'videos' folder.")

# --- Hashing Utilities ---
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# --- Login State Management ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# --- Supabase Initialization ---
supabase = None
try:
    if "supabase_url" in st.secrets and "supabase_key" in st.secrets:
        supabase = create_client(st.secrets["supabase_url"], st.secrets["supabase_key"])
except Exception:
    pass 

# --- Login Logic Function ---
def perform_login(username, password, user_type):
    # ... (This function remains unchanged)
    if user_type == "gov":
        if username in AUTHORIZED_GOV_USERS and password == "password":
            st.session_state['logged_in'] = True
            st.session_state['user_type'] = "gov"
            st.session_state['username'] = username
            return True
        else:
            return False
    elif user_type == "user":
        if not (username and password):
             st.warning("Please enter both username and password.")
             return False
        if not supabase:
            st.error("Database is not connected. Cannot log in.")
            return False
        
        res = supabase.table('user_logins').select('username, hashed_password').eq('username', username).execute()
        if res.data:
            user_data = res.data[0]
            if verify_password(password, user_data['hashed_password']):
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = "user"
                st.session_state['username'] = username
                return True
        return False

# --- Main Page Rendering ---
if st.session_state.get('logged_in'):
    st.sidebar.success(f"Welcome, {st.session_state['username']}!")
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user_type'] = None
        st.session_state['username'] = None
        st.rerun()

    st.title("SiliCoreX Portal Dashboard")
    st.markdown("### Please select a tool from the sidebar to continue.")
    
    if st.session_state.get('user_type') == 'gov':
        st.info("As a government user, you have access to specialized analysis tools.")
        with st.expander("🔑 Admin: Create New User"):
            # ... (create user form code remains unchanged)
            pass 
    else:
        st.info("Welcome! You can view information about the India Semiconductor Mission and find job opportunities.")
else:
    # --- LOGIN PAGE LOGIC ---
    load_css("style.css")
    add_portal_bg_video() # <-- CALL THE NEW BACKGROUND VIDEO FUNCTION

    try:
        header_cols = st.columns([1, 2, 1])
        with header_cols[0]:
            # ... (3D model code remains unchanged)
            pass
        with header_cols[1]:
            st.markdown("""<div class="title-block"><h1 class="main-title">SiliCoreX</h1><p class="subtitle">AI-driven hybrid model for Semiconductor Analytics</p></div>""", unsafe_allow_html=True)
        with header_cols[2]:
            # ... (3D model code remains unchanged)
            pass
    except FileNotFoundError:
        st.error("Header 3D model files not found.")

    if not supabase:
        st.warning("Supabase credentials not found or invalid. Database features are disabled.")

    st.markdown("""
    <div class="glass-card">
        <p class="section-header">Background (Problem)</p>
        <div class="text-block">
             The semiconductor industry faces challenges...
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("gov_login_form"):
            st.markdown('<p class="login-header">Government Login</p>', unsafe_allow_html=True)
            gov_user = st.text_input("Username", key="gov_user")
            gov_pass = st.text_input("Password", type="password", key="gov_pass")
            if st.form_submit_button("Login", use_container_width=True):
                if perform_login(gov_user, gov_pass, "gov"):
                    st.rerun()
                else:
                    st.error("Invalid government credentials.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("user_login_form"):
            st.markdown('<p class="login-header">User Login</p>', unsafe_allow_html=True)
            user_login_user = st.text_input("Username", key="user_login_user")
            user_login_pass = st.text_input("Password", type="password", key="user_login_pass")
            if st.form_submit_button("Login", use_container_width=True):
                if perform_login(user_login_user, user_login_pass, "user"):
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="news-container">
            <div class="news-ticker">
                <p><strong>India's Semiconductor Sector: Three New Plants Get Approved!</strong>...</p>
            </div>
        </div>
    """, unsafe_allow_html=True)