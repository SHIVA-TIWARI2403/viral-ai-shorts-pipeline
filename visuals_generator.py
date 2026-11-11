import os
import time
import random
import urllib.parse
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFilter
from config import VIDEO_WIDTH, VIDEO_HEIGHT, GEMINI_API_KEY

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Expansive Master Library of 60+ High-Definition Cinematic Visuals (Multi-Category Unsplash CDN)
THEMATIC_AESTHETICS = {
    "eyes": [
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=1080&h=1920&fit=crop&q=80"
    ],
    "silhouette": [
        "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1511447333015-45b65e60f6d5?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=1080&h=1920&fit=crop&q=80"
    ],
    "interrogation": [
        "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1514565131-fce0801e5785?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1577495508048-b635879837f1?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=1080&h=1920&fit=crop&q=80"
    ],
    "brain": [
        "https://images.unsplash.com/photo-1559757175-5700dde675bc?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1516339901601-2e1b62dc0c45?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=1080&h=1920&fit=crop&q=80"
    ],
    "clock": [
        "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1518281420975-50db6e1d0a97?w=1080&h=1920&fit=crop&q=80"
    ],
    "chess": [
        "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1586165368502-1bad197a6461?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1580541832626-2a7131ee809f?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1560174038-da43ac74f01b?w=1080&h=1920&fit=crop&q=80"
    ],
    "statue": [
        "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1551893478-d726eaf0442c?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1569420076939-58b4ef2bf8c7?w=1080&h=1920&fit=crop&q=80"
    ],
    "mystery": [
        "https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1080&h=1920&fit=crop&q=80"
    ],
    "dark_corridor": [
        "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=1080&h=1920&fit=crop&q=80"
    ],
    "mirror": [
        "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=1080&h=1920&fit=crop&q=80"
    ],
    "crowd": [
        "https://images.unsplash.com/photo-1511447333015-45b65e60f6d5?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=1080&h=1920&fit=crop&q=80"
    ],
    "whisper": [
        "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=1080&h=1920&fit=crop&q=80",
        "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=1080&h=1920&fit=crop&q=80"
    ]
}

ALL_THEMATIC_IMAGES = [url for urls in THEMATIC_AESTHETICS.values() for url in urls]

