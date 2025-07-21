import pytest
from pgn_quizzer.chess_src.presenter import ChessConsolePresenter

pytestmark =  pytest.mark.parametrize("sample_console_presenter",
                                      ["singleton",
                                       "sample_five"],
                                      indirect=True)

# this test seems dumb
def test_question_statement_states_question(sample_console_presenter: ChessConsolePresenter):
    assert sample_console_presenter.current_question.text in sample_console_presenter.question_statement()

def test_asset_reprs_nonempty_with_valid_bank_and_question(sample_console_presenter: ChessConsolePresenter):
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

def test_multiple_choice_repr_length(sample_console_presenter: ChessConsolePresenter):
    """
        Given: valid question
        When: question has N wrong answers
        Then: multiple_choice_repr presents N+1 options
    """

    user_choices_dict = sample_console_presenter.multiple_choice_repr()
    nb_wrong_answers = len(sample_console_presenter.current_question.wrong_answers)
    # note that in the dummy data there always is a right answer, as there should be
    assert len(user_choices_dict) == 1 + nb_wrong_answers

def test_multiple_choice_repr_right_answer(sample_console_presenter: ChessConsolePresenter):
    """
        Given: valid question
        Then: multiple_choice_repr contains right_answer
    """

    user_choices_dict = sample_console_presenter.multiple_choice_repr()
    right_answer = sample_console_presenter.current_question.right_answer
    assert right_answer in user_choices_dict.values()

def test_multiple_choice_repr_wrong_answers(sample_console_presenter: ChessConsolePresenter):
    """
        Given: valid question
        Then: multiple_choice_repr contains all wrong_answers
    """

    user_choices_dict = sample_console_presenter.multiple_choice_repr()
    wrong_answers = sample_console_presenter.current_question.wrong_answers
    assert set(wrong_answers).issubset(set(user_choices_dict.values()))

# this test could probably be a lot better, do I really need to test all possible invalid keys?
def test_check_answer_with_invalid_key(sample_console_presenter: ChessConsolePresenter):
    """
        Given: invalid answer key
        Then: check_answer returns None (exactly!)
    """

    user_choices_dict = sample_console_presenter.multiple_choice_repr()
    invalid_key = "?"
    result = sample_console_presenter.check_answer(invalid_key, user_choices_dict)
    assert result is None

def test_check_answer_with_right_answer(sample_console_presenter: ChessConsolePresenter):
    """
        Given: valid answer key
        When: key corresponds to right answer
        Then: check_answer returns True
    """

    user_choices_dict = sample_console_presenter.multiple_choice_repr()
    # find which key maps to the right answer
    correct_key,  = [k for k, v in user_choices_dict.items()
                       if v == sample_console_presenter.current_question.right_answer]
    # input right answer key
    result = sample_console_presenter.check_answer(correct_key, user_choices_dict)
    assert result is True
    
def test_check_answer_with_wrong_answer(sample_console_presenter: ChessConsolePresenter):
    """
        Given: valid answer key
        When: key corresponds to a wrong answer
        Then: check_answer returns False
    """

    user_choices_dict = sample_console_presenter.multiple_choice_repr()
    # find which key maps to the correct answer
    correct_key,  = [k for k, v in user_choices_dict.items()
                       if v == sample_console_presenter.current_question.right_answer]
    # input wrong answer keys
    for k in user_choices_dict.keys():
        if k != correct_key:
            result = sample_console_presenter.check_answer(k, user_choices_dict)
            assert result is False
    
# the following two tests are implementation-specific
# they should be replaced by tests of behaviour, e.g.,
# test_given_right_answer_then_result_feedback_nonempty
# test_given_wrong_answer_then_result_feedback_nonempty
def test_given_True_then_result_feedback_nonempty(sample_console_presenter: ChessConsolePresenter):
    assert sample_console_presenter.result_feedback(True)

def test_given_False_then_result_feedback_nonempty(sample_console_presenter: ChessConsolePresenter):
    assert sample_console_presenter.result_feedback(False)

# this test is kind of dumb
def test_scoreline_report_states_score(sample_console_presenter: ChessConsolePresenter):
    assert str(sample_console_presenter.quiz.user_score) in sample_console_presenter.scoreline_report()

# I reckon I will actually test these things in the view tests

# def test_given_answer_when_right_then_score_increases():
#     ...

# def test_given_answer_when_right_then_question_number_incremented():
#     ...

# def test_given_answer_when_wrong_then_question_number_incremented():
#     ...
