import os
import sys
import time
import argparse
import shutil
from datetime import datetime
from pathlib import Path

# Base directory for logging
SCRIPT_DIR = Path(__file__).resolve().parent
log_path = SCRIPT_DIR / "auto_upload.log"

# Robust Auto-Logger: captures both terminal (if present) and file output safely
class TeeLogger:
    def __init__(self, filename, original_stream=None, shared_file=None):
        self.terminal = original_stream
        if shared_file:
            self.logfile = shared_file
        else:
            try:
                self.logfile = open(filename, "a", encoding="utf-8", errors="replace")
            except Exception:
                self.logfile = None

    def write(self, message):
        if self.terminal:
            try:
                self.terminal.write(message)
            except Exception:
                pass
        if self.logfile:
            try:
                self.logfile.write(message)
                self.logfile.flush()
            except Exception:
                pass

    def flush(self):
        if self.terminal:
            try:
                self.terminal.flush()
            except Exception:
                pass
        if self.logfile:
            try:
                self.logfile.flush()
            except Exception:
                pass

# Safely wrap sys.stdout and sys.stderr (handles pythonw where streams are None, never crashes on file locks)
try:
    _shared_log = open(log_path, "a", encoding="utf-8", errors="replace")
except Exception:
    _shared_log = None

sys.stdout = TeeLogger(log_path, sys.stdout, shared_file=_shared_log)
sys.stderr = TeeLogger(log_path, sys.stderr, shared_file=_shared_log)

from config import (
    BASE_DIR,
    OUTPUT_DIR,
    TEMP_DIR,
    YOUTUBE_CLIENT_SECRETS_FILE
)

from content_generator import generate_viral_content
from voiceover_engine import create_voiceover_for_script
from visuals_generator import generate_visuals_for_scenes
from video_builder import build_short_video
from uploader_youtube import upload_short_to_youtube
from uploader_buffer import post_to_all_socials_buffer

ENGLISH_VOICE = "en-US-ChristopherNeural"
HINDI_VOICE = "hi-IN-MadhurNeural"

