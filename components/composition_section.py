import streamlit as st
from config.constants import EMOJIS
from utils.helpers import normalize_composition, create_composition_chart

def render_composition_section():
    """Render the compositional data section"""
    st.header("🧪 Compositional Data")
    
    cols = st.columns(2)
    
    with cols[0]:
        st.subheader("Input Components")
        
        # Component input fields
        for component in st.session_state.composition:
            st.session_state.composition[component] = st.number_input(
                f"{EMOJIS[component]} {component} (%)",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.composition[component],
                key=f"comp_{component}",
                format="%.2f"
            )

    with cols[1]:
        st.subheader("Controls")
        
        # Normalization button
        total_percentage = sum(st.session_state.composition.values())
        if abs(total_percentage - 100) > 0.01 and total_percentage != 0:
            if st.button("✨ Normalize to 100%"):
                normalized = normalize_composition(st.session_state.composition)
                st.session_state.composition.update(normalized)
                st.rerun()
        
        # Composition chart
        chart = create_composition_chart(st.session_state.composition)
        if chart:
            st.pyplot(chart)
        else:
            st.markdown("""<div style='border: 2px dashed #ccc; padding: 20px; text-align: center;'>
                            📭 No composition data</div>""", unsafe_allow_html=True)
        
        # Total percentage display
        status_color = "green" if abs(total_percentage - 100) < 0.01 else "red"
        st.markdown(f"""<div style='padding:10px; background-color:{status_color}20;'>
                        <h3 style='color:{status_color};'>Total: {total_percentage:.2f}%</h3></div>""",
                    unsafe_allow_html=True)

    # Moisture content calculation and input
    initial_moisture = _render_moisture_input()
    
    # Contaminants section
    _render_contaminants_section()
    
    return initial_moisture

def _render_moisture_input():
    """Render moisture content input with dynamic range based on organic waste"""
    if st.session_state.composition["Organic Waste"]:
        min_moisture = 0.7 * st.session_state.composition["Organic Waste"]
        if min_moisture > 50:
            min_moisture = 50
        initial_moisture = st.slider(
            "Initial Moisture Content (%)",
            min_value=float(min_moisture),
            max_value=85.0,
            value=float(min_moisture),
            step=0.1,
            format="%.1f"
        )
    else:
        initial_moisture = st.slider(
            "Initial Moisture Content (%)",
            0.0,
            85.0,
            25.0,
            step=0.1,
            format="%.1f"
        )

    # Moisture check notification
    if initial_moisture < 20:
        st.info("✅ No drying required. The initial moisture content is already below 20%, which is optimal for SRF production.")
    
    return initial_moisture

def _render_contaminants_section():
    """Render contaminants input section"""
    st.subheader("🛑 Contaminants (Optional)")
    
    st.session_state.contaminants['Chlorine'] = st.number_input(
        "Chlorine (%)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.contaminants['Chlorine'],
        key="cont_Chlorine",
        format="%.2f",
        help="Chlorine content in waste mixture"
    )

    st.session_state.contaminants['Mercury_median'] = st.number_input(
        "Mercury (Median) (mg/MJ, ar)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.contaminants['Mercury_median'],
        key="cont_Mercury_median",
        format="%.4f",
        help="Mercury content (median) in mg/MJ (as received)"
    )
    
    st.session_state.contaminants['Mercury_80th'] = st.number_input(
        "Mercury (80th Percentile) (mg/MJ, ar)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.contaminants['Mercury_80th'],
        key="cont_Mercury_80th",
        format="%.4f",
        help="Mercury content (80th percentile) in mg/MJ (as received)"
    )