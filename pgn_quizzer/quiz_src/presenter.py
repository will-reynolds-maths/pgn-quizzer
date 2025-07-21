from pgn_quizzer.quiz_src.model import Question
from pgn_quizzer.quiz_src.model import QuizBrain
from abc import ABC, abstractmethod

class QuizPresenter(ABC):
    """
    Abstract base class for presenters in model-view-presenter architecture.

    Acts as a mediator between the QuizBrain model and the view layer. Retrieves
    data from the model, formats it for presentation, and passes it to the view.

    This class is intended to be subclassed. Subclasses must implement the abstract
    methods listed below to define how data is rendered and how user input is handled.

    Methods:
        question_statement() [abstract]:
            Returns question statement for view to display.
        multiple_choice_repr() [abstract]:
            Returns multiple choice options for view to display.
        check_answer(user_answer: str, user_options: dict) [abstract]:
            Checks user's answer against the correct answer.
        result_feedback(result: bool) [abstract]:
            Returns feedback message for view to display.
        scoreline_report() [abstract]:
            Returns formatted user score for view to display.
        still_has_questions():
            Returns whether more questions remain.
        cue_next_question():
            Advances quiz state to the next question.
        question_assets():
            Returns data required by view to display question assets.
        post_question_update(result: bool):
            Updates quiz state after user answers.

    Attributes:
        quiz (QuizBrain):
            Quiz model which handles quiz logic.
        current_question (Question):
            Question being presented to the user; initializes as empty.
    """

    
    def __init__(self, quiz: QuizBrain):
        """
        Initialize the presenter with a quiz model.

        Args:
            quiz (QuizBrain): Quiz model which handles quiz logic
        """
        self.quiz = quiz
        self.current_question = Question("", "", [], []) # initialize as empty question
    
    @abstractmethod
    def question_statement(self):
        ...
    
    @abstractmethod
    def _render_asset_repr(self, asset: str) -> str:
            ...
    
    @abstractmethod
    def multiple_choice_repr(self) -> dict:
        ...

    @abstractmethod
    def check_answer(self, user_answer: str, user_options: dict):
        ...

    @abstractmethod
    def result_feedback(self, result: bool):
        ...
    
    @abstractmethod
    def scoreline_report(self):
        ...

    def still_has_questions(self) -> bool:
        return self.quiz.still_has_questions()
    
    def cue_next_question(self):
        self.current_question = self.quiz.next_question()
    
    def _get_asset_reprs(self) -> list:
        """
        Generate UI-specific representations for question assets.

        Returns:
            list[str]: A list of representations of the question assets suitable for the UI.
        """
        
        return [self._render_asset_repr(asset) for asset in self.current_question.assets]
    
    def question_assets(self) -> list:
        """Returns the data required by the view to display the question assets."""
        return self._get_asset_reprs()

    def _increment_score(self):
        self.quiz.increment_score()

    def _increment_nb_questions_answered(self):
        self.quiz.increment_nb_questions_answered()
    
    def post_question_update(self, result: bool):
        """Increments score and number of questions answered."""
        if result:
            self._increment_score()
        self._increment_nb_questions_answered()
    
    def _user_score(self) -> int:
        return self.quiz.user_score
    
    def _nb_questions_answered(self) -> int:
        return self.quiz.nb_questions_answered
