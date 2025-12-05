-- FactorBase Database Schema
-- Version: 1.0
-- Date: 2025-12-05
-- Purpose: Create database schema for FactorBase knowledge repository
-- Tables: papers, factors, measures, paper_measures

-- ==============================================================================
-- Table: papers
-- Purpose: Store research paper metadata and information
-- ==============================================================================
CREATE TABLE IF NOT EXISTS papers (
    paper_id        INT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(512) NOT NULL,
    authors         VARCHAR(512),
    year            INT,
    journal         VARCHAR(256),
    market          VARCHAR(64),        -- US, TW, Global, JP, etc.
    asset_class     VARCHAR(64),        -- Equity, Bond, FX, Commodity, etc.
    abstract        TEXT,
    conclusion_sign VARCHAR(16),        -- 'positive', 'negative', 'none', 'mixed'
    replicable      VARCHAR(16),        -- 'yes', 'no', 'unknown'
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_market (market),
    INDEX idx_year (year),
    INDEX idx_asset_class (asset_class)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- Table: factors
-- Purpose: Store factor classification and taxonomy
-- ==============================================================================
CREATE TABLE IF NOT EXISTS factors (
    factor_id       INT AUTO_INCREMENT PRIMARY KEY,
    factor_name     VARCHAR(128) NOT NULL UNIQUE,  -- 'Value', 'Momentum', 'Profitability', etc.
    style           VARCHAR(128),                   -- 'Style', 'Quality', 'Risk', 'Sentiment', etc.
    description     TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_factor_name (factor_name),
    INDEX idx_style (style)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- Table: measures
-- Purpose: Store measure definitions with formulas and metadata
-- ==============================================================================
CREATE TABLE IF NOT EXISTS measures (
    measure_id      INT AUTO_INCREMENT PRIMARY KEY,
    factor_id       INT NOT NULL,
    measure_name    VARCHAR(128) NOT NULL,          -- 'PB', 'EP_TTM', 'ROE_TTM', '12M_MOM', etc.
    display_name    VARCHAR(256),                   -- Human-readable description
    formula         TEXT,                           -- Formula description or pseudo-code
    formula_type    VARCHAR(64),                    -- 'ratio', 'difference', 'percentile', 'residual', etc.
    window          VARCHAR(64),                    -- 'TTM', 'MRQ', '3Y', '12M', '36M', etc.
    data_source     VARCHAR(256),                   -- 'financial_statement', 'price', 'analyst_forecast', 'intraday'
    frequency       VARCHAR(32),                    -- 'daily', 'monthly', 'quarterly', 'annual'
    normalization   VARCHAR(64),                    -- 'zscore_cross_sectional', 'rank', 'percentile', 'none'
    remarks         TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (factor_id) REFERENCES factors(factor_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_measure_name (measure_name),
    INDEX idx_factor_id (factor_id),
    INDEX idx_formula_type (formula_type),
    INDEX idx_frequency (frequency)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- Table: paper_measures
-- Purpose: Store relationships between papers and measures
-- ==============================================================================
CREATE TABLE IF NOT EXISTS paper_measures (
    paper_id        INT NOT NULL,
    measure_id      INT NOT NULL,
    role            VARCHAR(64),                    -- 'main_factor', 'control', 'sorting', 'risk_factor'
    usage_detail    TEXT,                           -- e.g., "sorted into quintiles, equal-weighted portfolios"
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (paper_id, measure_id),
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (measure_id) REFERENCES measures(measure_id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_paper_id (paper_id),
    INDEX idx_measure_id (measure_id),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- End of Schema
-- ==============================================================================
