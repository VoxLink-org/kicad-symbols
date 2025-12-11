DROP TABLE IF EXISTS components;
CREATE TABLE IF NOT EXISTS components (
    id INTEGER PRIMARY KEY,
    library TEXT,
    symbol TEXT,
    value TEXT,
    footprint TEXT,
    datasheet TEXT,
    description TEXT,
    lcsc_id TEXT,
    stock INTEGER,
    price TEXT,
    attributes TEXT,
    keywords TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(library, symbol)

-- 创建索引加速搜索
CREATE INDEX IF NOT EXISTS idx_symbol ON components(symbol);
CREATE INDEX IF NOT EXISTS idx_lcsc ON components(lcsc_id);
CREATE INDEX IF NOT EXISTS idx_desc ON components(description);
-- 可选：创建全文检索 (FTS) 表，后续再做

-- Query to find TP4056 in the database
SELECT *
FROM components
WHERE symbol LIKE '%TP4056%';