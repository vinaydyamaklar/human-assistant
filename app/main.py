import os
import io
import logging
import asyncio
import json

from gtts import gTTS

from pydantic import BaseModel

from .constants import UPLOAD_DIR

from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from .controllers.file_reader import read_document_to_string
from .controllers import file_reader, command_runner, calendar_manager
from .controllers.websocket_manager import manager


app = FastAPI(title="Human Voice Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
    result = file_reader.upload_file(file)
    if result.get("status") != "success":
        return {"status": "error", "message": result.get("message", f"Failed to save file: {file.filename}")}
    
    return {"status": "success", "file_name": file.filename}


@app.get("/list_files/")
async def list_uploaded_files():
    """
    Returns a list of all uploaded files in the upload directory.
    """
    try:
        print(f"Checking upload directory: {UPLOAD_DIR}")
        if not os.path.exists(UPLOAD_DIR):
            print(f"Upload directory does not exist: {UPLOAD_DIR}")
            return {"status": "success", "files": []}
        
        files = []
        all_files = os.listdir(UPLOAD_DIR)
        print(f"All files in directory: {all_files}")
        
        for filename in all_files:
            if filename.endswith(('.pdf', '.txt')):
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.isfile(file_path):
                    files.append(filename)
        
        print(f"Filtered files: {files}")
        return {"status": "success", "files": files}
    except Exception as e:
        print(f"Error in list_files: {str(e)}")
        return {"status": "error", "message": f"Failed to list files: {str(e)}"}


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


@app.websocket("/ws/stream_audio")
async def websocket_stream_audio(websocket: WebSocket):
    """
    WebSocket endpoint for real-time audio streaming.
    Streams audio chunks as they are generated from text.
    """
    await manager.connect(websocket)
    
    try:
        # Wait for the filename
        data = await websocket.receive_text()
        request_data = json.loads(data)
        filename = request_data.get("filename")
        
        if not filename:
            await manager.send_personal_message(
                json.dumps({"status": "error", "message": "No filename provided"}),
                websocket
            )
            return
        
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if not os.path.exists(file_path):
            await manager.send_personal_message(
                json.dumps({"status": "error", "message": "File not found"}),
                websocket
            )
            return
        
        # Send start message
        await manager.send_personal_message(
            json.dumps({"status": "start", "message": "Starting audio stream"}),
            websocket
        )
        
        try:
            # Read the file content
            file_content = read_document_to_string(file_path)
            
            # Split content into sentences for chunked processing
            sentences = [s.strip() for s in file_content.split('.') if s.strip()]
            
            # Handle empty content
            if not sentences:
                await manager.send_personal_message(
                    json.dumps({"status": "error", "message": "File content is empty"}),
                    websocket
                )
                return
            
            # Send total sentences count
            await manager.send_personal_message(
                json.dumps({"status": "info", "total_sentences": len(sentences)}),
                websocket
            )
            
            # Process each sentence and stream audio
            for i, sentence in enumerate(sentences):
                try:
                    # Send progress update
                    await manager.send_personal_message(
                        json.dumps({
                            "status": "progress", 
                            "current": i + 1, 
                            "total": len(sentences),
                            "sentence": sentence[:100] + "..." if len(sentence) > 100 else sentence
                        }),
                        websocket
                    )
                    
                    # Convert sentence to speech
                    tts = gTTS(sentence, lang='en')
                    audio_io = io.BytesIO()
                    tts.write_to_fp(audio_io)
                    audio_io.seek(0)
                    audio_data = audio_io.getvalue()
                    
                    # Send audio chunk with metadata
                    await manager.send_personal_message(
                        json.dumps({
                            "status": "audio_chunk",
                            "chunk_index": i,
                            "chunk_size": len(audio_data),
                            "sentence": sentence
                        }),
                        websocket
                    )
                    
                    # Send the actual audio data
                    await manager.send_personal_bytes(audio_data, websocket)
                    
                    # Small delay for natural speech flow (adjust as needed)
                    await asyncio.sleep(0.3)
                    
                except Exception as e:
                    await manager.send_personal_message(
                        json.dumps({
                            "status": "error", 
                            "message": f"Error processing sentence {i+1}: {str(e)}"
                        }),
                        websocket
                    )
                    continue
            
            # Send completion message
            await manager.send_personal_message(
                json.dumps({"status": "complete", "message": "Audio streaming completed"}),
                websocket
            )
            
        except Exception as e:
            await manager.send_personal_message(
                json.dumps({"status": "error", "message": f"Error reading file: {str(e)}"}),
                websocket
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_personal_message(
            json.dumps({"status": "error", "message": f"WebSocket error: {str(e)}"}),
            websocket
        )
        manager.disconnect(websocket)


# Add a route to serve the HTML file
frontend_dir = os.path.join(os.path.dirname(__file__), '.', 'templates')

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))