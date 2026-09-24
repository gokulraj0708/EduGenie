#!/usr/bin/env python3
"""
Run script for EduGenie
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    print(f"""
    🚀 Starting EduGenie - AI Learning Assistant
    📚 Google Gemini Powered Learning Assistant
    🌐 Server: http://{HOST}:{PORT}
    📖 API Docs: http://{HOST}:{PORT}/api/docs
    ❤️  Health: http://{HOST}:{PORT}/health
    
    Press CTRL+C to stop
    """)
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
