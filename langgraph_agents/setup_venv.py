import subprocess
import sys
import os
from pathlib import Path

def setup_venv():
    # Create virtual environment
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # Get the path to the virtual environment's Python interpreter
    if sys.platform == "win32":
        python_path = Path("venv") / "Scripts" / "python.exe"
    else:
        python_path = Path("venv") / "bin" / "python"
    
    # Upgrade pip
    subprocess.run([str(python_path), "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install requirements
    subprocess.run([str(python_path), "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("\nVirtual environment setup complete!")
    print("\nTo activate the virtual environment:")
    if sys.platform == "win32":
        print("    venv\\Scripts\\activate")
    else:
        print("    source venv/bin/activate")

if __name__ == "__main__":
    setup_venv() 