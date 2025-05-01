import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuration
st.set_page_config(page_title="SRF Production Calculator", layout="centered")
st.title("Solid Recovered Fuel (SRF) Production Calculator")

# Constants
EMOJIS = {
    "Plastic": "🧴",
    "Paper & Cardboard": "📦",
    "Textiles": "👕",
    "Biogenic Waste": "🌿",
    "Inert Materials": "🪨",
    "Other Materials": "♻",
    "Waste Collection": "🗑️",
    "Presorting": "↔️",
    "Primary Shredding": "🔩",
    "Mechanical Separation": "🧲",
    "Drying": "🔥",
    "Secondary Shredding": "⚙️",
    "Homogenization": "🔄",
    "Quality Control": "✔️",
    "Storage & Packaging": "📦"
}

HHV_VALUES = {
    "Plastic": 36.5,
    "Paper & Cardboard": 15.8,
    "Textiles": 19.2,
    "Biogenic Waste": 11.3,
    "Inert Materials": 0.5,
    "Other Materials": 9.7
}

# Session state initialization
if 'composition' not in st.session_state:
    st.session_state.composition = {
        "Plastic": 0.0,
        "Paper & Cardboard": 0.0,
        "Textiles": 0.0,
        "Biogenic Waste": 0.0,
        "Inert Materials": 0.0,
        "Other Materials": 0.0
    }

if 'contaminants' not in st.session_state:
    st.session_state.contaminants = {
        'Chlorine': 0.0,
        'Mercury_median': 0.0,
        'Mercury_80th': 0.0,
    }

# Updated drying methods database with real-world parameters
DRYING_METHODS = {  
    "Mechanical Press": {
        "applicable_moisture": (55, 65),
        "output_moisture": 40,
        "energy": "Low",
        "speed": "Hours",
        "equation": r"M_{out} = M_{in} \times (1 - 0.25t)",
        "info": "Mechanical dehydration using presses/screens for initial moisture reduction",
        "loss": 0.05
    },
    "Biodrying": {
        "applicable_moisture": (35, 55),
        "output_moisture": 17,
        "energy": "Low",
        "speed": "Days",
        "equation": r"M_{out} = 0.85M_{in} \times e^{-0.1t}",
        "info": "Biological drying using microbial activity to reduce moisture",
        "loss": 0.08
    },
    "Rotary Drum": {
        "applicable_moisture": (17,35),
        "output_moisture": 10,
        "energy": "High",
        "speed": "Hours",
        "equation": r"M_{out} = M_{in} \times (0.65 - 0.04T)",
        "info": "High-temperature thermal drying for final moisture reduction",
        "loss": 0.12
    },
    "Belt Dryer": {
        "applicable_moisture": (25, 35),
        "output_moisture": 15,
        "energy": "Medium",
        "speed": "Days",
        "equation": r"M_{out} = M_{in} \times (0.82 - 0.08v)",
        "info": "Conveyor belt system with heated zones for moderate drying",
        "loss": 0.06
    },
    "Solar Tunnel": {
        "applicable_moisture": (35, 45),
        "output_moisture": 20,
        "energy": "Very Low",
        "speed": "Days",
        "equation": r"M_{out} = M_{in} \times (0.75 - 0.02t)",
        "info": "Solar-assisted drying using greenhouse tunnel technology",
        "loss": 0.04
    },
}

# Helper functions
def normalize_composition():
    total = sum(st.session_state.composition.values())
    if total == 0:
        return
    factor = 100 / total
    for component in st.session_state.composition:
        st.session_state.composition[component] *= factor

def create_composition_chart():
    composition = st.session_state.composition
    total = sum(composition.values())
    
    if total == 0:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        composition.values(),
        labels=[f"{k}\n({v:.1f}%)" for k, v in composition.items()],
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.75,
        labeldistance=1.15,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
        textprops={'fontsize': 9, 'fontweight': 'bold', 'color': 'darkblue'},
        rotatelabels=True
    )
    
    plt.setp(texts + autotexts, rotation_mode='anchor', ha='center', va='center')
    for t in texts + autotexts:
        t.set_bbox(dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))
    
    ax.axis('equal')
    return fig

# Input Section
st.header("🔢 Input Waste Data")
waste_type = st.selectbox("Type of Waste", ["Municipal", "Industrial", "Commercial", "Mixed"])
input_mass = st.number_input("Total Waste Mass (kg)", min_value=0.0, value=0.0, step=100.0)

