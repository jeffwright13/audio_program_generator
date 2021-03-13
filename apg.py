"""
Description:
    apg.py: Generate audio program of custom phrases

    User populates a semicolon-separated text file with plain-text phrases,
    and accompanying inter-phrase durations. Each line of the file
    constitutes one phrase to be spoken, followed by a silence duration in
    seconds.

    The script generates and saves a single MP3 file. The base name of the MP3
    file is the same as the specified input file. So, for example, if the
    script is given input file "phrases.txt", the output file will be
    "phrases.mp3".

    Optionally, the script can play out the entire program (consisting of each
    phrase and its corresponding silence interval), using the "play" option.
Usage:
    apg [options] <phrase_file> [output_file]
    apg [options] mix <phrase_file> <wav_file> [output_file]
    apg -V --version
    apg -h --help
Options:
    -p --play       Play program after generating.
    -v --verbose    Print to console each line from <phrase_file>.
    -d --debug      Print debug statements to console.
Arguments:
    phrase_file     Name of semi-colon-separated text file containing
                    phrases and silence durations. Do not include
                    commas in this file.
    wav_file        A .wav file to be mixed into the generated program
                    file. Useful for background music/sounds.
    [output_file]   Name of file to write to dick once generated.
                    If not specified, it will be the same name as
                    <the phrase_file>
Examples:

Example <phrase_file> format:
    Let's meditate...;2
    Relax your body;60
    Relax your mind;60
    BOO!;0
Author:
    Jeff Wright <jeff.washcloth@gmail.com>
"""
import os
import sys
from tempfile import NamedTemporaryFile
from csv import reader
from pathlib import Path
from docopt import docopt
from gtts import gTTS
from audioplayer import AudioPlayer
from pydub import AudioSegment

debug = False


def mixer(file1, file2, level1=0, level2=0):
    if debug:
        print("In mixer()...")
        print("file1: ", file1, "file2: ", file2)

    speech = AudioSegment.from_file(file1, format="mp3") + level1
    bkgrnd = AudioSegment.from_file(file2, format="wav") + level2

    return speech.overlay(bkgrnd, position=0)


def main():
    args = docopt(__doc__, version="Audio Program Generator (apg) v1.2.0")
    phrase_file = args["<phrase_file>"]
    save_file = Path(phrase_file).stem + ".mp3"
    play = args["--play"]
    verbose = args["--verbose"]
    mix = args["mix"]
    debug = args["--debug"]
    if debug:
        print(args)

    with open(phrase_file, "r") as read_obj:
        combined = AudioSegment.empty()
        csv_reader = reader(read_obj)
        for row in csv_reader:
            tempfile = NamedTemporaryFile().name + ".mp3"
            try:
                print(row) if verbose else None
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
        combined.export(save_file, format="mp3")

    if mix:
        mixed_file = mixer(save_file, args["<wav_file>"])
        if play:
            AudioPlayer(mixed_file).play(block=True)
    else:
        if play:
            AudioPlayer(save_file).play(block=True)


if __name__ == "__main__":
    main()
