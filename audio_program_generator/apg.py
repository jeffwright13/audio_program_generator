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

    The script generates and saves a single MP3 file. The base name of the MP3
    file is the same as the specified input file. So, for example, if the
    script is given input file "phrases.txt", the output file will be
    "phrases.mp3".

    The "mix" command is used to mix in background sounds. This command takes
    an extra parameter, the path/filename of a sound file to be mixed in with
    the speech file generated from the phrase file. If the sound file is shorter
    in duration than the generated speech file, it will be looped. If it is
    longer, it will be truncated. The resulting background sound (looped or
    not) will be faded in and out to ensure a smooth transition. Currently,
    only .wav files are supported.


Usage:
    apg [options] <phrase_file>
    apg [options] mix <phrase_file> <sound_file>
    apg -V --version
    apg -h --help

Options:
    -a --attenuation LEV    Set attenuation level of background file (non-
                            negative number indicating dB attenuation)
                            ([default: 0]).
    -d --debug              Print debug statements to console.
    -V --version            Show version.
    -h --help               Show this screen.

Commands:
    mix                     Mix files

Arguments:
    phrase_file             Name of semicolon-separated text file containing
                            phrases and silence durations.
    sound_file              A file to be mixed into the generated program
                            file. Useful for background music/sounds. Must
                            be in .wav format.

Example <phrase_file> format:
    Phrase One;2
    Phrase Two;5
    Phrase Three;0

Author:
    Jeff Wright <jeff.washcloth@gmail.com>
"""
import sys
import math
from pathlib import Path
from docopt import docopt
from gtts import gTTS
from pydub import AudioSegment
from tqdm import tqdm


def num_lines_in_file(filename: Path) -> int:
    """
    Takes text filename ; returns the number of lines in a file
    """
    numlines = 1
    with open(filename, "r"):
        numlines += 1
    return numlines


class Apg:
    def __init__(
        self,
        phrase_file: Path,
        to_mix: bool = False,
        sound_file: Path = None,
        attenuation: int = 0,
    ):
        """Initialize class instance"""
        self.phrase_file = phrase_file  # Input file to generate speech segments
        self.speech_file = None  # Generated speech/silence
        self.mix_file = None  # Mixed speeech/sound
        self.to_mix = to_mix  # Specifies if mixing will take place
        self.sound_file = sound_file  # File with which to mix generated speech
        self.attenuation = attenuation  # Attenuation value, if mixing
        self.save_file = str(phrase_file.parent / phrase_file.stem) + ".mp3"

    def gen_speech(self):
        """Generate a combined speech file, made up of gTTS-generated speech
        snippets from each line in the phrase_file + corresponding silence."""

        with open(self.phrase_file, "r") as f:
            #pbar = ProgressBar(maxval=num_lines_in_file(self.phrase_file)).start()
            combined = AudioSegment.empty()
            lines = f.readlines()

            for line in tqdm(lines):
                try:
                    phrase, interval = line.split(";")
                except Exception as e:
                    print("Error parsing input file as CSV:")
                    print(line)
                    print(e.args)
                    sys.exit()

                if len(phrase) == 0:
                    print("Error: gTTS requires non-empty text to process.")
                    print("File: ", self.phrase_file)
                    print("Line: ", line)
                    sys.exit()

                # Each speech snippet generated from gTTS is saved locally
                # in a cache (if that exact phrase had not already been used).
                # Otherwise, it is simply re-used.
                Path.mkdir(Path.cwd() / ".cache") if not Path(
                    Path.cwd() / ".cache"
                ).exists() else None
                file = Path.cwd() / ".cache" / (phrase + ".mp3")
                if not Path(file).exists():
                    speech = gTTS(phrase)
                    speech.save(file)

                # Add the current speech snippet + corresponding silence
                # to the combined file, building up for each new line.
                speech = AudioSegment.from_file(file, format="mp3")
                combined += speech
                silence = AudioSegment.silent(duration=1000 * int(interval))
                combined += silence

        self.speech_file = combined

    def mix(self, segment1, segment2, seg2_atten=0, fadein=3000, fadeout=6000):
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

    def invoke(self):
        self.gen_speech()
        if self.to_mix == True:
            bkgnd = AudioSegment.from_file(self.sound_file, format="wav")
            self.mix_file = self.mix(self.speech_file, bkgnd, self.attenuation)
            self.mix_file.export(self.save_file, format="mp3")
        else:
            self.speech_file.export(self.save_file, format="mp3")


def main():
    args = docopt(__doc__, version="Audio Program Generator (apg) v1.5.0")

    phrase_file = Path(args["<phrase_file>"]) if args["<phrase_file>"] else None
    sound_file = Path(args["<sound_file>"]) if args["<sound_file>"] else None
    to_mix = True if args["mix"] else False
    attenuation = args["--attenuation"] if args["--attenuation"] else 0
    print(args) if args["--debug"] else None

    if not phrase_file:
        sys.exit("Phrase file " + phrase_file + " does not exist. Quitting.")
    if to_mix and not sound_file:
        sys.exit("Sound file " + sound_file + " does not exist. Quitting.")

    A = Apg(
        phrase_file,
        to_mix,
        sound_file,
        attenuation,
    )

    A.invoke()


if __name__ == "__main__":
    main()

