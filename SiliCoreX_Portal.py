import streamlit as st
import base64
import os
from supabase import create_client, Client

# --- Page Configuration (Must be the first Streamlit command) ---
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

# --- Login Logic Function ---
def perform_login(username, password, user_type, supabase_client):
    login_successful = False
    if user_type == "gov":
        if username == "madhurvwork@gmail.com" and password == "password":
            login_successful = True
    elif user_type == "user":
        if username:
            login_successful = True

    if login_successful:
        st.session_state['logged_in'] = True
        st.session_state['user_type'] = user_type
        st.session_state['username'] = username
        
        # Write to database on successful login
        if supabase_client:
            try:
                data, count = supabase_client.table('user_logins').insert({
                    "username": username,
                    "user_type": user_type
                }).execute()
            except Exception as e:
                st.error(f"Database Error: Could not log user. Details: {e}")
        return True
    else:
        return False

# --- Main Page Rendering ---

# If user is logged in, show the default themed pages
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

# If user is NOT logged in, show the styled landing/login page
else:
    # --- THE DEFINITIVE FIX: Render all visuals FIRST ---
    load_css("style.css")
    set_page_background('images/background.png')

    try:
        left_gif_b64 = base64.b64encode(open("images/chip_left.gif", "rb").read()).decode()
        right_gif_b64 = base64.b64encode(open("images/chip_right.gif", "rb").read()).decode()
        st.markdown(f"""
            <div class="header-flex-container">
                <img src="data:image/gif;base64,{left_gif_b64}" class="header-gif">
                <div class="title-block">
                    <h1 class="main-title">SiliCoreX</h1>
                    <p class="subtitle">AI-driven hybrid model for Semiconductor Analytics</p>
                </div>
                <img src="data:image/gif;base64,{right_gif_b64}" class="header-gif">
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Header GIF files not found. Please ensure 'chip_left.gif' and 'chip_right.gif' are in the 'images' folder.")

    # --- THEN, handle backend initializations ---
    supabase = None
    if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
        supabase = create_client(supabase_url, supabase_key)
    else:
        st.warning("Supabase credentials not found in secrets. Database logging will be disabled.")

    # --- Static content card ---
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
            gov_submitted = st.form_submit_button("Login", use_container_width=True)
            if gov_submitted:
                if perform_login(gov_user, gov_pass, "gov", supabase):
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    with col2:
        with st.form("user_login_form"):
            st.markdown('<p class="login-header">User Login</p>', unsafe_allow_html=True)
            user_user = st.text_input("Username", key="user_user")
            user_pass = st.text_input("Password (optional)", type="password", key="user_pass")
            user_submitted = st.form_submit_button("Login", use_container_width=True)
            if user_submitted:
                if perform_login(user_user, user_pass, "user", supabase):
                    st.rerun()
                else:
                    st.warning("Please enter a username.")

    # --- News Ticker at the bottom ---
    st.markdown("""
        <div class="news-container">
            <div class="news-ticker">
                <p><strong>India's Semiconductor Sector: Three New Plants Get Approved!</strong> Tata Group and CG Power–Renesas to boost manufacturing capacity. +++ <strong>Major Leap into Manufacturing: 3 Plants, Rs 1.26 Lakh Crore Investment Gets Nod.</strong> A significant step toward becoming self-reliant. +++ <strong>Maharashtra gets a boost with new Rs 63,647 crore plant.</strong> +++</p>
            </div>
        </div>
    """, unsafe_allow_html=True)