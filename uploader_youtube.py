import os
import json
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from config import (
    YOUTUBE_CLIENT_SECRETS_FILE,
    YOUTUBE_TOKEN_FILE,
    YOUTUBE_PRIVACY_STATUS
)

YOUTUBE_UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube.upload"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_authenticated_service():
    """
    Handles YouTube OAuth2 authentication flow.
    Saves credentials to token_youtube.json for zero-touch automatic re-authentication.
    """
    creds = None
    token_path = Path(YOUTUBE_TOKEN_FILE)
    secrets_path = Path(YOUTUBE_CLIENT_SECRETS_FILE)

    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), YOUTUBE_UPLOAD_SCOPE)
        except Exception as e:
            print(f"[YouTube Auth] Existing token invalid ({e}), requesting new token.")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[YouTube Auth] Refreshing expired token...")
            creds.refresh(Request())
        else:
            if not secrets_path.exists():
                raise FileNotFoundError(
                    f"\n[YouTube Auth Error] '{secrets_path.name}' not found!\n"
                    f"Please download your OAuth client credentials from Google Cloud Console\n"
                    f"and save it as: {secrets_path.resolve()}"
                )
            print("[YouTube Auth] Initiating browser login for one-time YouTube approval...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(secrets_path),
                YOUTUBE_UPLOAD_SCOPE
            )
            creds = flow.run_local_server(port=0)

        # Save credentials for future automatic uploads
        with open(token_path, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())
        print(f"[YouTube Auth] Saved credentials token to {token_path.name}")

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=creds)

def upload_short_to_youtube(
    video_file_path: str,
    title: str,
    description: str,
    tags: list = None,
    privacy_status: str = YOUTUBE_PRIVACY_STATUS
) -> str:
    """
    Uploads a short video directly to YouTube as a #Shorts video.
    Returns the uploaded video ID and URL.
    """
    video_file = Path(video_file_path)
    if not video_file.exists():
        raise FileNotFoundError(f"Video file not found: {video_file_path}")

    # Ensure title contains #Shorts for YouTube algorithm detection
    formatted_title = title if "#Shorts" in title else f"{title} #Shorts"
    formatted_tags = tags or ["Shorts", "DarkPsychology", "PsychologyFacts", "HumanBehavior", "Stoicism", "Mindset", "Viral"]

    body = {
        "snippet": {
            "title": formatted_title[:100],
            "description": f"{description}\n\nSubscribe for daily dark psychology insights!\n#Shorts #Viral #Psychology #DarkPsychology #HumanBehavior #Mindset",
            "tags": formatted_tags,
            "categoryId": "27", # Category 27 = Education
            "defaultLanguage": "en-US",
            "defaultAudioLanguage": "en-US"
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    youtube = get_authenticated_service()

    media = MediaFileUpload(
        str(video_file),
        mimetype="video/mp4",
        chunksize=1024 * 1024 * 2,
        resumable=True
    )

    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media
    )

    print(f"[YouTube Upload] Uploading '{video_file.name}' to YouTube Shorts ({privacy_status})...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"[YouTube Upload] Upload progress: {progress}%")

    video_id = response.get("id")
    video_url = f"https://youtube.com/shorts/{video_id}"
    print(f"[YouTube Upload] SUCCESS! Video is live at: {video_url}")
    return video_url

if __name__ == "__main__":
    print("YouTube uploader module loaded.")
