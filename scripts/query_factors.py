#!/usr/bin/env python3
"""
Query and display factors from factors.json.

This utility script provides convenient functions to:
1. List all factors
2. Get specific factor by name or ID
3. Filter factors by style
4. Display factor information in a readable format
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any


class FactorsQuery:
    """Class to query factors from factors.json."""
    
    def __init__(self, factors_file: str):
        """
        Initialize the FactorsQuery with the path to factors.json.
        
        Args:
            factors_file: Path to the factors.json file
        """
        with open(factors_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.factors = self.data['factors']
        self.metadata = self.data.get('metadata', {})
    
    def list_all(self) -> List[Dict[str, Any]]:
        """
        Get all factors.
        
        Returns:
            List of all factor dictionaries
        """
        return self.factors
    
    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a factor by its name.
        
        Args:
            name: Factor name (e.g., "Value", "Momentum")
            
        Returns:
            Factor dictionary or None if not found
        """
        for factor in self.factors:
            if factor['factor_name'].lower() == name.lower():
                return factor
        return None
    
    def get_by_id(self, factor_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a factor by its ID.
        
        Args:
            factor_id: Factor ID
            
        Returns:
            Factor dictionary or None if not found
        """
        for factor in self.factors:
            if factor['factor_id'] == factor_id:
                return factor
        return None
    
    def filter_by_style(self, style: str) -> List[Dict[str, Any]]:
        """
        Get all factors with a specific style.
        
        Args:
            style: Style name (e.g., "Style", "Quality", "Risk", "Sentiment")
            
        Returns:
            List of factor dictionaries matching the style
        """
        return [f for f in self.factors if f['style'].lower() == style.lower()]
    
    def display_factor(self, factor: Dict[str, Any], language: str = 'en'):
        """
        Display a factor in a readable format.
        
        Args:
            factor: Factor dictionary
            language: Language for description ('en' or 'zh')
        """
        print(f"\n{'='*60}")
        print(f"Factor ID: {factor['factor_id']}")
        print(f"Name: {factor['factor_name']}")
        print(f"Style: {factor['style']}")
        print(f"\nDescription ({language}):")
        print(f"{factor['description'][language]}")
        print(f"{'='*60}")
    
    def display_all(self, language: str = 'en'):
        """
        Display all factors.
        
        Args:
            language: Language for description ('en' or 'zh')
        """
        print(f"\n{'='*60}")
        print(f"FactorBase - Factors Taxonomy (v{self.metadata.get('version', 'N/A')})")
        print(f"Last Updated: {self.metadata.get('last_updated', 'N/A')}")
        print(f"Total Factors: {len(self.factors)}")
        print(f"{'='*60}")
        
        for factor in self.factors:
            self.display_factor(factor, language)
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata information.
        
        Returns:
            Metadata dictionary
        """
        return self.metadata


def main():
    """Main entry point for the query script."""
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    factors_file = project_root / 'factors' / 'factors.json'
    
    # Initialize query object
    query = FactorsQuery(str(factors_file))
    
    # Example usage
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'list':
            # List all factors
            query.display_all('en' if len(sys.argv) <= 2 else sys.argv[2])
        
        elif command == 'get' and len(sys.argv) > 2:
            # Get specific factor by name
            factor_name = sys.argv[2]
            factor = query.get_by_name(factor_name)
            if factor:
                query.display_factor(factor, 'en' if len(sys.argv) <= 3 else sys.argv[3])
            else:
                print(f"Factor '{factor_name}' not found")
        
        elif command == 'style' and len(sys.argv) > 2:
            # Filter by style
            style = sys.argv[2]
            factors = query.filter_by_style(style)
            if factors:
                print(f"\nFactors with style '{style}':")
                for factor in factors:
                    print(f"  - {factor['factor_name']} (ID: {factor['factor_id']})")
            else:
                print(f"No factors found with style '{style}'")
        
        else:
            print("Unknown command or missing arguments")
            print_usage()
    else:
        # Default: display all factors
        query.display_all('en')


def print_usage():
    """Print usage information."""
    print("\nUsage:")
    print("  python query_factors.py list [en|zh]          - List all factors")
    print("  python query_factors.py get <name> [en|zh]    - Get factor by name")
    print("  python query_factors.py style <style>         - Filter by style")
    print("\nExamples:")
    print("  python query_factors.py list")
    print("  python query_factors.py list zh")
    print("  python query_factors.py get Value")
    print("  python query_factors.py get Momentum zh")
    print("  python query_factors.py style Quality")


if __name__ == '__main__':
    main()
