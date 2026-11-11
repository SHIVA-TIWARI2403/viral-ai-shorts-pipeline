import os
import time
import requests
from pathlib import Path
from config import (
    INSTAGRAM_ACCESS_TOKEN,
    INSTAGRAM_ACCOUNT_ID,
    FACEBOOK_PAGE_ACCESS_TOKEN,
    FACEBOOK_PAGE_ID
)

META_GRAPH_API_VERSION = "v19.0"
BASE_GRAPH_URL = f"https://graph.facebook.com/{META_GRAPH_API_VERSION}"

def upload_reel_to_instagram(video_url_or_path: str, caption: str, hashtags: list = None) -> str:
    """
    Publishes a Reel to Instagram via Meta Graph Content Publishing API.
    Requirements:
    - Instagram Business or Creator Account linked to a Facebook Page.
    - Long-Lived User Access Token with 'instagram_content_publish' permission.
    """
    if not INSTAGRAM_ACCESS_TOKEN or not INSTAGRAM_ACCOUNT_ID:
        print("[Instagram Upload] Skipped: INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_ACCOUNT_ID not configured in .env")
        return ""

    full_caption = caption
    if hashtags:
        full_caption += "\n\n" + " ".join(hashtags)

    print(f"[Instagram Upload] Initializing Reel container for Account {INSTAGRAM_ACCOUNT_ID}...")

    # Step 1: Create Container
    container_url = f"{BASE_GRAPH_URL}/{INSTAGRAM_ACCOUNT_ID}/media"
    container_payload = {
        "media_type": "REELS",
        "video_url": video_url_or_path, # Must be a publicly accessible URL for Meta servers to download
        "caption": full_caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }

    resp = requests.post(container_url, data=container_payload, timeout=30)
    res_data = resp.json()

    if "id" not in res_data:
        raise RuntimeError(f"Failed to create Instagram Reel container: {res_data}")

    container_id = res_data["id"]
    print(f"[Instagram Upload] Container created (ID: {container_id}). Waiting for media processing...")

    # Step 2: Poll container status until READY
    status_url = f"{BASE_GRAPH_URL}/{container_id}"
    for attempt in range(15):
        time.sleep(5)
        status_resp = requests.get(status_url, params={"fields": "status_code", "access_token": INSTAGRAM_ACCESS_TOKEN})
        status_data = status_resp.json()
        code = status_data.get("status_code")
        print(f"[Instagram Upload] Media processing status: {code} (Check {attempt+1}/15)")
        if code == "FINISHED":
            break
        elif code == "ERROR":
            raise RuntimeError(f"Instagram media processing failed: {status_data}")

    # Step 3: Publish Reel
    publish_url = f"{BASE_GRAPH_URL}/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_payload = {
        "creation_id": container_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    pub_resp = requests.post(publish_url, data=publish_payload, timeout=30)
    pub_data = pub_resp.json()

    if "id" in pub_data:
        media_id = pub_data["id"]
        print(f"[Instagram Upload] SUCCESS! Reel published with ID: {media_id}")
        return f"https://www.instagram.com/reel/{media_id}"
    else:
        raise RuntimeError(f"Failed to publish Instagram Reel: {pub_data}")

def upload_video_to_facebook_page(video_file_path: str, title: str, description: str, hashtags: list = None) -> str:
    """
    Publishes video/reel to Facebook Page via Meta Graph API.
    """
    if not FACEBOOK_PAGE_ACCESS_TOKEN or not FACEBOOK_PAGE_ID:
        print("[Facebook Upload] Skipped: FACEBOOK_PAGE_ACCESS_TOKEN or FACEBOOK_PAGE_ID not configured in .env")
        return ""

    video_path = Path(video_file_path)
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_file_path}")

    full_description = description
    if hashtags:
        full_description += "\n\n" + " ".join(hashtags)

    upload_url = f"{BASE_GRAPH_URL}/{FACEBOOK_PAGE_ID}/videos"
    print(f"[Facebook Upload] Uploading '{video_path.name}' to Facebook Page ({FACEBOOK_PAGE_ID})...")

    with open(video_path, "rb") as video_file:
        files = {
            "source": (video_path.name, video_file, "video/mp4")
        }
        data = {
            "title": title,
            "description": full_description,
            "access_token": FACEBOOK_PAGE_ACCESS_TOKEN
        }
        resp = requests.post(upload_url, data=data, files=files, timeout=120)
        res_data = resp.json()

    if "id" in res_data:
        video_id = res_data["id"]
        post_url = f"https://www.facebook.com/{video_id}"
        print(f"[Facebook Upload] SUCCESS! Video published to Facebook: {post_url}")
        return post_url
    else:
        raise RuntimeError(f"Failed to publish to Facebook Page: {res_data}")

if __name__ == "__main__":
    print("Meta (Instagram/Facebook) uploader module loaded.")
