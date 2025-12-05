# Factors Taxonomy

This directory contains the standardized factor classification system for FactorBase.

## Overview

The `factors.json` file defines the core factors used to categorize all measures in the FactorBase system. Each factor represents a fundamental driver of cross-sectional stock returns based on extensive academic research.

## Core Factors (Version 1.0)

The current taxonomy includes 5 core factors:

1. **Value** - Companies with low valuations relative to fundamentals
2. **Size** - Market capitalization effect
3. **Momentum** - Persistence of past returns
4. **Profitability** - Earnings quality and profitability metrics
5. **Investment** - Capital expenditure and asset growth patterns

## JSON Structure

Each factor entry includes:

- `factor_id`: Unique identifier for the factor
- `factor_name`: Name of the factor (e.g., "Value", "Momentum")
- `style`: Classification of the factor type
  - `Style`: Traditional style factors (Value, Size, Momentum, Investment)
  - `Quality`: Quality-based factors (Profitability)
  - `Risk`: Risk-based factors
  - `Sentiment`: Sentiment-based factors
- `description`: Detailed explanation in both English and Chinese
  - `en`: English description
  - `zh`: Chinese description (繁體中文)

## Academic Foundation

The factors taxonomy is based on established academic research:

- **Fama & French (1993)**: Three-factor model (Market, Size, Value)
- **Carhart (1997)**: Four-factor model (added Momentum)
- **Fama & French (2015)**: Five-factor model (added Profitability, Investment)
- **Hou, Xue & Zhang (2015)**: q-factor model

## Usage

### For Research Team
- Reference this file when categorizing new measures
- Use factor definitions when designing new strategies
- Cite academic sources in research reports

### For Data Team
- Map measures to factors using `factor_name` or `factor_id`
- Integrate with MeasureDefinitionManager for automatic factor assignment

### For Application Team
- Build factor-based UI filters and selections
- Generate factor-based reports and analytics

### For Copilot Agents
```python
# Example: Query all measures for a specific factor
import json

with open('factors/factors.json', 'r') as f:
    factors_data = json.load(f)

# Get Value factor information
value_factor = next(f for f in factors_data['factors'] if f['factor_name'] == 'Value')
print(value_factor['description']['zh'])
```

## Version History

- **v1.0** (2025-12-05): Initial taxonomy with 5 core factors
  - Owner: Fama (Research Team)
  - Milestone: M1

## Future Extensions

Additional factors may be added in future versions:
- Quality (综合品質因子)
- Low Volatility (低波動性)
- Liquidity (流動性)
- Sentiment (市場情緒)

## Related Files

- `/measures/`: Measure definitions categorized by factors
- `/papers/`: Academic papers supporting each factor
- `/relations/paper_measures.json`: Mapping between papers and measures

## Contact

- **Owner**: Fama (Research Team)
- **Due Date**: 2025-12-12
- **Milestone**: M1
