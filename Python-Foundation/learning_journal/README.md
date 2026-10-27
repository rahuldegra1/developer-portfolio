# Learning Journal

A small Flask application for browsing Markdown journal posts. Post filenames become URL slugs and page titles; the app converts Markdown content to HTML for display.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install Flask Markdown Pygments
python app.py
```

Open `http://127.0.0.1:5002`. Add `.md` files to `posts/` to publish journal entries locally.

The Flask development server is intended for local use, not production deployment.
