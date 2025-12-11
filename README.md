# KiCad Components Index

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
