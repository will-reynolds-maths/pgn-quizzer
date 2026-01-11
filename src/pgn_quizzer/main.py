from argparse import ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path

# Import data‐loading and generation functions:
from pgn_quizzer.data import load_questions_from_json
from pgn_quizzer.data import load_questions_from_pgn # TODO

# Import core quiz logic (model):
from pgn_quizzer.model import QuizBrain

# Import domain presentation logic (presenter):
from pgn_quizzer.presenter import QuizPresenter

# Import UI entry points (view):
from pgn_quizzer.view import run_quiz_console, run_quiz_gui # TODO


def is_int_in_range(value: str) -> int:
    try:
        ivalue = int(value)
    except ValueError:
        raise ArgumentTypeError(f"{value!r} is not a valid integer")

    if not (1 <= ivalue <= 101):
        raise ArgumentTypeError(f"{ivalue} is out of allowed range [1, 101]")

    return ivalue

def parse_args() -> Namespace:
    """
    Set up and parse command-line flags, seeking:
      --source: either 'json' or 'pgn'
      --path:   path to the JSON or PGN file
      --ui:     either 'console' or 'gui'
      --num:    number of questions to ask (default = 5)
    """
    
    parser = ArgumentParser(description="Run PGN Quizzer.")

    parser.add_argument(
        "--path",
        type=str,
        help="Path to JSON (if --chess_quiz json) or PGN (if --chess_quiz pgn). "
             "If omitted: defaults to chess_sample_data.json for json; exits for pgn.",
    )
    parser.add_argument(
        "--ui",
        choices=["console", "gui"],
        default="console", # TODO: switch this to gui when gui_view implemented
        help="Which UI to launch: console or GUI (default: console).",
    )
    parser.add_argument(
        "--length",
        type=int,
        default=5,
        help="Number of questions to ask in each quiz session (default: 5).",
    )
    args = parser.parse_args()
    return args

def create_question_bank(source_path: Path):
    file_type = source_path.suffix
    if file_type == ".json":
        try:
            return load_questions_from_json(source_path)
        except (FileNotFoundError, ValueError) as e:
            raise SystemExit(
                f"--error: loading JSON questions from {source_path}: {e}"
                )

    elif file_type == ".pgn": # args.source == "pgn" # currently this always throws an exception TODO
        try:
            return load_questions_from_pgn(source_path)
        except Exception as e:
            raise SystemExit(
                f"Error loading PGN from {source_path}: {e}"
            )
    else:
        raise SystemExit(
            f"Error loading PGN or JSON from {source_path}"
        )


def main():
    args = parse_args()

    # Create question bank
    source_string = args.path or "./jsons/chess_sample_data.json"
    source_path = Path(source_string)
    question_bank = create_question_bank(source_path)

    # Create quiz and presenter:
    quiz = QuizBrain(question_bank=question_bank, nb_questions=args.length)
    presenter = QuizPresenter(quiz)

    # Dispatch to chosen UI:
    if args.ui == "console":
        while run_quiz_console(presenter, args.length):
            # new quiz instance means new randomization, same question bank
            quiz = QuizBrain(question_bank=question_bank, nb_questions=args.length)
            presenter = QuizPresenter(quiz)
        
    else:  # args.ui == "gui" # currently this always throws an exception TODO
        try:
            run_quiz_gui(presenter, args.length)

        except Exception:
            raise SystemExit(
                "--error: GUI not implemented yet."
            )

if __name__ == "__main__":
    main()
