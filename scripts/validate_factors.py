#!/usr/bin/env python3
"""
Validate factors.json file format and content.

This script checks:
1. JSON file is valid and can be parsed
2. Required fields are present for each factor
3. Style values are valid
4. Descriptions contain both English and Chinese
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def validate_factors_json(file_path: str) -> bool:
    """
    Validate the factors.json file.
    
    Args:
        file_path: Path to the factors.json file
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    try:
        # Load JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✓ Successfully loaded JSON from {file_path}")
        
        # Check top-level structure
        if 'factors' not in data:
            print("✗ Missing 'factors' key in JSON")
            return False
        
        if 'metadata' not in data:
            print("✗ Missing 'metadata' key in JSON")
            return False
        
        print("✓ Top-level structure is valid")
        
        # Validate each factor
        factors = data['factors']
        if not isinstance(factors, list):
            print("✗ 'factors' should be a list")
            return False
        
        if len(factors) == 0:
            print("✗ 'factors' list is empty")
            return False
        
        print(f"✓ Found {len(factors)} factors")
        
        # Valid style values
        valid_styles = {'Style', 'Quality', 'Risk', 'Sentiment'}
        
        # Required fields for each factor
        required_fields = {'factor_id', 'factor_name', 'style', 'description'}
        
        for idx, factor in enumerate(factors, 1):
            # Check required fields
            missing_fields = required_fields - set(factor.keys())
            if missing_fields:
                print(f"✗ Factor {idx}: Missing required fields: {missing_fields}")
                return False
            
            # Validate factor_id
            if not isinstance(factor['factor_id'], int):
                print(f"✗ Factor {idx}: factor_id should be an integer")
                return False
            
            # Validate factor_name
            if not isinstance(factor['factor_name'], str) or not factor['factor_name']:
                print(f"✗ Factor {idx}: factor_name should be a non-empty string")
                return False
            
            # Validate style
            if factor['style'] not in valid_styles:
                print(f"✗ Factor {idx} ({factor['factor_name']}): Invalid style '{factor['style']}'. "
                      f"Must be one of {valid_styles}")
                return False
            
            # Validate description structure
            description = factor['description']
            if not isinstance(description, dict):
                print(f"✗ Factor {idx} ({factor['factor_name']}): description should be a dict")
                return False
            
            if 'en' not in description or 'zh' not in description:
                print(f"✗ Factor {idx} ({factor['factor_name']}): description must contain 'en' and 'zh' keys")
                return False
            
            if not description['en'] or not description['zh']:
                print(f"✗ Factor {idx} ({factor['factor_name']}): Both English and Chinese descriptions are required")
                return False
            
            print(f"✓ Factor {idx}: {factor['factor_name']} ({factor['style']}) - Valid")
        
        # Validate metadata
        metadata = data['metadata']
        required_metadata_fields = {'version', 'last_updated', 'description'}
        missing_metadata = required_metadata_fields - set(metadata.keys())
        if missing_metadata:
            print(f"⚠ Metadata missing optional fields: {missing_metadata}")
        
        print("✓ Metadata structure is valid")
        
        print("\n" + "="*50)
        print("✓ All validations passed!")
        print("="*50)
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ JSON parsing error: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def main():
    """Main entry point for the validation script."""
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    factors_file = project_root / 'factors' / 'factors.json'
    
    print("FactorBase - Factors Taxonomy Validator")
    print("="*50)
    print(f"Validating: {factors_file}\n")
    
    success = validate_factors_json(str(factors_file))
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
