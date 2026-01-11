from dataclasses import dataclass, field
from json import dumps, load
from random import sample
from chess import Board
from pgn_quizzer.model import Question

#-------------------------
# Chess Data Processing
#-------------------------

@dataclass(frozen=False, order=False)
class ChessGame:
    title: str
    fen_assets: dict[str, list[str]] = field(default_factory=dict)

class ChessGameConstructor:
    """
    TODO: write a docstring
    """
    
    def __init__(self, pgn: str):
        self.pgn = pgn
        self.chessgames = []
        self.titles = []

    def _separate_games_within_pgn(self) -> list[str]:
        ...

    def _strip_annotation_text(self, subpgn: str) -> str:
        ...

    def _strip_irrelevant_moves(self, subpgn: str) -> str:
        ...

    def _extract_title(self, subpgn: str) -> str:
        ...

    def _strip_metadata(self, subpgn: str) -> str:
        ...

    def _get_fens(self, subpgn: str) -> dict[str, list[str]]:
        ...

    def _construct_chessgame_object(self, title: str, asset_fens: dict[str, list[str]]):
        return ChessGame(title, asset_fens)
    
    def construct(self):
        list_subpgns = self._separate_games_within_pgn()
        for subpgn in list_subpgns:
            subpgn = self._strip_annotation_text(subpgn)
            subpgn = self._strip_irrelevant_moves(subpgn)

            subpgn_title = self._extract_title(subpgn)
            self.titles.append(subpgn_title)
            
            subpgn = self._strip_metadata(subpgn)
            subpgn_asset_fens = self._get_fens(subpgn)
            
            game = self._construct_chessgame_object(subpgn_title, subpgn_asset_fens)
            self.chessgames.append(game)


def _sample_with_avoidance(lst: list[str], k: int, bad_val: str):
    while True:
        sample_attempt = sample(lst, k)
        if bad_val not in sample_attempt:
            break
    return sample_attempt

# TODO: the following function is delicately implemented and needs to be tested well
def _generate_question_data(game: ChessGame, constructor: ChessGameConstructor, nb_options: int):
    """
    TODO: write a docstring
    """
    
    question_text = {"desc1": "a",
                     "desc2": "b",
                     "desc3": "c",}
    
    question_data = {"text": "",
                     "right_answer": game.title, # N.B.
                     "wrong_answers": [],
                     "assets": []}
    question_list = []

    for desc in game.fen_assets.keys():
        question_data["text"] = question_text[desc]

        for fen in game.fen_assets[desc]:
            options = _sample_with_avoidance(constructor.titles, nb_options, game.title)
            question_data["wrong_answers"] = options
            question_data["assets"] = fen

            question_list.append(question_data)
    
    return question_list

# I guess at this stage I'm including this function just in case
# TODO: decide what you want to do with this function
def pgn_2_json(path: str, nb_options=3) -> str:
    with open(path, mode="r") as pgn_text:
        pgn = str(pgn_text)
    
    json_array_list = []
    constructor = ChessGameConstructor(pgn)
    constructor.construct()

    for game in constructor.chessgames:
        question_data_list = _generate_question_data(game, constructor, nb_options)
        json_array_list += question_data_list
    
    return dumps(json_array_list)

def load_questions_from_pgn(path: str, nb_options=3) -> list[Question]:
    if nb_options > 6:
        raise ValueError("More than 6 options is too many! "
                         "Choose a number of options less than 7.")
    with open(path, mode="r") as pgn_file:
        pgn = pgn_file.read()
    
    constructor = ChessGameConstructor(pgn)
    constructor.construct()
    question_data = []

    for game in constructor.chessgames:
        question_data += _generate_question_data(game, constructor, nb_options)
    
    return load_questions_from_data(question_data)

#-------------------------
# Quiz Data Processing
#-------------------------

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
