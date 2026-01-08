import os

from dotenv import load_dotenv
from flask import Flask, render_template_string, request

from main import call_openrouter


# Load environment variables from .env (including OPENROUTER_API_KEY)
load_dotenv()


app = Flask(__name__)


TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Football Match Predictor</title>
    <style>
      body { font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif; background: #0b1120; color: #e5e7eb; }
      .container { max-width: 480px; margin: 60px auto; padding: 24px 28px; background: #020617; border-radius: 16px; box-shadow: 0 20px 40px rgba(15,23,42,0.8); }
      h1 { font-size: 1.6rem; margin-bottom: 1rem; }
      label { display: block; margin-top: 0.75rem; margin-bottom: 0.25rem; font-size: 0.9rem; color: #9ca3af; }
      input { width: 100%; padding: 0.6rem 0.7rem; border-radius: 0.5rem; border: 1px solid #1f2937; background: #020617; color: #e5e7eb; }
      button { margin-top: 1rem; width: 100%; padding: 0.65rem; border-radius: 9999px; border: none; background: #22c55e; color: #022c22; font-weight: 600; cursor: pointer; }
      button:hover { background: #16a34a; }
      .error { margin-top: 1rem; padding: 0.75rem; border-radius: 0.5rem; background: #7f1d1d; color: #fee2e2; font-size: 0.9rem; }
      .card { margin-top: 1.25rem; padding: 0.9rem 1rem; border-radius: 0.75rem; background: #020617; border: 1px solid #1f2937; font-size: 0.95rem; }
      .label { font-weight: 600; color: #9ca3af; }
      .value { margin-bottom: 0.3rem; }
      .match { font-size: 0.95rem; margin-bottom: 0.5rem; color: #9ca3af; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>⚽ Football Match Predictor</h1>
      <form method="post">
        <label for="team1">Team 1</label>
        <input id="team1" name="team1" value="{{ team1 }}" placeholder="e.g. Liverpool" required>

        <label for="team2">Team 2</label>
        <input id="team2" name="team2" value="{{ team2 }}" placeholder="e.g. Chelsea" required>

        <button type="submit">Generate Prediction</button>
      </form>

      {% if error %}
        <div class="error">{{ error }}</div>
      {% endif %}

      {% if prediction %}
        <div class="card">
          <div class="match">Match: {{ team1 }} vs {{ team2 }}</div>
          <pre style="margin: 0; white-space: pre-wrap; font-family: inherit;">{{ prediction }}</pre>
        </div>
      {% endif %}
    </div>
  </body>
  </html>"""


@app.route("/", methods=["GET", "POST"])
def index():
    team1 = ""
    team2 = ""
    prediction = None
    error = None

    if request.method == "POST":
        team1 = (request.form.get("team1") or "").strip()
        team2 = (request.form.get("team2") or "").strip()
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            error = "API key not found. Please set OPENROUTER_API_KEY in your .env file."
        elif not team1 or not team2:
            error = "Please enter both teams."
        else:
            try:
                prediction = call_openrouter(api_key, team1, team2)
            except Exception as exc:  # surface model or network errors
                error = str(exc)

    return render_template_string(
        TEMPLATE,
        team1=team1,
        team2=team2,
        prediction=prediction,
        error=error,
    )


if __name__ == "__main__":
    # Run the Flask dev server locally
    app.run(debug=True)
