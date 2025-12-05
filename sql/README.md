# FactorBase Database Schema

This directory contains the SQL schema files for the FactorBase knowledge repository.

## Files

- `create_tables.sql` - Main schema definition file containing all table structures

## Database Tables

The schema consists of four core tables:

### 1. papers
Stores research paper metadata and information.

**Key Fields:**
- `paper_id` - Primary key (auto-increment)
- `title` - Paper title (required)
- `authors` - Author names
- `year` - Publication year
- `market` - Target market (US, TW, Global, JP, etc.)
- `asset_class` - Asset class (Equity, Bond, FX, Commodity, etc.)
- `conclusion_sign` - Research conclusion ('positive', 'negative', 'none', 'mixed')
- `replicable` - Replication status ('yes', 'no', 'unknown')

**Indexes:** market, year, asset_class

### 2. factors
Stores factor classifications and taxonomy.

**Key Fields:**
- `factor_id` - Primary key (auto-increment)
- `factor_name` - Factor name (unique, required) - 'Value', 'Momentum', 'Profitability', etc.
- `style` - Style category - 'Style', 'Quality', 'Risk', 'Sentiment', etc.
- `description` - Detailed factor description

**Indexes:** factor_name, style

### 3. measures
Stores measure definitions with formulas and metadata.

**Key Fields:**
- `measure_id` - Primary key (auto-increment)
- `factor_id` - Foreign key to factors table (required)
- `measure_name` - Measure identifier ('PB', 'EP_TTM', 'ROE_TTM', '12M_MOM', etc.)
- `display_name` - Human-readable description
- `formula` - Formula description or pseudo-code
- `formula_type` - Formula category ('ratio', 'difference', 'percentile', 'residual', etc.)
- `window` - Time window ('TTM', 'MRQ', '3Y', '12M', '36M', etc.)
- `data_source` - Data source identifier
- `frequency` - Update frequency ('daily', 'monthly', 'quarterly', 'annual')
- `normalization` - Normalization method ('zscore_cross_sectional', 'rank', 'percentile', 'none')

**Constraints:**
- Foreign key to `factors(factor_id)` with ON DELETE RESTRICT

**Indexes:** measure_name, factor_id, formula_type, frequency

### 4. paper_measures
Stores relationships between papers and measures.

**Key Fields:**
- `paper_id` - Foreign key to papers table
- `measure_id` - Foreign key to measures table
- `role` - Usage role ('main_factor', 'control', 'sorting', 'risk_factor')
- `usage_detail` - Detailed usage description

**Constraints:**
- Composite primary key (paper_id, measure_id)
- Foreign key to `papers(paper_id)` with ON DELETE CASCADE
- Foreign key to `measures(measure_id)` with ON DELETE CASCADE

**Indexes:** paper_id, measure_id, role

## Usage

### MySQL

```bash
# Create database
mysql -u username -p -e "CREATE DATABASE factorbase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Import schema
mysql -u username -p factorbase < create_tables.sql

# Verify tables
mysql -u username -p factorbase -e "SHOW TABLES;"
```

### SQLite (for development/testing)

**Note:** The provided `create_tables.sql` is designed for MySQL. For SQLite, you'll need to:
- Replace `INT AUTO_INCREMENT` with `INTEGER PRIMARY KEY AUTOINCREMENT`
- Remove `ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci`
- Separate index creation from table definition
- Always enable foreign key constraints before operations

Example SQLite usage (after converting syntax):

```bash
# Create database with converted schema
sqlite3 factorbase.db < create_tables_sqlite.sql

# Always enable foreign key constraints (required for each connection)
sqlite3 factorbase.db "PRAGMA foreign_keys = ON;"

# Verify tables
sqlite3 factorbase.db ".schema"
```

For testing purposes, it's recommended to use a MySQL/MariaDB instance or Docker container rather than SQLite to ensure compatibility with the production schema.

## Schema Design Principles

1. **Referential Integrity**: All foreign keys are properly defined with appropriate CASCADE/RESTRICT rules
2. **Performance**: Strategic indexes on frequently queried columns
3. **Extensibility**: TEXT fields for flexible metadata storage
4. **Timestamps**: Automatic created_at and updated_at tracking
5. **Unicode Support**: UTF-8 (utf8mb4) character set for international content

## Version History

- v1.0 (2025-12-05): Initial schema creation with four core tables
