import os
import shutil
from PyPDF2 import PdfReader

from ..constants import UPLOAD_DIR

from fastapi import UploadFile, File

# Define a directory to store uploaded files
os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_file(file: UploadFile = File(...)):
    """
    Accepts a PDF file upload, stores it on the server,
    and returns the name of the stored file.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # Save the uploaded file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"status": "success", "file_name": file.filename}
    except Exception as e:
        return {"status": "error", "message": f"Failed to save file: {e}"}


# The refactored function to read content
def read_document_to_string(file_path: str) -> str:
    """
    Reads the content of a file (PDF or TXT) and returns it as a single string.
    No security path checks are done here, as the caller should handle that.
    """
    if file_path.endswith('.pdf'):
        return _read_pdf(file_path)
    elif file_path.endswith('.txt'):
        return _read_txt(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF and TXT are supported.")


def _read_pdf(file_path: str) -> str:
    """Reads text from a PDF file."""
    text_content = ""
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text_content += page.extract_text() or ""
        return text_content
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {e}")

def _read_txt(file_path: str) -> str:
    """Reads text from a TXT file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise ValueError(f"Error reading text file: {e}")