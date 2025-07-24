import streamlit as st

def render_results_section(results, input_mass):
    """Render the production results section"""
    st.header("📊 Production Results")
    
    cols = st.columns(2)
    
    with cols[0]:
        # Mass and moisture metrics
        st.metric(
            "Final SRF Mass", 
            f"{results['output_mass']:.1f} kg", 
            delta=f"{-input_mass + results['output_mass']:.1f} kg vs input"
        )
        
        st.metric("Effective Moisture", f"{results['effective_moisture']:.1f}%")
        
        # CO2 avoided percentage
        if results['coal_carbon_emissions'] > 0:
            co2_percent = 100 * (1 - results['srf_carbon_emissions']/results['coal_carbon_emissions'])
            st.metric(
                "CO₂ Avoided (%)",
                f"{co2_percent:.1f}%",
                help="CO₂ emissions avoided when using SRF instead of coal"
            )

    with cols[1]:
        # Energy metrics
        st.metric("Heating Value (HHV)", f"{results['hhv']:.1f} MJ/kg")
        
        # Energy equivalents display
        st.markdown(f"""
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px; margin-top: -15px">
            Energy Equivalent
        </div>
        <div style="font-size: 22px; font-weight: bold">
            ⛽ {results['oil_eq']:.1f} kg oil<br>
            ⚫ {results['coal_eq']:.1f} kg coal
        </div>
        """, unsafe_allow_html=True)

    # Moisture warning
    if results['effective_moisture'] > 20:
        st.warning(
            f"⚠️ High Moisture Content: {results['effective_moisture']:.1f}% exceeds maximum "
            "recommended value (20%). This SRF may not meet quality standards. Consider "
            "improving drying efficiency or selecting a more effective drying method."
        )