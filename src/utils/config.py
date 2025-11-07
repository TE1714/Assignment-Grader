# src/utils/config.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the root directory
load_dotenv()

# Get the Google API key and make it available for other files to import
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# This check provides a clear error if the key is missing from your .env file
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file. Please add it.")