# Composition Input
st.header("🧪 Compositional Data")
cols = st.columns(2)
with cols[0]:
    st.subheader("Input Components")
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
    total_percentage = sum(st.session_state.composition.values())
    if abs(total_percentage - 100) > 0.01 and total_percentage != 0:
        if st.button("✨ Normalize to 100%"):
            normalize_composition()
            st.rerun()
    
    chart = create_composition_chart()
    if chart:
        st.pyplot(chart)
    else:
        st.markdown("""<div style='border: 2px dashed #ccc; padding: 20px; text-align: center;'>
                        📭 No composition data</div>""", unsafe_allow_html=True)
    
    status_color = "green" if abs(total_percentage - 100) < 0.01 else "red"
    st.markdown(f"""<div style='padding:10px; background-color:{status_color}20;'>
                    <h3 style='color:{status_color};'>Total: {total_percentage:.2f}%</h3></div>""",
                unsafe_allow_html=True)

# Moisture content slider based on Biogenic Waste percentage
if st.session_state.composition["Biogenic Waste"]:
    min_moisture = 0.7 * st.session_state.composition["Biogenic Waste"]
    if min_moisture > 50:
        min_moisture = 50
    initial_moisture = st.slider(
        "Initial Moisture Content (%)",
        min_value=float(min_moisture),
        max_value=60.0,
        value=float(min_moisture),
        step=0.1,
        format="%.1f"
    )
else:
    initial_moisture = st.slider(
        "Initial Moisture Content (%)",
        0.0,
        60.0,
        25.0,
        step=0.1,
        format="%.1f"
    )

# Moisture check notification
if initial_moisture < 20:
    st.info("✅ No drying required. The initial moisture content is already below 20%, which is optimal for SRF production.")

# Chlorine input
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

# Mercury inputs
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

# Processing Section
st.header("⚙ SRF Production Process Configuration")

# Modified process flow based on moisture content
if initial_moisture < 20:
    mandatory_steps = ["Presorting", "Primary Shredding", "Mechanical Separation"]
else:
    mandatory_steps = ["Presorting", "Primary Shredding", "Mechanical Separation", "Drying"]

optional_steps = ["Secondary Shredding"]

# Process Flow Visualization
process_flow = mandatory_steps.copy()
if st.checkbox("Include Secondary Shredding", help="Optional fine shredding"):
    process_flow.append("Secondary Shredding")

# Create block flow diagram
flow_html = '<div style="display: flex; align-items: center; overflow-x: auto; padding: 15px 0; margin: 10px 0;">'

for i, step in enumerate(process_flow):
    flow_html += f'''
    <div style="
        background-color: #4a8bc9;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        min-width: 120px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0 5px;
    ">{step}</div>'''
    
    if i < len(process_flow) - 1:
        flow_html += '''
        <div style="
            font-size: 20px;
            color: #4a8bc9;
            margin: 0 5px;
        ">→</div>'''

flow_html += '</div>'

# Display the diagram
st.markdown("### Process Flow Diagram")
st.markdown(flow_html, unsafe_allow_html=True)

with st.expander("⚙ Process Parameters Configuration"):
    if "Secondary Shredding" in process_flow:
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Secondary Shredding Parameters")
            shred_type = st.radio("Particle Size Target:",
                                ["Fine (<50mm)", "Medium (50-100mm)", "Rough (>100mm)"],
                                help="Final particle size distribution")
            match shred_type:
                case "Fine (<50mm)":
                    shred_loss = 0.05
                case "Medium (50-100mm)":
                    shred_loss = 0.017
                case "Rough (>100mm)":
                    shred_loss = 0.008 
            
            st.caption(f"Mass loss: {shred_loss*100:.1f}% ")
        drying_col = cols[1]
    else:
        drying_col = st.container()

    with drying_col:
        if initial_moisture >= 20:
            st.subheader("Primary Drying Method")
            applicable_methods_1 = [method for method, details in DRYING_METHODS.items() 
                                   if details['applicable_moisture'][0] <= initial_moisture <= details['applicable_moisture'][1]]
            drying_method_1 = st.selectbox("Select Primary Drying Method", 
                                         options=applicable_methods_1,
                                         key="drying_method_1",
                                         help="Select a drying method applicable to the current moisture content")
            
            if drying_method_1:
                details_1 = DRYING_METHODS[drying_method_1]
                intermediate_moisture = details_1['output_moisture']
                st.write(f"Moisture after primary drying: {intermediate_moisture}%")
                
                st.subheader("Secondary Drying Method (Optional)")
                applicable_methods_2 = [method for method, details in DRYING_METHODS.items() 
                                      if details['applicable_moisture'][0] <= intermediate_moisture <= details['applicable_moisture'][1]]
                drying_method_2 = st.selectbox("Select Secondary Drying Method", 
                                             options=applicable_methods_2,
                                             key="drying_method_2",
                                             help="Optional second drying method to further reduce moisture")
                
                if drying_method_2:
                    details_2 = DRYING_METHODS[drying_method_2]
                    final_moisture = details_2['output_moisture']
                    st.write(f"Final moisture after secondary drying: {final_moisture}%")
                else:
                    final_moisture = intermediate_moisture
            else:
                final_moisture = initial_moisture
        else:
            drying_method_1 = None
            drying_method_2 = None

