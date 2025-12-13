# KiCad Official Component Library Documentation (Markdown Version)

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

## Generation Method
The documentation is automatically generated through the [`gen_kicad_docs.py`](scripts/gen_kicad_docs.py) script, which:
- Clones source code from the KiCad official symbol library
- Parses `.kicad_sym` file format
- Extracts component information and converts it to Markdown format
- Generates easy-to-read and searchable documentation

## Use Cases
- AI-assisted electronic design
- Quick component search and retrieval
- Schematic drawing reference
- Electronic design automation tool integration
- Use https://mcp-link.vercel.app/connect-api to forward API to MCP for LLM
