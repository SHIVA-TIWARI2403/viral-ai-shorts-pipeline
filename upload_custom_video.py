import os
import sys
from pathlib import Path

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from uploader_youtube import upload_short_to_youtube
from uploader_buffer import post_to_all_socials_buffer

VIDEO_PATH = r"C:\Users\SHIVA TIWARI\.gemini\antigravity\brain\e1ec1810-f427-48e6-96ca-74b57954b457\.user_uploaded\media_1794279692008_86debecf.mp4"

TITLE_YT = "Billionaire Lion Boss Attitude 🦁🔥 | Real Sigma Rule #Shorts"
DESC_YT = (
    "Pump khareedne aaya tha, ab poora shehar khareed loonga! 🦁\n"
    "Billionaire Lion Boss Attitude Status.\n\n"
    "Subscribe for daily viral 3D animation shorts!\n"
    "#Shorts #LionAttitude #SigmaRule #Billionaire #Viral #AttitudeStatus #3DAnimation"
)
TAGS_YT = ["Shorts", "BillionaireLion", "LionAttitude", "SigmaRule", "AttitudeStatus", "Viral", "3DAnimation"]

CAPTION_INSTA = (
    "करोड़पति शेर का एटीट्यूड 🦁🔥 \"अब पूरा शहर खरीद लूँगा!\"\n.\n.\n"
    "Follow @ai_with_shiv24 for daily viral 3D animations! 🚀\n"
    "#billionairelion #lionattitude #sigmarule #attitudestatus #viralreels #reelsindia #trendingreels #3danimation #fyp"
)

CAPTION_FB = (
    "करोड़पति शेर का एटीट्यूड 🦁🔥 \"अब पूरा शहर खरीद लूँगा!\"\n.\n.\n"
    "#BillionaireLion #LionAttitude #SigmaRule #AttitudeStatus #TrendingReels #ViralVideos #3DAnimation"
)

def main():
    print("=" * 60)
    print("[*] Uploading Custom Video to YouTube, Instagram & Facebook...")
    print(f"[*] Target Video: {VIDEO_PATH}")
    print("=" * 60)

    # 1. YouTube Shorts Upload
    yt_url = None
    try:
        print("\n[Step 1/2] Uploading to YouTube Shorts...")
        yt_url = upload_short_to_youtube(
            video_file_path=VIDEO_PATH,
            title=TITLE_YT,
            description=DESC_YT,
            tags=TAGS_YT,
            privacy_status="public"
        )
        print(f"[YouTube] SUCCESS! Live at: {yt_url}")
    except Exception as e:
        print(f"[YouTube] ERROR: {e}")

    # 2. Instagram Reels & Facebook Upload via Buffer
    social_res = {}
    try:
        print("\n[Step 2/2] Uploading to Instagram Reels & Facebook Page...")
        social_res = post_to_all_socials_buffer(
            caption_insta=CAPTION_INSTA,
            caption_fb=CAPTION_FB,
            local_video_path=VIDEO_PATH
        )
        print(f"[Socials] Result: {social_res}")
    except Exception as e:
        print(f"[Socials] ERROR: {e}")

    print("\n" + "=" * 60)
    print("[*] COMPLETED CUSTOM UPLOAD!")
    print(f"YouTube: {yt_url}")
    print(f"Instagram & Facebook: {social_res}")
    print("=" * 60)

if __name__ == "__main__":
    main()
