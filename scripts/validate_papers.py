#!/usr/bin/env python3
"""
Validate and display summary of paper metadata files.

This script validates that all paper metadata JSON files conform to the
FactorBase schema and displays a summary of the papers collection.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


def load_paper_metadata(filepath: Path) -> Dict[str, Any]:
    """Load a paper metadata JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_paper_schema(paper: Dict[str, Any], filepath: str) -> List[str]:
    """
    Validate a paper metadata dict against the required schema.
    
    Returns a list of validation errors (empty if valid).
    """
    errors = []
    
    # Required fields
    required_fields = [
        'paper_id', 'title', 'authors', 'year', 'journal',
        'market', 'asset_class', 'abstract', 'conclusion_sign',
        'replicable', 'notes'
    ]
    
    for field in required_fields:
        if field not in paper:
            errors.append(f"{filepath}: Missing required field '{field}'")
        elif paper[field] is None or paper[field] == "":
            if field != 'notes':  # notes can be empty
                errors.append(f"{filepath}: Field '{field}' is empty")
    
    # Type validation
    if 'paper_id' in paper and not isinstance(paper['paper_id'], int):
        errors.append(f"{filepath}: 'paper_id' must be an integer")
    
    if 'year' in paper and not isinstance(paper['year'], int):
        errors.append(f"{filepath}: 'year' must be an integer")
    
    # Value validation
    if 'conclusion_sign' in paper:
        valid_conclusions = ['positive', 'negative', 'mixed', 'none']
        if paper['conclusion_sign'] not in valid_conclusions:
            errors.append(
                f"{filepath}: 'conclusion_sign' must be one of {valid_conclusions}"
            )
    
    if 'replicable' in paper:
        valid_replicable = ['yes', 'no', 'unknown']
        if paper['replicable'] not in valid_replicable:
            errors.append(
                f"{filepath}: 'replicable' must be one of {valid_replicable}"
            )
    
    return errors


def main():
    """Main function to validate and summarize paper metadata."""
    # Find metadata directory
    script_dir = Path(__file__).parent
    metadata_dir = script_dir.parent / 'papers' / 'metadata'
    
    if not metadata_dir.exists():
        print(f"Error: Metadata directory not found at {metadata_dir}")
        return 1
    
    # Load all paper metadata files
    papers = []
    all_errors = []
    
    for filepath in sorted(metadata_dir.glob('paper_*.json')):
        try:
            paper = load_paper_metadata(filepath)
            papers.append((filepath.name, paper))
            
            # Validate schema
            errors = validate_paper_schema(paper, filepath.name)
            all_errors.extend(errors)
            
        except json.JSONDecodeError as e:
            all_errors.append(f"{filepath.name}: Invalid JSON - {e}")
        except Exception as e:
            all_errors.append(f"{filepath.name}: Error loading file - {e}")
    
    # Print validation results
    print("=" * 80)
    print("PAPER METADATA VALIDATION REPORT")
    print("=" * 80)
    print()
    
    if all_errors:
        print("❌ VALIDATION ERRORS FOUND:")
        print()
        for error in all_errors:
            print(f"  • {error}")
        print()
        return 1
    else:
        print("✅ All paper metadata files are valid!")
        print()
    
    # Print summary
    print("=" * 80)
    print("PAPERS COLLECTION SUMMARY")
    print("=" * 80)
    print()
    print(f"Total papers: {len(papers)}")
    print()
    
    # Summary by market
    markets = {}
    for _, paper in papers:
        market = paper.get('market', 'Unknown')
        markets[market] = markets.get(market, 0) + 1
    
    print("By Market:")
    for market, count in sorted(markets.items()):
        print(f"  • {market}: {count}")
    print()
    
    # Summary by asset class
    asset_classes = {}
    for _, paper in papers:
        asset_class = paper.get('asset_class', 'Unknown')
        asset_classes[asset_class] = asset_classes.get(asset_class, 0) + 1
    
    print("By Asset Class:")
    for asset_class, count in sorted(asset_classes.items()):
        print(f"  • {asset_class}: {count}")
    print()
    
    # List all papers
    print("=" * 80)
    print("PAPERS LIST")
    print("=" * 80)
    print()
    
    for filename, paper in papers:
        print(f"📄 {filename}")
        print(f"   ID: {paper.get('paper_id')}")
        print(f"   Title: {paper.get('title')}")
        print(f"   Authors: {paper.get('authors')}")
        print(f"   Year: {paper.get('year')}")
        print(f"   Journal: {paper.get('journal')}")
        print(f"   Market: {paper.get('market')}")
        print(f"   Asset Class: {paper.get('asset_class')}")
        print(f"   Conclusion: {paper.get('conclusion_sign')}")
        print(f"   Replicable: {paper.get('replicable')}")
        print()
    
    return 0


if __name__ == '__main__':
    exit(main())
