# Pdf/Text file reader Assistant

A professional audio streaming application that converts uploaded documents (PDF/TXT) to speech using WebSocket-based real-time streaming.

## 🚀 Features

- **Real-time Audio Streaming**: WebSocket-based streaming for immediate audio playback
- **Document Upload**: Support for PDF and text files
- **Professional UI**: Modern, responsive design with audio controls
- **File Management**: Sidebar file browser with upload history
- **Audio Controls**: Play/pause, seek, speed control, and keyboard shortcuts
- **Progress Tracking**: Real-time progress indicators during streaming

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Audio Processing**: gTTS (Google Text-to-Speech)
- **Real-time Communication**: WebSockets
- **Document Processing**: PyPDF2

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd human-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python -m app.main
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8000`

## 📁 Project Structure

```
human-assistant/
├── app/
│   ├── __pycache__/
│   ├── assistant.py
│   ├── constants.py
│   ├── controllers/
│   │   ├── __pycache__/
│   │   ├── calendar_manager.py
│   │   ├── command_runner.py
│   │   ├── file_reader.py
│   │   └── websocket_manager.py
│   ├── docs/
│   │   └── api_docs.md
│   ├── main.py
│   └── templates/
│       └── index.html
├── uploaded_files/          # User uploaded files (gitignored)
├── venv/                    # Virtual environment (gitignored)
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
└── WEBSOCKET_STREAMING.md
```

## 🔒 Security & Privacy

### Git Ignore Configuration

The `.gitignore` file is configured to protect user privacy and prevent sensitive data from being committed:

- **`uploaded_files/`**: All user-uploaded documents are excluded
- **`*.pdf`, `*.txt`**: Individual document files are ignored
- **`*.mp3`, `*.wav`, `*.ogg`**: Generated audio files are excluded
- **`venv/`**: Virtual environment directory
- **`__pycache__/`**: Python cache files
- **`.env`**: Environment variables and secrets

### Data Handling

- Uploaded files are stored locally in the `uploaded_files/` directory
- Files are processed in-memory during streaming
- No data is sent to external services except Google TTS for audio generation
- All file operations are performed locally

## 🎵 Audio Streaming

### WebSocket Endpoint
- **URL**: `ws://localhost:8000/ws/stream_audio`
- **Protocol**: Real-time audio chunk streaming
- **Features**: Progress tracking, error handling, chunked processing

### Audio Controls
- **Play/Pause**: Space bar or click button
- **Stop**: Escape key or stop button
- **Seek**: Click/drag seek bar or arrow keys
- **Speed Control**: 0.5x, 1.0x, 1.5x, 2.0x
- **Keyboard Shortcuts**: Full keyboard navigation support

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application interface |
| `/upload_file/` | POST | Upload PDF/TXT files |
| `/list_files/` | GET | List uploaded files |
| `/ws/stream_audio` | WebSocket | Real-time audio streaming |
| `/stream_audio_from_file/` | POST | Legacy HTTP streaming |

## 🐳 Docker Support

### Using Docker Compose
```bash
docker-compose up --build
```

### Using Docker directly
```bash
docker build -t human-assistant .
docker run -p 8000:8000 human-assistant
```

## 🧪 Development

### Running in Development Mode
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Structure
- **`app/main.py`**: FastAPI application and endpoints
- **`app/controllers/`**: Business logic modules
- **`app/templates/index.html`**: Frontend interface
- **`app/constants.py`**: Application configuration

## 📊 Performance

- **Real-time Streaming**: Audio starts playing immediately
- **Chunked Processing**: Efficient memory usage
- **WebSocket Communication**: Low-latency audio delivery
- **Responsive Design**: Works on all device sizes

## 🔍 Troubleshooting

### Common Issues

1. **File upload fails**
   - Check file format (PDF/TXT only)
   - Ensure `uploaded_files/` directory exists
   - Verify file permissions

2. **Audio streaming issues**
   - Check WebSocket connection
   - Verify internet connection (for gTTS)
   - Check browser console for errors

3. **Port conflicts**
   - Change port in `main.py` or use different port
   - Check if port 8000 is already in use

### Debug Mode
- Open browser developer tools
- Check console for detailed error messages
- Monitor WebSocket connection status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review the API documentation
- Open an issue on GitHub

---

**Note**: This application processes user files locally and does not store or transmit any user data to external services except for Google TTS audio generation.
