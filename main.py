import PyPDF2
import os
import re

# Keywords for different job roles
job_keywords = {
    'AI & ML Engineer': [
        'artificial intelligence', 'machine learning', 'deep learning',
        'nlp', 'opencv', 'computer vision', 'tensorflow',
        'pytorch', 'keras', 'reinforcement learning'
    ],
    'Data Scientist': [
        'python', 'machine learning', 'pandas', 'numpy',
        'tensorflow', 'keras', 'scikit-learn', 'data analysis'
    ],
    'Web Developer': [
        'html', 'css', 'javascript', 'angular', 'react',
        'node', 'bootstrap', 'jquery'
    ],
    'Full Stack Developer': [
        'html', 'css', 'javascript', 'node', 'express',
        'mongodb', 'react', 'angular', 'mysql', 'php', 'django'
    ],
    'MERN Stack Developer': [
        'mern', 'mongodb', 'express', 'react', 'node.js', 'javascript'
    ],
    'Java Developer': [
        'java', 'spring', 'hibernate', 'j2ee', 'servlet'
    ],
    'Mobile Developer': [
        'android', 'kotlin', 'swift', 'flutter',
        'react native', 'ios development', 'ruby'
    ],
    'Database Administrator': [
        'mysql', 'oracle', 'sql server', 'mongodb',
        'database management', 'query optimization', 'nosql', 'postgresql'
    ],
    'Cyber Security': [
        'malware analysis', 'penetration testing',
        'vulnerability scanning', 'firewall', 'encryption',
        'ids', 'ips', 'siem', 'risk assessment'
    ],
}


def text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    if not os.path.exists(pdf_path):
        return ""

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        return ''.join(page.extract_text() or '' for page in reader.pages).lower()


def categorize_resume(text):
    """Categorize resume based on keyword matches."""
    for role, keywords in job_keywords.items():
        match_count = sum(
            1 for keyword in keywords if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE))

        if match_count >= 10:
            return role, match_count, 100  # 100% match

        if match_count > 0:
            percent_match = (match_count / len(keywords)) * 100
            return role, match_count, percent_match  # Return role and percentage for partial matches

    return "Unknown Role", 0, 0  # No match found


def process_resumes(folder_path):
    """Process PDF resumes in a folder."""
    categorized_resumes = {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            resume_text = text_from_pdf(pdf_path)
            role, match_count, percent_match = categorize_resume(resume_text)
            categorized_resumes[file_name] = (role, match_count, percent_match)

    return categorized_resumes


def display_results(results):
    """Display categorized resume results."""
    for resume, (role, match_count, percent_match) in results.items():
        if percent_match > 0:
            print(f"Resume: {resume} - Job Role: {role} - Matched Keywords: {match_count} ({percent_match:.2f}%)")
        else:
            print(f"Resume: {resume} - Job Role: Unknown Role - No keywords matched")


# Main execution
folder_path = r'C:\Users\HP\CodeVidhya\Python_Programming\Internship\BootCoding\Task_1\Resume'
results = process_resumes(folder_path)
display_results(results)