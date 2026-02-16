# BHARAT Study Label Generator

Web application for generating biobanking sample labels for the BHARAT Study (Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions).

## Features

- Generate labels for multiple participant codes
- Input methods: paste codes, CSV upload, Excel upload, or code range
- Output formats: PDF (requires Microsoft Word) or DOCX
- 6 label types per participant: Cryovial, Epigenetics, Samples, EDTA, SST/FL/Blood, Urine

## Requirements

- Windows with Microsoft Word installed
- Python 3.8+
- Cloudflare Tunnel (optional, for public access)

## Quick Start

### 1. Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Install Cloudflared (for public access)

```bash
winget install Cloudflare.cloudflared
```

### 3. Install Services (Run as Administrator)

```bash
# Install PDF worker (runs in background)
install_worker_service.bat

# Install web server + tunnel (runs in background)
install_server_service.bat
```

### 4. Get Your Public URL

```bash
get_url.bat
```

Share the `*.trycloudflare.com` URL with your team.

## Manual Start (Alternative)

If you prefer to run manually instead of as services:

**Terminal 1 - PDF Worker:**
```bash
start_worker.bat
```

**Terminal 2 - Web Server:**
```bash
start_local.bat          # Local network only
# OR
start_with_tunnel.bat    # Public access via Cloudflare
```

## Scripts Reference

### Service Scripts (Run as Administrator)

| Script | Description |
|--------|-------------|
| `install_worker_service.bat` | Install PDF worker as background service |
| `install_server_service.bat` | Install web server + tunnel as background service |
| `uninstall_worker_service.bat` | Remove worker service |
| `uninstall_server_service.bat` | Remove server service |

### Manual Start Scripts

| Script | Description |
|--------|-------------|
| `start_worker.bat` | Start PDF worker (visible window) |
| `start_local.bat` | Start web server (local network only) |
| `start_with_tunnel.bat` | Start web server with Cloudflare tunnel |

### Utility Scripts

| Script | Description |
|--------|-------------|
| `get_url.bat` | Show current public tunnel URL |
| `stop_worker.bat` | Stop PDF worker |
| `stop_server.bat` | Stop web server + tunnel |

## How It Works

1. User submits codes via web interface
2. App writes request to `output/codes.json`
3. Worker (running in background) generates DOCX and converts to PDF using Word
4. App reads PDFs and provides ZIP download

## Notes

- You must stay logged in to Windows for PDF conversion (Word requires a user session)
- The tunnel URL changes each restart (use `get_url.bat` to check)
- Lock screen (Win+L) is OK - signing out will stop PDF conversion
