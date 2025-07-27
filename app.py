import streamlit as st
import cv2
import pytesseract
from PIL import Image
import numpy as np
import pandas as pd
import re
import io
import base64
from typing import Dict, List, Any
import easyocr
from pdf2image import convert_from_bytes

# Configure Streamlit page
st.set_page_config(
    page_title="AI OCR Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

class OCREngine:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for better OCR results"""
        # Convert PIL image to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        
        # Apply noise reduction
        denoised = cv2.medianBlur(gray, 5)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return thresh
    
    def extract_text_tesseract(self, image: Image.Image) -> str:
        """Extract text using Tesseract OCR"""
        processed_image = self.preprocess_image(image)
        text = pytesseract.image_to_string(processed_image, lang='eng')
        return text
    
    def extract_text_easyocr(self, image: Image.Image) -> List[tuple]:
        """Extract text using EasyOCR"""
        image_array = np.array(image)
        results = self.reader.readtext(image_array)
        return results
    
    def parse_resume(self, text: str) -> Dict[str, Any]:
        """Parse resume text and extract structured information"""
        resume_data = {
            'name': '',
            'email': '',
            'phone': '',
            'skills': [],
            'experience': [],
            'education': []
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            resume_data['email'] = emails[0]
        
        # Extract phone number
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            resume_data['phone'] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
        
        # Extract name (assuming it's in the first few lines)
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if line and len(line.split()) <= 4 and not any(char.isdigit() for char in line):
                if '@' not in line and len(line) > 3:
                    resume_data['name'] = line
                    break
        
        # Extract skills (looking for common skill-related keywords)
        skill_keywords = ['python', 'java', 'javascript', 'react', 'angular', 'node.js', 
                         'sql', 'mongodb', 'aws', 'docker', 'kubernetes', 'git', 'html', 
                         'css', 'machine learning', 'data science', 'tensorflow', 'pytorch']
        
        text_lower = text.lower()
        found_skills = [skill for skill in skill_keywords if skill in text_lower]
        resume_data['skills'] = found_skills
        
        return resume_data
    
    def parse_aadhar(self, text: str) -> Dict[str, Any]:
        """Parse Aadhar card text and extract structured information"""
        aadhar_data = {
            'name': '',
            'aadhar_number': '',
            'dob': '',
            'gender': '',
            'address': ''
        }
        
        # Extract Aadhar number (12 digits)
        aadhar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
        aadhar_matches = re.findall(aadhar_pattern, text)
        if aadhar_matches:
            aadhar_data['aadhar_number'] = aadhar_matches[0].replace(' ', '')
        
        # Extract DOB pattern
        dob_pattern = r'\b\d{2}[/-]\d{2}[/-]\d{4}\b'
        dob_matches = re.findall(dob_pattern, text)
        if dob_matches:
            aadhar_data['dob'] = dob_matches[0]
        
        # Extract gender
        if 'male' in text.lower() and 'female' not in text.lower():
            aadhar_data['gender'] = 'Male'
        elif 'female' in text.lower():
            aadhar_data['gender'] = 'Female'
        
        # Extract name (heuristic approach)
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line.split()) <= 4 and not any(char.isdigit() for char in line):
                if 'government' not in line.lower() and 'india' not in line.lower():
                    aadhar_data['name'] = line
                    break
        
        return aadhar_data
    
    def parse_handwritten_notes(self, text: str) -> Dict[str, Any]:
        """Parse handwritten notes and provide basic structure"""
        notes_data = {
            'content': text,
            'word_count': len(text.split()),
            'line_count': len(text.split('\n')),
            'key_points': []
        }
        
        # Extract potential key points (lines starting with bullet points or numbers)
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('•', '-', '*')) or (line and line[0].isdigit() and '.' in line[:3]):
                notes_data['key_points'].append(line)
        
        return notes_data

def main():
    st.title("🔍 AI OCR Engine")
    st.markdown("### Advanced Optical Character Recognition with AI")
    
    # Initialize OCR engine
    if 'ocr_engine' not in st.session_state:
        st.session_state.ocr_engine = OCREngine()
    
    # Sidebar for options
    st.sidebar.title("📋 Options")
    document_type = st.sidebar.selectbox(
        "Select Document Type",
        ["Resume", "Aadhar Card", "Handwritten Notes", "General Text"]
    )
    
    ocr_method = st.sidebar.selectbox(
        "Select OCR Method",
        ["EasyOCR (Recommended)", "Tesseract OCR"]
    )
    
    # File upload
    st.subheader("📤 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'pdf'],
        help="Upload images in PNG, JPG, JPEG format or PDF files"
    )
    
    if uploaded_file is not None:
        try:
            # Handle PDF files
            if uploaded_file.type == "application/pdf":
                st.info("📄 PDF file detected. Converting to images...")
                pdf_images = convert_from_bytes(uploaded_file.getvalue())
                
                for i, image in enumerate(pdf_images):
                    st.subheader(f"Page {i+1}")
                    process_image(image, document_type, ocr_method, st.session_state.ocr_engine)
            else:
                # Handle image files
                image = Image.open(uploaded_file)
                process_image(image, document_type, ocr_method, st.session_state.ocr_engine)
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def process_image(image: Image.Image, document_type: str, ocr_method: str, ocr_engine: OCREngine):
    """Process a single image"""
    
    # Display image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Progress bar
    progress_bar = st.progress(0)
    progress_bar.progress(25)
    
    # Extract text
    st.subheader("🔍 Text Extraction")
    
    if ocr_method == "EasyOCR (Recommended)":
        results = ocr_engine.extract_text_easyocr(image)
        extracted_text = ' '.join([result[1] for result in results])
        
        # Display confidence scores
        st.subheader("📊 Detection Results")
        confidence_data = []
        for result in results:
            confidence_data.append({
                'Text': result[1],
                'Confidence': f"{result[2]:.2%}",
                'Coordinates': str(result[0])
            })
        
        if confidence_data:
            df = pd.DataFrame(confidence_data)
            st.dataframe(df)
    else:
        extracted_text = ocr_engine.extract_text_tesseract(image)
    
    progress_bar.progress(50)
    
    # Display raw text
    st.subheader("📝 Extracted Text")
    st.text_area("Raw Text", extracted_text, height=200)
    
    progress_bar.progress(75)
    
    # Parse based on document type
    st.subheader("📋 Structured Data")
    
    if document_type == "Resume":
        parsed_data = ocr_engine.parse_resume(extracted_text)
        display_resume_data(parsed_data)
    elif document_type == "Aadhar Card":
        parsed_data = ocr_engine.parse_aadhar(extracted_text)
        display_aadhar_data(parsed_data)
    elif document_type == "Handwritten Notes":
        parsed_data = ocr_engine.parse_handwritten_notes(extracted_text)
        display_notes_data(parsed_data)
    else:
        st.write("**General Text Extraction Complete**")
        st.info("Select a specific document type for structured parsing.")
    
    progress_bar.progress(100)
    
    # Download options
    st.subheader("💾 Download Options")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Download as Text"):
            st.download_button(
                label="Download Text File",
                data=extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("📊 Download as JSON") and document_type != "General Text":
            import json
            json_data = json.dumps(parsed_data, indent=2)
            st.download_button(
                label="Download JSON File",
                data=json_data,
                file_name="structured_data.json",
                mime="application/json"
            )

def display_resume_data(data: Dict[str, Any]):
    """Display parsed resume data"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Personal Information**")
        st.write(f"Name: {data['name']}")
        st.write(f"Email: {data['email']}")
        st.write(f"Phone: {data['phone']}")
    
    with col2:
        st.write("**Skills Found**")
        if data['skills']:
            for skill in data['skills']:
                st.write(f"• {skill.title()}")
        else:
            st.write("No specific skills detected")

def display_aadhar_data(data: Dict[str, Any]):
    """Display parsed Aadhar data"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Personal Details**")
        st.write(f"Name: {data['name']}")
        st.write(f"Date of Birth: {data['dob']}")
        st.write(f"Gender: {data['gender']}")
    
    with col2:
        st.write("**Document Information**")
        st.write(f"Aadhar Number: {data['aadhar_number']}")
        if data['aadhar_number']:
            st.success("✅ Aadhar number detected")
        else:
            st.warning("⚠️ Aadhar number not clearly detected")

def display_notes_data(data: Dict[str, Any]):
    """Display parsed handwritten notes data"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Document Statistics**")
        st.write(f"Word Count: {data['word_count']}")
        st.write(f"Line Count: {data['line_count']}")
    
    with col2:
        st.write("**Key Points Detected**")
        if data['key_points']:
            for point in data['key_points']:
                st.write(f"• {point}")
        else:
            st.write("No bullet points or numbered items detected")

if __name__ == "__main__":
    main()