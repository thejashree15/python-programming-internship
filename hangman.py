
import random
from pathlib import Path

MAX_ATTEMPTS = 6

HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    ========
    """
]


def load_words():
    file_path = Path(__file__).parent / "word.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        words = [
            line.strip().lower()
            for line in file
            if line.strip().isalpha()
            and line.strip().isascii()
            and len(line.strip()) >= 3
        ]

    if not words:
        raise ValueError("No valid words found in word.txt")

    return words


def display_game(secret_word, guessed_letters, mistakes):
    print(HANGMAN_STAGES[mistakes])

    masked_word = " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )

    print("Word:", masked_word)
    print(f"Incorrect guesses: {mistakes}/{MAX_ATTEMPTS}")
    print("Guessed letters:",
          " ".join(sorted(guessed_letters)) if guessed_letters else "None")


def play_hangman():
    secret_word = random.choice(load_words())
    guessed_letters = set()
    mistakes = 0

    print("=" * 35)
    print("       WELCOME TO HANGMAN!")
    print("=" * 35)
    print("Guess the hidden word one letter at a time.")

    while mistakes < MAX_ATTEMPTS:
        display_game(secret_word, guessed_letters, mistakes)

        guess = input("\nEnter a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isascii() or not guess.isalpha():
            print("Please enter one English letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"Correct! '{guess}' is in the word.")

            if all(letter in guessed_letters for letter in secret_word):
                print("\nCONGRATULATIONS! YOU WON!")
                print("The word was:", secret_word.upper())
                return
        else:
            mistakes += 1
            print(f"Sorry! '{guess}' is not in the word.")

    display_game(secret_word, guessed_letters, mistakes)
    print("\nGAME OVER!")
    print("The correct word was:", secret_word.upper())


if __name__ == "__main__":
    play_hangman()
