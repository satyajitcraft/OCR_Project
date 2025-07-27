import os

# OCR Configuration
TESSERACT_CONFIG = {
    'lang': 'eng',
    'config': '--oem 3 --psm 6'
}

EASYOCR_CONFIG = {
    'languages': ['en'],
    'gpu': False,  # Set to True if you have CUDA-capable GPU
    'width_ths': 0.7,
    'height_ths': 0.7
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    'max_upload_size': 200,  # MB
    'theme': {
        'primaryColor': '#FF6B6B',
        'backgroundColor': '#FFFFFF',
        'secondaryBackgroundColor': '#F0F2F6',
        'textColor': '#262730'
    }
}

# Document Processing Configuration
DOCUMENT_TYPES = {
    'resume': {
        'skills_keywords': [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'node.js', 'express', 'django', 'flask', 'fastapi',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'git', 'github', 'gitlab', 'jenkins', 'ci/cd',
            'html', 'css', 'sass', 'bootstrap', 'tailwind',
            'machine learning', 'deep learning', 'ai', 'ml',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas',
            'numpy', 'matplotlib', 'data science', 'analytics'
        ]
    },
    'aadhar': {
        'number_pattern': r'\b\d{4}\s?\d{4}\s?\d{4}\b',
        'dob_patterns': [
            r'\b\d{2}[/-]\d{2}[/-]\d{4}\b',
            r'\b\d{2}[/-]\d{2}[/-]\d{2}\b'
        ]
    }
}

# File paths (if needed)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
TEMP_FOLDER = 'temp'

# Create directories if they don't exist
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER]:
    os.makedirs(folder, exist_ok=True)