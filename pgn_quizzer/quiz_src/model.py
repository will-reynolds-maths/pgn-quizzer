from dataclasses import dataclass
from random import sample

@dataclass(frozen=True, order=False)
class Question:
    """
    Thin wrapper for question data.
    """
    text: str
    right_answer: str
    wrong_answers: list[str]
    assets: list[str]

class QuizBrain:
    """
    Tracks quiz progress and user performance.

    Manages quiz operations: tracks the user's score and number of questions
    answered, and maintains the sequence of questions. Quiz questions are 
    randomly selected upon instantiation, ensuring the quiz length respects the
    available question pool.

    Methods:
        current_question_number():
            Returns current question number (starts at 1).
        next_question():
            Gets the next question in the sequence.
        increment_nb_questions_answered():
            Advances question counter by 1.
        increment_score():
            Increases user score by 1.
        still_has_questions():
            Checks if more questions remain.
        multiple_choice_options(question: Question):
            Returns list of answer options for given question.

    Attributes:
        nb_questions_answered (int): Number of questions answered so far.
        user_score (int): Number of questions answered correctly.
        questions (list of Question): Fixed set of questions sampled at instantiation.
    """

    def __init__(self, question_bank: list[Question], nb_questions: int = 5):
        """
        Initialize the quiz with a set of questions and desired length.

        If `question_bank` contains fewer questions than `nb_questions`, then the quiz
        will use all available questions instead.

        Args:
            question_bank (list[Question]): List of available questions.
            nb_questions (int): Desired number of questions in the quiz.

        Raises:
            ValueError: If `question_bank` is empty or if `nb_questions` is non-positive.
            TypeError: If `nb_questions` is not of type int.
        """

        if question_bank == []:
            raise ValueError("No questions provided. "
                             "Argument question_bank should be non-empty.")
        if nb_questions <= 0:
            raise ValueError("No questions requested. "
                             "Argument nb_questions should be positive.")
        if not isinstance(nb_questions, int):
            raise TypeError("Non-integer number of questions requested. "
                            "Argument nb_questions must have type int.")
        self.nb_questions_answered = 0
        self.user_score = 0
        nb_questions = min(nb_questions, len(question_bank))
        self.questions = sample(question_bank, nb_questions) # randomization

    def current_question_number(self) -> int:
        return 1 + self.nb_questions_answered

    def next_question(self) -> Question:
        return self.questions[self.nb_questions_answered]
    
    def increment_nb_questions_answered(self) -> None:
        self.nb_questions_answered += 1
    
    def increment_score(self) -> None:
        self.user_score += 1
    
    def still_has_questions(self) -> bool:
        return self.nb_questions_answered < len(self.questions)
    
    def multiple_choice_options(self, question: Question) -> list[str]:
        '''
        Generates list of options for user to choose from.

        Args:
            question: 
                A `Question` instance, typically the next question in the quiz.
        
        Returns:
            user_choices_list:
                List containing `question`'s `right_answer` mixed in with the entries 
                of `wrong_answers`.
        '''
        user_choices_list = [question.right_answer] + question.wrong_answers
        user_choices_list = sample(user_choices_list, len(user_choices_list)) # randomization
        return user_choices_list
