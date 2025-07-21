from dataclasses import dataclass, field
from json import dumps
from random import sample
from chess import Board

from pgn_quizzer.quiz_src.data import load_questions_from_data
from pgn_quizzer.quiz_src.model import Question

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