import fitz
import docx
import re
import json
import os

# -------------------------------
# FILE EXTRACTION
# -------------------------------
def extract_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text


def extract_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


# -------------------------------
# CLEAN TEXT
# -------------------------------
def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    return text.strip()


# -------------------------------
# EMAIL
# -------------------------------
def extract_email(text):
    match = re.findall(r'\S+@\S+', text)
    return match[0] if match else None


# -------------------------------
# PHONE
# -------------------------------
def extract_phone(text):
    match = re.findall(r'\b\d{10}\b', text)
    return match[0] if match else None


# -------------------------------
# NAME (BALANCED LOGIC)
# -------------------------------
def extract_name(text):
    lines = text.split("\n")

    for line in lines[:10]:
        line = line.strip()

        # skip unwanted
        if any(word in line.lower() for word in ["email", "phone", "address"]):
            continue

        # skip numbers
        if any(char.isdigit() for char in line):
            continue

        words = line.split()

        # good name condition
        if 2 <= len(words) <= 3 and len(line) < 30:
            return line

    return None


# -------------------------------
# SKILLS
# -------------------------------
def extract_skills(text):
    try:
        file_path = os.path.join(os.path.dirname(__file__), "skills.json")
        with open(file_path) as f:
            skills_db = json.load(f)
    except:
        return []

    text = text.lower()
    found = []

    for skill in skills_db:
        if skill.lower() in text:
            found.append(skill)

    return list(set(found))


# -------------------------------
# EDUCATION
# -------------------------------
def extract_education(text):
    edu = []
    for line in text.split("\n"):
        if any(x in line.lower() for x in ["bachelor", "degree", "university", "college"]):
            edu.append(line.strip())
    return edu


# -------------------------------
# EXPERIENCE
# -------------------------------
def extract_experience(text):
    exp = []
    for line in text.split("\n"):
        if any(x in line.lower() for x in ["project", "developed", "built", "experience"]):
            exp.append(line.strip())
    return exp


# -------------------------------
# LINKEDIN
# -------------------------------
def extract_linkedin(text):
    match = re.findall(r'linkedin\.com/in/\S+', text)
    return match[0] if match else None


# -------------------------------
# GITHUB
# -------------------------------
def extract_github(text):
    match = re.findall(r'github\.com/\S+', text)
    return match[0] if match else None


# -------------------------------
# MAIN CLASS
# -------------------------------
class ResumeParser:

    def parse_file(self, file_path):

        if file_path.endswith(".pdf"):
            text = extract_pdf(file_path)
        elif file_path.endswith(".docx"):
            text = extract_docx(file_path)
        else:
            return {"error": "Unsupported file format"}

        text = clean_text(text)

        data = {
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "linkedin": extract_linkedin(text),
            "github": extract_github(text),
            "skills": extract_skills(text),
            "education": extract_education(text),
            "experience": extract_experience(text)
        }

        return data


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    parser = ResumeParser()

    result = parser.parse_file(r"C:\Users\srava\OneDrive\Desktop\sample_resume.pdf")

    print(result)