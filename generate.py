#!/usr/bin/env python3

import argparse
import secrets
from pathlib import Path

def main():
    # Get path to default word list
    script_dir = Path(__file__).resolve().parent
    words_alpha = str(script_dir / "words_alpha.txt")

    # Parse arguments
    parser = argparse.ArgumentParser(description="Generate a passphrase")
    parser.add_argument("-w", "--words", default=6)
    parser.add_argument("-m", "--min-word-length", default=5)
    parser.add_argument("-M", "--max-word-length", default=8)
    parser.add_argument("-s", "--soothe", action="store_true", help="Make password quality checkers happy by capitalizing the first letter, adding a special character, and adding two digits")
    parser.add_argument("-o", "--output", default="-")
    parser.add_argument("-d", "--word-list", default=words_alpha, help="Word list")
    args = parser.parse_args()

    # Validate word length
    if args.words < 1:
        raise ValueError("Words must be greater than 0")

    # Get word list
    with open(args.word_list, "r") as file:
        words = list(file.read().split())

    # Filter by word length
    words = list(w for w in words if len(w) in range(args.min_word_length, args.max_word_length + 1))

    # Generate password
    phrase_words = []
    for _ in range(args.words):
        word = secrets.choice(words)
        phrase_words.append(word)
        words.remove(word)
    phrase = " ".join(phrase_words)

    # Soothe
    if args.soothe:
        phrase_words[0] = f"{phrase_words[0][0].upper()}{phrase_words[0][1:]}"
        symbol = secrets.choice("`~!@#$%^&*()_+-=[]\;',./{}|:\"<>?")
        digit1 = secrets.randbelow(10)
        digit2 = secrets.randbelow(10)
        phrase = f"{phrase[0].upper()}{phrase[1:]}{symbol}{digit1}{digit2}"

    # Output
    if args.output == "-":
        print(phrase)
    else:
        with open(args.output, "w+") as file:
            file.write(phrase)

if __name__ == "__main__":
    main()