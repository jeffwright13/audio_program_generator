# apg (audio_program_generator)
Generates an audio program from a text file containing English sentences

# Prerequisites
* Some relatively recent version of Python (3.7+)
* FFMPEG with at least the ability to read mp3s and wavs, and write mp3s

# Description:
apg.py:
Generate audio program of spoken phrases, with optional background
sound file mixed in.

User populates a semicolon-separated text file with plain-text phrases,
each followed by an inter-phrase duration. Each line of the file is
comprised of:
  - one phrase to be spoken
  - a semicolon
  - a silence duration (specified in seconds)

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
only .wav files are supported as inputs.

# Usage:
    apg [options] <phrase_file>
    apg [options] mix <phrase_file> <sound_file>
    apg -V --version
    apg -h --help

# Options:
    -a --attenuation LEVEL  Set attenuation level of background file (non-
                            negative number, indicating dB attenuation).
    -d --debug              Print debug statements to console.
    -V --version            Show version.
    -h --help               Show this screen.

# Commands:
    mix                     Mix files

# Arguments:
    phrase_file             Name of semicolon-separated text file containing
                            phrases and silence durations. Do not include
                            commas in this file.
    sound_file              A file to be mixed into the generated program
                            file. Useful for background music/sounds. Must
                            be in .wav format.

# Example <phrase_file> format:
    Phrase One;2
    Phrase Two;5
    Phrase Three;0

# Author:
Jeff Wright <jeff.washcloth@gmail.com>

