"""
Generate audio program of spoken phrases, with optional background sound file mixed in
"""
import re
import math
import concurrent.futures

from dataclasses import dataclass
from io import StringIO, TextIOWrapper, BytesIO, BufferedReader
from typing import Union
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment
from alive_progress import alive_bar, config_handler
from sentence_splitter import split_text_into_sentences
from single_source import get_version


def parse_textfile(phrase_file_contents: str = "") -> list:
    """
    Clean up user-supplied phrase file to comform with expected format
    """

    def clean(dirty: str = "") -> str:
        cleaner = r"[^A-Za-z0-9\s;\v]"
        cleaned = re.compile(cleaner, flags=re.MULTILINE | re.UNICODE)
        return re.sub(cleaned, "", dirty)

    def capture(cleaned: str = "") -> list:
        capturer = r"^\s*([\w\s]+?)\s*;\s*(\d+)\s*$"
        captured = re.compile(capturer, flags=re.MULTILINE | re.UNICODE)
        return re.findall(captured, cleaned)

    return capture(clean(phrase_file_contents))


class AudioProgramGenerator:
    """Main class to generate speech output file with mixed-in background sound"""

    @dataclass
    class PhraseHandler:
        index: int
        phrase: str
        duration: float
        tempfile: BytesIO

    def __init__(
        self,
        phrase_file: Union[StringIO, TextIOWrapper],
        sound_file: BufferedReader = None,
        **kwargs,
    ):
        if isinstance(phrase_file, (TextIOWrapper, StringIO)):
            self.phrases = phrase_file.read()
        else:
            raise (
                TypeError,
                f"phrase_file must be either StringIO or TextIOWrapper, not {type(phrase_file)}.",
            )
        self.__version__ = get_version(__name__, Path(__file__).parent.parent)
        self.sound_file = sound_file  # Fileobj to mix w/ generated speech
        self.slow = kwargs.get("slow", False)  # Half-speed speech if True
        self.attenuation = kwargs.get("attenuation", 10)  # Attenuation value, if mixing
        self.tld = kwargs.get("tld", "com")  # TLD for accents
        self.speech_file = None  # Generated speech/silence
        self.mix_file = None  # Mixed speeech/sound
        self.result = BytesIO(None)  # File-like object to store final result
        self.hide_progress_bar = kwargs.get("hide_progress_bar", False)
        self.book_mode = kwargs.get("book_mode", False)
        self.output_format = kwargs.get("output_format", "wav")
        self.phrase_handlers = []  # List of PhraseHandler objects for ThreadExecution

        # Config items for progress bar
        config_handler.set_global(
            bar=None,
            stats=False,
            monitor=False,
            elapsed=False,
            disable=self.hide_progress_bar,
        )

    def _gen_speech(self):
        """
        Generate a combined speech file, made up of gTTS-generated speech
        snippets from each line in the phrase_file + corresponding silence.
        """

        def _create_tempfile(ph: AudioProgramGenerator.PhraseHandler) -> None:
            """Thread worker function to turn a phrase into encoded snippet"""
            tempfile = BytesIO(None)
            speech = gTTS(ph.phrase, slow=self.slow, tld=self.tld)
            speech.write_to_fp(tempfile)
            tempfile.seek(0)
            ph.tempfile = tempfile

        # Get phrases and durations, and store values in PhraseHandler
        i = 0
        if self.book_mode:
            for sentence in split_text_into_sentences(self.phrases, language="en"):
                phrase_handler = AudioProgramGenerator.PhraseHandler(
                    index=i, phrase=sentence, duration=1, tempfile=None
                )
                self.phrase_handlers.append(phrase_handler)
                i += 1
        else:
            phrases_and_durations = parse_textfile(self.phrases)
            for phrase_and_duration in phrases_and_durations:
                phrase_handler = AudioProgramGenerator.PhraseHandler(
                    index=i,
                    phrase=phrase_and_duration[0],
                    duration=phrase_and_duration[1],
                    tempfile=None,
                )
                self.phrase_handlers.append(phrase_handler)
                i += 1

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for phrase_handler in self.phrase_handlers:
                futures.append(executor.submit(_create_tempfile, ph=phrase_handler))
            concurrent.futures.as_completed(futures)

        self.speech_file = AudioSegment.empty()
        for phrase_handler in self.phrase_handlers:
            if not phrase_handler.tempfile:
                continue
            snippet = AudioSegment.from_file(phrase_handler.tempfile, format="mp3")
            self.speech_file += snippet
            if phrase_handler.duration:
                self.speech_file += AudioSegment.silent(
                    duration=1000 * int(phrase_handler.duration)
                )

    def _mix(
        self,
        segment1: AudioSegment,
        segment2: AudioSegment,
        seg2_atten: int = 0,
        fadein: int = 3000,
        fadeout: int = 6000,
    ) -> AudioSegment:
        """
        Mixes two pydub AudioSegments, then fades the result in/out.
        Returns mixed AudioSegment.
        """
        duration1 = len(segment1)
        duration2 = len(segment2)

        if duration1 > duration2:
            times = math.ceil(duration1 / duration2)
            segment2_normalized = segment2 * times
            segment2_normalized = segment2_normalized[:duration1]
        else:
            segment2_normalized = segment2[:duration1]

        return (segment1).overlay(
            (segment2_normalized - float(seg2_atten)).fade_in(fadein).fade_out(fadeout)
        )

    def invoke(self) -> BytesIO:
        """
        Generate gTTS speech snippets for each phrase; optionally mix with
        background sound-file.
        Returns BytesIO object (encoded in format specified by 'output_format').
        """
        # assert self.filenames_valid
        with alive_bar(0):
            self._gen_speech()
            if self.sound_file:
                bkgnd = AudioSegment.from_file(self.sound_file, format="wav")
                self.mix_file = self._mix(self.speech_file, bkgnd, self.attenuation)
                self.mix_file.export(self.result, format=self.output_format)
            else:
                self.speech_file.export(self.result, format=self.output_format)
        return self.result
