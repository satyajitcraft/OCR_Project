#!/usr/bin/env python3
"""
Local runner script for AI OCR Engine
This script helps set up and run the application locally
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version: {sys.version.split()[0]}")

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def check_tesseract():
    """Check if Tesseract is installed"""
    try:
        result = subprocess.run(["tesseract", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tesseract OCR is installed")
            return True
        else:
            print("⚠️  Tesseract OCR not found")
            return False
    except FileNotFoundError:
        print("⚠️  Tesseract OCR not found")
        return False

def install_tesseract_instructions():
    """Provide Tesseract installation instructions"""
    system = platform.system()
    print("\n📋 Tesseract Installation Instructions:")
    
    if system == "Windows":
        print("Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("Or use: winget install UB-Mannheim.TesseractOCR")
    elif system == "Darwin":  # macOS
        print("macOS: brew install tesseract")
    elif system == "Linux":
        print("Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("CentOS/RHEL: sudo yum install tesseract")
    
    print("\nAfter installation, restart this script.")

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting AI OCR Engine...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main function"""
    print("🔍 AI OCR Engine - Setup and Run")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Check Tesseract
    tesseract_available = check_tesseract()
    if not tesseract_available:
        install_tesseract_instructions()
        response = input("\nContinue without Tesseract? (EasyOCR will still work) [y/N]: ")
        if response.lower() != 'y':
            sys.exit(0)
    
    print("\n" + "=" * 40)
    print("🎉 Setup complete! Starting application...")
    print("=" * 40)
    
    # Run application
    run_streamlit()

if __name__ == "__main__":
    main()