import streamlit as st
import base64
from utils.pdf_generator import create_pdf_report

def render_report_section(waste_type, input_mass, initial_moisture, process_config, results):
    """Render the PDF report generation section"""
    st.markdown("---")
    st.subheader("📄 Generate PDF Report")

    if st.button("🖨 Generate Report"):
        try:
            # Prepare report data
            report_data = {
                'waste_type': waste_type,
                'input_mass': input_mass,
                'initial_moisture': initial_moisture,
                'process_config': process_config,
                'results': results,
                'composition': st.session_state.composition,
                'contaminants': st.session_state.contaminants
            }
            
            # Generate PDF report
            report_path = create_pdf_report(report_data)
            
            # Provide download link
            with open(report_path, "rb") as f:
                pdf_bytes = f.read()
            
            b64 = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="{report_path}">⬇️ Download Report</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("✅ Report generated successfully!")
            
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")