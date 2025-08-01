import streamlit as st
import base64
import os
from supabase import create_client, Client
import streamlit.components.v1 as components
import bcrypt

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
        st.warning(f"Background image not found at '{png_file}'.")

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

    supabase = None
    try:
        url = st.secrets.get("supabase_url") or st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("supabase_key") or st.secrets.get("SUPABASE_KEY")
        if url and key:
            supabase = create_client(url, key)
        else:
            st.warning("Supabase credentials not found. Database features disabled.")
    except Exception as e:
        st.warning(f"Could not connect to Supabase. DB features disabled. Error: {e}")

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
                if gov_user == "madhurvwork@gmail.com" and gov_pass == "password":
                    st.session_state['logged_in'] = True
                    st.session_state['user_type'] = "gov"
                    st.session_state['username'] = gov_user
                    st.rerun()
                else:
                    st.error("Invalid government credentials.")

    with col2:
        st.markdown('<div class="glass-card" style="padding: 2rem 2.5rem;">', unsafe_allow_html=True)
        login_tab, register_tab = st.tabs(["Login", "Register"])
        
        with login_tab:
            st.markdown('<p class="login-header">User Login</p>', unsafe_allow_html=True)
            with st.form("user_login_form"):
                user_login_user = st.text_input("Username", key="user_login_user")
                user_login_pass = st.text_input("Password", type="password", key="user_login_pass")
                if st.form_submit_button("Login", use_container_width=True):
                    if not supabase:
                        st.error("Database is not connected. Cannot log in.")
                    elif user_login_user and user_login_pass:
                        res = supabase.table('user_logins').select('username, hashed_password').eq('username', user_login_user).execute()
                        if res.data:
                            user_data = res.data[0]
                            if verify_password(user_login_pass, user_data['hashed_password']):
                                st.session_state['logged_in'] = True
                                st.session_state['user_type'] = "user"
                                st.session_state['username'] = user_login_user
                                st.rerun()
                            else:
                                st.error("Incorrect username or password.")
                        else:
                            st.error("Incorrect username or password.")
                    else:
                        st.warning("Please enter username and password.")
                
                st.markdown("<p style='text-align: center; color: white;'>or</p>", unsafe_allow_html=True)
                social_cols = st.columns(2)
                social_cols[0].button("Login with Google", use_container_width=True, key="google_login")
                social_cols[1].button("Login with GitHub", use_container_width=True, key="github_login")


        with register_tab:
            st.markdown('<p class="login-header">Register New User</p>', unsafe_allow_html=True)
            with st.form("user_reg_form"):
                user_reg_user = st.text_input("Username", key="user_reg_user")
                user_reg_pass = st.text_input("Password", type="password", key="user_reg_pass")
                if st.form_submit_button("Register", use_container_width=True):
                    if not supabase:
                        st.error("Database is not connected. Cannot register.")
                    elif user_reg_user and user_reg_pass:
                        res = supabase.table('user_logins').select('username').eq('username', user_reg_user).execute()
                        if res.data:
                            st.error("Username already exists.")
                        else:
                            hashed_pass = hash_password(user_reg_pass)
                            supabase.table('user_logins').insert({
                                "username": user_reg_user,
                                "user_type": "user",
                                "hashed_password": hashed_pass
                            }).execute()
                            st.success("Registration successful! Please log in using the Login tab.")
                    else:
                        st.warning("Please enter a username and password.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="news-container">
            <div class="news-ticker">
                <p><strong>India's Semiconductor Sector: Three New Plants Get Approved!</strong> Tata Group and CG Power–Renesas to boost manufacturing capacity. +++ <strong>Major Leap into Manufacturing: 3 Plants, Rs 1.26 Lakh Crore Investment Gets Nod.</strong> A significant step toward becoming self-reliant. +++ <strong>Maharashtra gets a boost with new Rs 63,647 crore plant.</strong> +++</p>
            </div>
        </div>
    """, unsafe_allow_html=True)