# Calculations
try:
    # Mass Balance Calculations
    mass = input_mass
    
    # Presorting Loss (fixed 5%)
    mass *= 0.95
    
    # Primary Shredding (fixed 3% loss)
    mass *= 0.97
    
    # Mechanical Separation (only if secondary shredding enabled)
    if "Secondary Shredding" in process_flow:
        mass *= (1 - shred_loss)
    
    # Drying Process
    current_moisture = initial_moisture
    if drying_method_1:
        details_1 = DRYING_METHODS[drying_method_1]
        if details_1['applicable_moisture'][0] <= current_moisture <= details_1['applicable_moisture'][1]:
            dry_mass = mass * (1 - current_moisture/100)
            new_moisture = details_1['output_moisture']
            mass_after_drying = dry_mass / (1 - new_moisture/100)
            mass = mass_after_drying * (1 - details_1['loss'])
            current_moisture = new_moisture
            
    if drying_method_2:
        details_2 = DRYING_METHODS[drying_method_2]
        if details_2['applicable_moisture'][0] <= current_moisture <= details_2['applicable_moisture'][1]:
            dry_mass = mass * (1 - current_moisture/100)
            new_moisture = details_2['output_moisture']
            mass_after_drying = dry_mass / (1 - new_moisture/100)
            mass = mass_after_drying * (1 - details_2['loss'])
            current_moisture = new_moisture
    
    effective_moisture = current_moisture
    
    # Secondary Shredding (if selected - fixed 3% loss)
    if "Secondary Shredding" in process_flow:
        mass *= 0.97
    
    # Final Output
    output_mass = mass
    
    # Energy Calculations
    hhv = sum(st.session_state.composition[k] * HHV_VALUES[k] for k in st.session_state.composition) / 100
    total_energy = output_mass * hhv  # MJ
    coal_eq = total_energy / 24  # 24 MJ/kg coal
    oil_eq = total_energy / 42   # 42 MJ/kg oil

except Exception as e:
    st.error(f"Calculation error: {str(e)}")
    output_mass = hhv = total_energy = coal_eq = oil_eq = 0
    effective_moisture = 0

# Results Section
st.header("📊 Production Results")
cols = st.columns(2)

with cols[0]:
    st.metric("Final SRF Mass", f"{output_mass:.1f} kg", 
             delta=f"{-input_mass + output_mass:.1f} kg vs input")
    st.metric("Effective Moisture", f"{effective_moisture:.1f}%")

with cols[1]:
    st.metric("Heating Value (HHV)", f"{hhv:.1f} MJ/kg")
    st.markdown(f"""
    <div style="color: white; font-size: 14px; font-weight: 600; margin-bottom: 8px; margin-top: -15px">
        Energy Equivalent
    </div>
    <div style="font-size: 24px; font-weight: bold">
        ⛽ {oil_eq:.1f} kg oil<br>
        ⚫ {coal_eq:.1f} kg coal
    </div>
    """, unsafe_allow_html=True)

# Moisture Warning
if effective_moisture > 20:
    st.warning(f"⚠️ High Moisture Content: {effective_moisture:.1f}% exceeds maximum recommended value (20%). "
              "This SRF may not meet quality standards. Consider improving drying efficiency or "
              "selecting a more effective drying method.")

