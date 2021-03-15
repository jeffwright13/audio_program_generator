"""
Description:
    apg.py:
    Generate audio program of spoken phrases, with optional background
    sound file mixed in.

    User populates a comma-separated text file with plain-text phrases,
    each followed by an inter-phrase duration. Each line of the file is
    comprised of:
      - one phrase to be spoken
      - a comma
      - a silence duration (specified in seconds)
    Obviously, do not include superfluous commas in this file. An exception
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
    -p --play       Play program after generating.
    -d --debug      Print debug statements to console.

Arguments:
    phrase_file     Name of comma-separated text file containing
                    phrases and silence durations. Do not include
                    commas in this file.
    sound_file      A file to be mixed into the generated program
                    file. Useful for background music/sounds.

Example <phrase_file> format:
    Phrase One;2
    Phrase Two;5
    Phrase Three;0

Author:
    Jeff Wright <jeff.washcloth@gmail.com>
"""
import os
import sys
import math
from tempfile import NamedTemporaryFile
from csv import reader
from pathlib import Path
from docopt import docopt
from gtts import gTTS
from audioplayer import AudioPlayer
from pydub import AudioSegment


def mix(segment1, segment2, level1=0, level2=-12, fadein=3000, fadeout=6000):
    """
    Mixes two pydub AudioSegments (with individual levels), then fades
    the result in/out.
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

    return (segment1 + level1).overlay(
        (segment2_normalized + level2).fade_in(fadein).fade_out(fadeout)
    )


def gen_speech(phrase_file):
    """
    Generates speech from a comma-separated file.
    Returns Audiosegment.
    """
    with open(phrase_file, "r") as read_obj:
        combined = AudioSegment.empty()
        csv_reader = reader(read_obj)
        for row in csv_reader:
            tempfile = NamedTemporaryFile().name + ".mp3"
            try:
                phrase, interval = row[0].split(";")
            except Exception as e:
                print("Error parsing input file as CSV:")
                print(row)
                print(e.args)
                sys.exit()
            speech = gTTS(phrase)
            speech.save(tempfile)
            speech = AudioSegment.from_file(tempfile, format="mp3")
            combined += speech
            os.remove(tempfile)
            silence = AudioSegment.silent(duration=1000 * int(interval))
            combined += silence
    return combined


def main():
    args = docopt(__doc__, version="Audio Program Generator (apg) v1.2.2")
    save_file = Path(args["<phrase_file>"]).stem + ".mp3"
    print(args) if args["--debug"] else None
    speech = gen_speech(args["<phrase_file>"])

    if args["mix"]:
        bkgnd = AudioSegment.from_file(args["<sound_file>"], format="wav")
        mixed = mix(speech, bkgnd)
        mixed.export(save_file, format="mp3")
    else:
        speech.export(save_file, format="mp3")

    if args["--play"]:
        AudioPlayer(save_file).play(block=True)


if __name__ == "__main__":
    main()
