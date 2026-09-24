#!/usr/bin/env python3
"""
Setup script for EduGenie
"""
import os
import sys
from pathlib import Path

def main():
    print("🔧 Setting up EduGenie...")
    
    base = Path(__file__).parent.parent
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check .env
    env_example = base / ".env.example"
    env_file = base / ".env"
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env from .env.example...")
        with open(env_example) as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        print("✓ .env created - Please add your GEMINI_API_KEY")
    elif env_file.exists():
        print("✓ .env exists")
    
    # Check dependencies
    print("📦 Checking dependencies...")
    try:
        import fastapi
        import uvicorn
        import jinja2
        print("✓ Core dependencies available")
    except ImportError as e:
        print(f"⚠️  Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
    
    # Check optional Gemini
    try:
        import google.generativeai
        print("✓ google-generativeai available")
    except ImportError:
        print("⚠️  google-generativeai not installed - fallback mode will be used")
    
    print("""
    ✅ Setup complete!
    
    Next steps:
    1. Edit .env and add your GEMINI_API_KEY (optional, fallback works without it)
       Get key from: https://aistudio.google.com/app/apikey
    
    2. Install dependencies:
       pip install -r requirements.txt
    
    3. Run the app:
       uvicorn app.main:app --reload
       or
       python scripts/run.py
    
    4. Open: http://127.0.0.1:8000
    
    5. Run tests:
       pytest tests/ -v
    """)

if __name__ == "__main__":
    main()
