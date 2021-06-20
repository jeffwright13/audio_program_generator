
# apg (audio_program_generator)
Generates an audio program from text, with option to mix in background sound.

Possible use cases:
- make your own yoga or qi gong routine
- create an audio book
- read a kid a bedtime story without actually having to do the reading

# Prerequisites
* Python (3.7+) [*note to mac users: your system may be using Python 2.7 by default. To find out, issue the command `python --version`. If your system shows anything less than 3.7, make sure you create a virtual environment before installing this package (see Installation section below)*]
* Local installation of [ffmpeg](https://www.ffmpeg.org/)

# Installation & Invocation
The easiest way to get started is to use `pip` to install apg as a package.
1. *(optional, but recommended)* create a virtual environment to install the package into:
`python -m venv .venv`
`source ./.venv/bin/activate`
2. Install the package:
`$ pip install audio-program-generator`
Once this is done, you will have an "apg" executable available in your terminal. You can type `apg` for basic help, or `apg --help` for full instructions.

An alternative is to build and install the package from source (requires [git](https://git-scm.com/) and [poetry](https://python-poetry.org/)):
`git clone https://github.com/jeffwright13/audio_program_generator.git`
`cd audio_program_generator`
`poetry install`
`poetry shell`
`apg`
Once this is done, you will have an "apg" executable available in your terminal. You can type `apg` for basic help, or `apg --help` for full instructions.

Finally, there is a [sister project](https://github.com/jeffwright13/apg_flask) that wraps the apg module in a bare-bones Flask app. This can be hosted locally, or in a cloud provider such as Heroku, Digital Ocean, or AWS. This method is considered experimental at the moment, and is not officially supported.

# Usage
*Assumes you are using the provided `apg` command line interface.*
1. Populate a semicolon-separated text file with plain-text phrases, each followed by an inter-phrase duration. Each line of the file is comprised of:
   - one phrase to be spoken
   - a semicolon
   - a silence duration (specified in seconds)
2. Provide a sound file for background sound (optional).
3. Execute the command in your terminal: `apg <phrase_file> [sound_file]`.

The script will generate and save a single MP3 file. The base name of the MP3 file is the same as the specified input file. For example, if the script is given input file "phrases.txt", the output file will be "phrases.mp3". It will be saved to the same folder that the input text file was taken from.

The optional `[sound_file]` parameter, when specified, is used to mix in background sounds/music. This parameter specifies the path/filename of the sound file to be mixed in with the speech generated from the phrase file. If the sound file is shorter in duration than the generated speech file, it will be looped. If it is longer, it will be truncated. The resulting background sound (looped or not) will be faded in and out to ensure a smooth transition (6 seconds at beginning and en). Currently, only .wav files are supported as inputs.

The `--attenuation` option allows fine-tuning the background sound level so it doesn't drown out the generated speech.

The `--slow` option generates each speech snippet is a slow-spoken style.

The CLI prints out a progress bar as the phrase file is converted into speech snippets. No progress bar is shown for the secondary mix step. There may be a significant delay in going from the end of the first stage (snippet generation) to the end of the second stage (mixing), primarily because of reading in the .wav file, which may be large. For this reason, you may want to select a sound file for mixing that
is small (suggested <20MB). Otherwise, be prepared to wait.
# Options
There are several options available on the command line to customize your generated program file.
```
-a  --attenuation  dB attenuation applied to
                   background file when mixing
-s  --slow         Generate slow speech snippets
-h  --help         Print out help
-V  --version      Print out apg version
```

# Example <phrase_file> format:
    Phrase One;2
    Phrase Two;5
    Phrase Three;0

# Author:
Jeff Wright <jeff.washcloth@gmail.com>
