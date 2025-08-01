import streamlit as st
import base64
import os
from supabase import create_client, Client
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="SiliCoreX Portal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Function to load and apply CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- Function to set background image ---
def set_page_background(png_file):
    try:
        with open(png_file, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Background image not found at '{png_file}'. Please ensure it is in the 'images' folder.")

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
    # Check for secrets and create the client
    if "supabase_url" in st.secrets and "supabase_key" in st.secrets:
        supabase = create_client(st.secrets["supabase_url"], st.secrets["supabase_key"])
except Exception:
    # Fail silently, the warning will be shown on the page
    pass

# --- Login Logic Function ---
def perform_login(username, password, user_type):
    login_successful = False
    if user_type == "gov":
        if username == "madhurvwork@gmail.com" and password == "password":
            login_successful = True
    elif user_type == "user":
        if username: # User only needs a username to log in
            login_successful = True

    if login_successful:
        st.session_state['logged_in'] = True
        st.session_state['user_type'] = user_type
        st.session_state['username'] = username
        
        # Log the successful login to the database
        if supabase:
            try:
                supabase.table('user_logins').insert({
                    "username": username,
                    "user_type": user_type
                }).execute()
            except Exception:
                # If DB write fails, don't block the login
                pass 
        return True
    else:
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
        st.info("As a government user, you have access to the **Site Analysis Tool**.")
    else:
        st.info("You can view information about the **India Semiconductor Mission**.")
else:
    load_css("style.css")
    set_page_background('images/background.png')

    try:
        header_cols = st.columns([1, 2, 1])
        with header_cols[0]:
            with open("images/chip_left.glb", "rb") as f:
                left_model_data = f.read()
            left_model_b64 = base64.b64encode(left_model_data).decode()
            left_model_src = f"data:model/gltf-binary;base64,{left_model_b64}"
            components.html(f"""<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script><model-viewer class="model-viewer" src="{left_model_src}" alt="A 3D model" auto-rotate camera-controls shadow-intensity="1"></model-viewer>""", height=160)
        with header_cols[1]:
            st.markdown("""<div class="title-block"><h1 class="main-title">SiliCoreX</h1><p class="subtitle">AI-driven hybrid model for Semiconductor Analytics</p></div>""", unsafe_allow_html=True)
        with header_cols[2]:
            with open("images/chip_right.glb", "rb") as f:
                right_model_data = f.read()
            right_model_b64 = base64.b64encode(right_model_data).decode()
            right_model_src = f"data:model/gltf-binary;base64,{right_model_b64}"
            components.html(f"""<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script><model-viewer class="model-viewer" src="{right_model_src}" alt="A 3D model" auto-rotate camera-controls shadow-intensity="1"></model-viewer>""", height=160)
    except FileNotFoundError:
        st.error("Header 3D model files not found.")

    if not supabase:
        st.warning("Supabase credentials not found or invalid. Database features are disabled.")

    st.markdown("""
    <div class="glass-card">
        <p class="section-header">Background (Problem)</p>
        <div class="text-block">
            The semiconductor industry faces challenges in site selection, resource management, and profitability forecasting due to complex dependencies on economic, logistical, and environmental factors. With rising demand for chips and constrained resources like pure water and raw materials, there is a critical need for data-driven tools to optimize manufacturing unit establishment and operations. The Indian government has launched ambitious initiatives under the <strong>India Semiconductor Mission (ISM)</strong> to build a self-reliant ecosystem.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        with st.form("gov_login_form"):
            st.markdown('<p class="login-header">Government Login</p>', unsafe_allow_html=True)
            gov_user = st.text_input("Username", key="gov_user")
            gov_pass = st.text_input("Password", type="password", key="gov_pass")
            if st.form_submit_button("Login", use_container_width=True):
                if perform_login(gov_user, gov_pass, "gov"):
                    st.rerun()
                else:
                    st.error("Invalid government credentials.")

    with col2:
        with st.form("user_login_form"):
            st.markdown('<p class="login-header">User Login</p>', unsafe_allow_html=True)
            user_user = st.text_input("Username", key="user_user")
            user_pass = st.text_input("Password (optional)", type="password", key="user_pass")
            if st.form_submit_button("Login", use_container_width=True):
                if perform_login(user_user, user_pass, "user"):
                    st.rerun()
                else:
                    st.warning("Please enter a username.")

    st.markdown("""
        <div class="news-container">
            <div class="news-ticker">
                <p><strong>India's Semiconductor Sector: Three New Plants Get Approved!</strong> Tata Group and CG Power–Renesas to boost manufacturing capacity. +++ <strong>Major Leap into Manufacturing: 3 Plants, Rs 1.26 Lakh Crore Investment Gets Nod.</strong> A significant step toward becoming self-reliant. +++ <strong>Maharashtra gets a boost with new Rs 63,647 crore plant.</strong> +++</p>
            </div>
        </div>
    """, unsafe_allow_html=True)