import pytest

from pgn_quizzer.quiz_src.model import Question
from pgn_quizzer.quiz_src.model import QuizBrain
from pgn_quizzer.quiz_src.data import load_questions_from_json
from _pytest.fixtures import FixtureRequest # only used for type hints

def sample_quiz_empty_bank_zero_questions():
    # Create a no-question quiz
    return QuizBrain([], nb_questions=0)

def sample_quiz_empty_bank_one_question():
    # Create a quiz with no questions but a request for one
    return QuizBrain([], nb_questions=1)

def sample_quiz_one_question():
    # Create a single‐question quiz with a known FEN
    fen = "8/8/8/8/8/8/8/8 w - - 0 1"
    q = Question("Dummy Q", "A", ["B","C","D"], [fen])
    return QuizBrain([q], nb_questions=1)

def sample_quiz_sample_json_zero_questions():
    # Create a sample quiz but with no requests for questions
    json_path = "chess_quiz/data/chess_sample_data.json"
    question_bank = load_questions_from_json(json_path)
    return QuizBrain(question_bank, nb_questions=0)

def sample_quiz_sample_json_five_questions():
    # Create a sample five-question quiz
    json_path = "chess_quiz/data/chess_sample_data.json"
    question_bank = load_questions_from_json(json_path)
    return QuizBrain(question_bank, nb_questions=5)

@pytest.fixture
def sample_quiz(request: FixtureRequest) -> QuizBrain:
    name = request.param
    if name == "empty_zero":
        # a no-question quiz
        return sample_quiz_empty_bank_zero_questions()
    elif name == "empty_one":
        # a quiz with no questions but a request for one
        return sample_quiz_empty_bank_one_question()
    elif name == "singleton":
        # a single‐question quiz with a known FEN
        return sample_quiz_one_question()
    elif name == "sample_zero":
        # a sample quiz but with no requests for questions
        return sample_quiz_sample_json_zero_questions()
    elif name == "sample_five":
        # a sample five-question quiz
        return sample_quiz_sample_json_five_questions()
    else:
        raise ValueError(f"Unknown quiz type: {name}")

pytestmark =  pytest.mark.parametrize("sample_quiz",
                                      ["singleton",
                                       "sample_five"],
                                      indirect=True)

# def test_(sample_quiz):
#     ...