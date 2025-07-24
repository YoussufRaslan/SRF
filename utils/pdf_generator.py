import datetime
import os
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf"])
    from fpdf import FPDF

from config.constants import LOGO_PATH
from utils.helpers import remove_emojis, create_composition_chart

def create_pdf_report(report_data):
    """
    Create a comprehensive PDF report for SRF production analysis
    
    Args:
        report_data (dict): Dictionary containing all report data
    
    Returns:
        str: Path to the generated PDF file
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Extract data from report_data
    waste_type = report_data['waste_type']
    input_mass = report_data['input_mass']
    initial_moisture = report_data['initial_moisture']
    process_config = report_data['process_config']
    results = report_data['results']
    composition = report_data['composition']
    contaminants = report_data['contaminants']
    
    # Generate report sections
    _add_header(pdf)
    _add_input_data_section(pdf, waste_type, input_mass, initial_moisture, composition, contaminants)
    _add_process_configuration_section(pdf, process_config)
    _add_results_section(pdf, input_mass, results)
    _add_classification_section(pdf, results)
    _add_warnings_section(pdf, results)
    _add_footer(pdf)
    
    # Save PDF
    pdf_file_name = f"SRF_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(pdf_file_name)
    return pdf_file_name

def _add_header(pdf):
    """Add branded header to the PDF"""
    try:
        pdf.image(LOGO_PATH, x=10, y=8, w=35)
        pdf.set_font('Helvetica', 'B', 18)
        pdf.set_text_color(14, 123, 138)
        pdf.set_xy(50, 10)
        pdf.cell(0, 10, "EcoFuel Pro", ln=1)
        pdf.set_font('Helvetica', '', 12)
        pdf.set_text_color(1, 38, 11)
        pdf.set_xy(50, 16)
        pdf.cell(0, 13, "SRF Production Analysis Report", ln=1)
        pdf.set_draw_color(14, 123, 138)
        pdf.line(10, 28, 200, 28)
        pdf.ln(15)
    except Exception as e:
        st.error(f"Could not load logo: {str(e)}")

    # Report date
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 10, remove_emojis(f"Report Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), 0, 1)
    pdf.ln(5)

def _add_input_data_section(pdf, waste_type, input_mass, initial_moisture, composition, contaminants):
    """Add input data section to PDF"""
    # Section header
    pdf.set_fill_color(230, 240, 255)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '1. Input Data', 0, 1, 'L', fill=True)
    pdf.set_font('Helvetica', '', 12)
    
    # Basic waste info
    pdf.cell(0, 10, remove_emojis(f"Waste Type: {waste_type}"), 0, 1)
    pdf.cell(0, 10, remove_emojis(f"Total Waste Mass: {input_mass:.2f} kg"), 0, 1)
    
    # Composition table
    _add_composition_table(pdf, composition)
    
    # Composition pie chart
    _add_composition_chart(pdf, composition)
    
    # Moisture and contaminants
    pdf.ln(5)
    pdf.cell(0, 10, remove_emojis(f"Initial Moisture Content: {initial_moisture:.2f}%"), 0, 1)
    
    _add_contaminants_info(pdf, contaminants)

def _add_composition_table(pdf, composition):
    """Add composition table to PDF"""
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Waste Composition:', 0, 1)
    
    # Table header
    pdf.set_fill_color(237, 246, 249)
    pdf.cell(100, 10, "Component", 1, 0, 'C', 1)
    pdf.cell(40, 10, "Percentage (%)", 1, 1, 'C', 1)
    pdf.set_font('Helvetica', '', 12)
    
    # Table rows
    for component, percentage in composition.items():
        pdf.cell(100, 10, remove_emojis(f"{component}"), 1)
        pdf.cell(40, 10, f"{percentage:.2f}", 1, 1)

def _add_composition_chart(pdf, composition):
    """Add composition pie chart to PDF"""
    try:
        pie_path = "composition_pie.png"
        fig = create_composition_chart(composition, figsize=(5, 5))
    
        if fig:
            plt.legend(bbox_to_anchor=(1.3, 0.8), loc='upper left')
            fig.savefig(pie_path, bbox_inches='tight', dpi=150, pad_inches=0.5)
            plt.close(fig)
        
        pdf.set_font('Helvetica', 'B', 12)
        pdf.ln(5)
        pdf.cell(0, 10, "Composition Distribution:", 0, 1)
        pdf.set_font('Helvetica', '', 12)
        
        # Center the pie chart
        pie_width = 120
        x_pos = (pdf.w - pie_width) / 2
        pdf.image(pie_path, x=x_pos, w=pie_width)
        
        # Clean up temp file 
        if os.path.exists(pie_path):
            os.remove(pie_path)
    except Exception as e:
        st.error(f"Error generating pie chart: {str(e)}")

def _add_contaminants_info(pdf, contaminants):
    """Add contaminants information to PDF"""
    pdf.set_font('Helvetica', 'BU', 12)
    pdf.cell(0, 10, 'Contaminants:', 0, 1)
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 10, remove_emojis(f"Chlorine: {contaminants['Chlorine']:.4f}%"), 0, 1)
    pdf.cell(0, 10, remove_emojis(f"Mercury (Median): {contaminants['Mercury_median']:.4f} mg/MJ"), 0, 1)
    pdf.cell(0, 10, remove_emojis(f"Mercury (80th): {contaminants['Mercury_80th']:.4f} mg/MJ"), 0, 1)
    pdf.ln(10)

def _add_process_configuration_section(pdf, process_config):
    """Add process configuration section to PDF"""
    if pdf.get_y() > 150:
        pdf.add_page()
    
    pdf.set_fill_color(230, 240, 255)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '2. Process Configuration', 0, 1, 'L', fill=True)
    pdf.set_font('Helvetica', '', 12)
    
    # Process flow diagram
    _add_process_flow_diagram(pdf, process_config['process_flow'])
    
    # Drying methods
    pdf.ln(5)
    if process_config.get('drying_method_1'):
        pdf.cell(0, 10, remove_emojis(f"Primary Drying Method: {process_config['drying_method_1']}"), 0, 1)
        pdf.cell(0, 10, remove_emojis(f"Moisture after primary drying: {process_config['intermediate_moisture']}%"), 0, 1)
    if process_config.get('drying_method_2'):
        pdf.cell(0, 10, remove_emojis(f"Secondary Drying Method: {process_config['drying_method_2']}"), 0, 1)
        pdf.cell(0, 10, remove_emojis(f"Final moisture content: {process_config['final_moisture']}%"), 0, 1)

def _add_process_flow_diagram(pdf, process_flow):
    """Add process flow diagram to PDF"""
    try:
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 10, "Process Flow Diagram:", 0, 1)
        pdf.set_font('Helvetica', '', 12)
        
        # Create process flow visualization
        flow_path = "process_flow.png"
        fig, ax = plt.subplots(figsize=(12, 3))
        ax.axis('off')
        
        # Calculate positions and draw process blocks
        n_steps = len(process_flow)
        step_width = 1.0 / n_steps
        
        for i, step in enumerate(process_flow):
            clean_step = remove_emojis(step)
            text_width = len(clean_step) * 0.1
            block_width = 0.75 * min(max(text_width * 1.1, 0.1), 0.2)
            
            # Draw block
            x = i * step_width + (step_width - block_width)/2
            rect = plt.Rectangle((x, 0.3), block_width, 0.4, 
                                fill=True, color='#4a8bc9', alpha=0.8)
            ax.add_patch(rect)
            
            # Add text with wrapping for long text
            if len(clean_step) > 15:
                parts = clean_step.split()
                if len(parts) > 1:
                    mid = len(parts) // 2
                    wrapped_text = "\n".join([" ".join(parts[:mid]), " ".join(parts[mid:])])
                else:
                    wrapped_text = clean_step
            else:
                wrapped_text = clean_step
                
            ax.text(x + block_width/2, 0.5, wrapped_text, 
                   ha='center', va='center', color='white', fontweight='bold', fontsize=14)
            
            # Draw arrow if not last step
            if i < n_steps - 1:
                arrow_start = x + block_width
                arrow_end = (i+1) * step_width + (step_width - block_width)/2
                arrow_length = arrow_end - arrow_start
                ax.arrow(arrow_start, 0.5, arrow_length*0.8, 0, 
                        head_width=0.1, head_length=arrow_length*0.2, 
                        fc='k', ec='k', linewidth=1)
        
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.savefig(flow_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        # Add to PDF
        flow_width = 190
        x_flow = (pdf.w - flow_width) / 2
        pdf.image(flow_path, x=x_flow, w=flow_width)
        
        # Clean up temp file
        if os.path.exists(flow_path):
            os.remove(flow_path)
    except Exception as e:
        st.error(f"Error generating process diagram: {str(e)}")

def _add_results_section(pdf, input_mass, results):
    """Add production results section to PDF"""
    if pdf.get_y() > 150:
        pdf.add_page()
    
    pdf.set_fill_color(230, 240, 255)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '3. Production Results', 0, 1, 'L', fill=True)
    pdf.set_font('Helvetica', '', 12)
    
    # Mass balance
    pdf.set_font('Helvetica', 'BU', 12)
    pdf.cell(0, 10, 'Mass Balance:', 0, 1)
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 10, remove_emojis(f"Input Mass: {input_mass:.2f} kg"), 0, 1)
    pdf.cell(0, 10, remove_emojis(f"Final SRF Mass: {results['output_mass']:.2f} kg"), 0, 1)
    
    # Calculate mass loss
    mass_loss = input_mass - results['output_mass']
    mass_loss_percent = (mass_loss / input_mass) * 100 if input_mass > 0 else 0.0
    pdf.cell(0, 10, remove_emojis(f"Mass Loss: {mass_loss:.2f} kg ({mass_loss_percent:.1f}%)"), 0, 1)
    pdf.cell(0, 10, remove_emojis(f"Effective Moisture: {results['effective_moisture']:.1f}%"), 0, 1)
    
    # Energy characteristics
    pdf.ln(5)
    pdf.set_font('Helvetica', 'BU', 12)
    pdf.cell(0, 10, 'Energy Characteristics:', 0, 1)
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 10, remove_emojis(f"Heating Value (HHV): {results['hhv']:.2f} MJ/kg"), 0, 1)
    pdf.cell(0, 10, remove_emojis(f"Total Energy: {results['total_energy']:.2f} MJ"), 0, 1)
    pdf.cell(0, 10, remove_emojis(f"Coal Equivalent: {results['coal_eq']:.2f} kg"), 0, 1)
    pdf.cell(0, 10, remove_emojis(f"Oil Equivalent: {results['oil_eq']:.2f} kg"), 0, 1)
    
    # Environmental impact
    pdf.ln(5)
    pdf.set_font('Helvetica','BU', 12)
    pdf.cell(0, 10, 'Environmental Impact:', 0, 1)
    pdf.set_font('Helvetica', '', 12)
    
    co2_avoided = results['co2_avoided']
    co2_percent = 100 * (1 - results['srf_carbon_emissions']/results['coal_carbon_emissions']) if results['coal_carbon_emissions'] > 0 else 0.0
    
    pdf.cell(0, 10, remove_emojis(f"CO2 Avoided: {co2_avoided:.2f} kg CO2"), 0, 1)
    pdf.cell(0, 10, remove_emojis(f"CO2 Avoided Percentage: {co2_percent:.1f}%"), 0, 1)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 10, remove_emojis("Note: Avoided emissions when substituting coal with SRF"), 0, 1)

def _add_classification_section(pdf, results):
    """Add SRF classification section to PDF"""
    if pdf.get_y() > 150:
        pdf.add_page()
    
    pdf.set_fill_color(230, 240, 255)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, '4. SRF Classification (EN 15359)', 0, 1, 'L', fill=True)
    
    # Classification table
    pdf.ln(5)
    pdf.set_fill_color(237, 246, 249)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(60, 10, "Parameter", 1, 0, 'C', 1)
    pdf.cell(40, 10, "Value", 1, 0, 'C', 1)
    pdf.cell(40, 10, "Class", 1, 1, 'C', 1)
    
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(60, 10, remove_emojis("Net Calorific Value (NCV)"), 1)
    pdf.cell(40, 10, f"{results['ncv']:.1f} MJ/kg", 1)
    pdf.cell(40, 10, str(results['ncv_class']), 1, 1)
    
    pdf.cell(60, 10, "Chlorine", 1)
    pdf.cell(40, 10, f"{results['cl_percent']:.4f}%", 1)
    pdf.cell(40, 10, str(results['cl_class']), 1, 1)
    
    pdf.cell(60, 10, "Mercury (Median)", 1)
    pdf.cell(40, 10, f"{results['hg_median']:.4f} mg/MJ", 1)
    pdf.cell(40, 10, str(results['hg_class']), 1, 1)
    
    pdf.cell(60, 10, "Mercury (80th)", 1)
    pdf.cell(40, 10, f"{results['hg_80th']:.4f} mg/MJ", 1)
    pdf.cell(40, 10, str(results['hg_class']), 1, 1)
    
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, remove_emojis(f"Overall SRF Classification: Class {results['srf_class']}"), 0, 1)

def _add_warnings_section(pdf, results):
    """Add warnings section to PDF if needed"""
    warning_exists = False
    if (results['effective_moisture'] > 20 or results['cl_class'] == 5 or 
        results['hg_class'] >= 4 or results['srf_class'] >= 4):
        warning_exists = True
        
        if pdf.get_y() > 150:
            pdf.add_page()
            
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, '5. Warnings', 0, 1, 'L')
        pdf.set_font('Helvetica', '', 12)
        
        # Warning formatting with yellow background
        pdf.set_fill_color(255, 255, 0)
        pdf.set_text_color(0, 0, 0)
        
        if results['effective_moisture'] > 20:
            pdf.cell(0, 10, remove_emojis("- High moisture content (>20%) may not meet quality standards"), 0, 1, fill=True)
            pdf.ln(2)
        if results['cl_class'] == 5:
            pdf.cell(0, 10, remove_emojis("- High chlorine content (>3.0%) may cause corrosion and emissions issues"), 0, 1, fill=True)
            pdf.ln(2)
        if results['hg_class'] >= 4:
            pdf.cell(0, 10, remove_emojis("- High mercury content - potential environmental hazard"), 0, 1, fill=True)
            pdf.ln(2)
        if results['srf_class'] >= 4:
            pdf.cell(0, 10, remove_emojis("- Low SRF classification (Class 4/5) - may not meet requirements for most applications"), 0, 1, fill=True)
            pdf.ln(2)
        
        # Reset colors to default
        pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(0, 0, 0)

def _add_footer(pdf):
    """Add footer to the PDF"""
    pdf.set_y(-50)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 10, remove_emojis("Generated by EcoFuel Pro - SRF Production Analysis Suite"), 0, 1, 'C')
    pdf.cell(0, 10, remove_emojis("Based on CEN/TS 15359 standards for SRF classification"), 0, 1, 'C')
    pdf.cell(0, 10, remove_emojis("Values represent theoretical estimates - actual results may vary"), 0, 1, 'C')