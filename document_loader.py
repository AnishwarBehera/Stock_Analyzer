import fitz 
import re

def extract_text_from_pdf(uploaded_file, document_type):
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    uploaded_file.seek(0)  

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        if text:
            full_text += text

            if document_type == "Annual Report" and len(full_text) >= 5000:
                yield full_text
                full_text = ""

            elif document_type == "Other Report" and len(full_text) >= 1000:
                yield full_text
                full_text = ""

    if full_text:
        yield full_text



def process_uploaded_files(uploaded_files, document_type):
    documents = []

    for uploaded_file in uploaded_files:
        for text_chunk in extract_text_from_pdf(uploaded_file, document_type):
            documents.append(text_chunk)

    return documents



def extract_text_and_page_count(uploaded_file):
    try:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        full_text = ""
        page_count = pdf_document.page_count

        for page_num in range(page_count):
            page = pdf_document.load_page(page_num)
            text = page.get_text("text")
            if text:
                full_text += text

        return full_text, page_count

    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")



def classify_document(uploaded_file):
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    num_pages = pdf_document.page_count

    uploaded_file.seek(0)

    if num_pages > 50:
        return "Annual Report"
    else:
        return "Other Report"



