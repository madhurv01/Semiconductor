import pandas as pd
import google.generativeai as genai
import streamlit as st
from translations import LANG_STRINGS, DISTRICT_MAP_EN_KN

@st.cache_data
def load_data():
    """
    Loads the three essential CSV files and standardizes district names.
    """
    try:
        rainfall_data = pd.read_csv('data/karnataka_avg_rain_2023.csv')
        boilers_data = pd.read_csv('data/District_wise_Registered_Boilers.csv')
        roads_data = pd.read_csv('data/Summary_of_length_of_roads.csv')

        rainfall_data.columns = rainfall_data.columns.str.strip()
        boilers_data.columns = boilers_data.columns.str.strip()
        roads_data.columns = roads_data.columns.str.strip()

        if 'District' in rainfall_data.columns:
            rainfall_data['District'] = rainfall_data['District'].str.replace('Mysore', 'Mysuru', case=False)
        if 'DISTRICT' in boilers_data.columns:
            boilers_data['DISTRICT'] = boilers_data['DISTRICT'].str.replace('Mysore', 'Mysuru', case=False)
        if 'District' in roads_data.columns:
            roads_data['District'] = roads_data['District'].str.replace('Mysore', 'Mysuru', case=False)

        return rainfall_data, boilers_data, roads_data
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}. Ensure the CSV files are in the 'data' directory.")
        return None, None, None

def get_llm_analysis_and_stream(district_en, rainfall_data, boilers_data, roads_data, language='en'):
    """
    This function uses a generator to stream the LLM response for a better user experience.
    """
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        if not api_key or "YOUR_API_KEY_HERE" in api_key:
             st.error("Please add your Google Gemini API key to the .streamlit/secrets.toml file.")
             return
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception:
        st.error("Failed to configure the LLM. Please check your API key in the secrets file.")
        return
    
    annual_rainfall_data = rainfall_data.groupby('District')['Avg_rainfall'].sum().reset_index()
    district_rainfall_series = annual_rainfall_data[annual_rainfall_data['District'].str.lower() == district_en.lower()]
    total_annual_rainfall = round(district_rainfall_series['Avg_rainfall'].iloc[0], 2) if not district_rainfall_series.empty else "Not Available"

    district_boilers_data = boilers_data[boilers_data['DISTRICT'].str.lower() == district_en.lower()]
    working_boilers = district_boilers_data['NO.OF WORKING BOILERS'].iloc[0] if not district_boilers_data.empty else "Not Available"

    district_roads = roads_data[roads_data['District'].str.lower() == district_en.lower()]
    total_road_length = district_roads['Total in Kms'].iloc[0] if not district_roads.empty else "Not Available"

    analysis_prompt = f"""
    **Role:** You are a senior semiconductor industry consultant.
    **Analysis Location:** {district_en}, Karnataka, India
    **Key Performance Indicators (KPIs) and Clear Benchmarks:**
    - **Water Security (Total Annual Rainfall):** {total_annual_rainfall} mm
        - *Benchmark:* > 700mm is a **Strength**.
    - **Industrial Ecosystem (Working Boilers):** {working_boilers}
        - *Benchmark:* > 40 is a **Strength**. < 20 is a **Weakness**.
    - **Logistics Infrastructure (Total Road Length):** {total_road_length} Kms
        - *Benchmark:* > 2000 Kms is a **Strength**.
    **Task (Strict Instructions):**
    1.  **Parameter Significance:** Briefly explain the importance of Water, Industrial Ecosystem, and Logistics.
    2.  **Data-Driven Analysis:** Analyze each KPI, stating its value and labeling it as a 'Strength' or 'Weakness'.
    3.  **Synthesis & Conclusion:** Summarize the findings. **Do not write a final verdict yourself.**
    Structure your response with clear, bold headings.
    """

    try:
        report_body_stream = model.generate_content(analysis_prompt, stream=True)
        
        full_report_body = ""
        for chunk in report_body_stream:
            yield chunk.text
            full_report_body += chunk.text
        
        strength_count = full_report_body.count("Strength")
        verdict_text = "Suitable" if strength_count >= 2 else "Not Suitable"
        final_verdict_chunk = f"\n\n**Final Verdict**\n{verdict_text}"

        if language == 'kn':
            translation_prompt = f"Translate the following professional report accurately into formal Kannada. Retain all original Markdown formatting:\n\n---\n\n{full_report_body}{final_verdict_chunk}"
            kannada_report_stream = model.generate_content(translation_prompt, stream=True)
            yield "<STOP_AND_CLEAR>"
            for chunk in kannada_report_stream:
                yield chunk.text
        else:
            yield final_verdict_chunk
            
    except Exception as e:
        st.error(f"An error occurred while communicating with the Gemini API: {e}")

def create_html_report(report_text, language, district_en):
    district_display = DISTRICT_MAP_EN_KN.get(district_en, district_en) if language == 'kn' else district_en
    report_title = LANG_STRINGS['pdf_report_title'][language]
    html_body = report_text.replace('\n', '<br>')
    while '**' in html_body:
        html_body = html_body.replace('**', '<strong>', 1)
        html_body = html_body.replace('**', '</strong>', 1)
    css_style = """<style> @import url('https://fonts.googleapis.com/css2?family=Noto+Sans&family=Noto+Sans+Kannada&display=swap'); body { font-family: 'Noto Sans', sans-serif; margin: 40px; line-height: 1.6; color: #333; background-color: #f9f9f9; } .kannada { font-family: 'Noto Sans Kannada', sans-serif; } .container { max-width: 800px; margin: auto; border: 1px solid #ddd; padding: 30px 50px; box-shadow: 0 0 15px rgba(0,0,0,0.05); background-color: #ffffff; border-radius: 8px; } h1, h2 { text-align: center; color: #0A192F; border-bottom: 2px solid #00A8E8; padding-bottom: 10px; } h2 { font-size: 1.2em; text-align: center; border-bottom: none; color: #555; margin-top: -15px; font-style: italic; } strong { display: block; font-size: 1.2em; margin-top: 25px; margin-bottom: 10px; color: #0A192F; } br { content: ""; margin: 1em; display: block; } </style>"""
    html_doc = f"""<!DOCTYPE html><html lang="{language}"><head><meta charset="UTF-8"><title>{report_title} - {district_display}</title>{css_style}</head><body class="{'kannada' if language == 'kn' else ''}"><div class="container"><h1>{report_title}</h1><h2>- {district_display} -</h2><br>{html_body}</div></body></html>"""
    return html_doc