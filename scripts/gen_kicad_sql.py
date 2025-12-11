import os
import shutil
import sys
import subprocess
import json
import sqlite3 # 仅用于转义字符串，不连接DB

# 检查依赖
try:
    import sexpdata
except ImportError:
    print("Error: 'sexpdata' module not found. Please run 'pip install sexpdata'")
    sys.exit(1)

# ================= 配置 =================
SOURCE_DIR = "temp_kicad_source"
OUTPUT_SQL_FILE = "import.sql"

# 定义我们要单独提取到列里的核心字段
CORE_FIELDS = {
    "Value": "value",
    "Footprint": "footprint",
    "Datasheet": "datasheet",
    "Description": "description",
    "LCSC": "lcsc_id",
    "Stock": "stock",
    "Price": "price",
    "ki_keywords": "keywords"
}

def clone_kicad_repository(source_dir):
    REPO_URL = "https://gitlab.com/kicad/libraries/kicad-symbols.git" # 或者你私有的库
    
    repo_url = REPO_URL
    """Clone the KiCad symbols repository"""
    if os.path.exists(source_dir):
        shutil.rmtree(source_dir)
    
    print(f"Cloning {repo_url}...")
    subprocess.run(["git", "clone", "--depth=1", repo_url, source_dir], check=True)

def clone_jlcpcb_library(source_dir):
    """Clone JLCPCB KiCad library and copy symbols to source directory"""
    temp_jlcpcb_dir = "temp_jlcpcb_source"
    JLCPCB_REPO_URL = "https://github.com/CDFER/JLCPCB-Kicad-Library.git"

    # Clean up existing directories
    if os.path.exists(temp_jlcpcb_dir):
        shutil.rmtree(temp_jlcpcb_dir)
    if os.path.exists(source_dir):
        shutil.rmtree(source_dir)
    
    # Create source directory
    os.makedirs(source_dir, exist_ok=True)
    
    print(f"Cloning {JLCPCB_REPO_URL}...")
    subprocess.run(["git", "clone", "--depth=1", JLCPCB_REPO_URL, temp_jlcpcb_dir], check=True)
    
    # Move symbols directory contents to source directory
    jlcpcb_symbols_dir = os.path.join(temp_jlcpcb_dir, "symbols")
    if os.path.exists(jlcpcb_symbols_dir):
        print(f"Moving symbols from {jlcpcb_symbols_dir} to {source_dir}...")
        for item in os.listdir(jlcpcb_symbols_dir):
            source_item = os.path.join(jlcpcb_symbols_dir, item)
            dest_item = os.path.join(source_dir, item)
            if os.path.isfile(source_item):
                shutil.move(source_item, dest_item)
            elif os.path.isdir(source_item):
                shutil.move(source_item, dest_item)
    
    # Clean up temporary directory
    shutil.rmtree(temp_jlcpcb_dir)
    print("JLCPCB library symbols downloaded successfully.")

def escape_sql_str(value):
    """简单的 SQL 字符串转义"""
    if value is None:
        return "NULL"
    return "'{}'".format(str(value).replace("'", "''"))

def extract_symbol_data(library_name, symbol_list):
    if not isinstance(symbol_list, list) or len(symbol_list) < 2:
        return None

    raw_name = symbol_list[1]
    symbol_name = str(raw_name) if not isinstance(raw_name, list) else str(raw_name[0])

    # 初始化记录
    record = {
        "library": library_name,
        "symbol": symbol_name,
        "attributes": {}
    }
    # 初始化核心字段为 None
    for k in CORE_FIELDS.values():
        record[k] = None

    # 遍历 S-Expression 解析属性
    for item in symbol_list[2:]:
        if isinstance(item, list) and len(item) > 1:
            tag = item[0]
            tag_str = str(tag) if hasattr(tag, 'value') else str(tag)
            
            if tag_str == "property":
                if len(item) >= 3:
                    key = item[1] # 属性名，如 "Value", "LCSC"
                    val = item[2] # 属性值
                    
                    # 处理 sexpdata 可能的封装
                    if hasattr(val, 'value'): val = val.value
                    elif isinstance(val, list): val = " ".join([str(x) for x in val])
                    
                    # 判断是核心字段还是普通属性
                    if key in CORE_FIELDS:
                        db_col = CORE_FIELDS[key]
                        record[db_col] = val
                    else:
                        # 排除掉一些无用的元数据
                        if key not in ["Reference", "ki_description", "ki_fp_filters"]:
                            record["attributes"][key] = val

    return record

