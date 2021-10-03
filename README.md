
# apg (audio_program_generator)
Generates an audio program from text, with option to mix in background sound

Possible use cases:
- make your own yoga or qi gong routine
- create an audio book
- read a kid a bedtime story without actually having to do the reading

# Prerequisites
* Python (3.7+) [*note to mac users: your system may be using Python 2.7 by default. To find out, issue the command `python --version`. If your system shows anything less than 3.7, make sure you create a virtual environment before installing this package (see Installation section below)*]
* [pip](https://pypi.org/project/pip/) (option 1)
* [git](https://git-scm.com/) + [poetry](https://python-poetry.org/) (option 2)
* Local installation of [ffmpeg](https://www.ffmpeg.org/)

# Installation & Execution
## With `pip`:
- Create a virtual environment and activate it:
    - `python -m venv venv`
    - `source ./venv/bin/activate`
 - Install the package:
    - `pip install audio-program-generator`
- Once this is done, you will have an "apg" executable available in your terminal. You can type `apg` for basic help, or `apg --help` for full instructions.
- Deactivate your virtual environment when finished:
    - `deactivate`

## With `poetry`:
- Clone the repo and cd into the directory:
    - `git clone https://github.com/jeffwright13/audio_program_generator.git`
    - `cd audio_program_generator`
- Install the dependencies using poetry, and activate the virtual environment:
    - `poetry install`
    - `poetry shell`
- Once this is done, you will have an "apg" executable available in your terminal. You can type `apg` for basic help, or `apg --help` for full instructions.
- Exit the poetry virtual environment when finished:
    - `exit`

## With `flask`:
- There is a [sister project](https://github.com/jeffwright13/apg_flask) that wraps the apg module in a bare-bones Flask app. This can be hosted locally, or in a cloud provider such as Heroku, Digital Ocean, or AWS. This method is considered experimental at the moment, and is not officially supported.

# Usage
*Assumes you are using the provided `apg` command line interface, installed with one of the methods above*
- Populate a semicolon-separated text file with plain-text phrases, each followed by an inter-phrase duration (see example below). Each line of the file is comprised of:
   - a phrase to be spoken (in English)
   - a semicolon
   - a silence duration (in seconds)
- Provide a sound file for background sound (optional)
- Execute the command in your terminal: `apg [options] <phrase_file> [sound_file]`

The script will generate and save a single MP3 file. The base name of the MP3 file is the same as the specified input file. For example, if the script is given input file "phrases.txt", the output file will be "phrases.mp3". It will be saved to the same folder that the input text file was taken from.

The optional `[sound_file]` parameter, when specified, is used to mix in background sounds/music. This parameter specifies the path/filename of the sound file to be mixed in with the speech generated from the phrase file. If the sound file is shorter in duration than the generated speech file, it will be looped. If it is longer, it will be truncated. The resulting background sound (looped or not) will be faded in and out to ensure a smooth transition (6 seconds at beginning and en). Currently, only .wav files are supported as inputs.

The `--attenuation` option allows fine-tuning the background sound level so it doesn't drown out the generated speech.

The `--slow` option generates each speech snippet is a slow-spoken style.

The `--tld` option allows the user to select one of several regional 'accents' (English only). For accents, select one from the following list: ["com.au", "co.uk", "com", "ca", "co.in", "ie", "co.za"]

The CLI prints out a progress bar as the phrase file is converted into speech snippets. No progress bar is shown for the secondary mix step. There may be a significant delay in going from the end of the first stage (snippet generation) to the end of the second stage (mixing), primarily because of reading in the .wav file, which may be large. For this reason, you may want to select a sound file for mixing that is small (suggested <20MB). Otherwise, be prepared to wait. The progress bar may be disabled with the `--no-progress-bar` option.

# Example <phrase_file> format:
    Phrase One;2
    Phrase Two;5
    Phrase Three;0

# Author:
Jeff Wright <jeff.washcloth@gmail.com>