def run_single_pipeline(topic_hint: str = None, upload_targets: list = None) -> dict:
    """
    Dual-Language Autonomous Pipeline:
    1. Generates English video -> Uploads to YouTube Shorts.
    2. Generates Hindi video -> Uploads to Instagram Reels & Facebook.
    """
    start_time = time.time()
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    work_dir = TEMP_DIR / f"run_{session_id}"
    work_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 60)
    print(f"[*] [START] Dual-Language AI Shorts Pipeline: {session_id}")
    print("=" * 60)

    # STEP 1: Content & Script Generation
    print("\n[Step 1/5] Generating Bilingual Topic & Retention Scripts (Gemini Pro)...")
    content = generate_viral_content(topic_hint)
    title_en = content.get("title_en", content.get("title", "Dark Psychology Secrets"))
    title_hi = content.get("title_hi", "Dark Psychology Secrets in Hindi")
    print(f"  [EN] Title: {title_en}")
    print(f"  [HI] Title: {title_hi}")
    print(f"  Total Scenes: {len(content['scenes'])}")

    # STEP 2: Visuals Generation (Shared between EN and HI)
    print("\n[Step 2/5] Generating 9:16 Cinematic AI Visuals...")
    image_paths = generate_visuals_for_scenes(content["scenes"], work_dir)
    print(f"  {len(image_paths)} visual scenes ready.")

    # STEP 3: Voiceover Generation
    # English Voiceover (YouTube)
    print("\n[Step 3/5] Generating English Voiceover (YouTube Shorts)...")
    voice_en = create_voiceover_for_script(content["scenes"], work_dir, voice=ENGLISH_VOICE, text_key="narration_en")
    print(f"  [EN] Duration: {voice_en['master_duration']:.1f}s")

    # Hindi Voiceover (Instagram & Facebook)
    print("Generating Hindi Voiceover (Instagram Reels & Facebook)...")
    voice_hi = create_voiceover_for_script(content["scenes"], work_dir, voice=HINDI_VOICE, text_key="narration_hi")
    print(f"  [HI] Duration: {voice_hi['master_duration']:.1f}s")

    # STEP 4: Video Assembly
    print("\n[Step 4/5] Assembling Final Videos...")
    slug = "".join(c for c in title_en if c.isalnum() or c in (" ", "_", "-")).rstrip().lower().replace(" ", "_")[:30]
    
    # 4A. English Video
    en_video_path = OUTPUT_DIR / f"{session_id}_EN_{slug}.mp4"
    final_video_en = build_short_video(
        image_paths=image_paths,
        scene_durations=voice_en["scene_durations"],
        master_audio_path=voice_en["master_audio"],
        master_srt_path=voice_en["master_srt"],
        output_video_path=str(en_video_path),
        work_dir=work_dir / "work_en"
    )
    print(f"  [EN Video Ready] {final_video_en}")

    # 4B. Hindi Video
    hi_video_path = OUTPUT_DIR / f"{session_id}_HI_{slug}.mp4"
    final_video_hi = build_short_video(
        image_paths=image_paths,
        scene_durations=voice_hi["scene_durations"],
        master_audio_path=voice_hi["master_audio"],
        master_srt_path=voice_hi["master_srt"],
        output_video_path=str(hi_video_path),
        work_dir=work_dir / "work_hi"
    )
    print(f"  [HI Video Ready] {final_video_hi}")

    # STEP 5: Publishing
    upload_results = {}
    if upload_targets:
        print("\n[Step 5/5] Publishing to Platforms...")

        # 5A. YouTube Shorts Upload (ENGLISH)
        if "youtube" in upload_targets:
            if Path(YOUTUBE_CLIENT_SECRETS_FILE).exists() or Path(BASE_DIR / "token_youtube.json").exists():
                try:
                    yt_url = upload_short_to_youtube(
                        video_file_path=final_video_en,
                        title=title_en,
                        description=content.get("hook_en", ""),
                        tags=content.get("hashtags_yt", [])
                    )
                    upload_results["youtube"] = yt_url
                except Exception as e:
                    print(f"  [!] YouTube Upload Error: {e}")

        # 5B. Instagram Reels & Facebook Upload via Buffer (HINDI)
        if "instagram" in upload_targets or "facebook" in upload_targets:
            try:
                caption_ig = f"{title_hi}\n\n{content.get('hook_hi', '')}\n\n" + " ".join(content.get('hashtags_insta', []))
                caption_fb = f"{title_hi}\n\n{content.get('hook_hi', '')}\n\n" + " ".join(content.get('hashtags_fb', []))
                buf_res = post_to_all_socials_buffer(
                    caption_insta=caption_ig,
                    caption_fb=caption_fb,
                    local_video_path=final_video_hi
                )
                upload_results.update(buf_res)
            except Exception as e:
                print(f"  [!] Social Media Upload Error: {e}")

    # Zero-Disk Storage Mode: Delete all local video files after upload (per user requirement)
    if upload_targets:
        print("\n[*] Zero-Disk Mode: Deleting local video files from laptop (Cloud-only mode)...")
        try:
            if Path(final_video_en).exists():
                Path(final_video_en).unlink(missing_ok=True)
            if Path(final_video_hi).exists():
                Path(final_video_hi).unlink(missing_ok=True)
            print("[*] SUCCESS: Local MP4 files removed from disk. Storage space freed completely.")
        except Exception as e:
            print(f"[!] Cleanup note: {e}")

    # Clean temporary intermediate files
    try:
        shutil.rmtree(work_dir, ignore_errors=True)
    except Exception:
        pass

    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"[COMPLETED] Dual Pipeline finished in {elapsed:.1f} seconds!")
    print(f"English Video (YouTube): {en_video_path.resolve()}")
    print(f"Hindi Video (Instagram/FB): {hi_video_path.resolve()}")
    if upload_results:
        print(f"Published Results: {upload_results}")
    print("=" * 60 + "\n")

    return {
        "video_en": str(en_video_path.resolve()),
        "video_hi": str(hi_video_path.resolve()),
        "uploads": upload_results
    }

def main():
    parser = argparse.ArgumentParser(description="Dual-Language Autonomous AI Shorts & Reels Generator")
    parser.add_argument("--mode", choices=["generate", "upload"], default="generate")
    parser.add_argument("--platform", choices=["all", "youtube", "facebook", "instagram"], default="all")
    parser.add_argument("--topic", type=str, default=None)
    parser.add_argument("--count", type=int, default=1)

    args = parser.parse_args()

    upload_targets = []
    if args.mode == "upload":
        if args.platform == "all":
            upload_targets = ["youtube", "facebook", "instagram"]
        else:
            upload_targets = [args.platform]

    for i in range(args.count):
        run_single_pipeline(topic_hint=args.topic, upload_targets=upload_targets)

if __name__ == "__main__":
    main()