def process_file(filepath, sql_lines):
    filename = os.path.basename(filepath)
    lib_name = os.path.splitext(filename)[0]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        parsed = sexpdata.loads(content, nil=None, true=True, false=False)
    except Exception as e:
        print(f"Skipping {filename}: {e}")
        return

    if not isinstance(parsed, list) or len(parsed) == 0:
        return

    # 检查是否为库文件头
    top_tag = parsed[0]
    if str(top_tag) != "kicad_symbol_lib":
        return

    count = 0
    for item in parsed:
        if isinstance(item, list) and len(item) > 0:
            tag = item[0]
            if str(tag) == "symbol":
                data = extract_symbol_data(lib_name, item)
                if data:
                    # 构建 SQL INSERT 语句
                    # 将 attributes 字典转为 JSON 字符串
                    attr_json = json.dumps(data["attributes"], ensure_ascii=False)
                    
                    # 处理 Stock (转为数字，去掉非数字字符)
                    stock_val = 0
                    if data["stock"]:
                        try:
                            stock_val = int(''.join(filter(str.isdigit, str(data["stock"]))))
                        except:
                            stock_val = 0

                    sql = (
                        "INSERT OR REPLACE INTO components "
                        "(library, symbol, value, footprint, datasheet, description, "
                        "lcsc_id, stock, price, keywords, attributes) VALUES ("
                        f"{escape_sql_str(data['library'])}, "
                        f"{escape_sql_str(data['symbol'])}, "
                        f"{escape_sql_str(data['value'])}, "
                        f"{escape_sql_str(data['footprint'])}, "
                        f"{escape_sql_str(data['datasheet'])}, "
                        f"{escape_sql_str(data['description'])}, "
                        f"{escape_sql_str(data['lcsc_id'])}, "
                        f"{stock_val}, "
                        f"{escape_sql_str(data['price'])}, "
                        f"{escape_sql_str(data['keywords'])}, "
                        f"{escape_sql_str(attr_json)}"
                        ");"
                    )
                    sql_lines.append(sql)
                    count += 1
    
    print(f"Processed {lib_name}: {count} symbols")

def main():
    # 1. 清理和下载
    # 选择使用哪个库：官方KiCad库或JLCPCB库
    clone_kicad_repository(SOURCE_DIR)  # 官方KiCad库
    clone_jlcpcb_library(SOURCE_DIR)  # JLCPCB库

    # 2. 准备 SQL 文件
    sql_lines = []
    
    # === 核心修改点：建表语句 ===
    # 不需要在这里写 DROP TABLE 了，因为你已经手动删过了。
    # 关键是加上 UNIQUE(library, symbol)
    sql_lines.append("""
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
    );
    """)
    
    # 重新创建索引 (删表后索引也没了，需要重建)
    sql_lines.append("CREATE INDEX IF NOT EXISTS idx_symbol ON components(symbol);")
    sql_lines.append("CREATE INDEX IF NOT EXISTS idx_lcsc ON components(lcsc_id);")
    # 对 Description 做索引有助于模糊搜索
    sql_lines.append("CREATE INDEX IF NOT EXISTS idx_desc ON components(description);")

    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".kicad_sym")]
    files.sort()
    
    print(f"Found {len(files)} symbol files. Generaring SQL...")
    for f in files:
        process_file(os.path.join(SOURCE_DIR, f), sql_lines)

    # 3. 写入文件
    with open(OUTPUT_SQL_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(sql_lines))

    print(f"\nSuccess! SQL generated at '{OUTPUT_SQL_FILE}' with {len(sql_lines)} statements.")

if __name__ == "__main__":
    main()
