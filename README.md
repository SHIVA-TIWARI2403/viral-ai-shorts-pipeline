# Short-Form Video Automation Pipeline

A modular content generation and publishing pipeline for YouTube Shorts and Instagram Reels. Automates script generation, neural text-to-speech rendering, subtitle timing, video compositing, and platform publishing via official APIs.

---

## Architecture

1. **Script Engine:** Generates focused, high-retention 30-40 second narrative scripts structured with early hooks.
2. **Audio Synthesis:** Uses Microsoft Edge Neural TTS (`edge-tts`) to generate high-fidelity voiceovers without third-party subscriptions.
3. **Compositing & Subtitles:** Builds 9:16 vertical videos using MoviePy and FFmpeg, applying burnt-in kinetic subtitles with high-contrast outlines and ambient background audio.
4. **Publishing Integrations:**
   - **YouTube Data API v3:** Automatic tag attachment, privacy setting, and OAuth token persistence.
   - **Meta Graph API:** Instagram Reels & Facebook Pages video publishing endpoints.

---

## Project Structure

```text
viral_ai_shorts_pipeline/
├── script_generator.py     # Script drafting and topic selection
├── voice_generator.py      # Edge-TTS voice synthesis
├── image_generator.py      # Visual prompt rendering & asset fetching
├── video_editor.py         # MoviePy / FFmpeg video assembly & subtitle burning
├── uploader_youtube.py     # YouTube Data API v3 publisher
├── uploader_meta.py        # Meta Graph API publisher
├── run_pipeline.py         # Main CLI coordinator
├── requirements.txt        # Python package dependencies
└── .env.example            # Environment variables template
```

---

## Setup & Usage

### 1. Installation
Requires Python 3.10+ and FFmpeg.

```bash
pip install -r requirements.txt
cp .env.example .env
```

### 2. Generate a Preview Video
To generate a test video locally without uploading:
```bash
python run_pipeline.py --mode generate
```
Output video files are saved to the `output/` directory.

### 3. Publishing Configuration

#### YouTube Shorts:
1. Enable **YouTube Data API v3** in the Google Cloud Console.
2. Create an **OAuth 2.0 Client ID (Desktop App)**.
3. Download the JSON credential file and save it as `client_secret.json` in the project root.
4. Run the upload command:
   ```bash
   python run_pipeline.py --mode upload --platform youtube
   ```

#### Meta (Instagram / Facebook):
Populate the following variables in your `.env`:
```env
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id
INSTAGRAM_ACCESS_TOKEN=your_user_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_access_token
```

---

## Disclaimer

Ensure all generated and uploaded content complies with YouTube Community Guidelines and Instagram Community Guidelines.
