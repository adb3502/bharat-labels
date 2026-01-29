# BHARAT Study Label Generator

Web app for generating biobanking sample labels for the BHARAT Study.

## Setup for Windows Lab Workstation

### Prerequisites
- Windows OS with Microsoft Word installed
- Python 3.8+
- Internet connection

### Installation

1. Install dependencies:
```bash
cd D:\Projects\bharat-labels
pip install -r requirements.txt
```

### Running Locally (Team Access)

**Option 1: Local Network Only**
```bash
streamlit run app.py --server.address 0.0.0.0
```
Team accesses at: `http://<YOUR_IP>:8501`

**Option 2: Public URL via ngrok (Recommended)**

1. Download ngrok from https://ngrok.com/download
2. Extract to a folder
3. Run the app:
```bash
streamlit run app.py
```

4. In a new terminal, run ngrok:
```bash
ngrok http 8501
```

5. Share the ngrok URL (e.g., `https://abc123.ngrok-free.app`) with your team

### Features

- Paste codes directly
- Upload CSV/Excel files
- Generate code ranges
- Automatic date extraction
- Output as PDF or DOCX
- Download all labels as ZIP
- Generates 5 document types:
  - Cryovial labels (5 per row)
  - Epigenetics labels
  - Sample labels
  - EDTA labels
  - SST/FL/Blood labels

### Deployment Notes

- App converts DOCX to PDF using Microsoft Word (requires Word installation)
- If Word is not installed, app will output DOCX files only
- Keep the terminal/command prompt running while team uses the app
- ngrok free tier URL changes each restart (upgrade for permanent URL)

### File Structure

- `app.py` - Streamlit web interface
- `label_generator.py` - Core label generation logic (DOCX)
- `pdf_generator.py` - Alternative PDF generation (not used with docx2pdf)
- `requirements.txt` - Python dependencies
