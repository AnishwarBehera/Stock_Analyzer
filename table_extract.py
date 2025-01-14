
import camelot
import tabula
import pandas as pd
import tempfile
from pdf2image import convert_from_path
import pytesseract
import fitz  
import numpy as np
import cv2

def check_pdf_content(uploaded_file_content):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file_content)
            temp_pdf_path = temp_pdf.name

        pdf_document = fitz.open(temp_pdf_path)
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")

        print(f"Extracted text length: {len(text)}")
    except Exception as e:
        print(f"Error reading PDF: {e}")

def extract_table_from_pdf(uploaded_file_content):
    try:
        check_pdf_content(uploaded_file_content)
        if not uploaded_file_content:
            raise ValueError("Uploaded file content is empty.")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file_content)
            temp_pdf_path = temp_pdf.name

        print(f"Temporary PDF path: {temp_pdf_path}")

        # 1. Try Camelot - Stream flavor
        try:
            tables = camelot.read_pdf(temp_pdf_path, pages='all', flavor='stream')
            if tables and len(tables) > 0:
                print("Tables detected using Camelot (Stream mode).")
                return [table.df for table in tables]
        except Exception as camelot_stream_error:
            print(f"Error using Camelot Stream: {camelot_stream_error}")

        # 2. Try Camelot - Lattice flavor 
        try:
            tables = camelot.read_pdf(temp_pdf_path, pages='all', flavor='lattice')
            if tables and len(tables) > 0:
                print("Tables detected using Camelot (Lattice mode).")
                return [table.df for table in tables]
        except Exception as camelot_lattice_error:
            print(f"Error using Camelot Lattice: {camelot_lattice_error}")

        # 3. Try Tabula
        try:
            tables = tabula.read_pdf(temp_pdf_path, pages='all', multiple_tables=True)
            if tables and len(tables) > 0:
                print("Tables detected using Tabula.")
                return tables
        except Exception as tabula_error:
            print(f"Error using Tabula: {tabula_error}")

        # 4. OCR-based extraction 
        try:
            print("Attempting OCR-based extraction...")
            images = convert_from_path(temp_pdf_path)
            ocr_data_frames = []
            for page_num, image in enumerate(images):
                image_np = np.array(image)
                image_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
                image_thresh = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

                custom_oem_psm_config = r'--oem 3 --psm 6'
                ocr_text = pytesseract.image_to_string(image_thresh, config=custom_oem_psm_config)

                rows = [line.split() for line in ocr_text.split("\n") if line.strip()]
                if rows:
                    df = pd.DataFrame(rows)
                    ocr_data_frames.append(df)

            if ocr_data_frames:
                print("Tables detected using OCR-based extraction.")
                return ocr_data_frames
        except Exception as ocr_error:
            print(f"Error using OCR-based extraction: {ocr_error}")

        print("No tables detected in the PDF.")
        return []

    except Exception as e:
        raise ValueError(f"Error extracting table from PDF: {e}")


