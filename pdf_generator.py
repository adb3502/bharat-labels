"""
PDF generator for BHARAT labels using ReportLab
Pure Python - no Word dependency
"""
from pathlib import Path
from typing import List
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# A4 dimensions
A4_WIDTH = 21.0 * cm
A4_HEIGHT = 29.7 * cm


def generate_pdf_labels(labels: List[str], output_path: Path, config: dict):
    """Generate PDF with labels using ReportLab."""
    c = canvas.Canvas(str(output_path), pagesize=A4)
    
    # Page setup
    margin_top = config['margins_cm']['top'] * cm
    margin_left = config['margins_cm']['left'] * cm
    margin_right = config['margins_cm']['right'] * cm
    
    # Calculate usable width
    usable_width = A4_WIDTH - margin_left - margin_right
    
    # Column setup
    num_cols = len(config['label_col_idx'])
    col_width = config['col_widths_cm'][0] * cm  # Width of label column
    col_gutter = config['col_widths_cm'][1] * cm if len(config['col_widths_cm']) > 1 else 0
    
    # Row setup
    row_height = config['row_h_cm'] * cm
    row_gutter = config['row_gutter_h_cm'] * cm if config['has_row_gutters'] else 0
    
    pos = 0
    total = len(labels)
    page_num = 0
    
    while pos < total:
        if page_num > 0:
            c.showPage()
        
        # Starting Y position (from top)
        y = A4_HEIGHT - margin_top - row_height
        
        for row in range(config['rows_per_page']):
            if pos >= total:
                break
                
            # Draw labels in this row
            x = margin_left
            for col in range(num_cols):
                if pos >= total:
                    break
                
                label = labels[pos]
                
                # Skip empty labels
                if label:
                    # Draw cell border (optional, for debugging)
                    # c.rect(x, y, col_width, row_height)
                    
                    # Draw BHARAT header (small, bold)
                    c.setFont("Helvetica-Bold", config['font_size_header'])
                    text_x = x + col_width / 2
                    text_y_header = y + row_height * 0.65
                    c.drawCentredString(text_x, text_y_header, "BHARAT")
                    
                    # Draw label code
                    c.setFont("Helvetica", config['font_size'])
                    text_y_code = y + row_height * 0.35
                    c.drawCentredString(text_x, text_y_code, label)
                
                pos += 1
                x += col_width + col_gutter
            
            # Move to next row
            y -= (row_height + row_gutter)
        
        page_num += 1
    
    c.save()
    return output_path


def generate_pdf_for_codes(codes: List[str], output_dir: Path, date_str: str = "") -> List[Path]:
    """
    Generate PDF labels for all document types.
    
    Args:
        codes: List of participant codes
        output_dir: Directory to save PDFs
        date_str: Optional date string for filename suffix
    
    Returns:
        List of paths to generated PDF files
    """
    from label_generator import create_label_collections, CRYO_CONFIG, NORMAL_CONFIG
    
    # Sort codes
    codes = sorted(codes)
    
    # Create label collections
    collections = create_label_collections(codes)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename suffix
    filename_suffix = f"_{date_str}" if date_str else ""
    
    generated_files = []
    
    # Generate cryovial PDF (5 per row)
    cryo_filename = f'labels_cryovial{filename_suffix}.pdf'
    cryo_path = generate_pdf_labels(collections['cryovial'], output_dir / cryo_filename, CRYO_CONFIG)
    generated_files.append(cryo_path)
    
    # Generate normal PDFs (4 per row)
    for group_name in ['epigenetics', 'samples', 'edta', 'sst_fl_blood']:
        pdf_filename = f'labels_{group_name}{filename_suffix}.pdf'
        pdf_path = generate_pdf_labels(collections[group_name], output_dir / pdf_filename, NORMAL_CONFIG)
        generated_files.append(pdf_path)
    
    return generated_files
