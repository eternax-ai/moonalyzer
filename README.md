# moonalyzer
Wen moon according to the stars

## Setup

1. Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Locally

### Setup .env file
1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### Run the script
```bash
# Activate virtual environment
source venv/bin/activate

# Run the forecast generator (it will automatically load from .env)
python scripts/generate_forecast.py
```

**Note:** The script will also work if you set `OPENAI_API_KEY` as an environment variable, but using `.env` is recommended for local development.

The script will:
- Calculate planetary positions using AstroPy
- Generate astrological aspects
- Create a forecast using OpenAI
- Save to `data/DDMMYYYY.json` and `data/latest.json`

## Local Frontend Testing

To test the frontend locally (avoiding CORS issues):

```bash
# Option 1: Use the Python server
python3 serve.py
# Then open http://localhost:8000 in your browser

# Option 2: Use Python's built-in server
python3 -m http.server 8000
```

**Note:** GitHub Pages serves files over HTTP, so the CORS issue only occurs when opening `index.html` directly with `file://`. Once deployed to GitHub Pages, everything works automatically.

## GitHub Pages

The site will be automatically available at `https://[username].github.io/moonalyzer` (or your custom domain).

The `index.html` uses relative paths (`./data/latest.json`) which work perfectly on GitHub Pages since files are served over HTTP.

## GitHub Actions

The workflow runs every 12 hours (00:00 and 12:00 UTC). Set `OPENAI_API_KEY` as a GitHub secret in your repository settings.
