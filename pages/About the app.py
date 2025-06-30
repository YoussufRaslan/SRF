import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

LOGO_PATH = "sustainability-squad-high-resolution-logo-transparent.png"
# Page configuration
st.set_page_config(page_title="EcoFuel Pro - Introduction", page_icon="ℹ️")

# Title with logo
col1, col2 = st.columns([1, 3])
with col1:
    st.image(LOGO_PATH, width=1350)  
with col2:
    st.title("Welcome to EcoFuel Pro")

# Introduction section
st.markdown("""
<div style='background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px;'>
<h3 style='color:#2E7D32;'>♻️ About This Tool</h3>
<p>Developed by chemical engineering students, this tool helps beginners in environmental engineering with calculations related to <strong>Solid Recovered Fuel (SRF)</strong> production and analysis.</p>
</div>
""", unsafe_allow_html=True)

# What is SRF section
st.header("🔍 What is SRF?")
st.markdown("""
**Solid Recovered Fuel (SRF)** is a sustainable waste-to-energy technology that converts various waste types into valuable fuel:

- Municipal waste 🏙️
- Industrial waste 🏭  
- Commercial waste 🏢
- Mixed waste 🗑️

Through specific processing steps shown in our interactive block flow diagram, this waste is transformed into SRF.
""")

with st.expander("📚 Learn more about SRF"):
    st.markdown("""
    - **Energy Content**: Typically 10-25 MJ/kg (compared to coal at ~24 MJ/kg)
    - **Environmental Benefit**: Reduces landfill use and fossil fuel dependence
    - **Contaminants**: May contain chlorine (corrosion risk) and mercury (toxic emissions)
    """)

# Report Preview Section
st.header("📊 Report Contents")
st.markdown("""
Your generated report will include:
<div style='margin-left:20px;'>
<div style='display:flex; align-items:center; margin:5px 0;'>🔥 <div style='margin-left:10px;'><b>Energy Analysis</b><br>Calorific value and fuel equivalents</div></div>
<div style='display:flex; align-items:center; margin:5px 0;'>🌱 <div style='margin-left:10px;'><b>Avoided CO₂</b><br>Percentage avoided vs conventional fuels</div></div>
<div style='display:flex; align-items:center; margin:5px 0;'>🏷️ <div style='margin-left:10px;'><b>Quality Classification</b><br>EN 15359 standard rating</div></div>
</div>
""", unsafe_allow_html=True)

# How It Works Section
st.header("🛠️ How to Use This Tool")
steps = [
    {"icon": "1️⃣", "title": "Waste Selection", "desc": "Choose type and mass of waste"},
    {"icon": "2️⃣", "title": "Composition Analysis", "desc": "Input component percentages"},
    {"icon": "3️⃣", "title": "Contaminant Check", "desc": "Specify chlorine/mercury levels"},
    {"icon": "4️⃣", "title": "Process Customization", "desc": "Modify the processing steps"},
    {"icon": "5️⃣", "title": "Results Analysis", "desc": "View energy recovery and classification"},
    {"icon": "6️⃣", "title": "Report Generation", "desc": "Download detailed PDF report"}
]

for step in steps:
    with st.container():
        st.markdown(f"""
        <div style='display:flex; align-items:center; background-color:#f9f9f9; padding:15px; border-radius:10px; margin:5px 0;'>
            <span style='font-size:1.5em; margin-right:15px;'>{step['icon']}</span>
            <div>
                <strong>{step['title']}</strong><br>
                {step['desc']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Final note
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:20px; background-color:#e8f5e9; border-radius:10px;'>
    We hope you enjoy using <strong>EcoFuel Pro</strong> and that it helps you understand SRF production and its environmental benefits! 🌍
</div>
""", unsafe_allow_html=True)