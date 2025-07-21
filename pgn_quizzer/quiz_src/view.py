from pgn_quizzer.quiz_src.presenter import QuizPresenter

def run_quiz_console(presenter: QuizPresenter,
                     nb_questions: int,
                     input_func = input, # abstraction for testing
                     output_func = print):
    """
    Coordinator function which runs the quiz in a console (text-based) interface.

    Prints formatted data to the console and collects input. All checking of
    answers, tracking of score, and data formatting is handled by `presenter`. The
    number of questions shown is controlled by `nb_questions`.

    Intended as a fallback interface for testing and debugging core quiz logic.

    Parameters:
        presenter (QuizPresenter):
            Interfaces with the model, tells the view what to display.
        nb_questions (int):
            The number of questions to ask in the current quiz session.

    Returns:
        True if the user wants to play again, False otherwise.
    """

    output_func(f"Welcome to the quiz! You'll be asked {nb_questions} questions.")
    output_func("")

    while presenter.still_has_questions():
        # confirm user still wants to play
        user_confirmation = input_func("Continue? [Y/n] ")
        if user_confirmation.lower() == "n":
            break
        output_func("")
        
        # load question
        presenter.cue_next_question()

        # print question statement
        output_func(presenter.question_statement())
        output_func("")
        
        # print assets
        output_func(*presenter.question_assets(), sep="\n\n")
        output_func("")
        
        # generate user answer choices
        user_choices_dict = presenter.multiple_choice_repr()

        # print user answer choices
        for k, v in user_choices_dict.items():
            output_func(f"{k}. {v}")
        output_func("")
        
        # prompt for user's answer
        user_answer = input_func(f"Your answer ({", ".join(user_choices_dict)}): ")
        
        # validate user input
        while presenter.check_answer(user_answer, user_choices_dict) is None:
            output_func(f"Please input one of the following options: {", ".join(user_choices_dict)}.")
            user_answer = input_func("Your answer: ")

        result = presenter.check_answer(user_answer, user_choices_dict)
        assert type(result) is bool # obviously true now because of the while loop

        # print feedback (correct/incorrect)
        output_func(presenter.result_feedback(result))

        presenter.post_question_update(result)

        if presenter.still_has_questions():
            output_func(f"Your current score is: {presenter.scoreline_report()}.")
            output_func("")

    output_func("")
    output_func("Quiz over!")
    output_func(f"Overall, you scored {presenter.scoreline_report()}.")
    output_func("")

    play_again = input_func("Would you like to play again? [Y/n] ")
    return play_again.lower() != "n"

def run_quiz_gui(presenter: QuizPresenter, nb_questions: int):
    """
    Coordinator function which runs the quiz in a graphical user interface.

    Prints formatted data to the screen and collects input. All checking of
    answers, tracking of score, and data formatting is handled by the
    presenter. The number of questions shown is controlled by `nb_questions`.

    Intended to be the default user interface.

    Parameters:
        presenter (QuizPresenter): 
            Interfaces with the model, tells the view what to display.
        nb_questions (int):
            The number of questions to ask in the current quiz session.

    Returns:
        bool: True if the user wants to play again, False otherwise.
    """

    raise Exception