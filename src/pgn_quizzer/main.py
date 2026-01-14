from argparse import ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path

from pgn_quizzer.data import create_question_bank
from pgn_quizzer.model import QuizBrain
from pgn_quizzer.presenter import QuizPresenter
from pgn_quizzer.view import run_quiz_console, run_quiz_gui # TODO


def is_int_in_range(value: str) -> int:
    try:
        ivalue = int(value)
    except ValueError:
        raise ArgumentTypeError(f"{repr(value)} is not a valid integer")

    if not (1 <= ivalue <= 101):
        raise ArgumentTypeError(f"{ivalue} is out of allowed range [1, 101]")

    return ivalue

def parse_args() -> Namespace:
    """
    Set up and parse command-line flags, seeking:
      --path:   path to the JSON or PGN file
      --ui:     either 'console' or 'gui'
      --num:    number of questions to ask (default = 5)
    """
    
    parser = ArgumentParser(description="Run PGN Quizzer.")

    parser.add_argument(
        "--path",
        type=str,
        help="Path to JSON or PGN. "
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


def main():
    # -------------------------
    # Setup:
    # -------------------------
    args = parse_args()
    given_path = args.path
    length = args.length
    ui = args.ui

    # -------------------------
    # Create question bank
    # -------------------------
    source_string = given_path or "./jsons/chess_sample_data.json"
    source_path = Path(source_string)
    question_bank = create_question_bank(source_path)

    # -------------------------
    # Create quiz & presenter
    # -------------------------
    quiz = QuizBrain(question_bank, length)
    presenter = QuizPresenter(quiz)

    # -------------------------
    # Dispatch to chosen UI
    # -------------------------
    if ui == "console":
        while run_quiz_console(presenter):
            # new quiz instance means new randomization, same question bank
            quiz = QuizBrain(question_bank, length)
            presenter = QuizPresenter(quiz)
        
    else:  # ui == "gui" # currently this always throws an exception TODO
        try:
            run_quiz_gui(presenter)

        except Exception:
            raise SystemExit(
                "--error: GUI not implemented yet."
            )
    
    # -------------------------
    # End of main
    # -------------------------

if __name__ == "__main__":
    main()
