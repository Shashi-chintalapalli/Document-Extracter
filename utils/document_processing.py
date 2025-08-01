import fitz  # PyMuPDF

def load_pdf(uploaded_file):
    # Loads and returns the PDF file object
    try:
        return fitz.open(stream=uploaded_file.read(), filetype="pdf")
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return None

def extract_text_from_pdf_doc(pdf_doc):
    if pdf_doc is None:
        return ""
    text = ""
    for page in pdf_doc:
        text += page.get_text()
    return text.strip()
