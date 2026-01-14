from chess import Board

from pgn_quizzer.presenter import QuizPresenter

def run_quiz_gui(presenter: QuizPresenter) -> None:
    """
    Coordinator function which runs the quiz in a graphical user interface.

    Prints formatted data to the screen and collects input. All checking of
    answers, tracking of score, and data formatting is handled by the
    presenter.

    Intended to be the default user interface.

    Parameters:
        presenter (QuizPresenter): 
            Interfaces with the model, tells the view what to display.

    Returns:
        bool: True if the user wants to play again, False otherwise.
    """

    raise Exception

def run_quiz_console(presenter: QuizPresenter,
                     input_func = input, # abstraction for testing
                     output_func = print
                     ) -> None:
    """
    Coordinator function which runs the quiz in a console (text-based) interface.

    Prints formatted data to the console and collects input. All checking of
    answers, tracking of score, and data formatting is handled by `presenter`.

    Intended as a fallback interface for testing and debugging core quiz logic.

    Parameters:
        presenter (QuizPresenter):
            Interfaces with the model, tells the view what to display.

    Returns:
        True if the user wants to play again, False otherwise.
    """

    output_func(f"Welcome to the quiz! You'll be asked {presenter.nb_questions_remaining()} questions.")
    output_func("")

    while presenter.nb_questions_remaining():
        # confirm user still wants to play
        user_confirmation = input_func("Continue? [Y/n] ")
        if user_confirmation.lower() == "n":
            break
        output_func("")
        
        # load question
        presenter.cue_next_question()

        # print question statement
        output_func(f"Q{1 + presenter.nb_questions_answered()}: {presenter.question_statement()}")
        output_func("")
        
        # print assets
        fen, *_ = presenter.question_assets()
        position = Board(fen)
        output_func(position.unicode(invert_color=True, orientation=position.turn), sep="\n\n")
        output_func("")
        
        # generate user answer choices
        user_choices_dict = presenter.current_user_choices

        # print user answer choices
        for k, v in user_choices_dict.items():
            output_func(f"{k}. {v}")
        output_func("")
        
        # prompt for user's answer
        user_answer_key = input_func(f"Your answer ({", ".join(user_choices_dict)}): ")
        
        # validate user input
        while presenter.is_correct(user_answer_key) is None:
            output_func(f"Please input one of the following options: {", ".join(user_choices_dict)}.")
            user_answer_key = input_func("Your answer: ")

        result = presenter.is_correct(user_answer_key)
        assert type(result) is bool # obviously true now because of the while loop

        # print feedback (correct/incorrect)
        if result:
            output_func("Correct!")
        else:
            output_func(f"Incorrect. The correct answer was {presenter.right_answer()}.")

        # update score and number of questions answered
        presenter.post_question_update(result)
        
        # inform user
        if presenter.nb_questions_remaining():
            output_func(f"Your current score is: {presenter.user_score()}/{presenter.nb_questions_answered()}.")
            output_func("")

    output_func("")
    output_func("Quiz over!")
    output_func(f"Overall, you scored {presenter.user_score()}/{presenter.nb_questions_answered()}.")
    output_func("")

    play_again = input_func("Would you like to play again? [Y/n] ")
    return play_again.lower() != "n"