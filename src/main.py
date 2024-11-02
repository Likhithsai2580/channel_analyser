import asyncio
import uvicorn
from dotenv import load_dotenv
import os
from app import app

# Load environment variables from .env file
load_dotenv()

# Verify required environment variables
required_vars = ["GROQ_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

if __name__ == "__main__":
    # Run the FastAPI application using uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        workers=1     # Number of worker processes
    ) 