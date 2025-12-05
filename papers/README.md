# Papers Directory

This directory contains research papers and their metadata for the FactorBase knowledge base.

## Directory Structure

```
papers/
├── raw_pdf/          # Original PDF files of research papers
├── metadata/         # Structured metadata for each paper (JSON format)
└── README.md         # This file
```

## Papers Metadata

The `metadata/` directory contains JSON files for key factor investing research papers. Each file follows the schema defined in the FactorBase implementation document.

### Required Fields

Each paper metadata JSON file must include:

- **paper_id**: Unique integer identifier
- **title**: Full title of the paper
- **authors**: Author names (semicolon-separated for multiple authors)
- **year**: Publication year
- **journal**: Journal or publication venue
- **market**: Target market (US, TW, Global, etc.)
- **asset_class**: Asset class studied (Equity, Bond, Multi-Asset, etc.)
- **abstract**: Paper abstract or summary
- **conclusion_sign**: Research conclusion ('positive', 'negative', 'mixed', 'none')
- **replicable**: Whether findings are replicable ('yes', 'no', 'unknown')
- **notes**: Additional notes or key takeaways

## Current Papers Collection

### paper_001.json - Fama & French (1993)
**Title:** Common risk factors in the returns on stocks and bonds  
**Key Contribution:** Introduced the three-factor model (Market, Size, Value)  
**Factors:** Market, Size (SMB), Value (HML)

### paper_002.json - Carhart (1997)
**Title:** On Persistence in Mutual Fund Performance  
**Key Contribution:** Added momentum factor to the three-factor model  
**Factors:** Market, Size, Value, Momentum (UMD)

### paper_003.json - Fama & French (2015)
**Title:** A five-factor asset pricing model  
**Key Contribution:** Extended to five factors adding profitability and investment  
**Factors:** Market, Size, Value, Profitability (RMW), Investment (CMA)

### paper_004.json - Novy-Marx (2013)
**Title:** The other side of value: The gross profitability premium  
**Key Contribution:** Introduced gross profitability as a powerful predictor  
**Factors:** Profitability (Gross Profits-to-Assets)

### paper_005.json - Hou, Xue, Zhang (2015)
**Title:** Digesting anomalies: An investment approach  
**Key Contribution:** Introduced the q-factor model based on investment theory  
**Factors:** Market, Size, Investment (I/A), Profitability (ROE)

### paper_006.json - Asness, Moskowitz, Pedersen (2013)
**Title:** Value and Momentum Everywhere  
**Key Contribution:** Demonstrated value and momentum work across asset classes  
**Factors:** Value, Momentum (across multiple asset classes)

### paper_007.json - Asness, Frazzini, Pedersen (2019)
**Title:** Quality Minus Junk  
**Key Contribution:** Comprehensive quality factor combining multiple characteristics  
**Factors:** Quality (QMJ)

## Usage

These metadata files serve as the foundation for:

1. **Literature tracking**: Maintain a structured knowledge base of factor research
2. **Factor attribution**: Link measures to academic sources
3. **Backtesting reports**: Automatically cite relevant papers in research reports
4. **Copilot integration**: Enable AI agents to reference academic literature
5. **MeasureDefinitionManager**: Connect measure definitions to their academic origins

## Adding New Papers

To add a new paper:

1. Create a new JSON file in `metadata/` following the naming convention `paper_XXX.json`
2. Ensure all required fields are included
3. Use the next available `paper_id` (8 or higher)
4. Add an entry to this README documenting the paper

## Related Documentation

- See `/meeting_20251205_project_2/FactorBase-implement.md` for detailed schema specifications
- See `.github/copilot-instructions.md` for project-specific rules and standards
