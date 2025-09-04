import streamlit as st
import os
import base64

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
        [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {{
            background: rgba(10, 25, 47, 0.45); /* Highly transparent */
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(0, 168, 232, 0.2);
            margin-bottom: 20px;
        }}
        /* Enhance text readability with a stronger shadow */
        h1, h2, h3, h4, p, .st-emotion-cache-1yy083c, .st-emotion-cache-1629p8f, .st-emotion-cache-1njjmv6, .st-emotion-cache-1r6slb0, .st-emotion-cache-1hg5474, .st-emotion-cache-1q8dd3i {{
             text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image 'ism.jpg' not found. Please add it to the 'images' folder.")

# --- Call the function to set the background ---
add_page_bg("images/ism.jpg")


# --- Page Content ---
st.title("About the India Semiconductor Mission (ISM)")
st.markdown("---")

st.markdown("""
The **India Semiconductor Mission (ISM)** was launched by the Government of India with a vision to build a vibrant semiconductor and display ecosystem to enable India’s emergence as a global hub for electronics manufacturing and design.
""")

st.subheader("Why India is a Potential Semiconductor Manufacturing Hub")
st.markdown("""
India is strategically positioning itself to become a key player in the global semiconductor landscape. This ambition is not just based on policy but is supported by a unique combination of demographic, economic, and geopolitical advantages.
""")

st.markdown("""
*   **Massive Talent Pool:** India produces millions of STEM (Science, Technology, Engineering, and Mathematics) graduates annually. This creates a vast and sustainable talent pool of engineers and technicians, which is the most critical resource for operating high-tech semiconductor fabs. Global companies already leverage India for its massive R&D and design workforce.

*   **Growing Domestic Market:** With over a billion mobile phone users, a rapidly growing automotive market, and increasing demand for consumer electronics, India represents one of the largest and fastest-growing markets for semiconductors in the world. Manufacturing locally allows companies to serve this massive internal demand more efficiently.

*   **Government Support and Policy Incentives:** The India Semiconductor Mission (ISM) is a clear statement of intent. The government is offering significant financial incentives, including production-linked incentive (PLI) schemes that can cover up to 50% of the project's capital expenditure. This drastically reduces the financial risk for companies looking to set up new fabs.

*   **Geopolitical Strategy & Supply Chain Diversification:** Global events have highlighted the risks of a geographically concentrated semiconductor supply chain. The "China Plus One" strategy is encouraging global corporations to diversify their manufacturing bases. As a stable democracy with strong international partnerships, India is an attractive and reliable alternative for de-risking the global supply chain.
""")

st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    if os.path.exists("images/ism_logo.png"):
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

if os.path.exists("images/fab_plant.png"):
    st.image("images/fab_plant.png", caption="An advanced semiconductor fabrication plant (fab).")