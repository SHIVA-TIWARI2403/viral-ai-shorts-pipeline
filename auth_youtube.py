import sys
import os
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from google_auth_oauthlib.flow import InstalledAppFlow
from uploader_youtube import YOUTUBE_UPLOAD_SCOPE, upload_short_to_youtube
from config import YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_TOKEN_FILE

def authenticate_and_upload():
    secrets_path = Path(YOUTUBE_CLIENT_SECRETS_FILE)
    token_path = Path(YOUTUBE_TOKEN_FILE)

    print("[*] Loading client_secret.json...")
    flow = InstalledAppFlow.from_client_secrets_file(
        str(secrets_path),
        YOUTUBE_UPLOAD_SCOPE
    )

    port = 8080
    flow.redirect_uri = f"http://localhost:{port}/"
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

    print("\n" + "=" * 60)
    print("OPEN THIS URL IN CHROME:")
    print(auth_url)
    print("=" * 60 + "\n")

    with open("AUTH_URL.txt", "w", encoding="utf-8") as f:
        f.write(auth_url)

    print("[*] Waiting for authorization in browser...")
    creds = flow.run_local_server(port=port, open_browser=True)

    with open(token_path, "w", encoding="utf-8") as f:
        f.write(creds.to_json())

    print("[*] SUCCESS! YouTube credentials saved to token_youtube.json")

    video_file = "output/20261104_164532_the_silent_interrogation_force_the_.mp4"
    title = "The Silent Interrogation: Force the Truth #Shorts"
    desc = "Here is how to force anyone to reveal the truth using dark psychology silence tricks. #Shorts #Viral"
    tags = ["Shorts", "DarkPsychology", "Psychology", "Facts", "Viral"]

    print("[*] Uploading video to YouTube Shorts now...")
    url = upload_short_to_youtube(video_file, title, desc, tags)
    print(f"\n[DONE] VIDEO IS LIVE ON YOUTUBE SHORTS: {url}")

if __name__ == "__main__":
    authenticate_and_upload()
