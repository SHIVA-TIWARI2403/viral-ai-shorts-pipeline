import os
from pathlib import Path
from dotenv import load_dotenv
import imageio_ffmpeg

# Base Directories
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
TEMP_DIR = BASE_DIR / "temp"

for directory in [OUTPUT_DIR, ASSETS_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Load environment variables from .env if present
load_dotenv(BASE_DIR / ".env")

# Video Settings (9:16 vertical for Shorts / Reels)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30

# Voiceover Settings (Microsoft Edge Neural Voice)
# "en-US-ChristopherNeural" is deep, authoritative, and cinematic (ideal for Dark Psychology)
DEFAULT_VOICE = os.getenv("VOICE_NAME", "en-US-ChristopherNeural")
VOICE_RATE = os.getenv("VOICE_RATE", "+0%")
VOICE_PITCH = os.getenv("VOICE_PITCH", "-2Hz")

# Gemini API Settings (Supports Gemini 1.5 Pro / 2.0 Flash)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

# YouTube Upload Settings
YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", str(BASE_DIR / "client_secret.json"))
YOUTUBE_TOKEN_FILE = str(BASE_DIR / "token_youtube.json")
YOUTUBE_PRIVACY_STATUS = os.getenv("YOUTUBE_PRIVACY_STATUS", "public") # "public", "private", "unlisted"

# Meta (Instagram & Facebook) Upload Settings
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "")

# FFmpeg Executable Resolution
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
