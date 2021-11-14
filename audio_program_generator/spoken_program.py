import math

from enum import Enum
from io import StringIO
from pathlib import Path
from typing import List, Union

import pydub
from tqdm import tqdm

from .phrase import Phrase
from .accent import Accent


class SpokenProgram:
    @classmethod
    def from_file(
        cls, path: Union[str, Path], structured: bool = True
    ) -> "SpokenProgram":
        """Returns a SpokenProgram whose source is read from `path`.

        :param path: str or Path
        :param structured: optional bool
        """
        if structured:
            parser = Phrase.phrases_from_structured_text
        else:
            parser = Phrase.phrases_from_unstructured_text

        phrases = list(parser(path))

        return cls(phrases)

    @classmethod
    def from_string(cls, source: str, structured: bool = True) -> "SpokenProgram":
        """Returns a SpokenProgram whose source text is a string.

        :param source: str
        :param structured: optional bool
        """
        buffer = StringIO(source)
        return cls.from_file(buffer, structured)

    def __init__(
        self,
        phrases: List[Phrase],
    ) -> None:
        self.phrases = phrases

    def __str__(self) -> str:
        return "\n".join([p.text for p in self.phrases])

    def render(
        self,
        bg_audio_path: Union[str, Path] = None,
        accent: Accent = None,
        slow: bool = False,
        attenuation: float = 0.0,
        fade_in: int = 3000,
        fade_out: int = 6000,
        hide_progress_bar: bool = False,
    ) -> pydub.AudioSegment:
        """Renders this SpokenProgram to a pydub.AudioSegment.

        :param bg_audio_path: str or Path
        :param accent: Accent, defaults to Accent.US
        :param slow: bool, defaults to False
        :param fade_in: int, defaults to 3000 ms
        :param fade_out: int, defaults to 6000 ms
        :param hide_progress_bar: bool, defaults to False
        :return: pydub.AudioSegment
        """

        accent = accent or Accent.US

        audio = pydub.AudioSegment.empty()

        for phrase in tqdm(self.phrases, disable=hide_progress_bar):
            audio += phrase.render(accent, slow)

        if not bg_audio_path:
            return audio

        bg_audio = pydub.AudioSegment.from_file(str(Path(bg_audio_path)))

        speech_duration = len(audio)
        bg_duration = len(bg_audio)

        if speech_duration > bg_duration:
            nrepeats = math.ceil(speech_duration / bg_duration)
            bg_audio *= nrepeats
        bg_audio = bg_audio[:speech_duration]
        bg_audio -= float(attenuation)
        bg_audio.fade_in(fade_in).fade_out(fade_out)

        return audio.overlay(bg_audio, loop=True)
