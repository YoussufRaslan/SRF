# Configuration constants for the SRF application

# File paths
LOGO_PATH = "sustainability-squad-high-resolution-logo-transparent.png"

# Emojis for UI elements
EMOJIS = {
    "Plastic": "🧴",
    "Paper & Cardboard": "📦",
    "Metals": "🔩",
    "Textiles": "👕",
    "Organic Waste": "🌿",
    "Inert Materials (wood, glass, diapers,...)": "🪨",
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

# Higher Heating Values (MJ/kg)
HHV_VALUES = {
    "Plastic": 36.5,
    "Paper & Cardboard": 15.8,
    "Metals": 0,
    "Textiles": 19.2,
    "Organic Waste": 11.3,
    "Inert Materials (wood, glass, diapers,...)": 0.5,
    "Other Materials": 9.7
}

# Drying methods database
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

# Default composition
DEFAULT_COMPOSITION = {
    "Plastic": 0.0,
    "Paper & Cardboard": 0.0,
    "Metals": 0.0,
    "Textiles": 0.0,
    "Organic Waste": 0.0,
    "Inert Materials (wood, glass, diapers,...)": 0.0,
    "Other Materials": 0.0
}

# Default contaminants
DEFAULT_CONTAMINANTS = {
    'Chlorine': 0.0,
    'Mercury_median': 0.0,
    'Mercury_80th': 0.0,
}

# Process losses
PROCESS_LOSSES = {
    'presorting': 0.05,
    'primary_shredding': 0.03,
    'secondary_shredding': 0.03,
    'fine_shredding': 0.05,
    'medium_shredding': 0.017,
    'rough_shredding': 0.008
}

# Energy constants
COAL_ENERGY_CONTENT = 24  # MJ/kg
OIL_ENERGY_CONTENT = 42   # MJ/kg
CARBON_FRACTION_SRF = 0.65
FOSSIL_CARBON_FRACTION = 0.35
COAL_CARBON_FRACTION = 0.75
CO2_EMISSION_FACTOR = 3.67  # kg CO2/kg C