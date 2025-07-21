# PGNQuizzer

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
<!--
![License](https://img.shields.io/github/license/will-reynolds-maths/pgn-quizzer)
![Last Commit](https://img.shields.io/github/last-commit/will-reynolds-maths/pgn-quizzer)
![Open Issues](https://img.shields.io/github/issues/will-reynolds-maths/pgn-quizzer)
![Repo Size](https://img.shields.io/github/repo-size/will-reynolds-maths/pgn-quizzer)
![Build](https://img.shields.io/github/actions/workflow/status/will-reynolds-maths/pgn-quizzer/python-app.yml) 
-->

PGNQuizzer is a a lightweight offline tool that turns a collection of annotated chess games into an interactive quiz, aiming to help chess players strengthen their game recall and deepen their positional understanding.

## Installation

Clone the repo:

```bash
git clone https://github.com/will-reynolds-maths/pgn-quizzer.git
cd pgn_quizzer
```

Make sure your Python version matches the project's requirements (check `pyproject.toml` for details).

Install the main dependency with your package manager of choice, for example using `pip`:

```bash
pip install python-chess
```

## Current Capabilities

This app:
- requires Python to be installed,
- currently only accepts JSON source,
- only runs as a console (command-line) interface.

You can choose the number of quiz questions (between 1 and 100).

## Usage

### CLI Usage

The following two examples launch the command-line interface with the same settings:

```bash
$ python pgn_quizzer.main
```

```bash
$ python pgn_quizzer.main --source "json" --path ".\pgn_quizzer\chess\chess_sample_data.json" --ui "console" --num "5"
```

In the command-line interface, you will be asked to input answers (always single letters: A, B, C, etc.) and confirm your continued participation with the quiz (Y/n input defaulting to Y).

### Example Output

Here is an example question:

```bash
>> Q.1: Which game is the following position from?

⭘ ♜ ⭘ ♝ ⭘ ⭘ ♜ ⭘
♟ ♞ ⭘ ⭘ ⭘ ⭘ ♟ ⭘
⭘ ⭘ ♚ ⭘ ⭘ ⭘ ⭘ ♟
⭘ ♖ ♟ ⭘ ♟ ♙ ⭘ ⭘
⭘ ⭘ ♙ ♟ ♙ ⭘ ♙ ⭘
♙ ⭘ ⭘ ♙ ⭘ ⭘ ⭘ ⭘
⭘ ⭘ ♔ ♗ ♗ ⭘ ⭘ ⭘
⭘ ♖ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘

A. Steinitz - Lipke, Vienna 1898
B. Anderssen - Minkowitz, Baden-Baden 1870
C. Janowski - Capablanca, New York 1916

Your answer (A, B, C):
```

## Features

- Currently accepts JSON input
- Currently supports command-line interface
- Randomization provides replayability

### Future Directions

In future versions the app will:
- Accept as input a PGN (from which to generate the quiz).
- Default to a graphical user interface.
- Be installable as a self-contained binary (no Python installation needed).

## Built With

- Python 3.12
- python-chess

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

You are free to:
- **Use** the software for personal, educational, or research purposes.
- **Share** and **redistribute** the code.
- **Modify** the code to suit your needs.

Under the following terms:
- **Attribution**: You must give appropriate credit and indicate if changes were made.
- **NonCommercial**: You may not use the material for commercial purposes, including but not limited to:
-- Hosting this software as part of a paid or ad-supported service.
-- Integrating it into subscription-based or monetized platforms.
-- Redistributing modified versions for commercial gain.

If you are unsure whether your use case qualifies as "non-commercial", you can read the license summary or review the full legal text.

### Note on Commercial Use
This license **explicitly prohibits commercial use**, including use in freemium, ad-supported, or subscription-based services.

## Credits / Acknowledgements

Quiz structure inspired by Angela Yu's "100 Days of Python" course.