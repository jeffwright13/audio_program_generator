"""
Description:
    apg.py:
    Generate audio program of spoken phrases, with optional background
    sound file mixed in.

    User populates a semicolon-separated text file with plain-text phrases,
    each followed by an inter-phrase duration. Each line of the file is
    comprised of:
      - one phrase to be spoken
      - a semicolon
      - a silence duration (specified in seconds)
    Obviously, do not include superfluous semicolons in this file. An exception
    will occur if you do.

    The script generates and saves a single MP3 file. The base name of the
    file is the same as the specified input file. So, for example, if the
    script is given input file "phrases.txt", the output file will be
    "phrases.mp3".

    Specifying the optional sound_file parameter allows the user to mix in
    background sounds. This parameter represents the path/filename of a sound
    ile to be mixed in with the speech file generated from the phrase file. If
    the sound file is shorter in duration than the generated speech file, it
    will be looped. If it is longer, it will be truncated. The resulting
    background sound (looped or  not) will be faded in and out to ensure a
    smooth transition. Currently, only .wav files are supported.

    The CLI prints out a progress bar as the phrase file is converted into gTTS
    speech snippets. However, no progress bar is shown for the secondary mix
    step (when the optional sound_file parameter is specified). There can be a
    significant delay in going from the end of the first stage (snippet
    generation) to the end of the second stage (mixing), primarily because of
    reading in the .wav file. For this reason, you may want to select a sound
    file for mixing that is small (suggested <20MB). Otherwise, be prepared to
    wait.


Usage:
    apg [options] <phrase_file> [<sound_file>]
    apg -V --version
    apg -h --help

Options:
    -a --attenuation LEV    Set attenuation level of background file (non-
                            negative number indicating dB attenuation)
                            ([default: 0]).
    -d --debug              Print debug statements to console.
    -s --slow               Generate speech at half-speed
    -V --version            Show version.
    -h --help               Show this screen.

Arguments:
    phrase_file             Path/name of semicolon-separated text file
                            containing phrases and silence durations.
    sound_file              Path/name of optional wavefile to mix with the
                            speech generated from the phrase file. Useful for
                            background music/sounds. Must be in .wav format.

Example <phrase_file> format:
    Phrase One;2
    Phrase Two;5
    Phrase Three;0

Author:
    Jeff Wright <jeff.washcloth@gmail.com>
"""
import re
import math
import pkg_resources
from io import StringIO, BytesIO
from pathlib import Path
from docopt import docopt
from gtts import gTTS
from pydub import AudioSegment
from tqdm import tqdm


def parse_textfile(phrase_file_contents: str = "") -> list:
    """Clean up user-supplied phrase file to comform with expected format"""

    def clean(input: str = "") -> str:
        cleaner = r"[^A-Za-z0-9\s;\v]"
        clean = re.compile(cleaner, flags=re.MULTILINE | re.UNICODE)
        return re.sub(clean, "", input)

    def capture(cleaned: str = "") -> list:
        capturer = r"^\s*([\w\s]+?)\s*;\s*(\d+)\s*$"
        captured = re.compile(capturer, flags=re.MULTILINE | re.UNICODE)
        return re.findall(captured, cleaned)

    return capture(clean(phrase_file_contents))


class AudioProgramGenerator:
    def __init__(self, phrase_file: StringIO, sound_file: BytesIO = None, **kwargs):
        """Initialize class instance"""
        self.phrase_file = phrase_file.read()  # Fileobj to generate speech segments
        self.sound_file = sound_file  # Fileobj to mix w/ generated speech
        self.slow = kwargs.pop(
            "slow", False
        )  # gTTS will generate half-speed speech if this is True
        self.attenuation = kwargs.pop("attenuation", 10)  # Attenuation value, if mixing
        self.speech_file = None  # Generated speech/silence
        self.mix_file = None  # Mixed speeech/sound
        self.result = BytesIO(None)  # File-like object to store final result

    def _gen_speech(self):
        """Generate a combined speech file, made up of gTTS-generated speech
        snippets from each line in the phrase_file + corresponding silence."""

        combined = AudioSegment.empty()

        for phrase, duration in tqdm(parse_textfile(self.phrase_file)):

            # Skip blank phrases or gTTS will throw exception
            if not phrase.strip():
                continue

            tmpfile = BytesIO(None)
            speech = gTTS(phrase, slow=self.slow)
            speech.write_to_fp(tmpfile)
            tmpfile.seek(0)

            # Add the current speech snippet + corresponding silence
            # to the combined file, building up for each new line.
            snippet = AudioSegment.from_file(tmpfile, format="mp3")
            combined += snippet
            silence = AudioSegment.silent(duration=1000 * int(duration))
            combined += silence

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
        """Mixes two pydub AudioSegments, then fades the result in/out.
        Returns mixed AudioSegment."""
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
        """Generate gTTS speech snippets for each phrase; optionally mix with
        background sound-file; then save resultant mp3."""
        self._gen_speech()

        if self.sound_file:
            bkgnd = AudioSegment.from_file(self.sound_file, format="wav")
            self.mix_file = self._mix(self.speech_file, bkgnd, self.attenuation)
            self.mix_file.export(self.result, format="mp3")
        else:
            self.speech_file.export(self.result, format="mp3")

        return self.result


def main():
    try:
        this_version = pkg_resources.get_distribution("audio_program_generator").version
    except:
        this_version = "UNKNOWN"

    args = docopt(__doc__, version=f"Audio Program Generator (apg) {this_version}")

    print(args) if args["--debug"] else None

    phrase_file = Path(args["<phrase_file>"]) if args["<phrase_file>"] else None
    sound_file = Path(args["<sound_file>"]) if args["<sound_file>"] else None
    slow = bool(args["--slow"])
    attenuation = int(args["--attenuation"]) if args["--attenuation"] else 0

    kwargs = dict(slow=slow, attenuation=attenuation)

    pfile, sfile = None, None
    try:
        pfile = open(phrase_file)
        sfile = open(sound_file, "rb") if sound_file else None

        apg = AudioProgramGenerator(pfile, sfile, **kwargs)
        result = apg.invoke()

        with open(str(phrase_file.parent / phrase_file.stem) + ".mp3", "wb") as f:
            f.write(result.getbuffer())
        result.close()
    except Exception as exc:
        # TODO: improve!
        print(exc)
    finally:
        pfile.close()
        sfile.close() if sfile else None


if __name__ == "__main__":
    main()
