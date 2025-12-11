DROP TABLE IF EXISTS components;
CREATE TABLE components (
    id INTEGER PRIMARY KEY,
    library TEXT,           -- 库文件名 (e.g. "Analog")
    symbol TEXT,            -- 元件名 (e.g. "Comparator, LM393DR2G")
    value TEXT,             -- 值 (e.g. "LM393DR2G")
    footprint TEXT,         -- 封装
    datasheet TEXT,         -- 链接
    description TEXT,       -- 描述
    lcsc_id TEXT,           -- LCSC 编号 (C7955)
    stock INTEGER,          -- 库存
    price TEXT,             -- 价格 (字符串方便带单位，或者解析为 float)
    attributes TEXT,        -- JSON 字符串，包含所有其他电气参数
    keywords TEXT,          -- 搜索关键词
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引加速搜索
CREATE INDEX idx_symbol ON components(symbol);
CREATE INDEX idx_lcsc ON components(lcsc_id);
-- 可选：创建全文检索 (FTS) 表，后续再做