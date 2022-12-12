from typing import List
from bs4 import BeautifulSoup


class WordCard:
    def __init__(self, gloss_div: str):
        self.word: str = self.get_word(gloss_div)
        self.kana: str = self.get_kana(gloss_div)
        self.definitions: List[str] = self.get_definitions(gloss_div)
        self.conjugation: List[str] = self.get_conjugation(gloss_div)

    def __repr__(self):
        return f' Word: {self.word}, \n Kana: {self.kana}, \n Def : {self.definitions}, \n Conj: {self.conjugation}\n'

    def return_dict(self) -> dict:
        return {
            "word": self.word,
            "kana": self.kana,
            "definitions": self.definitions,
            "conjugation": self.conjugation
        }

    def get_word(self, gloss_div: str) -> str:
        soup = BeautifulSoup(gloss_div, "html.parser")
        return self.__extract_kanji_word(soup.find_all("dt")[0].get_text())

    def get_kana(self, gloss_div: str) -> str or None:
        soup = BeautifulSoup(gloss_div, "html.parser")
        return self.__extract_kana(soup.find_all("dt")[0].get_text())

    def get_definitions(self, gloss_div: str) -> List[str]:
        soup = BeautifulSoup(gloss_div, "html.parser")
        def_html_list: List = soup.find(
            "ol", class_="gloss-definitions").find_all("li")
        return self.__extract_definitions(def_html_list)

    def get_conjugation(self, gloss_div: str) -> List[str]:
        soup = BeautifulSoup(gloss_div, "html.parser")
        li_list: List = soup.find(
            "ol", class_="gloss-definitions").find_all("li")

        word: str = ""
        kana: str or None = None
        definitions: List[str] = []

        conj_html_list = soup.find(
            "div", class_="conjugation")

        if conj_html_list:
            text = conj_html_list.find("dt").get_text()
            word = self.__extract_kanji_word(text)
            kana = self.__extract_kana(text)

            definitions = self.__extract_definitions(li_list)

        return [word, kana, definitions]

    def __extract_kanji_word(self, text: str) -> str:
        word: str = ""
        possible_word: str = text

        left: int = possible_word.find("【")

        if left != -1:
            for idx in range(0, left):
                word = word + possible_word[idx]
        else:
            word = possible_word

        return word

    def __extract_kana(self, text: str) -> str or None:
        kana: str = ""
        left: int = text.find("【")
        right: int = text.find("】")

        if left != -1 and right != -1:
            for idx in range(left + 1, right):
                kana = kana + text[idx]
        else:
            kana = text

        if kana:
            return kana
        return None

    def __extract_definitions(self, list_text: List) -> List[str]:
        definition_list: List[str] = []

        for definition in list_text:
            if definition:
                span_list = definition.find_all()
                for span in span_list:
                    temp: str = span.get_text(strip=True).replace("\n", "")
                    temp = ' '.join(temp.strip().split())

                    definition_list.append(temp)

        return definition_list
