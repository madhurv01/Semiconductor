import streamlit as st
import os

# --- Page Security ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if not st.session_state.get("logged_in"):
    st.error("Please log in from the main portal to access this page.")
    st.stop() 

# --- Page Content ---
st.title("About the India Semiconductor Mission (ISM)")
st.markdown("---")

# --- First Video Player ---
video_path_1 = "videos/semi.mp4"
if os.path.exists(video_path_1):
    st.video(video_path_1)
else:
    st.warning(f"Video file not found at '{video_path_1}'.")

# --- Expanded Content Section ---
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

# --- NEW: Second Video Player with Heading ---
st.subheader("Why India...?")
video_path_2 = "videos/indi.mp4"
if os.path.exists(video_path_2):
    st.video(video_path_2)
else:
    st.warning(f"Video file not found at '{video_path_2}'.")

st.markdown("---")

# --- Existing "Objectives" Section ---
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