import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def render_classification_section(results):
    """Render the SRF quality classification section"""
    st.subheader("📈 SRF Quality Classification")
    
    # Create classification data
    class_data = {
        'Parameter': ['NCV', 'Chlorine', 'Mercury'],
        'Class': [results['ncv_class'], results['cl_class'], results['hg_class']],
        'Values': [
            results['ncv'], 
            results['cl_percent'], 
            f"{results['hg_median']:.3f}/{results['hg_80th']:.3f}"
        ]
    }
    
    # Create and display classification chart
    _create_classification_chart(class_data)
    
    # Display classification information
    _display_classification_info(results)
    
    # Display warnings
    _display_classification_warnings(results)

def _create_classification_chart(class_data):
    """Create and display the classification chart"""
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.cm.RdYlGn_r(np.linspace(0, 1, 5))

    bars = ax.barh(
        class_data['Parameter'], 
        class_data['Class'], 
        color=[colors[c-1] for c in class_data['Class']], 
        edgecolor='black'
    )

    # Add value labels on bars
    for i, (class_val, value) in enumerate(zip(class_data['Class'], class_data['Values'])):
        ax.text(
            class_val + 0.1, i, 
            f"Class {class_val}\n({value})", 
            va='center', ha='left', fontweight='bold'
        )

    # Chart formatting
    ax.set_xlim(0, 5.5)
    ax.set_xticks(range(1, 6))
    ax.set_xlabel('Quality Class (1=Best, 5=Worst)')
    ax.set_title('SRF Quality Classification According to EN 15359')
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Add legend
    legend_labels = ['Class 1 (Best)', 'Class 2', 'Class 3', 'Class 4', 'Class 5 (Worst)']
    ax.legend(
        handles=[plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(5)],
        labels=legend_labels,
        title='Classification Scale',
        bbox_to_anchor=(1.05, 1), 
        loc='upper left'
    )

    plt.tight_layout()
    st.pyplot(fig)

def _display_classification_info(results):
    """Display detailed classification information"""
    class_info = f"""
    - **NCV**: {results['ncv']:.1f} MJ/kg (Class {results['ncv_class']})
    - **Chlorine**: {results['cl_percent']:.2f}% (Class {results['cl_class']})
    - **Mercury**: Median={results['hg_median']:.3f} mg/MJ, 80th={results['hg_80th']:.3f} mg/MJ (Class {results['hg_class']})
    """
    st.markdown(class_info)

def _display_classification_warnings(results):
    """Display classification-related warnings"""
    if results['cl_class'] == 5:
        st.warning("⚠️ High Chlorine Content: Exceeds 3.0% (Class 5) - may cause corrosion and emissions issues")
    
    if results['hg_class'] >= 4:
        st.warning(f"⚠️ High Mercury Content: Class {results['hg_class']} - potential environmental hazard")

    if results['srf_class'] >= 4:
        st.error("🚨 Class 4/5 SRF - May not meet quality requirements for most energy recovery applications")