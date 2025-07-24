# Copyright (c) 2025 Youssef Raslan. All rights reserved.
# Unauthorized use, reproduction, or distribution is strictly prohibited.

import streamlit as st
from config.constants import LOGO_PATH, EMOJIS
from utils.helpers import img_to_base64
from components.header import render_header
from components.input_section import render_input_section
from components.composition_section import render_composition_section
from components.process_section import render_process_section
from components.results_section import render_results_section
from components.classification_section import render_classification_section
from components.report_section import render_report_section
from utils.calculations import calculate_srf_production

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="EcoFuel Pro",
        page_icon="♻️",
        layout="centered"
    )
    
    # Custom CSS for responsive design
    st.markdown("""
    <style>
        @media (max-width: 768px) {
            .brand-logo { height: 50px !important; }
            .brand-text h1 { font-size: 1.8rem !important; }
            .brand-text p { font-size: 0.9rem !important; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    from utils.session_state import initialize_session_state
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Render input sections
    waste_type, input_mass = render_input_section()
    initial_moisture = render_composition_section()
    
    # Render process configuration
    process_config = render_process_section(initial_moisture)
    
    # Perform calculations
    results = calculate_srf_production(
        input_mass, initial_moisture, process_config, st.session_state
    )
    
    # Render results sections
    render_results_section(results, input_mass)
    render_classification_section(results)
    render_report_section(waste_type, input_mass, initial_moisture, 
                         process_config, results)
    
    # Footer
    st.markdown("---")
    st.caption("ℹ Based on CEN/TS 15359 standards for SRF classification")
    st.caption("⚠ Values represent theoretical estimates - actual results may vary")
    
    # Reset button
    if st.button("🧹 Reset All Inputs"):
        from utils.session_state import reset_session_state
        reset_session_state()
        st.rerun()

if __name__ == "__main__":
    main()