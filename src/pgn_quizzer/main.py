import argparse
import sys

# Import data‐loading and generation functions:
from pgn_quizzer.data import load_questions_from_json
from pgn_quizzer.data import load_questions_from_pgn # TODO

# Import core quiz logic (model):
from pgn_quizzer.model import QuizBrain

# Import domain presentation logic (presenter):
from pgn_quizzer.presenter import QuizPresenter

# Import UI entry points (view):
from pgn_quizzer.view import run_quiz_console, run_quiz_gui # TODO

# TODO: replace with pathlib
SAMPLE_PATH = ".\\jsons\\chess_sample_data.json"

def int_in_range(value: str) -> int:
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not a valid integer")

    if not (1 <= ivalue <= 101):
        raise argparse.ArgumentTypeError(f"{ivalue} is out of allowed range [1, 101]")

    return ivalue

def parse_args() -> argparse.Namespace:
    """
    Set up and parse command-line flags, seeking:
      --source: either 'json' or 'pgn'
      --path:   path to the JSON or PGN file
      --ui:     either 'console' or 'gui'
      --num:    number of questions to ask (default = 5)
    """
    
    parser = argparse.ArgumentParser(description="Run the Chess Quiz app.")
    parser.add_argument(
        "--source",
        choices=["json", "pgn"],
        default="json", # switch this to pgn when chess_pgn_2_json implemented
        help="Where to load questions from: JSON file or PGN file (default: json).",
    )
    parser.add_argument(
        "--path",
        help="Path to JSON (if --chess_quiz json) or PGN (if --chess_quiz pgn). "
             "If omitted: defaults to chess_sample_data.json for json; exits for pgn.",
    )
    parser.add_argument(
        "--ui",
        choices=["console", "gui"],
        default="console", # switch this to gui when gui_view implemented
        help="Which UI to launch: console or GUI (default: console).",
    )
    parser.add_argument(
        "--num",
        type=int_in_range,
        default=5,
        help="Number of questions to ask in each quiz session (default: 5).",
    )
    return parser.parse_args()

def main_function(args: argparse.Namespace):
    # Load or generate the questions list:
    if args.source == "json":
        json_path = args.path or SAMPLE_PATH
        try:
            question_bank = load_questions_from_json(json_path)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading JSON questions from {json_path}: {e}", file=sys.stderr)
            sys.exit(1)

    else:  # args.source == "pgn" # currently this always throws an exception TODO
        if not args.path:
            print("Error: --pgn pgn requires a --path to a PGN file.", file=sys.stderr)
            sys.exit(1)
        try:
            question_bank = load_questions_from_pgn(args.path)
        except Exception as e:
            print(f"Error loading PGN questions from {args.path}: {e}", file=sys.stderr)
            sys.exit(1)

    # Create QuizBrain instance:
    quiz = QuizBrain(question_bank, nb_questions=args.num)

    # Dispatch to chosen UI:
    if args.ui == "console":
        # Create ConsolePresenter instance:
        presenter = QuizPresenter(quiz)

        while run_quiz_console(presenter, args.num):
            quiz = QuizBrain(question_bank, nb_questions=args.num) # new instance means new randomization
                                                                   # same question bank
            presenter = QuizPresenter(quiz)
    else:  # args.ui == "gui" # currently this always throws an exception TODO
        try:
            # Create ConsolePresenter instance:
            presenter = QuizPresenter(quiz)
            
            run_quiz_gui(presenter, args.num)
        except Exception:
            print("Error: GUI not implemented yet.", file=sys.stderr)
            sys.exit(1)


def main():
    args = parse_args()
    main_function(args)

if __name__ == "__main__":
    main()
