"""
Generate audio program of spoken phrases, with optional background sound file mixed in

"""
import os
import re
import math
from io import StringIO, BytesIO
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment
from alive_progress import alive_bar, config_handler
from audio_program_generator import cli


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
    def __init__(self, phrase_file: StringIO, sound_file: BytesIO = None, **kwargs):
        """
        Initialize class instance
        """

        self.filenames_valid = self._validate_filename_extensions(
            phrase_file, sound_file
        )  # Only support '.txt', '.wav' for phrase_file, sound_file
        self.phrase_file = phrase_file.read()  # Fileobj to generate speech segments
        self.sound_file = sound_file  # Fileobj to mix w/ generated speech
        self.slow = kwargs.get("slow", False)  # Half-speed speech if True
        self.attenuation = kwargs.get("attenuation", 10)  # Attenuation value, if mixing
        self.tld = kwargs.get("tld", "com")  # TLD for accents
        self.speech_file = None  # Generated speech/silence
        self.mix_file = None  # Mixed speeech/sound
        self.result = BytesIO(None)  # File-like object to store final result
        self.hide_progress_bar = kwargs.get("hide_progress_bar", False)
        self.book_mode = kwargs.get("book_mode", False)

        config_handler.set_global(
            bar=None,
            stats=False,
            monitor=False,
            elapsed=False,
            disable=self.hide_progress_bar,
        )  # Set 'alive' progress bar global options

    def _gen_speech(self):
        """
        Generate a combined speech file, made up of gTTS-generated speech
        snippets from each line in the phrase_file + corresponding silence.
        """

        combined = AudioSegment.empty()

        if self.book_mode:
            phrases = self.phrase_file.split(os.linesep)
            durations = [None for elem in range(len(phrases))]
            items = list(zip(phrases, durations))
        else:
            items = parse_textfile(self.phrase_file)

        for phr, dur in items:
            # Skip blank phrases or gTTS will throw exception
            if not phr.strip():
                continue

            # Write gTTS snippet to temp file for later access
            tmpfile = BytesIO(None)
            speech = gTTS(phr, slow=self.slow, tld=self.tld)
            speech.write_to_fp(tmpfile)
            tmpfile.seek(0)

            # Add the current speech snippet + corresponding silence
            # to the combined file, building up for each new line.
            snippet = AudioSegment.from_file(tmpfile, format="mp3")
            combined += snippet
            if dur:
                combined += AudioSegment.silent(duration=1000 * int(dur))
            tmpfile.close()

        self.speech_file = combined

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

    def _validate_filename_extensions(
        self, phr_file: StringIO, snd_file: BytesIO
    ) -> bool:
        """
        Verify attempted use of filenames
        """

        if snd_file:
            return (
                Path(snd_file.name).suffix == ".wav"
                and Path(phr_file.name).suffix == ".txt"
            )
        return Path(phr_file.name).suffix == ".txt"

    def invoke(self) -> BytesIO:
        """
        Generate gTTS speech snippets for each phrase; optionally mix with
        background sound-file; then save resultant mp3.
        """
        assert self.filenames_valid
        with alive_bar(0):
            self._gen_speech()
            if self.sound_file:
                bkgnd = AudioSegment.from_file(self.sound_file, format="wav")
                self.mix_file = self._mix(self.speech_file, bkgnd, self.attenuation)
                self.mix_file.export(self.result, format="mp3")
            else:
                self.speech_file.export(self.result, format="mp3")
        return self.result
