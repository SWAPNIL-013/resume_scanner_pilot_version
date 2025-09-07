import fitz  # PyMuPDF
import docx  # python-docx
import re
import pdfplumber

# -----------------------------
# 📌 Resume Text Extraction
# -----------------------------
def extract_text(file_path: str, file_type: str) -> str:
    """
    Extract text from a resume file.
    Supports: PDF, DOCX, TXT
    """
    text = ""

    try:
        if file_type == "pdf":
            # ✅ Extract from PDF using PyMuPDF
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text("text")

        # if file_type == "pdf":
        #     text = ""
        #     with pdfplumber.open(file_path) as pdf:
        #         for page in pdf.pages:   # use .pages, not doc itself
        #             page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
        #             if page_text:
        #                 text += page_text + "\n"



        elif file_type == "docx":
            # ✅ Extract from DOCX using python-docx
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])

        elif file_type == "txt":
            # ✅ Extract from TXT
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    except Exception as e:
        print(f"⚠️ Error extracting text from {file_path}: {e}")

    return text.strip()


# -----------------------------
# 📌 Resume Rule-Based Parsing
# -----------------------------
# SKILL_SET = [
#     "Python", "Java", "C++", "SQL", "MySQL", "PostgreSQL",
#     "JavaScript", "React", "Angular", "Node.js", "HTML", "CSS",
#     "Django", "Flask", "FastAPI", "Spring Boot",
#     "Machine Learning", "Deep Learning", "Data Science",
#     "AWS", "Docker", "Kubernetes", "Git", "Linux"
# ]

# def parse_resume(text: str) -> dict:
#     """
#     Rule-based parsing of resume text.
#     Extracts: name, email, phone, skills.
#     """

#     # Email
#     email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
#     email = email_match.group(0) if email_match else ""

#     # Phone
#     phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\d{10}", text)
#     phone = phone_match.group(0) if phone_match else ""

#     # Name → first non-empty line that doesn’t look like "resume"
#     lines = text.splitlines()
#     name = ""
#     for line in lines:
#         line = line.strip()
#         if line and not any(x in line.lower() for x in ["resume", "cv", "curriculum"]):
#             name = line
#             break

#     # Skills → check against predefined skill set
#     skills_found = []
#     for skill in SKILL_SET:
#         if re.search(rf"\b{skill}\b", text, re.IGNORECASE):
#             skills_found.append(skill)

#     return {
#         "name": name,
#         "email": email,
#         "phone": phone,
#         "skills": ", ".join(skills_found)
#     }


def extract_skills_section(text: str) -> list:
    match = re.search(
        r"(?:\n|\r|\r\n)(skills|technical skills|key skills|skills & expertise)[:\s]*([\s\S]+?)(?=\n(?:education|experience|projects|certifications|achievements)\b|\Z)", 
        text, re.IGNORECASE
    )
    if match:
        section = match.group(2).strip()

        cleaned = []
        for line in section.splitlines():
            line = line.strip()
            if not line:
                continue
            # If line has a dash/colon, keep only the right-hand part
            if "-" in line:
                part = line.split("-", 1)[1]
                cleaned.append(part.strip())
            elif ":" in line:
                part = line.split(":", 1)[1]
                cleaned.append(part.strip())
            else:
                cleaned.append(line)

        # Now split the cleaned block by commas, semicolons, bullets, or newlines
        skills = re.split(r"[,;\n•\-]+", " ".join(cleaned))
        return [s.strip() for s in skills if s.strip()]

    return []



def parse_resume(text: str) -> dict:
    """
    Rule-based parsing of resume text.
    Extracts: name, email, phone, skills (from section, not hardcoded).
    """

    # Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    email = email_match.group(0) if email_match else ""

    # Phone
    phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\d{10}", text)
    phone = phone_match.group(0) if phone_match else ""

    # Name → first non-empty line that doesn’t look like "resume"
    lines = text.splitlines()
    name = ""
    for line in lines:
        line = line.strip()
        if line and not any(x in line.lower() for x in ["resume", "cv", "curriculum"]):
            name = line
            break

    # Skills → extract section dynamically
    skills_found = extract_skills_section(text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": ", ".join(skills_found)
    }


# -----------------------------
# ✅ Quick Test
# -----------------------------
if __name__ == "__main__":
    files = [
        ("sample_resumes/Swapnil_Shete_Resume (3).pdf", "pdf")
       # ("sample_resumes/Swapnil_Shete_Resume (3).docx", "docx"),
    ]

    for file_path, ftype in files:
        print("\n============================")
        print(f"📄 Extracting from {file_path} ...")
        text = extract_text(file_path, ftype)
        print("Extracted Text (preview):")
        print(text[:] + "...\n" if text else "⚠️ No text extracted!")

        parsed = parse_resume(text)
        print("Parsed Resume:", parsed)
