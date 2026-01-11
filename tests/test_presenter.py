import pytest
from pgn_quizzer.presenter import QuizPresenter

pytestmark =  pytest.mark.parametrize("sample_console_presenter",
                                      ["singleton",
                                       "sample_five"],
                                      indirect=True)

# this test seems dumb
def test_question_statement_states_question(sample_console_presenter: QuizPresenter):
    assert sample_console_presenter.current_question.text in sample_console_presenter.question_statement()

def test_asset_reprs_nonempty_with_valid_bank_and_question(sample_console_presenter: QuizPresenter):
    """
        Given: a nonempty question bank
        When: next question is non-zero and the asset is non-empty
        Then: asset_reprs is nonempty
    """

    asset_repr_strs = sample_console_presenter.question_assets()
    # asset_repr must be a nonempty board representation
    assert asset_repr_strs != []
    for board_render in asset_repr_strs:
        assert isinstance(board_render, str) and len(board_render.strip()) > 0

def test_multiple_choice_dict_length(sample_console_presenter: QuizPresenter):
    """
        Given: valid question
        When: question has N wrong answers
        Then: multiple_choice_dict presents N+1 options
    """

    user_choices_dict = sample_console_presenter.current_user_choices
    nb_wrong_answers = len(sample_console_presenter.current_question.wrong_answers)
    # note that in the dummy data there always is a right answer, as there should be
    assert len(user_choices_dict) == 1 + nb_wrong_answers

def test_multiple_choice_dict_right_answer(sample_console_presenter: QuizPresenter):
    """
        Given: valid question
        Then: multiple_choice_dict contains right_answer
    """

    user_choices_dict = sample_console_presenter.current_user_choices
    right_answer = sample_console_presenter.current_question.right_answer
    assert right_answer in user_choices_dict.values()

def test_multiple_choice_dict_wrong_answers(sample_console_presenter: QuizPresenter):
    """
        Given: valid question
        Then: multiple_choice_dict contains all wrong_answers
    """

    user_choices_dict = sample_console_presenter.current_user_choices
    wrong_answers = sample_console_presenter.current_question.wrong_answers
    assert set(wrong_answers).issubset(set(user_choices_dict.values()))

# this test could probably be a lot better, do I really need to test all possible invalid keys?
def test_is_correct_with_invalid_key(sample_console_presenter: QuizPresenter):
    """
        Given: invalid answer key
        Then: is_correct returns None (exactly!)
    """

    user_choices_dict = sample_console_presenter.current_user_choices
    invalid_key = "?"
    result = sample_console_presenter.is_correct(invalid_key)
    assert result is None

def test_is_correct_with_right_answer(sample_console_presenter: QuizPresenter):
    """
        Given: valid answer key
        When: key corresponds to right answer
        Then: is_correct returns True
    """

    user_choices_dict = sample_console_presenter.current_user_choices
    # find which key maps to the right answer
    correct_key,  = [k for k, v in user_choices_dict.items()
                       if v == sample_console_presenter.current_question.right_answer]
    # input right answer key
    result = sample_console_presenter.is_correct(correct_key)
    assert result is True
    
def test_is_correct_with_wrong_answer(sample_console_presenter: QuizPresenter):
    """
        Given: valid answer key
        When: key corresponds to a wrong answer
        Then: is_correct returns False
    """

    user_choices_dict = sample_console_presenter.current_user_choices
    # find which key maps to the correct answer
    correct_key,  = [k for k, v in user_choices_dict.items()
                       if v == sample_console_presenter.current_question.right_answer]
    # input wrong answer keys
    for k in user_choices_dict.keys():
        if k != correct_key:
            result = sample_console_presenter.is_correct(k)
            assert result is False

# I reckon I will actually test these things in the view tests

# def test_given_answer_when_right_then_score_increases():
#     ...

# def test_given_answer_when_right_then_question_number_incremented():
#     ...

# def test_given_answer_when_wrong_then_question_number_incremented():
#     ...
