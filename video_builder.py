import os
import subprocess
import shutil
import random
from pathlib import Path
from config import FFMPEG_EXE, VIDEO_WIDTH, VIDEO_HEIGHT, FPS, ASSETS_DIR

def build_short_video(
    image_paths: list,
    scene_durations: list,
    master_audio_path: str,
    master_srt_path: str,
    output_video_path: str,
    work_dir: Path
) -> str:
    """
    Renders a vertical 9:16 (1080x1920) cinematic short video:
    - Dynamic Ken Burns camera motion (slow zoom/pan) on every visual scene.
    - Crisp neural voiceover track.
    - Low-frequency ambient tension background sound.
    - Burned-in, high-retention kinetic subtitles (bright yellow & bold black outline).
    """
    output_video = Path(output_video_path)
    output_video.parent.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    # 1. Render animated clips with Ken Burns camera motion for each scene
    clip_files = []
    print(f"[VideoBuilder] Preparing {len(image_paths)} visual cuts (Video/Animated)...")
    for idx, (img_path, duration) in enumerate(zip(image_paths, scene_durations)):
        clip_name = f"clip_{idx}.mp4"
        clip_path = work_dir / clip_name
        dur = max(duration, 1.2)
        total_frames = max(int(dur * FPS), 30)

        is_video_clip = str(img_path).lower().endswith(".mp4")
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

        if is_video_clip:
            # Scale and crop the Gemini video clip to 1080x1920 and match scene duration
            clip_cmd = [
                FFMPEG_EXE, "-y", "-nostdin",
                "-stream_loop", "-1", "-i", str(Path(img_path).resolve()),
                "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},fps={FPS},format=yuv420p",
                "-t", f"{dur:.2f}",
                "-an",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "20",
                str(clip_path.resolve())
            ]
        else:
            # Multi-directional dynamic camera motion: 4 rotating cinematic presets
            motion_type = idx % 4
            if motion_type == 0:
                # Cinematic Zoom-In
                zoom_expr = f"zoompan=z='min(zoom+0.0016,1.20)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            elif motion_type == 1:
                # Cinematic Zoom-Out
                zoom_expr = f"zoompan=z='max(1.20-0.0016*on,1.0)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            elif motion_type == 2:
                # Pan Down with slight zoom
                zoom_expr = f"zoompan=z='1.12':d={total_frames}:x='iw/2-(iw/zoom/2)':y='min((ih-ih/zoom)*(on/{total_frames}),ih-ih/zoom)'"
            else:
                # Pan Up with slight zoom
                zoom_expr = f"zoompan=z='1.12':d={total_frames}:x='iw/2-(iw/zoom/2)':y='max((ih-ih/zoom)*(1-on/{total_frames}),0)'"

            clip_cmd = [
                FFMPEG_EXE, "-y", "-nostdin",
                "-loop", "1", "-i", str(Path(img_path).resolve()),
                "-vf", f"{zoom_expr}:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:fps={FPS},format=yuv420p",
                "-t", f"{dur:.2f}",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "20",
                str(clip_path.resolve())
            ]

        subprocess.run(
            clip_cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            errors="ignore",
            check=True,
            creationflags=creationflags
        )
        clip_files.append(clip_name)

    # 2. Write concat list for animated clips
    concat_list = work_dir / "concat_clips.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for c in clip_files:
            f.write(f"file '{c}'\n")

    # 3. Subtitles setup
    local_srt_name = "subtitles.srt"
    local_srt_path = work_dir / local_srt_name
    if Path(master_srt_path).resolve() != local_srt_path.resolve():
        shutil.copyfile(master_srt_path, local_srt_path)

    has_subtitles = False
    try:
        if local_srt_path.exists() and local_srt_path.stat().st_size > 10:
            has_subtitles = True
    except Exception:
        has_subtitles = False

    # Dynamic subtitle colors: Rotate between high-contrast viral shades
    PRIMARY_COLORS = [
        "&H0000FFFF",  # Electric Neon Yellow
        "&H00FFFF00",  # Cyber Cyan
        "&H0033FF00",  # Neon Acid Lime
        "&H00FFFFFF"   # Clean Hyper White
    ]
    sub_color = random.choice(PRIMARY_COLORS)

    sub_style = (
        "FontName=Arial,"
        "FontSize=22,"
        "Bold=1,"
        f"PrimaryColour={sub_color},"
        "OutlineColour=&H00000000,"
        "BorderStyle=1,"
        "Outline=3,"
        "Shadow=1.5,"
        "Alignment=2,"
        "MarginV=360"
    )

    # 4. Dynamic background soundtrack selection
    bg_tracks = [t for t in ASSETS_DIR.glob("*.mp3") if t.is_file()]
    if bg_tracks:
        bg_music_path = random.choice(bg_tracks)
        print(f"[VideoBuilder] Dynamic soundtrack chosen: {bg_music_path.name}")
        has_bg_music = True
    else:
        bg_music_path = ASSETS_DIR / "dark_ambient.mp3"
        has_bg_music = bg_music_path.exists()

    # 5. Final Concat & Audio Subtitle Pass
    cmd = [
        FFMPEG_EXE, "-y", "-nostdin",
        "-f", "concat",
        "-safe", "0",
        "-i", "concat_clips.txt",
        "-i", str(Path(master_audio_path).resolve())
    ]

    video_filter = "null"
    if has_subtitles:
        video_filter = f"subtitles={local_srt_name}:force_style='{sub_style}'"

    if has_bg_music:
        cmd.extend(["-i", str(bg_music_path.resolve())])
        filter_complex = (
            f"[0:v]{video_filter}[v];"
            f"[1:a]volume=1.0[voice];"
            f"[2:a]volume=0.15[bg];"
            f"[voice][bg]amix=inputs=2:duration=first:dropout_transition=2[a]"
        )
        cmd.extend([
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "[a]"
        ])
    else:
        cmd.extend([
            "-vf", video_filter,
            "-map", "0:v",
            "-map", "1:a"
        ])

    cmd.extend([
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "21",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-c:a", "aac",
        "-b:a", "192k",
        "-r", str(FPS),
        "-shortest",
        str(output_video.resolve())
    ])

    print(f"[VideoBuilder] Finalizing cinematic render to: {output_video.name}...")
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    proc = subprocess.run(
        cmd,
        cwd=str(work_dir),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="ignore",
        creationflags=creationflags
    )

    if proc.returncode != 0:
        print("[VideoBuilder] Error:\n", proc.stderr[-800:])
        raise RuntimeError(f"FFmpeg failed with exit code {proc.returncode}")

    print(f"[VideoBuilder] SUCCESS! Video created: {output_video.resolve()}")
    return str(output_video.resolve())
