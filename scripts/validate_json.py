#!/usr/bin/env python3
"""
FactorBase JSON Validation Tool
===============================
驗證 FactorBase 所有 JSON 檔案是否符合 Schema 定義。

使用方式:
    python validate_json.py           # 驗證所有檔案
    python validate_json.py --papers  # 只驗證 Papers
    python validate_json.py --measures # 只驗證 Measures
    python validate_json.py --relations # 只驗證 Relations
    python validate_json.py --verbose  # 詳細輸出
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

try:
    import jsonschema
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


# 專案根目錄
PROJECT_ROOT = Path(__file__).parent.parent


class ValidationResult:
    """驗證結果封裝"""
    def __init__(self, filepath: Path, valid: bool, errors: List[str] = None):
        self.filepath = filepath
        self.valid = valid
        self.errors = errors or []


def load_json(filepath: Path) -> Optional[Dict[str, Any]]:
    """載入 JSON 檔案"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析錯誤: {e}")


def validate_json_syntax(filepath: Path) -> ValidationResult:
    """驗證 JSON 語法"""
    try:
        load_json(filepath)
        return ValidationResult(filepath, True)
    except ValueError as e:
        return ValidationResult(filepath, False, [str(e)])


def validate_against_schema(data: Dict, schema: Dict, filepath: Path) -> ValidationResult:
    """根據 Schema 驗證 JSON"""
    if not HAS_JSONSCHEMA:
        return ValidationResult(filepath, True, ["⚠️ jsonschema 未安裝，跳過 schema 驗證"])
    
    try:
        validate(instance=data, schema=schema)
        return ValidationResult(filepath, True)
    except ValidationError as e:
        return ValidationResult(filepath, False, [f"Schema 驗證失敗: {e.message}"])


def validate_paper(filepath: Path, schema: Optional[Dict] = None) -> ValidationResult:
    """驗證單一 Paper JSON"""
    # 先檢查語法
    syntax_result = validate_json_syntax(filepath)
    if not syntax_result.valid:
        return syntax_result
    
    data = load_json(filepath)
    errors = []
    
    # 必要欄位檢查
    required_fields = ["paper_id", "title", "authors", "year", "journal"]
    for field in required_fields:
        if field not in data:
            errors.append(f"缺少必要欄位: {field}")
    
    # 型別檢查
    if "year" in data and not isinstance(data["year"], int):
        errors.append("year 必須為整數")
    
    # paper_id 格式
    if "paper_id" in data:
        if not data["paper_id"].startswith("paper_"):
            errors.append("paper_id 應以 'paper_' 開頭")
    
    # Schema 驗證
    if schema and HAS_JSONSCHEMA:
        schema_result = validate_against_schema(data, schema, filepath)
        if not schema_result.valid:
            errors.extend(schema_result.errors)
    
    return ValidationResult(filepath, len(errors) == 0, errors)


def validate_measure(filepath: Path, schema: Optional[Dict] = None) -> ValidationResult:
    """驗證單一 Measure JSON"""
    # 先檢查語法
    syntax_result = validate_json_syntax(filepath)
    if not syntax_result.valid:
        return syntax_result
    
    data = load_json(filepath)
    errors = []
    
    # 必要欄位檢查
    required_fields = ["measure_id", "measure_name", "display_name", "factor", "description"]
    for field in required_fields:
        if field not in data:
            errors.append(f"缺少必要欄位: {field}")
    
    # 概念層禁止欄位（應在 MeasureRetriever）
    forbidden_fields = ["data_source", "frequency"]
    for field in forbidden_fields:
        if field in data:
            errors.append(f"❌ 概念層不應包含: {field}（屬 MeasureRetriever）")
    
    # formula 結構檢查
    if "formula" in data:
        formula = data["formula"]
        if "type" not in formula:
            errors.append("formula 缺少 type 欄位")
    
    # Schema 驗證
    if schema and HAS_JSONSCHEMA:
        schema_result = validate_against_schema(data, schema, filepath)
        if not schema_result.valid:
            errors.extend(schema_result.errors)
    
    return ValidationResult(filepath, len(errors) == 0, errors)


def validate_paper_measures(filepath: Path, schema: Optional[Dict] = None) -> ValidationResult:
    """驗證 Paper-Measure 關聯 JSON"""
    # 先檢查語法
    syntax_result = validate_json_syntax(filepath)
    if not syntax_result.valid:
        return syntax_result
    
    data = load_json(filepath)
    errors = []
    
    # 必要結構
    if "paper_measure_links" not in data:
        errors.append("缺少 paper_measure_links 陣列")
        return ValidationResult(filepath, False, errors)
    
    links = data["paper_measure_links"]
    
    # 收集所有 paper_id 和 measure_id 供後續驗證
    paper_ids = set()
    measure_ids = set()
    
    for i, link in enumerate(links):
        # 必要欄位
        if "paper_id" not in link:
            errors.append(f"link[{i}] 缺少 paper_id")
        else:
            paper_ids.add(link["paper_id"])
        
        if "measure_id" not in link:
            errors.append(f"link[{i}] 缺少 measure_id")
        else:
            measure_ids.add(link["measure_id"])
    
    # 驗證 paper_id 是否存在
    papers_dir = PROJECT_ROOT / "papers" / "metadata"
    for paper_id in paper_ids:
        paper_file = papers_dir / f"{paper_id}.json"
        if not paper_file.exists():
            errors.append(f"參照的論文不存在: {paper_id}")
    
    # 驗證 measure_id 是否存在
    index_path = PROJECT_ROOT / "measures" / "index.json"
    index = load_json(index_path)
    if index:
        existing_measures = set()
        for factor_group in index.get("factors", []):
            for m in factor_group.get("measures", []):
                existing_measures.add(m.get("measure_id"))
        
        for measure_id in measure_ids:
            if measure_id not in existing_measures:
                errors.append(f"參照的 Measure 不存在: {measure_id}")
    
    # Schema 驗證
    if schema and HAS_JSONSCHEMA:
        schema_result = validate_against_schema(data, schema, filepath)
        if not schema_result.valid:
            errors.extend(schema_result.errors)
    
    return ValidationResult(filepath, len(errors) == 0, errors)


