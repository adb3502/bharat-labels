import streamlit as st
import pandas as pd
import tempfile
import zipfile
from pathlib import Path
import io
import re
from label_generator import generate_labels_for_codes

# Try to import PDF conversion (requires Word)
try:
    from convert_to_pdf import generate_pdfs
    HAS_DOCX2PDF = True
except ImportError as e:
    HAS_DOCX2PDF = False
    print(f"PDF import failed: {e}")

st.set_page_config(page_title="BHARAT Label Generator", page_icon="🏷️", layout="wide")

st.title("🏷️ BHARAT Study Label Generator")
st.markdown("Generate sample labels for the BHARAT Study biobanking")

# Output format selection
if HAS_DOCX2PDF:
    output_format = st.radio(
        "Output format:",
        ["PDF", "Word (DOCX)"],
        horizontal=True
    )
else:
    output_format = "Word (DOCX)"
    st.info("PDF conversion requires Microsoft Word. Currently outputting DOCX files only.")

# Input method selection
input_method = st.radio(
    "Choose input method:",
    ["Paste codes", "Upload CSV", "Upload Excel", "Code range"],
    horizontal=True
)

codes = []
date_str = ""

# Handle different input methods
if input_method == "Paste codes":
    col1, col2 = st.columns([3, 1])
    with col1:
        pasted_codes = st.text_area(
            "Paste participant codes (one per line):",
            height=200,
            placeholder="1A-001\n1A-002\n1A-003"
        )
    with col2:
        date_str = st.text_input("Sampling date (DD-MM-YYYY):", placeholder="23-01-2025")
    
    if pasted_codes:
        codes = [line.strip() for line in pasted_codes.split('\n') if line.strip()]

elif input_method in ["Upload CSV", "Upload Excel"]:
    col1, col2 = st.columns([3, 1])
    with col1:
        file_type = "csv" if input_method == "Upload CSV" else "xlsx"
        uploaded_file = st.file_uploader(
            f"Upload {file_type.upper()} file with codes:",
            type=[file_type]
        )
    with col2:
        date_str = st.text_input("Sampling date (DD-MM-YYYY):", placeholder="23-01-2025")
    
    if uploaded_file:
        try:
            if file_type == "csv":
                df = pd.read_csv(uploaded_file, header=None)
            else:
                df = pd.read_excel(uploaded_file, header=None)
            
            # Get first column
            codes = df.iloc[:, 0].dropna().astype(str).str.strip().tolist()
            codes = [c for c in codes if c]
            
        except Exception as e:
            st.error(f"Error reading file: {e}")

elif input_method == "Code range":
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        start_code = st.text_input("Start code:", placeholder="1A-001")
    with col2:
        end_code = st.text_input("End code:", placeholder="1A-030")
    with col3:
        date_str = st.text_input("Date (DD-MM-YYYY):", placeholder="23-01-2025")
    
    if start_code and end_code:
        try:
            start_match = re.match(r'([A-Za-z0-9]+)-(\d+)', start_code)
            end_match = re.match(r'([A-Za-z0-9]+)-(\d+)', end_code)
            
            if start_match and end_match:
                prefix_start, num_start = start_match.groups()
                prefix_end, num_end = end_match.groups()
                
                if prefix_start == prefix_end:
                    num_width = len(num_start)
                    for i in range(int(num_start), int(num_end) + 1):
                        codes.append(f"{prefix_start}-{str(i).zfill(num_width)}")
                else:
                    st.error("Prefix mismatch between start and end codes")
            else:
                st.error("Invalid code format. Use format like 1A-001")
        except Exception as e:
            st.error(f"Error generating range: {e}")

# Display preview
if codes:
    st.success(f"✓ Found {len(codes)} participant codes")
    
    with st.expander("Preview codes"):
        preview_df = pd.DataFrame(codes, columns=["Participant Code"])
        st.dataframe(preview_df, height=200)

# Generate button
if codes:
    if st.button("Generate Labels", type="primary", use_container_width=True):
        with st.spinner("Generating labels..."):
            try:
                if output_format == "PDF" and HAS_DOCX2PDF:
                    # Generate PDFs using subprocess (files saved in ./output folder)
                    from io import StringIO
                    import sys as _sys
                    old_stdout = _sys.stdout
                    _sys.stdout = mystdout = StringIO()

                    files_to_zip = generate_pdfs(codes, date_str)

                    output = mystdout.getvalue()
                    _sys.stdout = old_stdout

                    if output:
                        with st.expander("Log", expanded=False):
                            st.code(output)

                    file_ext = "pdf"

                else:
                    # Generate DOCX using fixed output folder
                    output_folder = Path(__file__).parent / "output"
                    output_folder.mkdir(exist_ok=True)
                    for f in output_folder.glob("*"):
                        f.unlink()

                    files_to_zip = generate_labels_for_codes(codes, output_folder, date_str)
                    file_ext = "docx"

                # Create zip
                if files_to_zip:
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for file_path in files_to_zip:
                            zipf.write(file_path, file_path.name)

                    zip_buffer.seek(0)

                    filename_suffix = f"_{date_str}" if date_str else ""
                    st.success(f"✓ Generated {len(files_to_zip)} {file_ext.upper()} files!")
                    st.download_button(
                        label=f"📥 Download Labels (ZIP)",
                        data=zip_buffer,
                        file_name=f"bharat_labels{filename_suffix}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                else:
                    st.error("No files were generated.")

            except Exception as e:
                st.error(f"Error: {e}")
                st.exception(e)

# Footer
st.markdown("---")
st.markdown("*BHARAT Study - Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions*")
