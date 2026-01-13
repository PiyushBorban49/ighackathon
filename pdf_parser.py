import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    """
    Extracts raw text from a Streamlit UploadedFile object (PDF).
    """
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"