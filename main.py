import json
import asyncio
import requests

from typing import List
from typing import Union

from bs4 import BeautifulSoup

from Line import Line
from WordCard import WordCard

lyrics: List[str] = []
with open('lyrics.txt') as lyrics_file:
    lines = lyrics_file.readlines()
    for l in lines:
        lyrics.append(l)


async def get_line(lyric_line: str) -> Line or None:
    line: Line or None = None

    ichi_url: str = "https://ichi.moe/cl/qr/?q="
    url_end: str = "&r=kana"
    r = requests.get(url=ichi_url + lyric_line + url_end)

    if r.status_code == 200:
        html_content: str or None = r.content

        soup = BeautifulSoup(html_content, "html.parser")
        card_rows = soup.find("div", class_="row gloss-row")

        if card_rows is None:
            return Line(lyric_line, [])

        word_card_list: List[WordCard] = []

        card_html_list = []
        for i in range(0, 9):
            card_html_list.append(card_rows.select(f"div#g-0-0-{i}"))

        for card in card_html_list:
            if card:
                word_card_list.append(WordCard(str(card)))
        line = Line(lyric_line, word_card_list)
    else:
        print("wrong")

    await asyncio.sleep(1)
    return line


async def read_lyrics(lyrics: List[str]):
    all_lines: Union[Line, int, str] = []
    for lyric_line in lyrics:
        cl = lyric_line.replace("\n", "").strip()
        if cl == "":
            all_lines.append("")
        else:
            t_idx = -1
            for idx, line_card in enumerate(all_lines):
                if isinstance(line_card, Line):
                    if line_card.is_same_line(cl):
                        print(f"{lyric_line} already found")
                        t_idx = idx
                        all_lines.append(idx)

            if t_idx == -1:
                print(f"Getting new line: {lyric_line}")
                t = await get_line(cl)
                all_lines.append(t)

    json_dict = {}
    for idx, l in enumerate(all_lines):
        if isinstance(l, Line):
            json_dict[idx] = l.return_dict()
        else:
            json_dict[idx] = l

    out_file = open("done.json", "w")
    json.dump(json_dict, out_file)
    out_file.close()

asyncio.run(read_lyrics(lyrics))
