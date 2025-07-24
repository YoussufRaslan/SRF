import streamlit as st
import base64
from pathlib import Path
import matplotlib.pyplot as plt

def img_to_base64(img_path):
    """Convert image to base64 for HTML embedding"""
    if Path(img_path).exists():
        return base64.b64encode(Path(img_path).read_bytes()).decode()
    st.error(f"Logo image not found at: {img_path}")
    return None

def normalize_composition(composition):
    """Normalize composition percentages to sum to 100%"""
    total = sum(composition.values())
    if total == 0:
        return composition
    
    factor = 100 / total
    normalized = {}
    for component, value in composition.items():
        normalized[component] = value * factor
    return normalized

def create_composition_chart(composition, figsize=(8,8)):
    """Create pie chart for waste composition"""
    total = sum(composition.values())
    
    if total == 0:
        return None
    
    fig, ax = plt.subplots(figsize=figsize)
    wedges, texts, autotexts = ax.pie(
        composition.values(),
        labels=[f"{k}\n({v:.1f}%)" for k, v in composition.items()],
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.5,
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

def remove_emojis(text):
    """Remove emojis from text for PDF compatibility"""
    return ''.join(char for char in text if char.isascii())

def create_process_flow_html(process_flow):
    """Create HTML visualization of process flow"""
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
    return flow_html