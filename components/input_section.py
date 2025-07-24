import streamlit as st

def render_input_section():
    """Render the input waste data section"""
    st.header("🔢 Input Waste Data")
    
    waste_type = st.selectbox(
        "Type of Waste", 
        ["Municipal", "Industrial", "Commercial", "Mixed"]
    )
    
    input_mass = st.number_input(
        "Total Waste Mass (kg)", 
        min_value=0.0, 
        value=0.0, 
        step=100.0
    )
    
    return waste_type, input_mass