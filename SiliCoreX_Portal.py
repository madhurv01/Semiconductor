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
        pass # Errors will be handled where files are used

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

# --- Supabase Initialization (Done once at the top) ---
supabase = None
try:
    # Use the standard, direct method. This will raise an error if secrets are missing.
    if "supabase_url" in st.secrets and "supabase_key" in st.secrets:
        supabase = create_client(st.secrets["supabase_url"], st.secrets["supabase_key"])
except Exception:
    # The warning will be shown on the login page if supabase is still None
    pass

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
        # --- THE DEBUG TOOL ---
        with st.expander("⚙️ Admin Tools & Debug"):
            st.subheader("Secrets Verification")
            st.write("This shows the names of the secrets your deployed app can see.")
            st.write("They MUST exactly match the names used in the code (`supabase_url`, `supabase_key`, `GEMINI_API_KEY`).")
            st.write(st.secrets.keys())

            st.subheader("Create New User")
            if not supabase:
                st.error("Database connection failed. Cannot create user.")
            else:
                with st.form("create_user_form"):
                    new_username = st.text_input("New User's Username")
                    new_password = st.text_input("New User's Password", type="password")
                    if st.form_submit_button("Create User"):
                        if new_username and new_password:
                            res = supabase.table('user_logins').select('username').eq('username', new_username).execute()
                            if res.data:
                                st.error("This username already exists.")
                            else:
                                hashed_pass = hash_password(new_password)
                                supabase.table('user_logins').insert({
                                    "username": new_username,
                                    "user_type": "user",
                                    "hashed_password": hashed_pass
                                }).execute()
                                st.success(f"User '{new_username}' created successfully!")
                        else:
                            st.warning("Please provide both a username and a password.")

    else: # Regular user is logged in
        st.info("You can view information about the **India Semiconductor Mission**.")
else:
    # --- LOGIN PAGE LOGIC ---
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
        st.error("Header 3D model files not found. Please ensure 'chip_left.glb' and 'chip_right.glb' are in the 'images' folder.")

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
        with st.form("user_login_form"):
            st.markdown('<p class="login-header">User Login</p>', unsafe_allow_html=True)
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

    st.markdown("""
        <div class="news-container">
            ...
        </div>
    """, unsafe_allow_html=True)