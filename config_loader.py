#!/usr/bin/env python3
"""
Configuration Loader

Handles loading and validating configuration files.
"""

import json
import os
from pathlib import Path


def load_config(config_path):
    """
    Load configuration from JSON file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is invalid JSON
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {config_path}: {e.msg}", e.doc, e.pos)
    
    # Validate configuration
    _validate_config(config)
    
    return config


def _validate_config(config):
    """
    Validate configuration structure and content.
    
    Args:
        config: Configuration dictionary to validate
        
    Raises:
        ValueError: If configuration is invalid
    """
    # Check required fields
    if 'species' not in config:
        raise ValueError("Configuration must contain 'species' field")
    
    species = config['species']
    if not isinstance(species, list) or len(species) == 0:
        raise ValueError("'species' must be a non-empty list")
    
    # Validate species
    for i, spec in enumerate(species):
        if not isinstance(spec, dict):
            raise ValueError(f"Species {i} must be a dictionary")
        if 'name' not in spec or 'color' not in spec:
            raise ValueError(f"Species {i} must have 'name' and 'color' fields")
        if not isinstance(spec['color'], list) or len(spec['color']) != 3:
            raise ValueError(f"Species {i} color must be RGB list [r, g, b]")
        
        # Validate RGB values
        for j, val in enumerate(spec['color']):
            if not (0 <= val <= 255):
                raise ValueError(f"Species {i} color[{j}] must be between 0-255")
    
    # Validate interaction matrix if present
    if 'interaction_matrix' in config:
        matrix = config['interaction_matrix']
        if not isinstance(matrix, list):
            raise ValueError("'interaction_matrix' must be a list of lists")
        
        n = len(species)
        if len(matrix) != n:
            raise ValueError(f"interaction_matrix must be {n}x{n}")
        
        for i, row in enumerate(matrix):
            if not isinstance(row, list) or len(row) != n:
                raise ValueError(f"interaction_matrix row {i} must have {n} elements")
    
    # Validate parameters if present
    if 'parameters' in config:
        params = config['parameters']
        if not isinstance(params, dict):
            raise ValueError("'parameters' must be a dictionary")
        
        # Check parameter ranges
        if 'interaction_radius' in params:
            if params['interaction_radius'] <= 0:
                raise ValueError("'interaction_radius' must be positive")
        
        if 'force_strength' in params:
            if params['force_strength'] == 0:
                raise ValueError("'force_strength' must be non-zero")
        
        if 'friction_damping' in params:
            damping = params['friction_damping']
            if not (0 < damping <= 1):
                raise ValueError("'friction_damping' must be between 0 and 1")


def save_config(config, config_path):
    """
    Save configuration to JSON file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration to
    """
    os.makedirs(os.path.dirname(config_path) or '.', exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Configuration saved to {config_path}")
