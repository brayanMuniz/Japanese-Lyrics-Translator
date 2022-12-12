from typing import List
from WordCard import WordCard


class Line:
    def __init__(self, line: str, word_card_list: List[WordCard]):
        self.line: str = line
        self.word_card_list: List[WordCard] = word_card_list

    def __repr__(self):
        return f'Line: {self.line}, Cards: {len(self.word_card_list)}'

    def is_same_line(self, test_line: str) -> bool:
        return self.line == test_line

    def return_dict(self) -> dict:
        json_card: List = []
        for card in self.word_card_list:
            json_card.append(card.return_dict())

        return {
            "line": self.line,
            "cards": json_card
        }
