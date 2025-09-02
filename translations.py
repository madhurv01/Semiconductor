# Central repository for all UI text strings and mappings
LANG_STRINGS = {
    'title': {
        'en': "🤖 LLM-Powered Semiconductor Site Analysis",
        'kn': "🤖 ಎಲ್ಎಲ್ಎಂ-ಚಾಲಿತ ಸೆಮಿಕಂಡಕ್ಟರ್ ಸೈಟ್ ವಿಶ್ಲೇಷಣೆ"
    },
    'caption': {
        'en': "This tool uses the Google Gemini LLM to analyze the suitability of a location for a semiconductor manufacturing unit based on key infrastructure data.",
        'kn': "ಈ ಉಪಕರಣವು ಪ್ರಮುಖ ಮೂಲಸೌಕರ್ಯ ಡೇಟಾವನ್ನು ಆಧರಿಸಿ ಸೆಮಿಕಂಡಕ್ಟರ್ ತಯಾರಿಕಾ ಘಟಕಕ್ಕೆ ಸ್ಥಳದ ಸೂಕ್ತತೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಲು ಗೂಗಲ್ ಜೆಮಿನಿ ಎಲ್ಎಲ್ಎಂ ಅನ್ನು ಬಳಸುತ್ತದೆ."
    },
    'sidebar_header': {
        'en': "Settings",
        'kn': "ಸಂಯೋಜನೆಗಳು"
    },
    'lang_label': {
        'en': "Select Language",
        'kn': "ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ"
    },
    'site_selection_header': {
        'en': "Site Selection",
        'kn': "ಸೈಟ್ ಆಯ್ಕೆ"
    },
    'site_selection_info': {
        'en': "Select a district from Karnataka to generate an AI-powered feasibility report.",
        'kn': "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ-ಚಾಲಿತ ಕಾರ್ಯಸಾಧ್ಯತಾ ವರದಿಯನ್ನು ರಚಿಸಲು ಕರ್ನಾಟಕದ ಒಂದು ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ."
    },
    'district_label': {
        'en': "Select District",
        'kn': "ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ"
    },
    'analyze_button': {
        'en': "Analyze with Gemini AI",
        'kn': "ಜೆಮಿನಿ AI ನೊಂದಿಗೆ ವಿಶ್ಲೇಷಿಸಿ"
    },
    'spinner_text': {
        'en': "Querying Gemini LLM for analysis on {district}... This may take a moment.",
        'kn': "{district} ಕುರಿತು ವಿಶ್ಲೇಷಣೆಗಾಗಿ ಜೆಮಿನಿ ಎಲ್ಎಲ್ಎಂ ಅನ್ನು ಪ್ರಶ್ನಿಸಲಾಗುತ್ತಿದೆ... ಇದು ಸ್ವಲ್ಪ ಸಮಯ ತೆಗೆದುಕೊಳ್ಳಬಹುದು."
    },
    'report_header': {
        'en': "Feasibility Report for {district}",
        'kn': "{district} ಗಾಗಿ ಕಾರ್ಯಸಾಧ್ಯತಾ ವರದಿ"
    },
    'success_message': {
        'en': "Report generated successfully.",
        'kn': "ವರದಿಯನ್ನು ಯಶಸ್ವಿಯಾಗಿ ರಚಿಸಲಾಗಿದೆ."
    },
    'error_message': {
        'en': "Could not generate the report. Please check the error messages above.",
        'kn': "ವರದಿಯನ್ನು ರಚಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮೇಲಿನ ದೋಷ ಸಂದೇಶಗಳನ್ನು ಪರಿಶೀಲಿಸಿ."
    },
    'data_load_error': {
        'en': "Application cannot start because one or more data files failed to load. Please check the 'data' directory.",
        'kn': "ಒಂದು ಅಥವಾ ಹೆಚ್ಚು ಡೇಟಾ ಫೈಲ್‌ಗಳು ಲೋಡ್ ಆಗದ ಕಾರಣ ಅಪ್ಲಿಕೇಶನ್ ಪ್ರಾರಂಭಿಸಲು ಸಾಧ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು 'data' ಡೈರೆಕ್ಟರಿಯನ್ನು ಪರಿಶೀಲಿಸಿ."
    },
    'download_button': {
        'en': "📄 Download Report as HTML",
        'kn': "📄 ವರದಿಯನ್ನು HTML ಆಗಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ"
    },
    'pdf_report_title': { # Note: Re-using this key for the HTML title
        'en': "Semiconductor Fab Site Feasibility Report",
        'kn': "ಸೆಮಿಕಂಡಕ್ಟರ್ ಫ್ಯಾಬ್ ಸೈಟ್ ಕಾರ್ಯಸಾಧ್ಯತಾ ವರದಿ"
    },
    'job_portal_title': {
        'en': "🛰️ Semiconductor Job Portal",
        'kn': "🛰️ ಸೆಮಿಕಂಡಕ್ಟರ್ ಉದ್ಯೋಗ ಪೋರ್ಟಲ್"
    },
    'job_portal_info': {
        'en': "Find real-time job openings in the Indian semiconductor industry from top hiring platforms.",
        'kn': "ಉನ್ನತ ನೇಮಕಾತಿ ಪ್ಲಾಟ್‌ಫಾರ್ಮ್‌ಗಳಿಂದ ಭಾರತೀಯ ಸೆಮಿಕಂಡಕ್ಟರ್ ಉದ್ಯಮದಲ್ಲಿ ನೈಜ-ಸಮಯದ ಉದ್ಯೋಗಾವಕಾಶಗಳನ್ನು ಹುಡುಕಿ."
    },
    'job_type_label': {
        'en': "Select Job Type",
        'kn': "ಉದ್ಯೋಗ ಪ್ರಕಾರವನ್ನು ಆಯ್ಕೆಮಾಡಿ"
    },
    'experience_label': {
        'en': "Experience in Years",
        'kn': "ವರ್ಷಗಳ ಅನುಭವ"
    },
    'search_button': {
        'en': "Search for Jobs",
        'kn': "ಉದ್ಯೋಗಗಳಿಗಾಗಿ ಹುಡುಕಿ"
    },
    'spinner_text_jobs': {
        'en': "Searching for {job_type} jobs with {experience} years experience...",
        'kn': "{experience} ವರ್ಷಗಳ ಅನುಭವದೊಂದಿಗೆ {job_type} ಉದ್ಯೋಗಗಳಿಗಾಗಿ ಹುಡುಕಲಾಗುತ್ತಿದೆ..."
    },
    'results_header': {
        'en': "Search Results ({count} found)",
        'kn': "ಹುಡುಕಾಟ ಫಲಿತಾಂಶಗಳು ({count} ಸಿಕ್ಕಿವೆ)"
    },
    'no_results_warning': {
        'en': "No job openings found matching your criteria. Try broadening your search.",
        'kn': "ನಿಮ್ಮ ಮಾನದಂಡಗಳಿಗೆ ಹೊಂದುವ ಯಾವುದೇ ಉದ್ಯೋಗಾವಕಾಶಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ನಿಮ್ಮ ಹುಡುಕಾಟವನ್ನು ವಿಸ್ತರಿಸಲು ಪ್ರಯತ್ನಿಸಿ."
    },
    'apply_button_text': {
        'en': "Apply Now &rarr;",
        'kn': "ಈಗ ಅನ್ವಯಿಸಿ &rarr;"
    },
    # --- Job Type Translations ---
    'job_types': {
        'en': ["Hardware", "Software", "VLSI Design", "Chip Design", "Verification", "Firmware"],
        'kn': ["ಹಾರ್ಡ್‌ವೇರ್", "ಸಾಫ್ಟ್‌ವೇರ್", "ವಿಎಲ್‌ಎಸ್‌ಐ ವಿನ್ಯಾಸ", "ಚಿಪ್ ವಿನ್ಯಾಸ", "ಪರಿಶೀಲನೆ", "ಫರ್ಮ್‌ವೇರ್"]
    }
}

