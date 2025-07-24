import streamlit as st
from config.constants import LOGO_PATH
from utils.helpers import img_to_base64

def render_header():
    """Render the application header with logo and branding"""
    logo_base64 = img_to_base64(LOGO_PATH)
    
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: center; margin: -30px 0 25px 0;">
            <img class="brand-logo" src="data:image/png;base64,{logo_base64}" 
                 style="height: 100px; margin-right: 20px; transition: 0.3s all ease;">
            <div class="brand-text" style="border-left: 3px solid #4CAF50; padding-left: 20px;">
                <h1 style="color: #2E7D32; margin: 0 0 5px 0; font-size: 2.5rem;">EcoFuel Pro</h1>
                <p style="color: #666; margin: 0; font-size: 1.1rem;">SRF Production Analysis Suite</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )