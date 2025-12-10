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

# ================= README Content =================
README_CONTENT = """# KiCad Official Component Library Documentation (Markdown Version)

## Introduction
This repository contains automatically generated component documentation converted from the [KiCad Official Symbols Library](https://gitlab.com/kicad/libraries/kicad-symbols). These documents are cleaned and formatted, optimized for AI context retrieval (Context7), and designed to assist with electronic design, component selection, and schematic drawing.

## Directory Structure
- Each `.md` file corresponds to a KiCad symbol library file (e.g., `Device.md` corresponds to the general discrete component library).
- The filename is the library name (Library Name).

## Data Format Description
Each component in the documentation contains the following key attributes:

*   **Level 1 Heading (Library)**: Library name.
*   **Level 2 Heading (Symbol Name)**: The unique name of the component in the library.
*   **Reference (Designator)**: The default reference prefix in schematics (e.g., `R` for resistors, `U` for ICs).
*   **Description**: A brief description of the component's function.
*   **Keywords**: Tags used to search for the component.
*   **Datasheet**: Link to the official datasheet.
*   **Alias of**: Indicates that the component is a variant of another base component.
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