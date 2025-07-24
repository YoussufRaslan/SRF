import streamlit as st
from config.constants import (
    HHV_VALUES, DRYING_METHODS, PROCESS_LOSSES,
    COAL_ENERGY_CONTENT, OIL_ENERGY_CONTENT,
    CARBON_FRACTION_SRF, FOSSIL_CARBON_FRACTION,
    COAL_CARBON_FRACTION, CO2_EMISSION_FACTOR
)

def calculate_srf_production(input_mass, initial_moisture, process_config, session_state):
    """
    Calculate SRF production results based on input parameters
    
    Returns:
        dict: Dictionary containing all calculation results
    """
    try:
        results = {}
        
        # Mass Balance Calculations
        mass = input_mass
        current_moisture = initial_moisture
        
        # Process steps with losses
        mass = _apply_process_losses(mass, process_config)
        
        # Drying process
        mass, current_moisture = _apply_drying_process(
            mass, current_moisture, process_config
        )
        
        # Final output mass and moisture
        results['output_mass'] = mass
        results['effective_moisture'] = current_moisture
        
        # Energy calculations
        results.update(_calculate_energy_values(mass, session_state.composition))
        
        # CO2 calculations
        results.update(_calculate_co2_emissions(results, mass))
        
        # Store CO2 avoided in session state
        session_state.co2_avoided = results['co2_avoided']
        
        # SRF Classification
        results.update(_calculate_srf_classification(
            results, current_moisture, session_state.contaminants
        ))
        
        return results
        
    except Exception as e:
        st.error(f"Calculation error: {str(e)}")
        return _get_default_results()

def _apply_process_losses(mass, process_config):
    """Apply losses from various process steps"""
    # Presorting Loss (fixed 5%)
    mass *= (1 - PROCESS_LOSSES['presorting'])
    
    # Primary Shredding (fixed 3% loss)
    mass *= (1 - PROCESS_LOSSES['primary_shredding'])
    
    # Secondary Shredding losses (if enabled)
    if "Secondary Shredding" in process_config.get('process_flow', []):
        shred_type = process_config.get('shred_type', 'Medium (50-100mm)')
        if shred_type == "Fine (<50mm)":
            mass *= (1 - PROCESS_LOSSES['fine_shredding'])
        elif shred_type == "Medium (50-100mm)":
            mass *= (1 - PROCESS_LOSSES['medium_shredding'])
        else:  # Rough
            mass *= (1 - PROCESS_LOSSES['rough_shredding'])
    
    return mass

def _apply_drying_process(mass, current_moisture, process_config):
    """Apply drying process calculations"""
    # Primary drying
    if process_config.get('drying_method_1'):
        mass, current_moisture = _apply_single_drying_step(
            mass, current_moisture, process_config['drying_method_1']
        )
    
    # Secondary drying
    if process_config.get('drying_method_2'):
        mass, current_moisture = _apply_single_drying_step(
            mass, current_moisture, process_config['drying_method_2']
        )
    
    # Final secondary shredding loss (if applicable)
    if "Secondary Shredding" in process_config.get('process_flow', []):
        mass *= (1 - PROCESS_LOSSES['secondary_shredding'])
    
    return mass, current_moisture

def _apply_single_drying_step(mass, current_moisture, drying_method):
    """Apply a single drying step"""
    if not drying_method or drying_method not in DRYING_METHODS:
        return mass, current_moisture
    
    details = DRYING_METHODS[drying_method]
    
    # Check if method is applicable
    min_moisture, max_moisture = details['applicable_moisture']
    if not (min_moisture <= current_moisture <= max_moisture):
        return mass, current_moisture
    
    # Calculate new mass after drying
    dry_mass = mass * (1 - current_moisture/100)
    new_moisture = details['output_moisture']
    mass_after_drying = dry_mass / (1 - new_moisture/100)
    
    # Apply process loss
    final_mass = mass_after_drying * (1 - details['loss'])
    
    return final_mass, new_moisture

def _calculate_energy_values(output_mass, composition):
    """Calculate energy-related values"""
    # Calculate Higher Heating Value (HHV)
    hhv = sum(composition[k] * HHV_VALUES[k] for k in composition) / 100
    
    # Energy calculations
    total_energy = output_mass * hhv  # MJ
    coal_eq = total_energy / COAL_ENERGY_CONTENT  # kg coal equivalent
    oil_eq = total_energy / OIL_ENERGY_CONTENT    # kg oil equivalent
    
    return {
        'hhv': hhv,
        'total_energy': total_energy,
        'coal_eq': coal_eq,
        'oil_eq': oil_eq
    }

def _calculate_co2_emissions(results, output_mass):
    """Calculate CO2 emissions and avoided emissions"""
    # SRF carbon emissions
    srf_carbon_emissions = (
        output_mass * CARBON_FRACTION_SRF * FOSSIL_CARBON_FRACTION * CO2_EMISSION_FACTOR
    )
    
    # Coal carbon emissions
    coal_carbon_emissions = (
        results['coal_eq'] * COAL_CARBON_FRACTION * CO2_EMISSION_FACTOR
    )
    
    # CO2 avoided
    co2_avoided = coal_carbon_emissions - srf_carbon_emissions
    
    return {
        'srf_carbon_emissions': srf_carbon_emissions,
        'coal_carbon_emissions': coal_carbon_emissions,
        'co2_avoided': co2_avoided
    }

def _calculate_srf_classification(results, effective_moisture, contaminants):
    """Calculate SRF classification according to EN 15359"""
    # Calculate Net Calorific Value (NCV)
    ncv = round((results['hhv'] * (1 - effective_moisture/100) - 2.443 * (effective_moisture/100)) * 0.95, 2)
    if ncv < 0:
        ncv = 0.0

    # NCV Classification
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

    # Chlorine Classification
    cl_percent = contaminants['Chlorine']
    if cl_percent <= 0.2:
        cl_class = 1
    elif cl_percent <= 0.6:
        cl_class = 2
    elif cl_percent <= 1.0:
        cl_class = 3
    elif cl_percent <= 1.5:
        cl_class = 4
    else:
        cl_class = 5

    # Mercury Classification
    hg_median = contaminants['Mercury_median']
    hg_80th = contaminants['Mercury_80th']
    
    if hg_median <= 0.02 and hg_80th <= 0.04:
        hg_class = 1
    elif hg_median <= 0.03 and hg_80th <= 0.06:
        hg_class = 2
    elif hg_median <= 0.08 and hg_80th <= 0.16:
        hg_class = 3
    elif hg_median <= 0.15 and hg_80th <= 0.30:
        hg_class = 4
    else:
        hg_class = 5

    # Overall SRF class (worst of all parameters)
    srf_class = max(ncv_class, cl_class, hg_class)
    
    return {
        'ncv': ncv,
        'ncv_class': ncv_class,
        'cl_percent': cl_percent,
        'cl_class': cl_class,
        'hg_median': hg_median,
        'hg_80th': hg_80th,
        'hg_class': hg_class,
        'srf_class': srf_class
    }

def _get_default_results():
    """Return default results in case of calculation error"""
    return {
        'output_mass': 0,
        'effective_moisture': 0,
        'hhv': 0,
        'total_energy': 0,
        'coal_eq': 0,
        'oil_eq': 0,
        'srf_carbon_emissions': 0,
        'coal_carbon_emissions': 0,
        'co2_avoided': 0,
        'ncv': 0,
        'ncv_class': 5,
        'cl_percent': 0,
        'cl_class': 1,
        'hg_median': 0,
        'hg_80th': 0,
        'hg_class': 1,
        'srf_class': 5
    }