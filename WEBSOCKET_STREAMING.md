# WebSocket Audio Streaming Implementation

## Overview

This application now supports **real-time audio streaming** using WebSockets instead of the previous HTTP-based approach. This provides much better performance and true streaming capabilities.

## How It Works

### 1. **WebSocket Connection**
- Client establishes WebSocket connection to `/ws/stream_audio`
- Sends filename to start streaming
- Receives audio chunks and status updates in real-time

### 2. **Chunked Processing**
- File content is split into sentences
- Each sentence is converted to speech individually
- Audio chunks are sent as they're generated
- Progress updates are sent for each sentence

### 3. **Real-time Streaming**
- Audio starts playing before the entire file is processed
- Low latency - no waiting for complete file conversion
- Smooth, continuous playback experience

## API Endpoints

### WebSocket Endpoint
```
ws://localhost:8000/ws/stream_audio
```

### Message Format
**Client → Server:**
```json
{
  "filename": "document.pdf"
}
```

**Server → Client:**
```json
// Status messages
{
  "status": "start|info|progress|audio_chunk|complete|error",
  "message": "Description",
  "current": 1,
  "total": 10,
  "sentence": "Current sentence being processed...",
  "chunk_index": 0,
  "chunk_size": 1234
}

// Audio data (binary)
[Binary audio data]
```

## Features

### ✅ **Real-time Progress**
- Progress bar showing streaming completion
- Current sentence display
- WebSocket connection status

### ✅ **Audio Queue Management**
- Automatic audio chunk queuing
- Seamless playback between chunks
- Error handling for failed chunks

### ✅ **Connection Management**
- Connection timeout handling (10 seconds)
- Automatic cleanup on disconnect
- Error recovery

### ✅ **Performance Benefits**
- No waiting for complete file processing
- Lower memory usage
- Better user experience

## Usage

1. **Upload a file** (PDF or TXT)
2. **Select the file** from the left sidebar
3. **Click "Stream Audio"** to start WebSocket streaming
4. **Monitor progress** in real-time
5. **Audio plays automatically** as chunks arrive

## Technical Details

### Dependencies
- `fastapi` - Web framework with WebSocket support
- `websockets` - WebSocket handling
- `gtts` - Text-to-speech conversion
- `asyncio` - Asynchronous processing

### Architecture
```
Client ←→ WebSocket ←→ FastAPI Server
         ↓
    Audio Processing
         ↓
    gTTS Conversion
         ↓
    Chunked Streaming
```

### Error Handling
- File not found
- Empty file content
- Processing errors
- Connection timeouts
- WebSocket disconnections

## Comparison: Old vs New

| Feature | HTTP Streaming | WebSocket Streaming |
|---------|----------------|-------------------|
| Latency | High (wait for complete file) | Low (start immediately) |
| Memory | High (load entire file) | Low (process in chunks) |
| Progress | None | Real-time updates |
| User Experience | Poor (waiting) | Excellent (immediate) |
| Scalability | Limited | Better |

## Troubleshooting

### Common Issues
1. **Connection timeout**: Check server status and network
2. **Audio not playing**: Verify browser supports WebSocket
3. **File not found**: Ensure file exists in upload directory

### Debug Mode
- Open browser console for detailed logging
- WebSocket messages are logged
- Audio chunk processing is tracked

## Future Enhancements

- [ ] Multiple language support
- [ ] Voice selection options
- [ ] Streaming speed control
- [ ] Audio quality settings
- [ ] Batch file processing
