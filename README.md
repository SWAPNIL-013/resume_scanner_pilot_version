📄Resume Scanner Pilot (No LLM)
A simple resume parsing tool built with Python, Streamlit, and rule-based regex extraction.
It allows you to upload multiple resumes (PDF/DOCX/TXT), extract structured data (name, email, phone, skills), and export everything into an Excel file.

🚀 Features
Upload multiple resumes at once (PDF, DOCX, TXT).
Extract fields using rule-based parsing:
Name (first non-empty line heuristic)
Email (regex)
Phone (regex)
Skills (matched against predefined list)
Save all parsed resumes into an Excel file (parsed_resumes.xlsx).
View parsed data directly in the UI.
Download the generated Excel.

📂 Project Structure
resume_scanner_pilot_version/
│── app.py          # Streamlit frontend
│── parser.py       # Resume text extraction + parsing logic
│── utils.py        # Processing & Excel export
│── requirements.txt# Python dependencies
│── .gitignore

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone <your-repo-url>
cd resume_scanner_pilot_version

2️⃣ Create virtual environment & activate
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

▶️ Running the Application
Run the Streamlit app:
streamlit run app.py

This will start a local server (e.g., http://localhost:8501).
Open it in your browser.

🖥️ Usage Flow
Upload multiple resumes (PDF/DOCX/TXT).
Click Process & Save to Excel.
View parsed data in the app with See Uploaded Data.
Download the generated Excel with Download Excel.
