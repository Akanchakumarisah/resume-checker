import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from utils.file_handler import extract_text_from_file

# Download NLTK data (only needed once)
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

def analyze_resume(resume_path, job_description):
    # Extract text from resume
    resume_text = extract_text_from_file(resume_path)
    
    # Preprocess both texts
    processed_resume = preprocess_text(resume_text)
    processed_jd = preprocess_text(job_description)
    
    # Simple keyword matching (count based)
    resume_words = set(processed_resume.split())
    jd_words = set(processed_jd.split())
    
    # Calculate matching score
    matching_words = resume_words.intersection(jd_words)
    score = min(100, len(matching_words) * 5)  # Simple scoring (5 points per match)
    if score > 100:
        score = 100
    
    # Get important keywords from JD missing in resume
    missing_keywords = list(jd_words - resume_words)  # Convert to list immediately
    
    # Get sections from resume
    sections = identify_sections(resume_text)
    
    return {
        'score': score,
        'missing_keywords': missing_keywords[:10],  # Now slicing a list
        'sections': sections,
        'feedback': generate_feedback(score, missing_keywords, sections)
    }

def identify_sections(resume_text):
    sections = {}
    common_sections = ['experience', 'education', 'skills', 'projects', 'certifications']
    
    for section in common_sections:
        # Look for section headers (case insensitive)
        pattern = re.compile(fr'\n\s*{section}\s*[\n:]', re.IGNORECASE)
        match = pattern.search(resume_text)
        if match:
            sections[section] = True
    
    return sections

def generate_feedback(score, missing_keywords, sections):
    feedback = []
    
    # Score feedback
    if score >= 80:
        feedback.append("Excellent! Your resume is highly relevant to the job description.")
    elif score >= 60:
        feedback.append("Good match. Your resume is relevant but could be improved.")
    else:
        feedback.append("Your resume needs significant improvement to match the job requirements.")
    
    # Missing keywords feedback
    if missing_keywords:
        # missing_keywords is now guaranteed to be a list
        feedback.append(f"Consider adding these keywords: {', '.join(missing_keywords[:5])}")
    else:
        feedback.append("Great job! Your resume includes all important keywords from the job description.")
    
    # Sections feedback
    if not sections.get('skills', False):
        feedback.append("Consider adding a dedicated Skills section.")
    if not sections.get('experience', False):
        feedback.append("Make sure to highlight your work experience clearly.")
    if not sections.get('education', False):
        feedback.append("Include your education background if relevant.")
    
    return feedback