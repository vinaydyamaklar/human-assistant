import os
import io
import logging

from gtts import gTTS

from pydantic import BaseModel

from .constants import UPLOAD_DIR

from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse

from .controllers.file_reader import read_document_to_string
from .controllers import file_reader, command_runner, calendar_manager


app = FastAPI(title="Human Voice Assistant")
# ... (existing middleware and model setup)

# New Pydantic models for API requests
class CommandRequest(BaseModel):
    command: str

class FileRequest(BaseModel):
    file_path: str

class CalendarRequest(BaseModel):
    action: str  # e.g., "add_event", "list_events"
    data: dict   # details for the action

class TextRequest(BaseModel):
    text: str


# --- Endpoints ---

@app.post("/execute_command/")
async def execute_command(request: CommandRequest):
    """
    Securely executes a basic desktop command and returns the output.
    """
    try:
        output = command_runner.run_secure_command(request.command)
        return {"status": "success", "output": output}
    except ValueError as e:
        return {"status": "error", "message": str(e)}


@app.post("/upload_file/")
async def file_upload(file: UploadFile = File(...)):
    """
    Accepts a PDF file upload, stores it on the server,
    and returns the name of the stored file.
    """
    print(file.content_type)
    if file.content_type not in ["application/pdf", "text/plain"]:
        return {"status": "error", "message": "Only PDF files are supported."}
    
    status = file_reader.upload_file(file)
    if not status:
        return {"status": "error", "message": f"Failed to save file: {file.filename}"}
    
    return {"status": "success", "file_name": file.filename}


@app.post("/interact_calendar/")
async def interact_calendar(request: CalendarRequest):
    """
    Interacts with the user's calendar (e.g., list events, add event).
    """
    try:
        result = calendar_manager.perform_calendar_action(request.action, request.data)
        return {"status": "success", "result": result}
    except ValueError as e:
        return {"status": "error", "message": str(e)}



@app.post("/stream_audio_from_file/")
async def stream_audio_from_file(request: TextRequest):
    """
    Takes a file name, reads its content, and streams it back as audio.
    """
    file_path = os.path.join(UPLOAD_DIR, request.text)

    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found."}
    
    # Read the file content as a single string
    try:
        file_content = read_document_to_string(file_path)
    except ValueError as e:
        return {"status": "error", "message": str(e)}

    # Convert the entire content to speech using gTTS
    tts = gTTS(file_content, lang='en')
    
    # Save the audio to a BytesIO object
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    
    # Return the audio as a streaming response
    return StreamingResponse(audio_io, media_type="audio/mpeg")


# Add a route to serve the HTML file
frontend_dir = os.path.join(os.path.dirname(__file__), '.', 'templates')

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))