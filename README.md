# 🕵️ AI-Powered Murder Mystery Game

An **Interactive command-line** murder mystery game powered by Google's Gemini AI. Every game generates a unique theft investigation scenario with dynamic suspects, motives, alibis, clues and contradictions for players to uncover.

## Features

- 🤖 AI-generated mystery scenarios using Gemini
- 🕵️ Three unique suspects with professions and motives
- 🔍 Dynamic clue discovery through interrogations
- ⚖️ Contradiction analysis system
- 🎯 Detective scoring system
- 🎲 Randomized thief selection for replayability
- 🔄 Play multiple unique cases

## How It Works

The game uses Gemini AI to generate:

- A stolen valuable item
- A crime location
- Three suspects
- Individual motives
- Alibis
- Multiple clues
- Contradictions between clues and alibis

As the detective, your goal is to:

- Interrogate suspects
- Collect clues
- Analyze contradictions
- Identify the thief
- Maximize your detective score

## Project Structure

```
AI-Detective-Game/
│
├── main.py
├── .env
├── .env.sample
├── requirements.txt
└── README.md
```

## Installation

- Clone the Repository
  git clone https://github.com/Abhimanyu-Kushwaha-Dev/AI-Detective-Game.git
- cd AI-Detective-Game

### Create a Virtual Environment

```
python -m venv venv
```

### Activate the environment:

```
Windows: venv\Scripts\activate
Linux/macOS: source venv/bin/activate
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Environment Variables

Create a .env file in the project root:

`GOOGLE_API_KEY=<--your_gemini_api_key-->`

Get your API key from Google AI Studio.

## Running the Game

```
python main.py
```

## Gameplay

### Main Menu

1. Interrogate a suspect
2. View clues
3. Check for contradictions
4. Make an accusation
5. Quit game

### Scoring System

- Action (Points)
- Finding a contradiction (+50)
- Correct accusation (+100)
- Winning

Successfully identify the thief before running out of investigation opportunities.

## Technologies Used

- Python 3.x (3.14.4)
- Google Gemini API
- python-dotenv

## Author

🍵 Developed with caffeined brain by Abhimanyu Kushwaha.
