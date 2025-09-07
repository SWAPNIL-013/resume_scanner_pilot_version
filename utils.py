import os
import pandas as pd
from datetime import datetime
from parser import extract_text, parse_resume

def process_resumes(file_list, output_file="parsed_resumes.xlsx"):
    """
    Process multiple resumes → extract text → parse → save/append to Excel.
    
    Args:
        file_list (list): List of tuples [(file_path, file_type), ...]
        output_file (str): Path to save Excel file

    Returns:
        pd.DataFrame: Parsed resume data (all records)
    """
    parsed_data = []

    # Load old data if file exists
    if os.path.exists(output_file):
        df_old = pd.read_excel(output_file)
        sr_start = df_old["sr_no"].max() + 1
    else:
        df_old = pd.DataFrame()
        sr_start = 1

    for idx, (file_path, ftype) in enumerate(file_list, start=sr_start):
        text = extract_text(file_path, ftype)
        parsed = parse_resume(text)
        parsed["sr_no"] = idx
        parsed["uploaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parsed_data.append(parsed)

    df_new = pd.DataFrame(parsed_data)

    # Reorder columns
    cols = ["sr_no", "name", "email", "phone", "skills", "uploaded_at"]
    df_new = df_new[cols]

    # Append or create new
    if not df_old.empty:
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new

    # Save to Excel
    df_final.to_excel(output_file, index=False)

    return df_final
