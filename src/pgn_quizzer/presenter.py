from pgn_quizzer.model import Question
from pgn_quizzer.model import QuizBrain

class QuizPresenter:
    def __init__(self, quiz: QuizBrain):
        self.quiz: QuizBrain = quiz
        self.current_question: Question = Question("", "", [], [])
        self.current_user_choices: dict[str, str] = {"": ""}
    
    def multiple_choice_dict(self) -> dict[str, str]:
        user_choices_list = self.quiz.generate_multiple_choice_options(self.current_question)
        return dict(zip("ABCDEF", user_choices_list))
    
    def is_correct(self, user_answer_key: str) -> bool | None:
        try:
            key = user_answer_key.upper()
            user_answer = self.current_user_choices[key]
        except KeyError:
            return None
        else:
            return user_answer == self.current_question.right_answer
    
    def user_score(self) -> int:
        return self.quiz.user_score
    
    def nb_questions_answered(self) -> int:
        return self.quiz.nb_questions_answered
    
    def question_statement(self) -> str:
        return self.current_question.text
    
    def right_answer(self) -> str:
        return self.current_question.right_answer
    
    def question_assets(self) -> list:
        return self.current_question.assets

    def cue_next_question(self) -> None:
        self.current_question = self.quiz.next_question()
        self.current_user_choices = self.multiple_choice_dict()
    
    def nb_questions_remaining(self) -> int:
        return self.quiz.nb_questions_remaining()
    
    def post_question_update(self, result: bool) -> None:
        if result:
            self.quiz.increment_score()
        self.quiz.increment_nb_questions_answered()

