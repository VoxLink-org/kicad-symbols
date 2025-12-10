# gen_kicad_docs.py
import os
import shutil
import sys
import subprocess
import json  # 新增 json 库用于生成标准格式

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

# ================= 新版 README (包含代码块以骗过索引器) =================
README_CONTENT = """# KiCad Components Index

This documentation contains KiCad symbol definitions formatted as JSON objects for Context7 indexing.

## Data Structure Example

Each component is represented by a JSON block like this:

```json
{
  "symbol_name": "Device_Name",
  "type": "component",
  "properties": {
    "reference": "U",
    "description": "Component description text",
    "keywords": "search tags",
    "datasheet": "http://example.com/sheet.pdf"
  }
}
```

## Usage
Context7 should treat these JSON blocks as code snippets. When querying, look for the `description` and `keywords` fields inside the JSON structure.
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

    # 至少要有点内容才提取
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

    # === 生成 Markdown (专门针对 Context7 优化) ===
    lines = [f"# Library: {lib_name}", ""]
    
    for sym in symbols_data:
        lines.append(f"## {sym['name']}")
        lines.append("Definition:")
        
        # 构造一个干净的字典对象
        component_obj = {
            "symbol": sym['name'],
            "library": lib_name,
            "ref_prefix": sym['reference'],
            "description": sym['description'],
            "keywords": sym['keywords'],
            "datasheet": sym['datasheet']
        }
        
        if sym['extends']:
            component_obj["alias_of"] = sym['extends']
            
        # 关键点：使用 json.dumps 生成标准的 JSON 格式
        # 并放入 ```json 代码块中，强迫 Context7 索引它
        json_str = json.dumps(component_obj, indent=2, ensure_ascii=False)
        
        lines.append("```json")
        lines.append(json_str)
        lines.append("```")
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

    create_readme(OUTPUT_DIR)

    print(f"\nAll done. JSON-formatted docs generated in '{OUTPUT_DIR}/'")

if __name__ == "__main__":
    main()
