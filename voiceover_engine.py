import os
import time
import asyncio
import re
import subprocess
from pathlib import Path
import edge_tts
from config import DEFAULT_VOICE, VOICE_RATE, VOICE_PITCH, FFMPEG_EXE

async def _edge_tts_stream_to_file(text: str, output_audio: Path, output_srt_path: str = None, voice: str = None):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=VOICE_RATE,
        pitch=VOICE_PITCH
    )
    submaker = edge_tts.SubMaker()
    with open(output_audio, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)

    if output_srt_path:
        with open(output_srt_path, "w", encoding="utf-8") as srt_file:
            srt_file.write(submaker.get_srt())

async def generate_scene_voiceover(text: str, output_audio_path: str, output_srt_path: str = None, voice: str = None) -> float:
    """
    Generates realistic neural voiceover for the given text with auto-retry and alternate voice fallbacks.
    Supports both English (en-US-ChristopherNeural) and Hindi (hi-IN-MadhurNeural).
    """
    output_audio = Path(output_audio_path)
    output_audio.parent.mkdir(parents=True, exist_ok=True)

    clean_text = text.strip()
    if not clean_text:
        clean_text = "..."

    selected_voice = voice or DEFAULT_VOICE
    
    # Alternative voice fallbacks in case of Microsoft TTS temporary glitches
    alt_voice = "hi-IN-SwaraNeural" if "hi-" in selected_voice.lower() else "en-US-GuyNeural"

    last_error = None
    for attempt in range(1, 4):
        voice_to_use = selected_voice if attempt < 3 else alt_voice
        try:
            await _edge_tts_stream_to_file(clean_text, output_audio, output_srt_path, voice=voice_to_use)
            if output_audio.exists() and output_audio.stat().st_size > 1000:
                duration = get_audio_duration(str(output_audio))
                return duration
        except Exception as e:
            last_error = e
            time.sleep(0.8 * attempt)

    print(f"[Voiceover] Warning: Edge TTS retries exhausted ({last_error}), generating fallback audio track.")
    # Safe fallback: Generate 4s silent audio with FFmpeg if Edge TTS network drops
    try:
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        subprocess.run(
            [FFMPEG_EXE, "-y", "-nostdin", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "4", str(output_audio)],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=creationflags
        )
        return 4.0
    except Exception:
        return 4.0

def get_audio_duration(audio_path: str) -> float:
    """
    Uses FFmpeg to accurately determine audio file duration in seconds.
    """
    cmd = [FFMPEG_EXE, "-nostdin", "-i", audio_path]
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    process = subprocess.run(
        cmd,
        stdin=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        errors="ignore",
        creationflags=creationflags
    )
    # Matches Duration: 00:00:05.12
    match = re.search(r"Duration:\s*(\d{2}):(\d{2}):(\d{2}\.\d+)", process.stderr)
    if match:
        hours = float(match.group(1))
        minutes = float(match.group(2))
        seconds = float(match.group(3))
        return hours * 3600 + minutes * 60 + seconds
    return 10.0 # fallback estimate

def create_voiceover_for_script(scenes: list, work_dir: Path, voice: str = None, text_key: str = "narration") -> dict:
    """
    Takes scenes list from content_generator and generates audio files for each scene
    as well as a master concatenated audio track with subtitles.
    Supports English or Hindi neural voiceover.
    """
    audio_files = []
    durations = []
    
    selected_voice = voice or DEFAULT_VOICE
    full_text = " ".join([s.get(text_key, s.get("narration", "")) for s in scenes])
    master_audio_path = work_dir / f"master_voiceover_{selected_voice[:5]}.mp3"
    master_srt_path = work_dir / f"subtitles_{selected_voice[:5]}.srt"

    # Generate master track with subtitles
    master_duration = asyncio.run(
        generate_scene_voiceover(full_text, str(master_audio_path), str(master_srt_path), voice=selected_voice)
    )

    # Generate individual scene audios to know exact duration per scene for visual timing
    for idx, scene in enumerate(scenes):
        time.sleep(0.3)
        scene_audio = work_dir / f"scene_{idx}_{selected_voice[:5]}.mp3"
        scene_text = scene.get(text_key, scene.get("narration", ""))
        dur = asyncio.run(generate_scene_voiceover(scene_text, str(scene_audio), voice=selected_voice))
        audio_files.append(str(scene_audio))
        durations.append(dur)

    return {
        "master_audio": str(master_audio_path),
        "master_srt": str(master_srt_path),
        "master_duration": master_duration,
        "scene_audios": audio_files,
        "scene_durations": durations
    }

if __name__ == "__main__":
    from pathlib import Path
    test_scenes = [
        {"narration": "First dark psychology rule: Silence makes people panic."},
        {"narration": "Second rule: Never apologize when you did nothing wrong."}
    ]
    test_dir = Path("./temp_test")
    test_dir.mkdir(exist_ok=True)
    res = create_voiceover_for_script(test_scenes, test_dir)
    print("Master duration:", res["master_duration"])
    print("Scene durations:", res["scene_durations"])
