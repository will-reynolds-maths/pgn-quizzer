import pytest
from _pytest.fixtures import FixtureRequest # only used for type hints

from random import choice

from pgn_quizzer.quiz_src.model import Question, QuizBrain
from pgn_quizzer.quiz_src.data import load_questions_from_json

from pgn_quizzer.chess_src.presenter import ChessConsolePresenter

# print("CONFTEST") # useful for debugging

def sample_presenter_empty_bank_zero_questions():
    # Create a no-question quiz
    quiz = QuizBrain([], nb_questions=0)
    return ChessConsolePresenter(quiz)

def sample_presenter_empty_bank_one_question():
    # Create a quiz with no questions but a request for one
    quiz = QuizBrain([], nb_questions=1)
    return ChessConsolePresenter(quiz)

def sample_presenter_one_question():
    # Create a single‐question quiz with a known FEN
    fen = "8/8/8/8/8/8/8/8 w - - 0 1"
    q = Question("Dummy Q", "A", ["B","C","D"], [fen])
    quiz = QuizBrain([q], nb_questions=1)
    presenter = ChessConsolePresenter(quiz)
    presenter.cue_next_question()
    return presenter

def sample_presenter_two_questions():
    # Create a single‐question quiz with a known FEN
    fen = "8/8/8/8/8/8/8/8 w - - 0 1"
    q = Question("Dummy Q", "A", ["B","C","D"], [fen])
    quiz = QuizBrain([q, q], nb_questions=2)
    presenter = ChessConsolePresenter(quiz)
    presenter.cue_next_question()
    return presenter

def sample_presenter_sample_json_zero_questions():
    # Create a sample quiz but with no requests for questions
    json_path = "pgn_quizzer/chess_src/chess_sample_data.json"
    question_bank = load_questions_from_json(json_path)
    quiz = QuizBrain(question_bank, nb_questions=0)
    return ChessConsolePresenter(quiz)

def sample_presenter_sample_json_five_questions():
    # Create a sample five-question quiz
    json_path = "pgn_quizzer/chess_src/chess_sample_data.json"
    question_bank = load_questions_from_json(json_path)
    quiz = QuizBrain(question_bank, nb_questions=5)
    sample_console_presenter = ChessConsolePresenter(quiz)
    random_nb = choice(range(1, 5)) # randomized
    for _ in range(1, random_nb):
        sample_console_presenter.cue_next_question()
        if choice([True, False]): # randomized
            quiz.increment_score()
    sample_console_presenter.cue_next_question()
    return sample_console_presenter

@pytest.fixture
def sample_console_presenter(request: FixtureRequest) -> ChessConsolePresenter:
    name = request.param
    if name == "empty_zero":
        # a no-question quiz
        return sample_presenter_empty_bank_zero_questions()
    elif name == "empty_one":
        # a quiz with no questions but a request for one
        return sample_presenter_empty_bank_one_question()
    elif name == "singleton":
        # a single‐question quiz with a known FEN
        return sample_presenter_one_question()
    elif name == "doublet":
        # a two‐question quiz with a known FEN
        return sample_presenter_two_questions()
    elif name == "sample_zero":
        # a sample quiz but with no requests for questions
        return sample_presenter_sample_json_zero_questions()
    elif name == "sample_five":
        # a sample five-question quiz
        return sample_presenter_sample_json_five_questions()
    else:
        raise ValueError(f"Unknown presenter type: {name}")
