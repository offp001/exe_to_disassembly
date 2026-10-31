<h1 align="center">
  Windows executable (.exe) to Disassembly (Linux)
</h1>

<h3 align="center">PyInstaller Exe (3.14 and 3.15) to Disassembly</h3>

<p align="center">Extract and convert Windows executable (.exe) binaries created with PyInstaller into readable Python bytecode disassembly output.</p>

<p align="center">
  <img src="https://img.shields.io/github/license/offp001/exe_to_disassembly" alt="exe_to_disassembly license">
</p>

---

## Overview

**exe_to_disassembly** automates the process of extracting contents from PyInstaller-compiled `.exe` files and disassembling the raw bytecode into readable `.pyasm` and structured text format. 

---

## FAQ

**Why this wont convert it to actually .py file?** Beacuse this is for Python 3.14 and 3.15, its hard to decompile 3.14 and 3.15.

---

## Usage

### 1. Downloading
Download the repo or clone it using `git clone https://github.com/offp001/exe_to_disassembly.git`

### 2. File Placement
Place your target `.exe` file in the same directory as `decompile.py`.

### 3. Execution
Run the script using your Python environment:

```bash
python3 decompile.py
```

### 4. User Input
When prompted, enter the file name **without** its `.exe` extension:

```text
enter exe name (without extension): target_app
```

---

## Output Structure

Once the conversion completes, an extraction folder named `<target_name>.exe_extracted` will be generated with the following layout:

```text
<target_name>.exe_extracted/
├── all_functions_disasm.txt    # Consolidated master report containing all disassembled blocks
├── script_name.pyasm           # Disassembled Python bytecode per module
└── ...                         # Extracted assets and support binaries
```

### Output File Details

* **`all_functions_disasm.txt`**: Serves as the primary reference document during analysis. Every function is separated by a clear header detailing the original file name, function name, and starting line number:
  ```text
  source: file.pyc
  ------------------------------------------------------
  # Disassembly code appears here
  ```
* **`.pyasm` Files**: Contain full disassemblies of individual compiled Python modules for targeted inspection.

---

<p align="center">
  <sub>by offp001</sub>
</p>
