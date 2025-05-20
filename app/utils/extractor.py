
import re
import fitz  
from docx import Document


SKILL_GROUPS = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Swift",
        "Go", "Rust", "Kotlin", "TypeScript", "SQL", "HTML", "CSS",
        "PHP", "Shell", "Bash", "Perl", "R", "Scala", "Julia", "Haskell"
    ],
    "Frameworks & Libraries": [
        "React", "Angular", "Vue.js", "Django", "Flask", "Spring", "Express"
    ],
    "Cloud & DevOps Tools": [
        "AWS", "Azure", "Docker", "Kubernetes", "Jenkins",
        "Ansible", "Git", "JIRA", "Confluence"
    ],
    "Testing & QA": [
        "Unit Testing", "Integration Testing", "System Testing",
        "Acceptance Testing", "Regression Testing", "Performance Testing",
        "Security Testing", "Usability Testing"
    ],
    "Data & Machine Learning": [
        "Machine Learning", "Deep Learning", "Data Science",
        "Data Analysis", "Data Visualization"
    ],
    "Operating Systems": [
        "Linux", "Windows", "MacOS", "Unix"
    ],
    "Methodologies": [
        "Agile", "Scrum", "Kanban", "Waterfall", "Lean", "Six Sigma"
    ],
    "Computer Science Fundamentals": [
        "Data Structures", "Algorithms", "Computer Networks"
    ],
    "Soft Skills": [
        "Leadership", "Teamwork", "Communication", "Problem Solving"
    ],
    "Languages": [
      "English", "Hindi", "Spanish", "French", "German", "Chinese", "Japanese"
    ]
}


ALL_SKILLS = [skill for group in SKILL_GROUPS.values() for skill in group]

def extractTextFromPDF(file_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        raise RuntimeError(f"Error extracting text from PDF: {str(e)}")


def extractSkills(text: str) -> dict:
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    found_skills = {category: [] for category in SKILL_GROUPS}
    for category, skills in SKILL_GROUPS.items():
        for skill in skills:
            if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE):
                found_skills[category].append(skill)
    return found_skills



def extractTextFromDOCX(file_bytes: bytes) -> str:
    try:
        # Save bytes to a temporary file since python-docx can't read from bytes directly
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        doc = Document(tmp_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        raise RuntimeError(f"Error extracting text from DOCX: {str(e)}")

def extractTextFromTXT(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        raise RuntimeError(f"Error extracting text from TXT: {str(e)}")



def extractTextAndSkills(filename: str, content: bytes) -> dict:
    filename = filename.lower()

    if filename.endswith('.pdf'):
        text = extractTextFromPDF(content)
    elif filename.endswith('.docx'):
        text = extractTextFromDOCX(content)
    elif filename.endswith('.txt'):
        text = extractTextFromTXT(content)
    else:
        raise ValueError("Unsupported file format. Only PDF, DOCX, and TXT are allowed.")

    grouped_skills = extractSkills(text)
  

 
    grouped_skills = {k: v for k, v in grouped_skills.items() if v}
    return grouped_skills
