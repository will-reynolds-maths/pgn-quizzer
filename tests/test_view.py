import pytest
from pgn_quizzer.view import run_quiz_console

pytestmark =  pytest.mark.parametrize("sample_console_presenter",
                                      ["doublet"],
                                      indirect=True)

def make_input_provider(inputs: list):
    inputs_iter = iter(inputs)
    def dummy_input(prompt) -> str:
        return next(inputs_iter)
    return dummy_input

def make_output_collector():
    collected = []
    def fake_print(*args, sep=" ", end="\n"):
        text = sep.join(str(arg) for arg in args) + end
        collected.append(text)
    return fake_print, collected

def test_console_view_basic_checks(sample_console_presenter):
    # rather than writing lots of implementation-specific tests,
    # I thought I would just put in this test, which lets me know
    # if my edits have somehow affected the process I'm expecting
    # (but nothing more than that)

    dummy_inputs_list = ["", "?", "A", "y", "b", "n", "hello"]
    dummy_input = make_input_provider(dummy_inputs_list)
    output_list = make_output_collector()
    run_quiz_console(sample_console_presenter, dummy_input, print)
    # assert [bool(s) for s in output_list].count(False) == 19
    assert dummy_input("") == "hello"

def test_console_view_output_checks(sample_console_presenter):
    # rather than writing lots of implementation-specific tests,
    # I thought I would just put in this test, which lets me know
    # if my edits have somehow affected the process I'm expecting
    # (but nothing more than that)

    dummy_inputs_list = ["", "?", "A", "y", "b", "n", "hello"]
    dummy_input = make_input_provider(dummy_inputs_list)
    fake_print, collected = make_output_collector()
    run_quiz_console(sample_console_presenter, dummy_input, fake_print)
    # TODO: figure out what collected is supposed to contain and then test it
    # or mock sample_console_presenter.still_has_questions() and count the
    # number of times it is used?
    assert dummy_input("") == "hello"
