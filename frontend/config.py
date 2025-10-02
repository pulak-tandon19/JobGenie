import os
from dotenv import load_dotenv

load_dotenv()
BASE_API_URL = os.getenv("BASE_API_URL", "http://localhost:8000")
# BASE_API_URL = "http://127.0.0.1:8000"