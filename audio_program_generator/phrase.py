"""
"""

from io import BytesIO
from pathlib import Path
from typing import Dict, Generator, Union

import pydub

from gtts import gTTS

from .accent import Accent


class Phrase:
    @classmethod
    def phrases_from_structured_text(
        cls,
        path: Union[str, Path],
        default_pause: float = 0.1,
    ) -> Generator["Phrase", None, None]:
        """Generates a list of Phrase instances from the input file."""

        path = Path(path)

        with path.open("r") as input_file:
            for line in input_file:
                try:
                    yield cls(line, ";", pause=default_pause)
                except ValueError:
                    pass

    @classmethod
    def phrases_from_unstructured_text(
        cls,
        path: Union[str, Path],
        punctuation: Dict[str, float] = None,
        default_pause: float = None,
    ) -> Generator["Phrase", None, None]:
        """Generates a list of Phrase instances from raw text in the input file."""

        path = Path(path)

        if not punctuation:
            punctuation = {
                "!": 0.1,
                "?": 0.1,
                ":": 0.1,
                ";": 0.1,
                ",": 0.1,
                ".": 0.1,
                "(": 0.1,
                ")": 0.1,
            }

        tt = {ord(k): f"; {v}\n" for k, v in punctuation.items()}

        text = path.read_text().replace("\n", " ").replace("  ", " ")

        for line in text.translate(tt).splitlines():
            try:
                yield cls(line, ";", pause=default_pause)
            except ValueError:
                pass

    def __init__(self, raw_text: str, sep: str, pause: float = 0.7) -> None:
        """
        :param raw_text: str
        :param sep: str
        :param pause: optional float defaults to 0.7
        """

        if not raw_text.strip():
            raise ValueError("Unable to generate a phrase from empty text.")

        self.raw_text = raw_text.strip()
        self.sep = sep
        self.default_pause = pause

        if not self.text:
            raise ValueError("Empty phrases are not allowed")

    def __repr__(self) -> str:

        return "".join(
            [
                f"{type(self).__name__}(",
                f"raw_text={self.raw_text!r}, ",
                f"sep={self.sep!r}, ",
                f"pause={self.pause!r})",
            ]
        )
        return

    def __str__(self) -> str:
        return self.text

    @property
    def text(self) -> str:
        """The text of the phrase."""
        try:
            return self._text
        except AttributeError:
            pass
        self._text, *_ = self.raw_text.partition(self.sep)
        return self._text

    @property
    def pause(self) -> float:
        """Duration of pause in seconds at the end of the phrase."""
        try:
            return self._pause
        except AttributeError:
            pass
        *_, self._pause = self.raw_text.partition(self.sep)
        try:
            self._pause = float(self._pause)
        except ValueError:
            self._pause = self.default_pause
        return self._pause

    @pause.setter
    def pause(self, new_value: float) -> None:
        self._pause = float(new_value)

    def render(self, accent: Accent, slow: bool = False) -> pydub.AudioSegment:
        """Returns an AudioSegment for the phrase's text.

        :param accent: Accent
        :param slow: optional bool
        :return: pydub.AudioSegment
        """
        speech = gTTS(self.text, slow=slow, tld=accent.tld)

        with BytesIO() as buffer:
            speech.write_to_fp(buffer)
            buffer.seek(0)
            segment = pydub.AudioSegment.from_file(buffer, format="mp3")
            if self.pause > 0:
                segment += pydub.AudioSegment.silent(duration=int(self.pause * 1000))

        return segment
