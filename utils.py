import re
import cv2
import numpy as np
from PIL import Image
from typing import List, Dict, Any, Tuple
import base64
import io

def preprocess_image_advanced(image: np.ndarray) -> np.ndarray:
    """Advanced image preprocessing for better OCR results"""
    
    # Convert to grayscale if not already
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # Noise reduction
    denoised = cv2.medianBlur(gray, 3)
    
    # Contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)
    
    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Morphological operations to clean up
    kernel = np.ones((1,1), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    return cleaned

def extract_email_addresses(text: str) -> List[str]:
    """Extract all email addresses from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)

def extract_phone_numbers(text: str) -> List[str]:
    """Extract phone numbers from text"""
    patterns = [
        r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
        r'\+\d{1,3}\s?\d{10}',  # International format
        r'\d{10}',  # Simple 10-digit
    ]
    
    phone_numbers = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        phone_numbers.extend(matches)
    
    return list(set(phone_numbers))  # Remove duplicates

def extract_dates(text: str) -> List[str]:
    """Extract dates from text"""
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',  # DD/MM/YYYY or MM/DD/YYYY
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',  # YYYY/MM/DD
        r'\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b',  # DD Mon YYYY
    ]
    
    dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        dates.extend(matches)
    
    return dates

def clean_text(text: str) -> str:
    """Clean and normalize extracted text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s@.-]', ' ', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def confidence_score_to_color(confidence: float) -> str:
    """Convert confidence score to color for visualization"""
    if confidence >= 0.8:
        return "green"
    elif confidence >= 0.6:
        return "orange"
    else:
        return "red"

def image_to_base64(image: Image.Image) -> str:
    """Convert PIL image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def validate_aadhar_number(aadhar: str) -> bool:
    """Validate Aadhar number format"""
    # Remove spaces and check if it's 12 digits
    aadhar_clean = re.sub(r'\s+', '', aadhar)
    return len(aadhar_clean) == 12 and aadhar_clean.isdigit()

def extract_skills_from_text(text: str, skill_keywords: List[str]) -> List[str]:
    """Extract skills from text based on predefined keywords"""
    text_lower = text.lower()
    found_skills = []
    
    for skill in skill_keywords:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))  # Remove duplicates

def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts (simple Jaccard similarity)"""
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    if len(union) == 0:
        return 0.0
    
    return len(intersection) / len(union)

def format_extraction_results(results: List[Tuple], min_confidence: float = 0.5) -> Dict[str, Any]:
    """Format OCR results with filtering"""
    formatted_results = {
        'high_confidence': [],
        'medium_confidence': [],
        'low_confidence': [],
        'all_text': '',
        'average_confidence': 0.0
    }
    
    total_confidence = 0
    valid_results = []
    
    for result in results:
        coordinates, text, confidence = result
        
        if confidence >= min_confidence:
            valid_results.append(result)
            total_confidence += confidence
            
            if confidence >= 0.8:
                formatted_results['high_confidence'].append({
                    'text': text,
                    'confidence': confidence,
                    'coordinates': coordinates
                })
            elif confidence >= 0.6:
                formatted_results['medium_confidence'].append({
                    'text': text,
                    'confidence': confidence,
                    'coordinates': coordinates
                })
            else:
                formatted_results['low_confidence'].append({
                    'text': text,
                    'confidence': confidence,
                    'coordinates': coordinates
                })
    
    if valid_results:
        formatted_results['all_text'] = ' '.join([r[1] for r in valid_results])
        formatted_results['average_confidence'] = total_confidence / len(valid_results)
    
    return formatted_results