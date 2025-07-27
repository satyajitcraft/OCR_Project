#!/usr/bin/env python3
"""
Check if all required modules are installed
"""

import sys

# List of required modules from requirements.txt
required_modules = [
    'streamlit',
    'cv2',  # opencv-python
    'pytesseract',
    'PIL',  # Pillow
    'transformers',
    'torch',
    'pdf2image',
    'numpy',
    'pandas',
    'easyocr'
]

def check_module(module_name):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        return True, "✅ Installed"
    except ImportError as e:
        return False, f"❌ Not installed: {str(e)}"

def main():
    print("🔍 Checking Required Modules Installation")
    print("=" * 50)
    
    all_installed = True
    
    for module in required_modules:
        installed, status = check_module(module)
        print(f"{module:<15} : {status}")
        if not installed:
            all_installed = False
    
    print("=" * 50)
    
    if all_installed:
        print("🎉 All modules are installed successfully!")
        print("You can now run: python3 run_local.py")
    else:
        print("⚠️  Some modules are missing. Please install them:")
        print("python3 -m pip install -r requirements.txt")
    
    # Additional system checks
    print("\n🔧 System Dependencies:")
    
    # Check Tesseract
    import subprocess
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"Tesseract OCR: ✅ {version}")
        else:
            print("Tesseract OCR: ❌ Not found")
    except FileNotFoundError:
        print("Tesseract OCR: ❌ Not installed (run: brew install tesseract)")
    
    print(f"\nPython Version: {sys.version}")

if __name__ == "__main__":
    main()