# SRF Classification according to EN 15359
try:
    # Calculate Net Calorific Value (NCV)
    ncv = round((hhv * (1 - effective_moisture/100) - 2.443 * (effective_moisture/100)) * 0.95,2)
    if ncv < 0:
        ncv = 0.0

    # Classification logic
    if ncv >= 25:
        ncv_class = 1
    elif ncv >= 20:
        ncv_class = 2
    elif ncv >= 15:
        ncv_class = 3
    elif ncv >= 10:
        ncv_class = 4
    else:
        ncv_class = 5

    cl_percent = st.session_state.contaminants['Chlorine']
    if cl_percent <= 0.2:
        cl_class = 1
    elif cl_percent <= 0.6:
        cl_class = 2
    elif cl_percent <= 1.0:
        cl_class = 3
    elif cl_percent <= 1.5:
        cl_class = 4
    elif cl_percent <= 3.0:
        cl_class = 5
    else:
        cl_class = 5
        st.warning("Chlorine content exceeds 3.0% (Class 5 maximum)")

    hg_median = st.session_state.contaminants['Mercury_median']
    hg_80th = st.session_state.contaminants['Mercury_80th']
    hg_class = 5

    if hg_median <= 0.02 and hg_80th <= 0.04:
        hg_class = 1
    elif hg_median <= 0.03 and hg_80th <= 0.06:
        hg_class = 2
    elif hg_median <= 0.08 and hg_80th <= 0.16:
        hg_class = 3
    elif hg_median <= 0.15 and hg_80th <= 0.30:
        hg_class = 4
    elif hg_median <= 0.50 and hg_80th <= 1.00:
        hg_class = 5
    else:
        st.warning("Mercury values exceed Class 5 thresholds")

    # Display classification results
    st.subheader("SRF Classification (EN 15359)")
    class_info = f"""
    - **NCV**: {ncv:.1f} MJ/kg (Class {ncv_class})
    - **Chlorine**: {cl_percent:.2f}% (Class {cl_class})
    - **Mercury**: Median={hg_median:.3f} mg/MJ, 80th={hg_80th:.3f} mg/MJ (Class {hg_class})"""
    
    st.markdown(class_info)

    # Visualization
    st.subheader("📈 SRF Quality Classification")
    class_data = {
        'Parameter': ['NCV', 'Chlorine', 'Mercury'],
        'Class': [ncv_class, cl_class, hg_class],
        'Values': [ncv, cl_percent, f"{hg_median:.3f}/{hg_80th:.3f}"]
    }

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.cm.RdYlGn_r(np.linspace(0, 1, 5))

    bars = ax.barh(class_data['Parameter'], class_data['Class'], 
                color=[colors[c-1] for c in class_data['Class']], 
                edgecolor='black')

    for i, (class_val, value) in enumerate(zip(class_data['Class'], class_data['Values'])):
        ax.text(class_val + 0.1, i, 
                f"Class {class_val}\n({value})", 
                va='center', ha='left', fontweight='bold')

    ax.set_xlim(0, 5.5)
    ax.set_xticks(range(1,6))
    ax.set_xlabel('Quality Class (1=Best, 5=Worst)')
    ax.set_title('SRF Quality Classification According to EN 15359')
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    legend_labels = ['Class 1 (Best)', 'Class 2', 'Class 3', 'Class 4', 'Class 5 (Worst)']
    ax.legend(handles=[plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(5)],
            labels=legend_labels,
            title='Classification Scale',
            bbox_to_anchor=(1.05, 1), 
            loc='upper left')

    plt.tight_layout()
    st.pyplot(fig)
    srf_class = max(ncv_class , cl_class , hg_class)
    
    if cl_class == 5:
        st.warning("⚠️ High Chlorine Content: Exceeds 3.0% (Class 5) - may cause corrosion and emissions issues")
    
    if hg_class >= 4:
        st.warning(f"⚠️ High Mercury Content: Class {hg_class} - potential environmental hazard")

    if srf_class >= 4:
        st.error("🚨 Class 4/5 SRF - May not meet quality requirements for most energy recovery applications")

except Exception as e:
    st.error(f"Classification error: {str(e)}")

# Footer
st.markdown("---")
st.caption("ℹ Based on CEN/TS 15359 standards for SRF classification")
st.caption("⚠ Values represent theoretical estimates - actual results may vary")

if st.button("🧹 Reset All Inputs"):
    for component in st.session_state.composition:
        st.session_state.composition[component] = 0.0
    for contaminant in st.session_state.contaminants:
        st.session_state.contaminants[contaminant] = 0.0
    st.rerun()