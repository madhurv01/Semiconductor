import streamlit as st

# --- Page Configuration and Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# This check ensures that a user must be logged in to see this page.
if not st.session_state.get("logged_in"):
    st.error("Please log in from the main portal to access this page.")
    st.stop() # Stop execution if not logged in

# --- Page Content ---
st.title("About the India Semiconductor Mission (ISM)")
st.markdown("---")

st.markdown("""
The **India Semiconductor Mission (ISM)** was launched by the Government of India with a vision to build a vibrant semiconductor and display ecosystem to enable India’s emergence as a global hub for electronics manufacturing and design.
""")

col1, col2 = st.columns([1, 2])

with col1:
    if "images/ism_logo.png":
        st.image("images/ism_logo.png", caption="Logo of the India Semiconductor Mission")

with col2:
    st.markdown("""
    #### Key Objectives of the Mission:
    - **Develop a robust and sustainable semiconductor manufacturing ecosystem.**
    - **Promote research and innovation** in semiconductor design and manufacturing.
    - **Attract significant investments** from global semiconductor companies.
    - **Create a skilled workforce** to support the growing industry.
    - **Achieve self-reliance** in a critical, strategic sector of the economy.
    """)

st.markdown("---")
st.markdown("#### The Path to a Self-Reliant India")
st.markdown("""
By providing substantial financial incentives and policy support, the ISM aims to establish large-scale semiconductor fabrication plants (fabs), display fabs, and other parts of the supply chain, including packaging, assembly, and testing units. This strategic initiative is poised to reduce India's dependence on imports, bolster national security, and create millions of high-value jobs.
""")

if "images/fab_plant.png":
    st.image("images/fab_plant.png", caption="An advanced semiconductor fabrication plant (fab).")