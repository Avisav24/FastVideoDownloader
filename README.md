# FastVideoDownloader

# Deployment

This repository contains a static frontend (`frontend/index.html`) and a Python FastAPI backend (`backend/main.py`).

Recommended deployment approach:

- Frontend: deploy to Vercel as a static site.
  - Connect this GitHub repository to Vercel.
  - In Vercel project settings, set the `Root Directory` to the repository root and the `Output Directory` to `frontend` (or let `vercel.json` route to `/frontend`).
  - Before deploying, edit `frontend/index.html` and set the `<meta name="api-base" content="https://your-backend.example">` to your backend URL.

- Backend: deploy to a server that supports installing `ffmpeg` and running long-lived processes (examples: Render, Railway, Fly, DigitalOcean App Platform, or a VPS).
  - Vercel serverless functions are not recommended for this backend because yt-dlp may require `ffmpeg`, long-running downloads, and filesystem storage.
  - To run on Render/Railway, the repo already contains `backend/requirements.txt`. Configure the start command to:

```
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

## Local testing

1. Install dependencies for the backend:

```bash
python -m pip install -r backend/requirements.txt
```

2. Start the backend locally:

```bash
uvicorn backend.main:app --reload --port 8000
```

3. Edit `frontend/index.html` (optional) and set the API base meta tag for local testing:

```html
<meta name="api-base" content="http://127.0.0.1:8000" />
```

4. Open `frontend/index.html` in your browser and use the UI.

## Notes on `ffmpeg`

Merging video and audio requires `ffmpeg` to be installed on the system where the backend runs. See https://ffmpeg.org/download.html for installation instructions.
