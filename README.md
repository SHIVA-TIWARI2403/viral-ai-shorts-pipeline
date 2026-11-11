# 🚀 Viral AI Shorts & Reels Automation Pipeline

Autonomous AI Pipeline jo **YouTube Shorts**, **Instagram Reels**, aur **Facebook Reels** ke liye automatically viral videos generate aur upload karta hai.

---

## 🌟 Features
- **Niche:** Dark Psychology & Human Behavior Mysteries (English) — currently the highest-earning & most viral short-form niche globally.
- **AI Script Engine:** 3-second scroll-stopping hooks, high-retention 30-40s psychological scripts.
- **Deep Neural Voice:** Ultra-realistic baritone voice (`en-US-ChristopherNeural`).
- **Cinematic Visuals:** 9:16 vertical AI generated images (Pollinations Flux/SDXL with local fallback).
- **Auto-Editing:** Burned-in, high-contrast kinetic subtitles (yellow/white with bold outlines) + ambient background tension audio.
- **Direct Uploaders:**
  - YouTube Data API v3 (Automatic `#Shorts` tagging & OAuth handling).
  - Meta Graph API (Instagram Reels & Facebook Pages).

---

## 🛠️ Quick Start

### 1. Ek Test Video Generate Karein (Preview)
Apne terminal / PowerShell me yeh command chalayein:
```powershell
cd "C:\Users\SHIVA TIWARI\.gemini\antigravity\scratch\viral_ai_shorts_pipeline"
python run_pipeline.py --mode generate
```
Yeh command bina kisi API key ke turant ek video generate karke `output/` folder me save karegi jise aap dekh sakte hain!

---

### 2. Auto-Upload Setup (Access Setup)

#### A. YouTube Shorts Auto-Upload (Google Cloud Setup):
1. [Google Cloud Console](https://console.cloud.google.com/) par jayein.
2. New Project create karein aur **YouTube Data API v3** enable karein.
3. **APIs & Services > Credentials** me jayein:
   - Create Credentials > **OAuth Client ID**.
   - Application Type: **Desktop App**.
4. Download JSON button par click karein aur file ko rename karke `client_secret.json` naam se is project folder me rakh dein:
   `C:\Users\SHIVA TIWARI\.gemini\antigravity\scratch\viral_ai_shorts_pipeline\client_secret.json`
5. Ab jab aap pehli baar upload karenge:
   ```powershell
   python run_pipeline.py --mode upload --platform youtube
   ```
   Browser me Google login window khulegi. Ek baar allow karne ke baad `token_youtube.json` ban jayega aur future me 100% automatically background me upload hoga!

---

#### B. Instagram Reels & Facebook Setup (Meta Developer):
1. [Meta for Developers](https://developers.facebook.com/) par app create karein.
2. Instagram Graph API aur Facebook Pages access token generate karein.
3. `.env` file me apni details daalein:
   ```env
   INSTAGRAM_ACCOUNT_ID=your_id
   INSTAGRAM_ACCESS_TOKEN=your_token
   FACEBOOK_PAGE_ID=your_page_id
   FACEBOOK_PAGE_ACCESS_TOKEN=your_token
   ```

---

## ⏱️ Daily Automation / Scheduling (Windows Task Scheduler)
Roz automatically video banakar upload karne ke liye:
1. Windows search me **Task Scheduler** open karein.
2. **Create Basic Task** par click karein -> Name: "Daily AI Shorts".
3. Trigger: **Daily** (e.g. 5:00 PM).
4. Action: **Start a program**:
   - Program: `python`
   - Arguments: `run_pipeline.py --mode upload --platform youtube`
   - Start in: `C:\Users\SHIVA TIWARI\.gemini\antigravity\scratch\viral_ai_shorts_pipeline`
