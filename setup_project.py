#!/usr/bin/env python3
"""
Setup script to create the AI OCR Engine project structure
Run this script in an empty directory to set up the project
"""

import os

# File contents dictionary
files = {
    "requirements.txt": """streamlit==1.28.1
opencv-python==4.8.1.78
pytesseract==0.3.10
Pillow==10.0.1
transformers==4.35.0
torch==2.1.0
pdf2image==1.16.3
numpy==1.24.3
pandas==1.5.3
easyocr==1.7.0""",

    "README.md": """# AI OCR Engine with Streamlit

A powerful web application that performs Optical Character Recognition (OCR) on various document types including resumes, Aadhar cards, and handwritten notes.

## Features

- **Multi-Document Support**: Resume, Aadhar Card, Handwritten Notes
- **Dual OCR Engines**: EasyOCR and Tesseract OCR
- **Structured Data Extraction**: Parses documents into structured format
- **PDF Support**: Process multi-page PDF documents
- **Download Options**: Export results as text or JSON
- **Confidence Scoring**: View OCR confidence levels
- **Responsive UI**: Clean, modern interface

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR on your system:
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

## Usage

Run the application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Quick Start

```bash
# Run the setup script
python run_local.py
```

This will automatically install dependencies and start the application.
""",

    ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/

# Uploads and temp files
uploads/
outputs/
temp/
*.tmp
"""
}

def create_project_structure():
    """Create the project directory structure and files"""
    
    print("🚀 Setting up AI OCR Engine project...")
    
    # Create directories
    directories = ["uploads", "outputs", "temp"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Create files
    for filename, content in files.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Created file: {filename}")
    
    print("\n✅ Project structure created successfully!")
    print("\n📋 Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Install Tesseract OCR (see README.md for instructions)")
    print("3. Run the application: python run_local.py")
    print("\n🎉 Happy coding!")

if __name__ == "__main__":
    create_project_structure()