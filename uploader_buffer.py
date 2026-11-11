import os
import sys
import time
import requests
from pathlib import Path
from config import BASE_DIR
from dotenv import load_dotenv

load_dotenv(BASE_DIR / ".env")

BUFFER_ACCESS_TOKEN = os.getenv("BUFFER_ACCESS_TOKEN", "PusyzNtSvSHFlLIGi1yzLLmA4Fl_5kLFHQ8t51-59MH")
BUFFER_INSTAGRAM_CHANNEL_ID = os.getenv("BUFFER_INSTAGRAM_CHANNEL_ID", "6aeb2da7e29c69a1715c9ba7")
BUFFER_FACEBOOK_CHANNEL_ID = os.getenv("BUFFER_FACEBOOK_CHANNEL_ID", "6aeb3fece29c69a1715d8b02")
BUFFER_GRAPHQL_URL = "https://api.buffer.com/graphql"

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://aljlnisvrveuwlishgyv.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFsamxuaXN2cnZldXdsaXNoZ3l2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTMzNjIwNTQsImV4cCI6MjEwODkzODA1NH0.d3g45738VxcaNuP-7zkzhlqGSlrDb_pQBVCJAK5cuHM")
SUPABASE_BUCKET = "videos"

def upload_video_to_supabase(local_mp4_path: str) -> str:
    """
    Uploads a local MP4 file to Supabase Public Storage and returns the public CDN URL.
    Includes automated retries and binary buffer reuse to handle network flakiness.
    """
    path = Path(local_mp4_path)
    if not path.exists():
        raise FileNotFoundError(f"Video not found: {local_mp4_path}")

    filename = path.name
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "video/mp4",
        "x-upsert": "true"
    }

    size_mb = path.stat().st_size / (1024 * 1024)
    print(f"[*] Uploading video to Supabase Storage CDN: {filename} ({size_mb:.1f} MB)...")
    
    with open(path, "rb") as f:
        video_bytes = f.read()

    last_error = None
    for attempt in range(1, 4):
        try:
            resp = requests.post(
                f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{filename}",
                headers=headers,
                data=video_bytes,
                timeout=90
            )
            if resp.status_code in (200, 201):
                public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{filename}"
                print(f"[*] Video CDN URL Ready: {public_url}")
                return public_url
            else:
                last_error = f"Status {resp.status_code}: {resp.text}"
                print(f"[Supabase Upload] Attempt {attempt}/3 returned error: {last_error}")
        except Exception as e:
            last_error = str(e)
            print(f"[Supabase Upload] Attempt {attempt}/3 failed: {last_error}")
        
        time.sleep(3 * attempt)

    raise RuntimeError(f"Supabase upload failed after 3 attempts: {last_error}")

def post_to_buffer_channel(channel_id: str, caption: str, video_url: str = None, service_name: str = "Channel") -> bool:
    """
    Publishes a video/reel to a specific connected Buffer channel (Instagram or Facebook).
    Uses Buffer's official GraphQL API with verified schema.
    """
    if not BUFFER_ACCESS_TOKEN or not channel_id:
        print(f"[Buffer {service_name}] Missing token or channel ID.")
        return False

    headers = {
        "Authorization": f"Bearer {BUFFER_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post {
            id
            status
          }
        }
        ... on InvalidInputError {
          message
        }
        ... on UnexpectedError {
          message
        }
      }
    }
    """

    payload = {
        "channelId": channel_id,
        "text": caption,
        "mode": "shareNow",
        "schedulingType": "automatic"
    }

    # Social platform Reel metadata
    if service_name.lower() == "instagram":
        payload["metadata"] = {
            "instagram": {
                "type": "reel",
                "shouldShareToFeed": True
            }
        }
    elif service_name.lower() == "facebook":
        payload["metadata"] = {
            "facebook": {
                "type": "reel"
            }
        }

    # Video Asset attachment
    if video_url:
        payload["assets"] = [{
            "video": {
                "url": video_url
            }
        }]

    try:
        resp = requests.post(
            BUFFER_GRAPHQL_URL,
            headers=headers,
            json={"query": mutation, "variables": {"input": payload}},
            timeout=30
        )
        data = resp.json()
        print(f"[Buffer {service_name}] Response:", data)
        create_res = data.get("data", {}).get("createPost", {})
        if "post" in create_res:
            post_id = create_res["post"].get("id")
            post_status = create_res["post"].get("status")
            print(f"[Buffer {service_name}] SUCCESS! Post ID: {post_id}, Status: {post_status}")
            return True
        else:
            err_msg = create_res.get("message", str(data))
            print(f"[Buffer {service_name}] Failed: {err_msg}")
            return False
    except Exception as e:
        print(f"[Buffer {service_name}] Exception: {e}")
        return False

def post_to_all_socials_buffer(caption_insta: str, caption_fb: str, local_video_path: str = None, video_url: str = None) -> dict:
    """
    Publishes simultaneously to both Instagram and Facebook Page via Buffer.
    Automatically uploads local MP4 to Supabase CDN if video_url is not provided.
    """
    results = {}

    # Step 1: Ensure we have a public CDN video URL
    if not video_url and local_video_path:
        try:
            video_url = upload_video_to_supabase(local_video_path)
        except Exception as e:
            print(f"[Buffer Socials] Failed to upload video to CDN: {e}")
            return results

    if not video_url:
        print("[Buffer Socials] No video URL or valid local file provided.")
        return results

    # Step 2: Instagram Reel (Hindi voiceover)
    if BUFFER_INSTAGRAM_CHANNEL_ID:
        print(f"[*] Dispatching Hindi Reel to Instagram (@ai_with_shiv24)...")
        ok_ig = post_to_buffer_channel(BUFFER_INSTAGRAM_CHANNEL_ID, caption_insta, video_url, "Instagram")
        if ok_ig:
            results["instagram"] = "Published to Instagram Reel (@ai_with_shiv24)"

    # Step 3: Facebook Page (Hindi voiceover)
    if BUFFER_FACEBOOK_CHANNEL_ID:
        print(f"[*] Dispatching Hindi Video to Facebook Page...")
        ok_fb = post_to_buffer_channel(BUFFER_FACEBOOK_CHANNEL_ID, caption_fb, video_url, "Facebook")
        if ok_fb:
            results["facebook"] = "Published to Facebook Page"
    else:
        print("[*] Note: BUFFER_FACEBOOK_CHANNEL_ID not set in .env. Skipping Facebook auto-post.")

    return results

if __name__ == "__main__":
    print("Buffer multi-channel uploader ready.")