# Mapping of English district names (from CSV) to Kannada
DISTRICT_MAP_EN_KN = {
    'Bagalkote': 'ಬಾಗಲಕೋಟೆ', 'Bangalore Rural': 'ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ', 'Bangalore Urban': 'ಬೆಂಗಳೂರು ನಗರ', 'Belagavi': 'ಬೆಳಗಾವಿ', 'Bellary': 'ಬಳ್ಳಾರಿ', 'Bidar': 'ಬೀದರ್', 'Chamarajanagar': 'ಚಾಮರಾಜನಗರ', 'Chikkaballapur': 'ಚಿಕ್ಕಬಳ್ಳಾಪುರ', 'Chikkamagaluru': 'ಚಿಕ್ಕಮಗಳೂರು', 'Chitradurga': 'ಚಿತ್ರದುರ್ಗ', 'Dakshina Kannada': 'ದಕ್ಷಿಣ ಕನ್ನಡ', 'Davanagere': 'ದಾವಣಗೆರೆ', 'Dharwad': 'ಧಾರವಾಡ', 'Gadag': 'ಗದಗ', 'Hassan': 'ಹಾಸನ', 'Haveri': 'ಹಾವೇರಿ', 'Kalaburagi': 'ಕಲಬುರಗಿ', 'Kodagu': 'ಕೊಡಗು', 'Kolar': 'ಕೋಲಾರ', 'Koppal': 'ಕೊಪ್ಪಳ', 'Mandya': 'ಮಂಡ್ಯ', 'Mysuru': 'ಮೈಸೂರು', 'Raichur': 'ರಾಯಚೂರು', 'Ramanagara': 'ರಾಮನಗರ', 'Shivamogga': 'ಶಿವಮೊಗ್ಗ', 'Tumakuru': 'ತುಮಕೂರು', 'Udupi': 'ಉಡುಪಿ', 'Uttara Kannada': 'ಉತ್ತರ ಕನ್ನಡ', 'Vijayapura': 'ವಿಜಯಪುರ', 'Yadgir': 'ಯಾದಗಿರಿ'
}

# Create a reverse mapping from Kannada to English for easy lookup
DISTRICT_MAP_KN_EN = {v: k for k, v in DISTRICT_MAP_EN_KN.items()}