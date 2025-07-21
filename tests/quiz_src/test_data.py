import pytest
import pgn_quizzer.quiz_src.data as loader

from pgn_quizzer.quiz_src.model import Question

@pytest.fixture
def sample_question() -> Question:
    return Question(text          = "",
                    right_answer  = "True",
                    wrong_answers = ["False"],
                    assets        = [])

def test_skip_invalid_data_when_right_answer_trivial(sample_question):
    """
        Given: list of question data
        When: item in list has trivial "right_answer" string
        Then: skip that data
    """
    
    dummy_data = [{ # valid data
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": ["False"],
                       "assets": []
                   },
                   { # right_answer trivial string
                       "text": "",
                       "right_answer": "",
                       "wrong_answers": ["False"],
                       "assets": []
                    }]
    result = loader.load_questions_from_data(dummy_data)
    assert result == [sample_question]

def test_skip_invalid_data_when_wrong_answers_empty(sample_question):
    """
        Given: list of question data
        When: item in list is missing "wrong_answers" list
        Then: skip that data
    """
    
    dummy_data = [{ # valid data
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": ["False"],
                       "assets": []
                   },
                   { # wrong_answers empty
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": [],
                       "assets": []
                    }]
    result = loader.load_questions_from_data(dummy_data)
    assert result == [sample_question]

def test_skip_invalid_data_when_wrong_answers_contains_trivial_string(sample_question):
    """
        Given: list of question data
        When: item in list has a "wrong_answers" list but it contains trivial string
        Then: skip that data
    """
    
    dummy_data = [{ # valid data
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": ["False"],
                       "assets": []
                   },
                   { # wrong_answers contains a trivial string
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": ["False", ""],
                       "assets": []
                    }]
    result = loader.load_questions_from_data(dummy_data)
    assert result == [sample_question]

def test_skip_invalid_data_when_text_not_a_string(sample_question):
    """
        Given: list of question data
        When: item in list has "text" value which is not a string
        Then: skip that data
    """
    
    dummy_data = [{ # valid data
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": ["False"],
                       "assets": []
                   },
                   { # text is not a string
                       "text": 0,
                       "right_answer": "True",
                       "wrong_answers": ["False"],
                       "assets": []
                    }]
    result = loader.load_questions_from_data(dummy_data)
    assert result == [sample_question]

def test_skip_invalid_data_when_right_answer_not_a_string(sample_question):
    """
        Given: list of question data
        When: item in list has "right_answer" value which is not a string
        Then: skip that data
    """
    
    dummy_data = [{ # valid data
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": ["False"],
                       "assets": []
                   },
                   { # right_answer is not a string
                       "text": "",
                       "right_answer": True,
                       "wrong_answers": ["False"],
                       "assets": []
                    }]
    result = loader.load_questions_from_data(dummy_data)
    assert result == [sample_question]

def test_skip_invalid_data_when_wrong_answers_not_a_list(sample_question):
    """
        Given: list of question data
        When: item in list has "wrong_answers" value which is not a list
        Then: skip that data
    """
    
    dummy_data = [{ # valid data
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": ["False"],
                       "assets": []
                   },
                   { # wrong_answers is not a list
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": False,
                       "assets": []
                    }]
    result = loader.load_questions_from_data(dummy_data)
    assert result == [sample_question]

def test_skip_invalid_data_when_wrong_answers_list_contains_non_string(sample_question):
    """
        Given: list of question data
        When: item in list has a "wrong_answers" list but it contains an entry which is not a string
        Then: skip that data
    """
    
    dummy_data = [{ # valid data
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": ["False"],
                       "assets": []
                   },
                   { # wrong_answers is not a list of strings
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": [False],
                       "assets": []
                    }]
    result = loader.load_questions_from_data(dummy_data)
    assert result == [sample_question]

def test_skip_invalid_data_when_assets_not_a_list(sample_question):
    """
        Given: list of question data
        When: item in list has "assets" value which is not a list
        Then: skip that data
    """
    
    dummy_data = [{ # valid data
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": ["False"],
                       "assets": []
                   },
                   { # assets is not a list
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": [],
                       "assets": "8/8/8/8/8/8/8/8 w - - 0 1"
                    }]
    result = loader.load_questions_from_data(dummy_data)
    assert result == [sample_question]

def test_skip_invalid_data_when_assets_list_contains_non_string(sample_question):
    """
        Given: list of question data
        When: item in list has an "assets" list but it contains an entry which is not a string
        Then: skip that data
    """
    
    dummy_data = [{ # valid data
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": ["False"],
                       "assets": []
                   },
                   { # assets is not a list of strings
                       "text": "",
                       "right_answer": "True",
                       "wrong_answers": [],
                       "assets": [0]
                    }]
    result = loader.load_questions_from_data(dummy_data)
    assert result == [sample_question]
