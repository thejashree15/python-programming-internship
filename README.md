# Hangman Game – Python Programming Internship

## Project Description

Hangman is a terminal-based word-guessing game developed using Python. The player must guess a randomly selected English word one letter at a time, with a maximum of six incorrect attempts.

## Features

- Randomly selects a word from an English word list.
- Displays hidden letters using underscores.
- Updates the ASCII hangman drawing after incorrect guesses.
- Tracks previously guessed letters.
- Prevents duplicate guesses from reducing the remaining attempts.
- Validates user input.
- Displays win and game-over messages.

## Technologies Used

- Python 3
- PyCharm
- Python standard libraries: `random` and `pathlib`

## Project Structure

```text
PythonProject/
├── hangman.py
├── word.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3 installed on your computer.
- The `word.txt` file must be in the same directory as `hangman.py`.

## How to Run

1. Clone or download this repository.
2. Open the project folder in PyCharm or a terminal.
3. Make sure `hangman.py` and `word.txt` are in the same directory.
4. Run the following command:

```bash
python hangman.py
```

5. Enter one English letter at a time to guess the hidden word.

## Game Rules

- Guess the hidden word one letter at a time.
- Each incorrect guess uses one attempt.
- You can make up to six incorrect guesses.
- Repeated guesses do not use additional attempts.
- Guess all the letters before your attempts run out to win.

## Learning Outcomes

- Practiced Python functions, loops, and conditional statements.
- Used sets to track guessed letters.
- Learned file handling and random word selection.
- Implemented input validation and game logic.

## Author

**Thejashree H. S.**

## Internship Task

Python Programming Internship – Task 1: Hangman Game