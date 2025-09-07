# import streamlit as st
# import pandas as pd
# import tempfile
# import os
# import time

# from utils import process_resumes

# # --------------------------
# # Streamlit UI
# # --------------------------
# st.set_page_config(page_title="Resume Parser", layout="wide")
# st.title("📄 Resume Parser")

# uploaded_files = st.file_uploader(
#     "Upload resumes (PDF/DOCX/TXT)", 
#     type=["pdf", "docx", "txt"], 
#     accept_multiple_files=True
# )

# if uploaded_files:
#     st.success(f"✅ {len(uploaded_files)} resumes uploaded successfully!")

#     if st.button("Process & Save to Excel"):
#         temp_files = []

#         for f in uploaded_files:
#             # Save uploaded file temporarily
#             suffix = os.path.splitext(f.name)[-1]
#             tmp_path = os.path.join(tempfile.gettempdir(), f.name)
#             with open(tmp_path, "wb") as tmp_file:
#                 tmp_file.write(f.read())
#             file_type = suffix.replace(".", "").lower()
#             temp_files.append((tmp_path, file_type))

#         # Process resumes (this now APPENDS to existing Excel)
#         df = process_resumes(temp_files)
#         st.session_state["parsed_df"] = df  

#         st.success("✅ Resumes processed and saved to Excel!")
#         time.sleep(1)  # short delay for UX

# # --------------------------
# # Buttons for viewing & downloading (outside processing block)
# # --------------------------
# if "parsed_df" in st.session_state:
#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("👀 See Uploaded Data"):
#             st.dataframe(st.session_state["parsed_df"])

#     with col2:
#         with open("parsed_resumes.xlsx", "rb") as f:
#             st.download_button(
#                 label="📥 Download Excel",
#                 data=f,
#                 file_name="parsed_resumes.xlsx",
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             )
import streamlit as st
import pandas as pd
import tempfile
import os
import time

from utils import process_resumes

# --------------------------
# Streamlit UI Setup
# --------------------------
st.set_page_config(page_title="Resume Parser", layout="wide")
st.title("📄 Resume Parser")

# --------------------------
# File Uploader
# --------------------------
uploaded_files = st.file_uploader(
    "Upload resumes (PDF/DOCX/TXT)", 
    type=["pdf", "docx", "txt"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} resumes uploaded successfully!")

    if st.button("Process & Save to Excel"):
        temp_files = []

        for f in uploaded_files:
            # Save uploaded file temporarily
            suffix = os.path.splitext(f.name)[-1]
            tmp_path = os.path.join(tempfile.gettempdir(), f.name)
            with open(tmp_path, "wb") as tmp_file:
                tmp_file.write(f.read())
            file_type = suffix.replace(".", "").lower()
            temp_files.append((tmp_path, file_type))

        # Process resumes (append to existing Excel if exists)
        df = process_resumes(temp_files)
        st.session_state["parsed_df"] = df  

        st.success("✅ Resumes processed and saved to Excel!")
        time.sleep(1)  # short delay for UX

# --------------------------
# Display & Download Parsed Data
# --------------------------
if "parsed_df" in st.session_state:
    st.subheader("Parsed Resume Data")
    
    # Full-width DataFrame
    st.dataframe(st.session_state["parsed_df"], width="stretch")
    
    # Excel Download Button
    excel_path = "parsed_resumes.xlsx"
    if os.path.exists(excel_path):
        with open(excel_path, "rb") as f:
            st.download_button(
                label="📥 Download Excel",
                data=f,
                file_name="parsed_resumes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
