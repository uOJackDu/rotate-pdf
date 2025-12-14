# rotate-pdf

A simple command-line tool to rotate all pages in a PDF file by 90, 180, or 270 degrees, either clockwise or counterclockwise.

Built with [`pypdf`](https://pypi.org/project/pypdf/) and managed with [`uv`](https://docs.astral.sh/uv/).

**Code is 100% written by AI!**

## Features

- Rotates every page in the PDF (relative rotation, preserves existing orientation)
- Normalizes rotation values to standard 0/90/180/270
- Safe: never overwrites the original file
- Default output: `<input>_out.pdf`
- Direction: `0` (counterclockwise, default) or `1` (clockwise)
- Fully tested with `pytest`

## Installation

Requires Python 3.12+ and `uv` (recommended).

1. Install `uv` if you don't have it:
   https://docs.astral.sh/uv/getting-started/installation/

2. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/rotate-pdf.git
   cd rotate-pdf
   ```
3. Install in editable mode
   ```bash
   uv sync          # Installs dependencies (pypdf and dev deps)
   uv pip install -e .   # Installs the console script
   ```

### Usage

Activate the environment (optional if using uv run):
```bash
source .venv/bin/activate   # macOS/Linux
# or .venv\Scripts\activate  # Windows
```

Run the tool (works from any directory after activation):
```bash
rotate-pdf input.pdf                     # 90° counterclockwise → input_out.pdf
rotate-pdf input.pdf --direction 1       # 90° clockwise → input_out.pdf
rotate-pdf input.pdf output.pdf --degrees 180 --direction 0
rotate-pdf input.pdf --degrees 270 --direction 1
```

With uv run (no activation needed, run from project root):
```bash
uv run rotate-pdf input.pdf
```

### Options
```
usage: rotate-pdf [-h] [--degrees {90,180,270}] [--direction {0,1}] input_path [output_path]

positional arguments:
  input_path            Path to the input PDF file
  output_path           Path to the output rotated PDF file (optional; defaults to input_path with '_out' suffix)

options:
  -h, --help            show this help message and exit
  --degrees {90,180,270}
                        Degrees to rotate (default: 90)
  --direction {0,1}     Direction: 0 for counterclockwise (default), 1 for clockwise
```

### Running Tests
```bash
uv run pytest -v
```
