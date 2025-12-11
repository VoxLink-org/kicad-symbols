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
REPO_URL = "https://gitlab.com/kicad/libraries/kicad-symbols.git" # 或者你私有的库
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
    if os.path.exists(SOURCE_DIR):
        shutil.rmtree(SOURCE_DIR)
    
    # 如果你有自己的私有库，改这里的 URL
    # 如果是本地测试，可以注释掉这行，手动放文件进去
    print(f"Cloning {REPO_URL}...")
    subprocess.run(["git", "clone", "--depth=1", REPO_URL, SOURCE_DIR], check=True)

    # 2. 准备 SQL 文件
    sql_lines = []
    
    # === 修改点 1: 删除这一行 ===
    # sql_lines.append("BEGIN TRANSACTION;") 
    
    # 建议加上建表语句，防止表不存在报错
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
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    # 如果你想每次全量覆盖，可以取消下面这行的注释，但会消耗更多额度
    # sql_lines.append("DELETE FROM components;") 
    
    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".kicad_sym")]
    files.sort()
    
    print(f"Found {len(files)} symbol files. Generaring SQL...")
    for f in files:
        process_file(os.path.join(SOURCE_DIR, f), sql_lines)
    # === 修改点 2: 删除这一行 ===
    # sql_lines.append("COMMIT;")

    # 3. 写入文件
    with open(OUTPUT_SQL_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(sql_lines))

    print(f"\nSuccess! SQL generated at '{OUTPUT_SQL_FILE}' with {len(sql_lines)-2} statements.")

if __name__ == "__main__":
    main()