def load_schemas() -> Dict[str, Optional[Dict]]:
    """載入所有 Schema"""
    schemas_dir = PROJECT_ROOT / "docs" / "schemas"
    
    schemas = {}
    for schema_name in ["paper_schema", "measure_schema", "paper_measure_schema"]:
        schema_path = schemas_dir / f"{schema_name}.json"
        if schema_path.exists():
            schemas[schema_name] = load_json(schema_path)
        else:
            schemas[schema_name] = None
    
    return schemas


def validate_all_papers(schema: Optional[Dict] = None, verbose: bool = False) -> List[ValidationResult]:
    """驗證所有 Paper JSON"""
    papers_dir = PROJECT_ROOT / "papers" / "metadata"
    results = []
    
    for paper_file in sorted(papers_dir.glob("paper_*.json")):
        result = validate_paper(paper_file, schema)
        results.append(result)
        
        if verbose or not result.valid:
            status = "✅" if result.valid else "❌"
            print(f"  {status} {paper_file.name}")
            if result.errors:
                for error in result.errors:
                    print(f"      └─ {error}")
    
    return results


def validate_all_measures(schema: Optional[Dict] = None, verbose: bool = False) -> List[ValidationResult]:
    """驗證所有 Measure JSON"""
    measures_dir = PROJECT_ROOT / "measures"
    results = []
    
    # 遍歷各因子子目錄
    for factor_dir in sorted(measures_dir.iterdir()):
        if factor_dir.is_dir() and factor_dir.name != "__pycache__":
            for measure_file in sorted(factor_dir.glob("*.json")):
                result = validate_measure(measure_file, schema)
                results.append(result)
                
                if verbose or not result.valid:
                    status = "✅" if result.valid else "❌"
                    print(f"  {status} {factor_dir.name}/{measure_file.name}")
                    if result.errors:
                        for error in result.errors:
                            print(f"      └─ {error}")
    
    return results


def validate_relations(schema: Optional[Dict] = None, verbose: bool = False) -> List[ValidationResult]:
    """驗證 Relations JSON"""
    relations_path = PROJECT_ROOT / "relations" / "paper_measures.json"
    results = []
    
    if relations_path.exists():
        result = validate_paper_measures(relations_path, schema)
        results.append(result)
        
        if verbose or not result.valid:
            status = "✅" if result.valid else "❌"
            print(f"  {status} paper_measures.json")
            if result.errors:
                for error in result.errors:
                    print(f"      └─ {error}")
    else:
        print("  ⚠️ paper_measures.json 不存在")
    
    return results


def print_summary(results: List[ValidationResult]) -> int:
    """輸出摘要並回傳 exit code"""
    total = len(results)
    passed = sum(1 for r in results if r.valid)
    failed = total - passed
    
    print("\n" + "=" * 50)
    print(f"📋 驗證摘要: {passed}/{total} 通過")
    
    if failed > 0:
        print(f"   ❌ {failed} 個檔案有錯誤")
        return 1
    else:
        print("   ✅ 所有檔案驗證通過！")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="FactorBase JSON 驗證工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--papers", action="store_true", help="只驗證 Papers")
    parser.add_argument("--measures", action="store_true", help="只驗證 Measures")
    parser.add_argument("--relations", action="store_true", help="只驗證 Relations")
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細輸出")
    
    args = parser.parse_args()
    
    # 載入 Schemas
    schemas = load_schemas()
    
    if not HAS_JSONSCHEMA:
        print("⚠️ jsonschema 套件未安裝，將只進行基本驗證")
        print("   安裝: pip install jsonschema\n")
    
    all_results = []
    
    # 若沒指定特定類型，則驗證全部
    validate_all = not (args.papers or args.measures or args.relations)
    
    if validate_all or args.papers:
        print("\n📄 驗證 Papers...")
        results = validate_all_papers(schemas.get("paper_schema"), args.verbose)
        all_results.extend(results)
    
    if validate_all or args.measures:
        print("\n📊 驗證 Measures...")
        results = validate_all_measures(schemas.get("measure_schema"), args.verbose)
        all_results.extend(results)
    
    if validate_all or args.relations:
        print("\n🔗 驗證 Relations...")
        results = validate_relations(schemas.get("paper_measure_schema"), args.verbose)
        all_results.extend(results)
    
    exit_code = print_summary(all_results)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