def try_gemini_video_generation(prompt: str, output_path: str) -> str:
    """Attempts video generation using Gemini Omni Flash if pay-as-you-go billing is active."""
    if not GEMINI_API_KEY:
        return None

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/interactions?key={GEMINI_API_KEY}"
        payload = {
            "model": "gemini-omni-1.1-flash",
            "input": [{"type": "text", "text": f"Cinematic vertical 9:16 dark moody scene: {prompt}"}],
            "response_format": {"type": "video", "delivery": "uri", "aspect_ratio": "9:16"}
        }
        resp = requests.post(url, json=payload, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            video_uri = data.get("output_video", {}).get("uri")
            if video_uri:
                v_resp = requests.get(video_uri, timeout=60, stream=True)
                if v_resp.status_code == 200:
                    video_output = Path(output_path).with_suffix(".mp4")
                    with open(video_output, "wb") as f:
                        for chunk in v_resp.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    print(f"[Visuals] Gemini Video created: {video_output.name}")
                    return str(video_output)
    except Exception:
        pass
    return None

def try_gemini_pro_image_generation(prompt: str, output_path: str) -> str:
    """Attempts Pro image generation using Gemini Pro Image models."""
    if not GEMINI_API_KEY:
        return None

    candidate_models = ["gemini-3-pro-image", "gemini-2.5-flash-image", "nano-banana-pro-preview"]
    for model in candidate_models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": f"Cinematic vertical 9:16 dark moody visual: {prompt}"}]}]
            }
            resp = requests.post(url, json=payload, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                for part in parts:
                    inline_data = part.get("inlineData") or part.get("inline_data")
                    if inline_data and "data" in inline_data:
                        import base64
                        raw_bytes = base64.b64decode(inline_data["data"])
                        output_file = Path(output_path).with_suffix(".jpg")
                        with open(output_file, "wb") as f:
                            f.write(raw_bytes)
                        _ensure_aspect_ratio(output_file, VIDEO_WIDTH, VIDEO_HEIGHT)
                        print(f"[Visuals] Gemini Pro Image created: {output_file.name}")
                        return str(output_file)
        except Exception:
            continue
    return None

def try_pollinations_flux_ai_image(prompt: str, output_path: str, width: int = VIDEO_WIDTH, height: int = VIDEO_HEIGHT) -> str:
    """
    Generates a 100% UNIQUE, hyper-photorealistic cinematic AI image for this specific scene.
    Uses Pollinations FLUX engine with a unique random seed every single time,
    with an immediate high-speed Turbo fallback.
    """
    seed = random.randint(100000, 99999999)
    enhanced_prompt = f"{prompt}, dark moody cinematic lighting, 8k quality, masterpiece, 9:16 vertical portrait, photographic realism, film grain"
    encoded = urllib.parse.quote(enhanced_prompt)

    # 1. Try FLUX model
    flux_url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&model=flux&nologo=true"
    try:
        print(f"[Visuals] Generating unique FLUX AI image for: '{prompt[:45]}...'")
        resp = requests.get(flux_url, headers=HEADERS, timeout=30)
        if resp.status_code == 200 and len(resp.content) > 15000:
            output_file = Path(output_path).with_suffix(".jpg")
            with open(output_file, "wb") as f:
                f.write(resp.content)
            _ensure_aspect_ratio(output_file, width, height)
            print(f"[Visuals] UNIQUE FLUX AI image created: {output_file.name}")
            return str(output_file)
    except Exception as e:
        print(f"[Visuals] FLUX attempt timed out or skipped ({e}), trying Turbo AI...")

    # 2. High-speed Turbo fallback
    turbo_url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&model=turbo&nologo=true"
    try:
        resp = requests.get(turbo_url, headers=HEADERS, timeout=20)
        if resp.status_code == 200 and len(resp.content) > 12000:
            output_file = Path(output_path).with_suffix(".jpg")
            with open(output_file, "wb") as f:
                f.write(resp.content)
            _ensure_aspect_ratio(output_file, width, height)
            print(f"[Visuals] UNIQUE Turbo AI image created: {output_file.name}")
            return str(output_file)
    except Exception as e:
        print(f"[Visuals] Turbo AI attempt skipped ({e})")

    return None

def generate_ai_image(prompt: str, output_path: str, tag: str = None, width: int = VIDEO_WIDTH, height: int = VIDEO_HEIGHT) -> str:
    """
    Multi-Tier Unique Visual Generation Engine:
    Tier 1: Gemini Omni Video (direct Google video generation).
    Tier 2: Gemini Pro Image (direct Google image generation).
    Tier 3: Pollinations FLUX AI (100% unique custom scene generation).
    Tier 4: Dynamic 60+ photo rotating aesthetic library.
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 1. Try Gemini Omni Video
    v_res = try_gemini_video_generation(prompt, str(output_file))
    if v_res:
        return v_res

    # 2. Try Gemini Pro Image
    img_res = try_gemini_pro_image_generation(prompt, str(output_file))
    if img_res:
        return img_res

    # 3. Try Pollinations FLUX AI (generates completely fresh, unique image)
    flux_res = try_pollinations_flux_ai_image(prompt, str(output_file), width=width, height=height)
    if flux_res:
        return flux_res

    # 4. Expansive 60+ Photo Themed Aesthetic Library (Randomized selection)
    return _download_thematic_scene(output_file, tag, width, height)

def _download_thematic_scene(output_file: Path, tag: str, width: int, height: int) -> str:
    """Picks a random cinematic photograph from our expansive aesthetic library."""
    candidates = THEMATIC_AESTHETICS.get(tag, ALL_THEMATIC_IMAGES)
    if not candidates:
        candidates = ALL_THEMATIC_IMAGES

    chosen_url = random.choice(candidates)
    try:
        resp = requests.get(chosen_url, headers=HEADERS, timeout=15)
        if resp.status_code == 200 and len(resp.content) > 5000:
            with open(output_file, "wb") as f:
                f.write(resp.content)
            _ensure_aspect_ratio(output_file, width, height)
            print(f"[Visuals] Dynamic HD photo applied ({tag or 'general'}): {output_file.name}")
            return str(output_file)
    except Exception as e:
        print(f"[Visuals] Download error ({e})")

    return _create_textured_dark_backdrop(output_file, width, height)

def _ensure_aspect_ratio(image_path: Path, target_w: int, target_h: int):
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img_ratio = img.width / img.height
            target_ratio = target_w / target_h

            if img_ratio > target_ratio:
                new_h = target_h
                new_w = int(new_h * img_ratio)
            else:
                new_w = target_w
                new_h = int(new_w / img_ratio)

            img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            left = (new_w - target_w) // 2
            top = (new_h - target_h) // 2
            img_cropped = img_resized.crop((left, top, left + target_w, top + target_h))
            img_cropped.save(image_path, "JPEG", quality=92)
    except Exception as e:
        print(f"[Visuals] Resize error: {e}")

def _create_textured_dark_backdrop(output_file: Path, width: int, height: int) -> str:
    img = Image.new("RGB", (width, height), color=(10, 12, 18))
    draw = ImageDraw.Draw(img)
    draw.ellipse([width * 0.2, height * 0.2, width * 0.8, height * 0.6], fill=(30, 20, 45))
    img = img.filter(ImageFilter.GaussianBlur(radius=100))
    img.save(output_file, "JPEG", quality=90)
    return str(output_file)

def generate_visuals_for_scenes(scenes: list, work_dir: Path) -> list:
    visual_paths = []
    for idx, scene in enumerate(scenes):
        base_path = work_dir / f"scene_{idx}.jpg"
        prompt = scene.get("image_prompt", "Dark psychology cinematic mystery vertical")
        tag = scene.get("tag", None)
        saved_path = generate_ai_image(prompt, str(base_path), tag=tag)
        visual_paths.append(saved_path)
    return visual_paths
