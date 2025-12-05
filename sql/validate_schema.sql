-- FactorBase Schema Validation Script
-- Purpose: Verify that all tables and constraints are properly created
-- Usage: mysql -u username -p factorbase < validate_schema.sql
--        or: sqlite3 factorbase.db < validate_schema.sql (with syntax adjustments)

-- Check if all tables exist
SELECT 'Checking tables...' AS status;
SELECT 
    'papers' AS table_name, 
    COUNT(*) AS exists 
FROM information_schema.tables 
WHERE table_schema = DATABASE() AND table_name = 'papers'
UNION ALL
SELECT 
    'factors' AS table_name, 
    COUNT(*) AS exists 
FROM information_schema.tables 
WHERE table_schema = DATABASE() AND table_name = 'factors'
UNION ALL
SELECT 
    'measures' AS table_name, 
    COUNT(*) AS exists 
FROM information_schema.tables 
WHERE table_schema = DATABASE() AND table_name = 'measures'
UNION ALL
SELECT 
    'paper_measures' AS table_name, 
    COUNT(*) AS exists 
FROM information_schema.tables 
WHERE table_schema = DATABASE() AND table_name = 'paper_measures';

-- Check foreign key constraints
SELECT 'Checking foreign keys...' AS status;
SELECT 
    constraint_name,
    table_name,
    referenced_table_name
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE()
    AND referenced_table_name IS NOT NULL
ORDER BY table_name, constraint_name;

-- Check indexes
SELECT 'Checking indexes...' AS status;
SELECT 
    table_name,
    index_name,
    GROUP_CONCAT(column_name ORDER BY seq_in_index) AS columns
FROM information_schema.statistics
WHERE table_schema = DATABASE()
    AND table_name IN ('papers', 'factors', 'measures', 'paper_measures')
GROUP BY table_name, index_name
ORDER BY table_name, index_name;

-- Validation summary
SELECT 'Schema validation complete!' AS status;
