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
        # ... (Header code remains the same)
        with header_cols[0]:
            # ... (3D model code)
        with header_cols[1]:
            st.markdown("""<div class="title-block"><h1 class="main-title">SiliCoreX</h1><p class="subtitle">AI-driven hybrid model for Semiconductor Analytics</p></div>""", unsafe_allow_html=True)
        with header_cols[2]:
            # ... (3D model code)
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
        <div class="text-block">...</div>
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
            user_login_form = st.form("user_login_form")
            with user_login_form:
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

        with register_tab:
            st.markdown('<p class="login-header">Register New User</p>', unsafe_allow_html=True)
            user_reg_form = st.form("user_reg_form")
            with user_reg_form:
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

    # ... (News Ticker code remains the same) ...```

---

### **Phase 2: Adding Social Logins (Google/GitHub)**

Implementing full OAuth (the technology behind social logins) from scratch in Streamlit is extremely complex and can introduce security risks if not done perfectly.

The industry-standard and most secure way to do this is to use a **dedicated authentication service**. A great free option is **Auth0**.

#### **How it Would Work (High-Level Architecture):**

1.  **You would create a free account at [Auth0](https://auth0.com/).**
2.  In Auth0's dashboard, you would enable "Social Connections" for Google and GitHub. This is just a matter of clicking a few buttons.
3.  You would then replace your current login forms with a single "Login" button.
4.  When a user clicks this button, your Streamlit app redirects them to your special Auth0 login page.
5.  The Auth0 page shows the "Login with Google" and "Login with GitHub" buttons automatically.
6.  After the user authenticates, Auth0 securely redirects them back to your Streamlit app, now with a logged-in status.

#### **Adding the Buttons to Your UI**

To show you how it would look, you can add these buttons to your `SiliCoreX_Portal.py` file inside the `user_login_form`. This code won't *work* without the full Auth0 integration, but it will display the buttons correctly.

**In `SiliCoreX_Portal.py`, inside the `with user_login_form:` block, add:**
```python
# ... inside the User Login form ...
st.markdown("<p style='text-align: center; color: white;'>or</p>", unsafe_allow_html=True)
cols = st.columns(2)
cols[0].button("Login with Google", use_container_width=True)
cols[1].button("Login with GitHub", use_container_width=True)