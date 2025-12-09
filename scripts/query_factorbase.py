#!/usr/bin/env python3
"""
FactorBase Query Tool
=====================
用於查詢 FactorBase 概念層資料的命令列工具。

使用方式:
    python query_factorbase.py --measure BM
    python query_factorbase.py --paper paper_001
    python query_factorbase.py --factor Value
    python query_factorbase.py --list-papers
    python query_factorbase.py --list-measures
    python query_factorbase.py --list-factors
    python query_factorbase.py --paper-measures paper_001
"""

import argparse
import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any


# 專案根目錄
PROJECT_ROOT = Path(__file__).parent.parent


def load_json(filepath: Path) -> Optional[Dict[str, Any]]:
    """載入 JSON 檔案"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 檔案不存在: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析錯誤: {filepath} - {e}")
        return None


def get_measure(measure_id: str) -> Optional[Dict[str, Any]]:
    """
    根據 measure_id 查詢 Measure 定義
    """
    index_path = PROJECT_ROOT / "measures" / "index.json"
    index = load_json(index_path)
    if not index:
        return None
    
    # 在 index 中搜尋 measure
    for factor_group in index.get("factors", []):
        for measure in factor_group.get("measures", []):
            if measure.get("measure_id") == measure_id:
                # 找到後載入完整 JSON
                measure_file = PROJECT_ROOT / "measures" / measure.get("file")
                return load_json(measure_file)
    
    print(f"❌ 找不到 Measure: {measure_id}")
    return None


def get_paper(paper_id: str) -> Optional[Dict[str, Any]]:
    """
    根據 paper_id 查詢論文資訊
    """
    # paper_id 格式為 paper_001，檔案為 paper_001.json
    paper_path = PROJECT_ROOT / "papers" / "metadata" / f"{paper_id}.json"
    paper = load_json(paper_path)
    
    if not paper:
        print(f"❌ 找不到論文: {paper_id}")
        return None
    
    return paper


def get_measures_by_factor(factor: str) -> List[Dict[str, Any]]:
    """
    根據因子類別取得所有 Measures
    """
    index_path = PROJECT_ROOT / "measures" / "index.json"
    index = load_json(index_path)
    if not index:
        return []
    
    results = []
    for factor_group in index.get("factors", []):
        if factor_group.get("factor", "").lower() == factor.lower():
            for measure in factor_group.get("measures", []):
                measure_file = PROJECT_ROOT / "measures" / measure.get("file")
                measure_data = load_json(measure_file)
                if measure_data:
                    results.append(measure_data)
    
    if not results:
        print(f"❌ 找不到因子類別: {factor}")
    
    return results


def get_paper_measures(paper_id: str) -> List[Dict[str, Any]]:
    """
    取得特定論文使用的所有 Measures
    """
    relations_path = PROJECT_ROOT / "relations" / "paper_measures.json"
    relations = load_json(relations_path)
    if not relations:
        return []
    
    results = []
    for link in relations.get("paper_measure_links", []):
        if link.get("paper_id") == paper_id:
            results.append(link)
    
    return results


def list_papers() -> List[Dict[str, Any]]:
    """
    列出所有論文
    """
    papers_dir = PROJECT_ROOT / "papers" / "metadata"
    results = []
    
    for paper_file in sorted(papers_dir.glob("paper_*.json")):
        paper = load_json(paper_file)
        if paper:
            results.append({
                "paper_id": paper.get("paper_id"),
                "title": paper.get("title"),
                "authors": paper.get("authors"),
                "year": paper.get("year"),
                "journal": paper.get("journal")
            })
    
    return results


def list_measures() -> List[Dict[str, str]]:
    """
    列出所有 Measures（摘要）
    """
    index_path = PROJECT_ROOT / "measures" / "index.json"
    index = load_json(index_path)
    if not index:
        return []
    
    results = []
    for factor_group in index.get("factors", []):
        factor_name = factor_group.get("factor")
        for measure in factor_group.get("measures", []):
            results.append({
                "measure_id": measure.get("measure_id"),
                "display_name": measure.get("display_name"),
                "factor": factor_name,
                "original_paper_id": measure.get("original_paper_id")
            })
    
    return results


def list_factors() -> List[Dict[str, Any]]:
    """
    列出所有因子類別
    """
    index_path = PROJECT_ROOT / "measures" / "index.json"
    index = load_json(index_path)
    if not index:
        return []
    
    results = []
    for factor_group in index.get("factors", []):
        results.append({
            "factor": factor_group.get("factor"),
            "count": factor_group.get("count"),
            "measures": [m.get("measure_id") for m in factor_group.get("measures", [])]
        })
    
    return results


def print_json(data: Any, indent: int = 2) -> None:
    """格式化輸出 JSON"""
    print(json.dumps(data, ensure_ascii=False, indent=indent))


def main():
    parser = argparse.ArgumentParser(
        description="FactorBase 概念層查詢工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
    python query_factorbase.py --measure BM
    python query_factorbase.py --paper paper_001
    python query_factorbase.py --factor Value
    python query_factorbase.py --paper-measures paper_001
    python query_factorbase.py --list-papers
    python query_factorbase.py --list-measures
    python query_factorbase.py --list-factors
        """
    )
    
    # 查詢單一項目
    parser.add_argument("--measure", "-m", type=str, help="查詢指定 Measure (e.g., BM, ROE_TTM)")
    parser.add_argument("--paper", "-p", type=str, help="查詢指定論文 (e.g., paper_001)")
    parser.add_argument("--factor", "-f", type=str, help="查詢指定因子的所有 Measures (e.g., Value)")
    parser.add_argument("--paper-measures", "-pm", type=str, help="查詢論文使用的 Measures (e.g., paper_001)")
    
    # 列表
    parser.add_argument("--list-papers", action="store_true", help="列出所有論文")
    parser.add_argument("--list-measures", action="store_true", help="列出所有 Measures")
    parser.add_argument("--list-factors", action="store_true", help="列出所有因子類別")
    
    # 輸出格式
    parser.add_argument("--compact", action="store_true", help="緊湊輸出（無縮排）")
    
    args = parser.parse_args()
    
    indent = None if args.compact else 2
    
    # 處理查詢
    if args.measure:
        result = get_measure(args.measure)
        if result:
            print(f"\n📊 Measure: {args.measure}")
            print("=" * 50)
            print_json(result, indent)
    
    elif args.paper:
        result = get_paper(args.paper)
        if result:
            print(f"\n📄 Paper: {args.paper}")
            print("=" * 50)
            print_json(result, indent)
    
    elif args.factor:
        results = get_measures_by_factor(args.factor)
        if results:
            print(f"\n📁 Factor: {args.factor} ({len(results)} measures)")
            print("=" * 50)
            print_json(results, indent)
    
    elif args.paper_measures:
        results = get_paper_measures(args.paper_measures)
        print(f"\n🔗 Paper-Measure Links for {args.paper_measures} ({len(results)} links)")
        print("=" * 50)
        if results:
            print_json(results, indent)
        else:
            print("沒有找到相關連結")
    
    elif args.list_papers:
        results = list_papers()
        print(f"\n📚 All Papers ({len(results)} papers)")
        print("=" * 50)
        print_json(results, indent)
    
    elif args.list_measures:
        results = list_measures()
        print(f"\n📊 All Measures ({len(results)} measures)")
        print("=" * 50)
        print_json(results, indent)
    
    elif args.list_factors:
        results = list_factors()
        print(f"\n📁 All Factors ({len(results)} factors)")
        print("=" * 50)
        print_json(results, indent)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
