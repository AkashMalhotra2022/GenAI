# Flake8: noqa
import uvicorn
from .server import app
from dotenv import load_dotenv

load_dotenv()  # Add this line

def main():
    uvicorn.run(app, port=8000, host="0.0.0.0")

main()