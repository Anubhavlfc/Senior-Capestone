# Football Match Predictor (OpenRouter)

A minimal Python 3 CLI that uses an OpenRouter-hosted LLM to generate a short football (soccer) match insight between two teams.

User flow:

1. Run the program.
2. Enter **Team 1** name.
3. Enter **Team 2** name.
4. The app calls the OpenRouter Chat Completions API.
5. A concise match insight is printed with a key factor, player to watch, and prediction.

---

## Requirements

- Python **3.11+**
- An OpenRouter API key
- Python packages:
  - `requests`
  - `python-dotenv`

Install dependencies (once):

```bash
pip install requests python-dotenv
```

---

## Configuration

The app reads the API key from an environment variable named `OPENROUTER_API_KEY`.

The easiest way to set it is with a `.env` file in the same directory as `main.py`:

```bash
# .env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

`python-dotenv` will automatically load this into the environment when the app starts.

> Note: The API key is **not** hardcoded anywhere in the code.

---

## How It Works

- Prompts you for two team names via the terminal.
- Sends a single chat completion request to:
  - `https://openrouter.ai/api/v1/chat/completions`
- Uses an OpenRouter-compatible, inexpensive model (default: `openai/gpt-4o-mini`).
- Follows OpenAI-style chat formatting with `system` and `user` messages.
- Instructs the model to respond **exactly** in this format:

```text
Key Factor:
Player to Watch:
Prediction:
```

The model’s response is then printed with simple headings to keep the output short and user-friendly.

---

## Running the App

From the project directory (where `main.py` lives):

```bash
python main.py
```

You’ll see prompts like:

```text
=== Football Match Predictor (OpenRouter) ===

Enter Team 1 team name: 
Enter Team 2 team name: 
```

After entering both teams, you’ll get a match insight, for example:

```text
=== Match Insight ===

Match: Team 1 vs Team 2

Key Factor: ...
Player to Watch: ...
Prediction: ...
```

---

## Error Handling

The CLI is designed to fail gracefully:

- **Missing API key** – prints a clear message explaining how to set `OPENROUTER_API_KEY` (via `.env` or shell export) and exits.
- **Network/API errors** – prints a short, helpful error message if the API request fails or returns an unexpected response.

---

## Files

- `main.py` – Single-file CLI implementation.
- `README.md` – This documentation.
