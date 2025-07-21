from pgn_quizzer.quiz_src.presenter import QuizPresenter
from chess import Board

class ChessConsolePresenter(QuizPresenter):
    """
    Presenter for command-line interface views.

    Implements the abstract interface defined by QuizPresenter to format
    quiz content for presentation in a terminal-based UI. Outputs
    Unicode representations of questions, options, assets and feedback
    to standard output.

    Inherits from:
        QuizPresenter
    
    Implements:
        question_statement():
            Returns question statement for view to display.
        multiple_choice_repr():
            Returns multiple choice options for view to display.
        check_answer(user_answer: str, user_options: dict):
            Checks user's answer against the correct answer.
        result_feedback(result: bool):
            Returns feedback message for view to display.
        scoreline_report():
            Returns formatted user score for view to display.
    
    Notes:
        Assumes standard output and input via terminal. No support for rich text,
        media assets, or event-driven user input.
    """
    
    def question_statement(self) -> str:
        return f"Q.{self.quiz.current_question_number()}: {self.current_question.text}"
    
    def _render_asset_repr(self, fen: str) -> str:
        # the only part of the class that actually uses python-chess
        position = Board(fen)
        return position.unicode(invert_color=True, orientation=position.turn)
    
    # consider making this core? would need to implement ConsolePresenter class then
    def multiple_choice_repr(self) -> dict[str, str]:
        """
        Gets user's options from self.quiz and labels resulting list A, B, C, etc.

        Returns:
            user_choices_dict (dict):
                The labelled randomized user options.

            For example:

            {"A": "Janowski - Capablanca, New York 1916",
             "B": "Steinitz - Lipke, Vienna 1898",
             "C": "Lasker - Capablanca, St. Petersburg 1914"}
            
            Note that the values are delivered in the random order quiz puts them in.
        """

        user_choices_list = self.quiz.multiple_choice_options(self.current_question)
        user_choices_dict = dict(zip("ABCDEF", user_choices_list))
        return user_choices_dict
    
    def check_answer(self, user_answer: str, user_choices: dict[str, str]) -> bool | None: # core? cf gui
        """
        TODO
        """

        try:
            return user_choices[user_answer.upper()] == self.current_question.right_answer
        except KeyError:
            return None
    
    def result_feedback(self, result: bool) -> str:
        if result:
            return "Correct!"
        else:
            return f"Incorrect. The correct answer was {self.current_question.right_answer}."
    
    def scoreline_report(self) -> str:
        return f"{self._user_score()}/{self._nb_questions_answered()}"


class ChessGUIPresenter(QuizPresenter):
    def question_statement(self) -> str:
        ...
    
    def _render_asset_repr(self, fen: str) -> str:
        ...
    
    # consider making this core? need to implement ConsolePresenter class then
    def multiple_choice_repr(self) -> dict:
        """
        Calls quiz to randomize user choices and labels resulting list A, B, C, etc.

        Returns:
            user_choices_dict:
                The labelled randomized list.

            For example:

            {"A": "Janowski - Capablanca, New York 1916",
             "B": "Steinitz - Lipke, Vienna 1898",
             "C": "Lasker - Capablanca, St. Petersburg 1914"}
            
            Note that the values are delivered in the random order quiz puts them in.
        """

        user_choices_list = self.quiz.multiple_choice_options(self.current_question)
        return {} # This needs changing, obviously
    
    def check_answer(self, user_answer: str, user_options: dict): # core? cf gui
        """
        TODO
        """

        try: # this almost does the right thing, just needs tweaking (frustrating, really)
            return user_options[user_answer.upper()] == self.current_question.right_answer
        except KeyError:
            return None
    
    def result_feedback(self, result: bool):
        if result:
            ...
        else:
            ...
    
    # maybe this can be the same!?
    def scoreline_report(self) -> str: 
        return f"{self._user_score()}/{self._nb_questions_answered()}"
