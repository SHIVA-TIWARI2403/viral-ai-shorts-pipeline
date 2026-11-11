import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from uploader_buffer import upload_video_to_supabase, post_to_buffer_channel, BUFFER_FACEBOOK_CHANNEL_ID

fb_video_path = SCRIPT_DIR / "temp_fb_1080.mp4"

def main():
    print(f"[*] Uploading 1080p video to Supabase: {fb_video_path.name}")
    cdn_url = upload_video_to_supabase(str(fb_video_path))
    print(f"[*] CDN URL Ready: {cdn_url}")

    caption_fb = (
        "करोड़पति शेर का एटीट्यूड 🦁🔥 \"अब पूरा शहर खरीद लूँगा!\"\n.\n.\n"
        "#BillionaireLion #LionAttitude #SigmaRule #AttitudeStatus #TrendingReels #ViralVideos #3DAnimation"
    )

    res = post_to_buffer_channel(BUFFER_FACEBOOK_CHANNEL_ID, caption_fb, cdn_url, platform_name="Facebook")
    print(f"[Facebook Result]: {res}")

    if fb_video_path.exists():
        fb_video_path.unlink()
        print("[*] SUCCESS: temp_fb_1080.mp4 deleted from laptop (Zero-Disk Mode)!")

if __name__ == "__main__":
    main()
