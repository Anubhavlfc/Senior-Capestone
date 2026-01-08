"""Simple CLI to get a football (soccer) match prediction
using OpenRouter's Chat Completions API.

Requirements:
- Python 3.11+
- requests
- python-dotenv

User flow:
User runs the program → enters Team 1 and Team 2 →
program calls OpenRouter → prints a short match insight.
"""

import os
import sys
from typing import Optional

import requests
from dotenv import load_dotenv


OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openai/gpt-4o-mini"  # inexpensive, GPT-4o-mini–class model


def load_api_key() -> Optional[str]:
    """Load the OpenRouter API key from environment using python-dotenv.

    Returns the API key string if found, otherwise None.
    """

    # Load variables from a .env file into the environment (if present)
    load_dotenv()

    return os.getenv("OPENROUTER_API_KEY")


def build_prompt(team1: str, team2: str) -> str:
    """Build the prompt instructing the LLM to return a structured prediction."""

    return (
        "You are an expert football (soccer) analyst. "
        "For the upcoming match between "
        f"{team1} and {team2}, provide concise insights in EXACTLY this format, "
        "with each item on its own line and no extra text:\n\n"
        "Key Factor: <one short key factor in the match>\n"
        "Player to Watch: <one key player and their team>\n"
        "Prediction: <one short sentence predicting the result>\n\n"
        "Do not add any other commentary, explanations, or headings."
    )


def call_openrouter(api_key: str, team1: str, team2: str) -> str:
    """Call OpenRouter's Chat Completions API and return the model's text.

    Raises a RuntimeError with a helpful message if the request fails.
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "You are a concise, neutral football match analyst.",
            },
            {
                "role": "user",
                "content": build_prompt(team1, team2),
            },
        ],
        # Keep the response short and inexpensive
        "max_tokens": 200,
        "temperature": 0.7,
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=20,
        )
    except requests.RequestException as exc:  # network or connection issues
        raise RuntimeError(
            "Failed to reach OpenRouter API. Please check your internet "
            "connection and try again."
        ) from exc

    if response.status_code != 200:
        # Try to surface a helpful message from the response body if available
        detail: str
        try:
            data = response.json()
            detail = data.get("error", {}).get("message") or data.get("message") or "Unknown error from API."
        except ValueError:
            detail = response.text or "Unknown error from API."

        raise RuntimeError(
            "OpenRouter API request failed "
            f"(status {response.status_code}): {detail}"
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("Unable to parse response from OpenRouter as JSON.") from exc

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as exc:
        raise RuntimeError(
            "Unexpected response format from OpenRouter API. "
            "Please try again later."
        ) from exc


def prompt_for_team(name: str) -> str:
    """Prompt the user for a team name and ensure it is not empty."""

    while True:
        team = input(f"Enter {name} team name: ").strip()
        if team:
            return team
        print("Team name cannot be empty. Please try again.\n")


def main() -> None:
    """Entry point for the CLI application."""

    print("=== Football Match Predictor (OpenRouter) ===\n")

    # Get team names from the user via terminal input
    team1 = prompt_for_team("Team 1")
    team2 = prompt_for_team("Team 2")

    # Load the API key using python-dotenv
    api_key = load_api_key()
    if not api_key:
        print(
            "Error: OPENROUTER_API_KEY is not set.\n\n"
            "Please create a .env file in this directory with a line like:\n"
            "OPENROUTER_API_KEY=your_api_key_here\n"
            "or otherwise export the variable in your shell."
        )
        sys.exit(1)

    # Call OpenRouter and handle errors gracefully
    try:
        prediction_text = call_openrouter(api_key, team1, team2)
    except RuntimeError as err:
        print("\nCould not generate prediction:")
        print(f"  {err}")
        sys.exit(1)

    # Print a clean, readable match insight to the terminal
    print("\n=== Match Insight ===\n")
    print(f"Match: {team1} vs {team2}\n")
    print(prediction_text)


if __name__ == "__main__":
    main()
