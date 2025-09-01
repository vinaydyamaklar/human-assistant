import os

# Use relative path from project root instead of absolute system path
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploaded_files")