import os
import io
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

HEADERS = {"User-Agent": "Mozilla/5.0"}

def create_profile_picture(output_path: Path):
    """
    Creates an 800x800 dark aesthetic classical statue avatar with golden rim lighting.
    """
    url = "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=800&h=800&fit=crop&q=95"
    resp = requests.get(url, headers=HEADERS, timeout=20)
    img = Image.open(io.BytesIO(resp.content)).convert("RGB")
    img = img.resize((800, 800), Image.Resampling.LANCZOS)

    # Enhance contrast and add moody vignette
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)

    # Dark vignette mask
    vignette = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for r in range(400, 200, -5):
        alpha = int((400 - r) * 0.7)
        vdraw.ellipse([400 - r, 400 - r, 400 + r, 400 + r], outline=(0, 0, 0, alpha), width=5)

    img.paste(vignette, (0, 0), vignette)

    # Outer subtle golden circular border
    draw = ImageDraw.Draw(img)
    draw.ellipse([20, 20, 780, 780], outline=(212, 175, 55), width=6)

    img.save(output_path, "PNG", quality=95)
    print(f"[Branding] Profile Avatar saved to: {output_path}")

def create_youtube_banner(output_path: Path):
    """
    Creates a 2560x1440 YouTube Banner matching the Dark Psychology theme.
    Safe area for all devices is 1546x423 centered (X: 507-2053, Y: 508-931).
    """
    width = 2560
    height = 1440
    banner = Image.new("RGB", (width, height), color=(10, 11, 15))

    # Background ambient moody glow in the center
    bg_glow = Image.new("RGB", (width, height), color=(10, 11, 15))
    draw_glow = ImageDraw.Draw(bg_glow)
    draw_glow.ellipse([width*0.2, height*0.3, width*0.8, height*0.7], fill=(25, 20, 40))
    bg_glow = bg_glow.filter(ImageFilter.GaussianBlur(radius=150))
    banner = Image.blend(banner, bg_glow, 0.7)

    # Fetch and embed classical statue illustration on the left of safe zone
    statue_url = "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=420&h=420&fit=crop&q=90"
    try:
        s_resp = requests.get(statue_url, headers=HEADERS, timeout=15)
        statue_img = Image.open(io.BytesIO(s_resp.content)).convert("RGBA")
        statue_img = statue_img.resize((360, 360), Image.Resampling.LANCZOS)

        # Soft circular mask for statue
        mask = Image.new("L", (360, 360), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.ellipse([0, 0, 360, 360], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(radius=8))

        statue_x = 560
        statue_y = 540
        banner.paste(statue_img, (statue_x, statue_y), mask)

        # Golden ring around statue
        bdraw = ImageDraw.Draw(banner)
        bdraw.ellipse([statue_x - 4, statue_y - 4, statue_x + 364, statue_y + 364], outline=(212, 175, 55), width=4)
    except Exception as e:
        print(f"[Branding] Statue load error: {e}")

    # Typography
    draw = ImageDraw.Draw(banner)
    font_title_path = "C:/Windows/Fonts/segoeuib.ttf"
    font_sub_path = "C:/Windows/Fonts/arialbd.ttf"

    font_title = ImageFont.truetype(font_title_path, 72)
    font_tagline = ImageFont.truetype(font_sub_path, 28)
    font_badge = ImageFont.truetype(font_sub_path, 24)

    text_x = 980
    title_y = 580

    # Title: DARK PSYCHOLOGY VAULT
    # Drop shadow
    draw.text((text_x + 3, title_y + 3), "DARK PSYCHOLOGY VAULT", fill=(0, 0, 0), font=font_title)
    # White main title with golden accent
    draw.text((text_x, title_y), "DARK PSYCHOLOGY", fill=(255, 255, 255), font=font_title)
    title_w = draw.textlength("DARK PSYCHOLOGY ", font=font_title)
    draw.text((text_x + title_w, title_y), "VAULT", fill=(212, 175, 55), font=font_title)

    # Gold accent line
    line_y = title_y + 95
    draw.line([(text_x, line_y), (text_x + 750, line_y)], fill=(212, 175, 55), width=4)

    # Tagline: DECODE HUMAN BEHAVIOR • MIND SECRETS • DAILY SHORTS
    tag_y = line_y + 25
    draw.text((text_x, tag_y), "DECODE HUMAN BEHAVIOR  •  MIND SECRETS  •  DAILY SHORTS", fill=(200, 205, 220), font=font_tagline)

    # Badge: "SUBSCRIBE FOR DAILY ADVANTAGE"
    badge_y = tag_y + 55
    badge_text = "✦  NEW SHORTS EVERY DAY  ✦"
    draw.text((text_x, badge_y), badge_text, fill=(212, 175, 55), font=font_badge)

    banner.save(output_path, "PNG", quality=95)
    print(f"[Branding] YouTube Banner saved to: {output_path}")

def generate_branding_kit():
    desktop1 = Path("C:/Users/SHIVA TIWARI/OneDrive/Desktop")
    desktop2 = Path("C:/Users/SHIVA TIWARI/Desktop")

    avatar_name = "YouTube_Channel_Profile_Avatar.png"
    banner_name = "YouTube_Channel_Banner_2560x1440.png"

    local_avatar = Path(avatar_name)
    local_banner = Path(banner_name)

    create_profile_picture(local_avatar)
    create_youtube_banner(local_banner)

    # Copy to User's Desktop
    import shutil
    for d in [desktop1, desktop2]:
        if d.exists():
            shutil.copy(local_avatar, d / avatar_name)
            shutil.copy(local_banner, d / banner_name)
            print(f"[Branding] Copied to: {d}")

if __name__ == "__main__":
    generate_branding_kit()
