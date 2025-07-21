from json import load
from pgn_quizzer.quiz_src.model import Question

def _load_data_from_json(path: str) -> list[dict]:
    '''Validated at runtime.'''
    # hard to test!
    with open(path, mode='r') as json:
        question_data = load(json)
    return question_data

def _validate_data(q: dict) -> bool:
    # the data must be of the correct types
    if not isinstance(q["text"], str):
        return False
    elif not isinstance(q["right_answer"], str):
        return False
    elif not isinstance(q["wrong_answers"], list):
        return False
    elif not isinstance(q["assets"], list):
        return False
    elif not all([isinstance(a, str) for a in q["wrong_answers"]]):
        return False
    elif not all([isinstance(a, str) for a in q["assets"]]):
        return False
    
    # this is a multiple choice quiz
    # each question needs at least one right answer and at least one wrong answer
    # and none of the entries of `wrong_answers` are allowed to be empty strings
    choices = [q["right_answer"]] + q["wrong_answers"]
    wrong_answers_exist = bool(q["wrong_answers"])
    no_trivial_answers = all(choices)
    return wrong_answers_exist and no_trivial_answers

def load_questions_from_data(question_data: list[dict]) -> list[Question]:
    '''Generates list of Question objects from question data; invalid data
    is ignored (skipped over).'''

    valid_data = filter(_validate_data, question_data)
    return [Question(text          = q["text"],
                     right_answer  = q["right_answer"],
                     wrong_answers = q["wrong_answers"],
                     assets        = q["assets"])
                     for q in valid_data]

def load_questions_from_json(path: str) -> list[Question]:
    '''
    Opens file at path, parses JSON, and returns list of Question instances.

    Invalid data - question data with no right answer, or with no wrong 
    answers - is skipped over. Questions can have no text for the
    question statement, and questions can have no assets to display
    alongside the answer options and/or text.

    Args:
        path (str):
            The path to a JSON file.
    
    Returns:
        questions (list):
            List of Question objects created using the data in the JSON.
    '''

    data = _load_data_from_json(path)
    questions = load_questions_from_data(data)
    return questions
