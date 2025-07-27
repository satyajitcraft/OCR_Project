# AI OCR Engine with Streamlit

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

## Supported Document Types

### Resume
- Extracts: Name, Email, Phone, Skills
- Recognizes common programming languages and technologies
- Structured output for HR systems

### Aadhar Card
- Extracts: Name, Aadhar Number, Date of Birth, Gender
- Validates Aadhar number format
- Handles various Aadhar card layouts

### Handwritten Notes
- Extracts: Full text content
- Identifies bullet points and numbered lists
- Provides document statistics

## Technical Details

- **Frontend**: Streamlit
- **OCR Engines**: EasyOCR, Tesseract
- **Image Processing**: OpenCV, PIL
- **Text Processing**: Regular expressions, NLP techniques
- **File Support**: PNG, JPG, JPEG, PDF

## Configuration

The application uses adaptive thresholding and noise reduction for better OCR accuracy. You can modify the preprocessing parameters in the `OCREngine.preprocess_image()` method.

## Limitations

- OCR accuracy depends on image quality
- Handwritten text recognition may vary
- Structured parsing uses heuristic approaches
- Languages: Currently optimized for English

## Future Enhancements

- Multi-language support
- Machine learning-based document classification
- Advanced NLP for better information extraction
- Integration with cloud OCR services
- Batch processing capabilities