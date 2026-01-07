# Football Match Prediction CLI ⚽

A simple Python CLI application that uses OpenRouter API to generate football (soccer) match predictions powered by AI.

## Features

- Interactive command-line interface
- AI-powered match predictions using OpenRouter
- Key match factors and player insights
- Clean, readable output format

## Requirements

- Python 3.11 or higher
- OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai/keys))

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Anubhavlfc/Senior-Capestone.git
cd Senior-Capestone
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenRouter API key:
     ```
     OPENROUTER_API_KEY=your_actual_api_key_here
     ```

## Usage

Run the application:
```bash
python main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

The application will:
1. Ask you to enter the first team name
2. Ask you to enter the second team name
3. Generate an AI-powered prediction including:
   - One key factor in the match
   - One player to watch
   - A one-sentence prediction

## Example

```
⚽ Football Match Prediction CLI ⚽
----------------------------------------

Enter the first team name: Manchester United
Enter the second team name: Liverpool

Generating prediction for Manchester United vs Liverpool...

============================================================
MATCH PREDICTION: Manchester United vs Liverpool
============================================================

Key Factor: The midfield battle will be crucial as both teams look to control possession.
Player to Watch: Mohamed Salah for Liverpool, whose pace could exploit United's high defensive line.
Prediction: Liverpool is likely to edge this match 2-1 with their clinical finishing and solid defense.

============================================================
```

## Project Structure

- `main.py` - Main CLI application
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variable template
- `.gitignore` - Git ignore rules

## Technical Details

- Uses OpenRouter's Chat Completions API
- Model: GPT-4o-mini (cost-effective option)
- HTTP library: `requests`
- Environment variables: `python-dotenv`

## Error Handling

The application handles:
- Missing API key
- Network errors
- API request failures
- Invalid user input

## License

MIT