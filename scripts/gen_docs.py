# gen_kicad_docs.py
import os
import shutil
import sys
import subprocess

# 检查依赖
try:
    import sexpdata
except ImportError:
    print("Error: 'sexpdata' module not found. Please run 'pip install sexpdata'")
    sys.exit(1)

# ================= 配置 =================
# KiCad 官方库地址
REPO_URL = "https://gitlab.com/kicad/libraries/kicad-symbols.git"
# 临时下载目录 (脚本运行完可以忽略)
SOURCE_DIR = "temp_kicad_source"
# 输出文档的目录
OUTPUT_DIR = "docs_output"

def extract_symbol_info(symbol_list):
    """
    使用 sexpdata 解析后的 list 提取 symbol 信息
    """
    if not isinstance(symbol_list, list) or len(symbol_list) < 2:
        return None

    # 获取 Symbol 名称
    raw_name = symbol_list[1]
    symbol_name = str(raw_name) if not isinstance(raw_name, list) else str(raw_name[0])

    data = {
        "name": symbol_name,
        "description": "",
        "keywords": "",
        "reference": "",
        "datasheet": "",
        "extends": ""
    }

    # 遍历子元素寻找 property 和 extends
    for item in symbol_list[2:]:
        if isinstance(item, list) and len(item) > 1:
            tag = item[0]
            tag_str = str(tag) if hasattr(tag, 'value') else str(tag)
            
            if tag_str == "property":
                if len(item) >= 3:
                    key = item[1]
                    val = item[2]
                    if hasattr(val, 'value'): val = val.value
                    elif isinstance(val, list): val = " ".join([str(x) for x in val])
                    
                    if key == "Description":
                        data["description"] = val
                    elif key == "ki_keywords":
                        data["keywords"] = val
                    elif key == "Reference":
                        data["reference"] = val
                    elif key == "Datasheet":
                        data["datasheet"] = val
            
            elif tag_str == "extends":
                if len(item) >= 2:
                    data["extends"] = str(item[1])

    # 过滤无效数据 (如果是图形单元且没有别名，通常忽略)
    if not data["description"] and not data["keywords"] and not data["extends"]:
        return None

    return data

def process_file(filepath, output_dir):
    filename = os.path.basename(filepath)
    lib_name = os.path.splitext(filename)[0]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # 解析 S-Expression
        parsed = sexpdata.loads(content, nil=None, true=True, false=False)
    except Exception as e:
        print(f"Skipping {filename}: {e}")
        return

    if not isinstance(parsed, list) or len(parsed) == 0:
        return

    # 校验是否为符号库
    top_tag = parsed[0]
    top_tag_str = str(top_tag) if hasattr(top_tag, 'value') else str(top_tag)
    if top_tag_str != "kicad_symbol_lib":
        return

    symbols_data = []
    for item in parsed:
        if isinstance(item, list) and len(item) > 0:
            tag = item[0]
            tag_str = str(tag) if hasattr(tag, 'value') else str(tag)
            if tag_str == "symbol":
                info = extract_symbol_info(item)
                if info:
                    symbols_data.append(info)

    if not symbols_data:
        return

    # 生成 Markdown
    lines = [f"# Library: {lib_name}", f"\nSource file: `{filename}`\n"]
    
    for sym in symbols_data:
        lines.append(f"## {sym['name']}")
        if sym['extends']:
            lines.append(f"- **Alias of**: {sym['extends']}")
        if sym['reference']:
            lines.append(f"- **Reference**: `{sym['reference']}`")
        if sym['description']:
            lines.append(f"- **Description**: {sym['description']}")
        if sym['keywords']:
            lines.append(f"- **Keywords**: {sym['keywords']}")
        if sym['datasheet'] and sym['datasheet'] != "~":
            lines.append(f"- **Datasheet**: {sym['datasheet']}")
        lines.append("")

    out_file = os.path.join(output_dir, f"{lib_name}.md")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Generated: {lib_name}.md")

def main():
    # 1. Clone KiCad 库
    if os.path.exists(SOURCE_DIR):
        print(f"Cleaning old source dir: {SOURCE_DIR}")
        shutil.rmtree(SOURCE_DIR)
    
    print(f"Cloning {REPO_URL}...")
    subprocess.run(["git", "clone", "--depth=1", REPO_URL, SOURCE_DIR], check=True)

    # 2. 准备输出目录
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # 3. 处理文件
    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".kicad_sym")]
    files.sort()
    
    print(f"Found {len(files)} symbol files. Processing...")
    for f in files:
        process_file(os.path.join(SOURCE_DIR, f), OUTPUT_DIR)

    print(f"\nAll done. Docs generated in '{OUTPUT_DIR}/'")

if __name__ == "__main__":
    main()