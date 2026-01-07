#!/usr/bin/env python3
"""
Football Match Prediction CLI
A simple CLI tool that uses OpenRouter API to generate football match predictions.
"""

import os
import sys
import requests
from dotenv import load_dotenv


def load_api_key():
    """Load the OpenRouter API key from environment variable."""
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not found.")
        print("Please set your OpenRouter API key in a .env file or as an environment variable.")
        sys.exit(1)
    
    return api_key


def get_team_input(prompt):
    """Get team name input from user."""
    team = input(prompt).strip()
    
    if not team:
        print("Error: Team name cannot be empty.")
        sys.exit(1)
    
    return team


def create_prediction_prompt(team1, team2):
    """Create the prompt for the LLM to generate match prediction."""
    return f"""You are a football (soccer) analyst. Provide a brief prediction for a match between {team1} and {team2}.

Please respond in this exact format:

Key Factor:
Player to Watch:
Prediction:

Keep each section to one sentence or brief phrase."""


def call_openrouter_api(api_key, team1, team2):
    """Call OpenRouter API to get match prediction."""
    # OpenRouter API endpoint
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Required headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Create the prompt
    prompt = create_prediction_prompt(team1, team2)
    
    # Request payload - using a free/inexpensive model
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        # Make the API request
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Extract the response content
        data = response.json()
        prediction = data['choices'][0]['message']['content']
        
        return prediction
        
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please try again.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to connect to OpenRouter API.")
        print(f"Details: {str(e)}")
        sys.exit(1)
    except (KeyError, IndexError) as e:
        print("Error: Unexpected response format from API.")
        print(f"Details: {str(e)}")
        sys.exit(1)


def display_prediction(team1, team2, prediction):
    """Display the match prediction in a clean, readable format."""
    print("\n" + "="*60)
    print(f"MATCH PREDICTION: {team1} vs {team2}")
    print("="*60)
    print()
    print(prediction)
    print()
    print("="*60)


def main():
    """Main function to run the CLI application."""
    print("⚽ Football Match Prediction CLI ⚽")
    print("-" * 40)
    print()
    
    # Load API key
    api_key = load_api_key()
    
    # Get team names from user
    team1 = get_team_input("Enter the first team name: ")
    team2 = get_team_input("Enter the second team name: ")
    
    print()
    print(f"Generating prediction for {team1} vs {team2}...")
    print()
    
    # Get prediction from OpenRouter API
    prediction = call_openrouter_api(api_key, team1, team2)
    
    # Display the prediction
    display_prediction(team1, team2, prediction)


if __name__ == "__main__":
    main()
