# import camelot
# import pandas as pd
# import tempfile

# def extract_table_from_pdf(uploaded_file_content):
#     try:
#         # Create a temporary file to save the uploaded PDF content
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
#             temp_pdf.write(uploaded_file_content)
#             temp_pdf_path = temp_pdf.name

#         # Use Camelot to read the tables from the temporary file
#         tables = camelot.read_pdf(temp_pdf_path, pages='all', flavor='stream')

#         if not tables:
#             return None

#         # Extract the tables as dataframes
#         data_frames = [table.df for table in tables]

#         return data_frames
#     except Exception as e:
#         raise ValueError(f"Error extracting table from PDF: {e}")


import camelot
import pandas as pd
import tempfile


import fitz  # PyMuPDF

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
        # Check if uploaded file content is empty
        check_pdf_content(uploaded_file_content)
        if not uploaded_file_content:
            raise ValueError("Uploaded file content is empty.")
        
        # Create a temporary file to save the uploaded PDF content
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file_content)
            temp_pdf_path = temp_pdf.name

        # Debugging statement to check if temp file is created correctly
        print(f"Temporary PDF path: {temp_pdf_path}")

        # Use Camelot to read the tables from the temporary file
        tables = camelot.read_pdf(temp_pdf_path, pages='all', flavor='stream')

        # Debugging statement to check number of tables found
        if tables:
            print(f"Number of tables extracted: {len(tables)}")
        else:
            print("No tables found by Camelot.")

        # If no tables found, return None
        if not tables or len(tables) == 0:
            return None

        # Extract the tables as dataframes
        data_frames = [table.df for table in tables]

        return data_frames
    except Exception as e:
        raise ValueError(f"Error extracting table from PDF: {e}")
