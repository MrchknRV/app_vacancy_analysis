import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")

PATH = Path(__file__).parent

EMPLOYER_IDS = [1740, 3529, 78638, 2748, 3776, 41862, 67611, 87021, 2180, 84585]
