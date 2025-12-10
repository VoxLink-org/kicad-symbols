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
REPO_URL = "https://gitlab.com/kicad/libraries/kicad-symbols.git"
SOURCE_DIR = "temp_kicad_source"
OUTPUT_DIR = "docs_output"

# ================= README 内容 =================
README_CONTENT = """# KiCad 官方元器件库文档 (Markdown版)

## 简介
本仓库包含了从 [KiCad Official Symbols Library](https://gitlab.com/kicad/libraries/kicad-symbols) 自动转换生成的元器件文档。这些文档经过清洗和格式化，专为 AI 上下文检索 (Context7) 优化，用于辅助电子设计、元器件选型和原理图绘制。

## 目录结构
- 每个 `.md` 文件对应一个 KiCad 符号库文件 (例如 `Device.md` 对应通用分立元器件库)。
- 文件名即为库名称 (Library Name)。

## 数据格式说明
文档中的每个元器件包含以下关键属性：

*   **一级标题 (Library)**: 库名称。
*   **二级标题 (Symbol Name)**: 元器件在库中的唯一名称。
*   **Reference (位号)**: 原理图中默认的位号前缀 (例如 `R` 代表电阻, `U` 代表芯片)。
*   **Description (描述)**: 元器件的功能简述。
*   **Keywords (关键词)**: 用于搜索该元器件的标签。
*   **Datasheet (数据手册)**: 官方数据手册链接。
*   **Alias of (别名)**: 表示该元器件是另一个基础元器件的变体。
"""

def extract_symbol_info(symbol_list):
    if not isinstance(symbol_list, list) or len(symbol_list) < 2:
        return None

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

    if not data["description"] and not data["keywords"] and not data["extends"]:
        return None

    return data

def process_file(filepath, output_dir):
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

def create_readme(output_dir):
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(README_CONTENT)
    print("Generated: README.md")

def main():
    if os.path.exists(SOURCE_DIR):
        print(f"Cleaning old source dir: {SOURCE_DIR}")
        shutil.rmtree(SOURCE_DIR)
    
    print(f"Cloning {REPO_URL}...")
    subprocess.run(["git", "clone", "--depth=1", REPO_URL, SOURCE_DIR], check=True)

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".kicad_sym")]
    files.sort()
    
    print(f"Found {len(files)} symbol files. Processing...")
    for f in files:
        process_file(os.path.join(SOURCE_DIR, f), OUTPUT_DIR)

    # 关键修改：生成 README
    create_readme(OUTPUT_DIR)

    print(f"\nAll done. Docs generated in '{OUTPUT_DIR}/'")

if __name__ == "__main__":
    main()