import pytest
from _pytest.fixtures import FixtureRequest # only used for type hints

from random import choice
from pathlib import Path

from pgn_quizzer.model import Question, QuizBrain
from pgn_quizzer.data import create_question_bank

from pgn_quizzer.presenter import QuizPresenter

# print("CONFTEST") # useful for debugging

def sample_presenter_empty_bank_zero_questions():
    # Create a no-question quiz
    quiz = QuizBrain([], length=0)
    return QuizPresenter(quiz)

def sample_presenter_empty_bank_one_question():
    # Create a quiz with no questions but a request for one
    quiz = QuizBrain([], length=1)
    return QuizPresenter(quiz)

def sample_presenter_one_question():
    # Create a single‐question quiz with a known FEN
    fen = "8/8/8/8/8/8/8/8 w - - 0 1"
    q = Question("Dummy Q", "A", ["B","C","D"], fen)
    quiz = QuizBrain([q], length=1)
    presenter = QuizPresenter(quiz)
    presenter.cue_next_question()
    return presenter

def sample_presenter_two_questions():
    # Create a single‐question quiz with a known FEN
    fen = "8/8/8/8/8/8/8/8 w - - 0 1"
    q = Question("Dummy Q", "A", ["B","C","D"], fen)
    quiz = QuizBrain([q, q], length=2)
    presenter = QuizPresenter(quiz)
    presenter.cue_next_question()
    return presenter

def sample_presenter_sample_json_zero_questions():
    # Create a sample quiz but with no requests for questions
    json_path = Path(".\\jsons\\chess_sample_data.json")
    question_bank = create_question_bank(json_path)
    quiz = QuizBrain(question_bank, length=0)
    return QuizPresenter(quiz)

def sample_presenter_sample_json_five_questions():
    # Create a sample five-question quiz
    json_path = Path(".\\jsons\\chess_sample_data.json")
    question_bank = create_question_bank(json_path)
    quiz = QuizBrain(question_bank, length=5)
    sample_console_presenter = QuizPresenter(quiz)
    random_nb = choice(range(1, 5)) # randomized
    for _ in range(1, random_nb):
        sample_console_presenter.cue_next_question()
        if choice([True, False]): # randomized
            quiz.increment_score()
    sample_console_presenter.cue_next_question()
    return sample_console_presenter

@pytest.fixture
def sample_console_presenter(request: FixtureRequest) -> QuizPresenter:
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
