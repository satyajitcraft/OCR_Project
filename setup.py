from setuptools import setup, find_packages

setup(
    name="ai-ocr-engine",
    version="1.0.0",
    description="AI-powered OCR engine for document processing",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.1",
        "opencv-python>=4.8.1",
        "pytesseract>=0.3.10",
        "Pillow>=10.0.1",
        "transformers>=4.35.0",
        "torch>=2.1.0",
        "pdf2image>=1.16.3",
        "numpy>=1.24.3",
        "pandas>=1.5.3",
        "easyocr>=1.7.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)