#!/usr/bin/env python3
"""
Generate papers index from metadata files.

This script reads all paper metadata files and generates an index
that can be used for quick lookups and queries.
"""

import json
from pathlib import Path
from typing import Dict, List, Any


def load_all_papers(metadata_dir: Path) -> List[Dict[str, Any]]:
    """Load all paper metadata files."""
    papers = []
    for filepath in sorted(metadata_dir.glob('paper_*.json')):
        with open(filepath, 'r', encoding='utf-8') as f:
            papers.append(json.load(f))
    return papers


def generate_index(papers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate an index of papers by various attributes.
    
    Returns a dict with the following structure:
    {
        "by_id": {...},
        "by_market": {...},
        "by_asset_class": {...},
        "by_year": {...},
        "by_author": {...}
    }
    """
    index = {
        "by_id": {},
        "by_market": {},
        "by_asset_class": {},
        "by_year": {},
        "by_author": {}
    }
    
    for paper in papers:
        paper_id = paper['paper_id']
        
        # Index by ID
        index["by_id"][paper_id] = paper
        
        # Index by market
        market = paper['market']
        if market not in index["by_market"]:
            index["by_market"][market] = []
        index["by_market"][market].append(paper_id)
        
        # Index by asset class
        asset_class = paper['asset_class']
        if asset_class not in index["by_asset_class"]:
            index["by_asset_class"][asset_class] = []
        index["by_asset_class"][asset_class].append(paper_id)
        
        # Index by year
        year = paper['year']
        if year not in index["by_year"]:
            index["by_year"][year] = []
        index["by_year"][year].append(paper_id)
        
        # Index by author
        authors = paper['authors'].split(';')
        for author in authors:
            author = author.strip()
            if author not in index["by_author"]:
                index["by_author"][author] = []
            index["by_author"][author].append(paper_id)
    
    return index


def main():
    """Generate and save papers index."""
    script_dir = Path(__file__).parent
    metadata_dir = script_dir.parent / 'papers' / 'metadata'
    output_file = metadata_dir.parent / 'papers_index.json'
    
    if not metadata_dir.exists():
        print(f"Error: Metadata directory not found at {metadata_dir}")
        return 1
    
    # Load all papers
    papers = load_all_papers(metadata_dir)
    print(f"Loaded {len(papers)} papers")
    
    # Generate index
    index = generate_index(papers)
    
    # Save index
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"Index saved to {output_file}")
    print()
    print("Index statistics:")
    print(f"  Markets: {len(index['by_market'])}")
    print(f"  Asset classes: {len(index['by_asset_class'])}")
    print(f"  Years: {len(index['by_year'])}")
    print(f"  Authors: {len(index['by_author'])}")
    
    return 0


if __name__ == '__main__':
    exit(main())
