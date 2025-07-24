import streamlit as st
from config.constants import DRYING_METHODS
from utils.helpers import create_process_flow_html

def render_process_section(initial_moisture):
    """Render the SRF production process configuration section"""
    st.header("⚙ SRF Production Process Configuration")
    
    # Determine process flow based on moisture content
    process_config = _configure_process_flow(initial_moisture)
    
    # Display process flow diagram
    _display_process_flow(process_config['process_flow'])
    
    # Configure process parameters
    _configure_process_parameters(process_config, initial_moisture)
    
    return process_config

def _configure_process_flow(initial_moisture):
    """Configure the process flow based on initial moisture content"""
    if initial_moisture < 20:
        mandatory_steps = ["Presorting", "Primary Shredding", "Mechanical Separation"]
    else:
        mandatory_steps = ["Presorting", "Primary Shredding", "Mechanical Separation", "Drying"]

    process_flow = mandatory_steps.copy()
    
    # Optional secondary shredding
    if st.checkbox("Include Secondary Shredding", help="Optional fine shredding"):
        process_flow.append("Secondary Shredding")
    
    return {
        'process_flow': process_flow,
        'drying_method_1': None,
        'drying_method_2': None,
        'shred_type': None,
        'intermediate_moisture': initial_moisture,
        'final_moisture': initial_moisture
    }

def _display_process_flow(process_flow):
    """Display the process flow diagram"""
    st.markdown("### Process Flow Diagram")
    flow_html = create_process_flow_html(process_flow)
    st.markdown(flow_html, unsafe_allow_html=True)

def _configure_process_parameters(process_config, initial_moisture):
    """Configure detailed process parameters"""
    with st.expander("⚙ Process Parameters Configuration"):
        cols = st.columns(2) if "Secondary Shredding" in process_config['process_flow'] else [st.container()]
        
        # Secondary shredding parameters
        if "Secondary Shredding" in process_config['process_flow']:
            with cols[0]:
                process_config['shred_type'] = _configure_secondary_shredding()
            drying_col = cols[1]
        else:
            drying_col = cols[0] if isinstance(cols, list) else cols

        # Drying parameters
        with drying_col:
            if initial_moisture >= 20:
                _configure_drying_methods(process_config, initial_moisture)

def _configure_secondary_shredding():
    """Configure secondary shredding parameters"""
    st.subheader("Secondary Shredding Parameters")
    
    shred_type = st.radio(
        "Particle Size Target:",
        ["Fine (<50mm)", "Medium (50-100mm)", "Rough (>100mm)"],
        help="Final particle size distribution"
    )
    
    # Display mass loss information
    loss_mapping = {
        "Fine (<50mm)": 0.05,
        "Medium (50-100mm)": 0.017,
        "Rough (>100mm)": 0.008
    }
    
    loss = loss_mapping[shred_type]
    st.caption(f"Mass loss: {loss*100:.1f}%")
    
    return shred_type

def _configure_drying_methods(process_config, initial_moisture):
    """Configure drying methods"""
    st.subheader("Primary Drying Method")
    
    # Primary drying method selection
    applicable_methods_1 = [
        method for method, details in DRYING_METHODS.items() 
        if details['applicable_moisture'][0] <= initial_moisture <= details['applicable_moisture'][1]
    ]
    
    drying_method_1 = st.selectbox(
        "Select Primary Drying Method", 
        options=applicable_methods_1,
        key="drying_method_1",
        help="Select a drying method applicable to the current moisture content"
    )
    
    process_config['drying_method_1'] = drying_method_1
    
    if drying_method_1:
        details_1 = DRYING_METHODS[drying_method_1]
        intermediate_moisture = details_1['output_moisture']
        process_config['intermediate_moisture'] = intermediate_moisture
        
        st.write(f"Moisture after primary drying: {intermediate_moisture}%")
        
        # Secondary drying method selection
        st.subheader("Secondary Drying Method (Optional)")
        
        applicable_methods_2 = [
            method for method, details in DRYING_METHODS.items() 
            if details['applicable_moisture'][0] <= intermediate_moisture <= details['applicable_moisture'][1]
        ]
        
        drying_method_2 = st.selectbox(
            "Select Secondary Drying Method", 
            options=[None] + applicable_methods_2,
            key="drying_method_2",
            help="Optional second drying method to further reduce moisture"
        )
        
        process_config['drying_method_2'] = drying_method_2
        
        if drying_method_2:
            details_2 = DRYING_METHODS[drying_method_2]
            final_moisture = details_2['output_moisture']
            process_config['final_moisture'] = final_moisture
            st.write(f"Final moisture after secondary drying: {final_moisture}%")
        else:
            process_config['final_moisture'] = intermediate_moisture