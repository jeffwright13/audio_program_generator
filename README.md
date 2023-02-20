
[![Python package](https://github.com/jeffwright13/audio_program_generator/actions/workflows/python-package.yml/badge.svg)](https://github.com/jeffwright13/audio_program_generator/actions/workflows/python-package.yml)
[![CodeQL](https://github.com/jeffwright13/audio_program_generator/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/jeffwright13/audio_program_generator/actions/workflows/codeql-analysis.yml)

# apg (audio_program_generator)
Generates an audio program from text, with option to mix in background sound

Possible use cases:
- make your own yoga or qi gong routine
- play a list of daily affirmations
- meditate to a mantra with drone music in the background
- create an audio book
- read a kid a bedtime story without actually having to do the reading

# Basic Usage
#### (see 'Detailed Usage' below for more info)
```
Usage: apg [OPTIONS] PHRASE_PATH [SOUND_PATH]

Arguments:
  PHRASE_PATH   Absolute or relative path to phrase file.  [required]
  [SOUND_PATH]  Path to .wav file to mix with generated speech. [optional]

Options:
  -o, --output-path PATH          Path to store resulting audio file.
  -f, --format, --output-format [wav|mp3|ogg|aac|flac]
                                  File format for output file.  [default: wav]
  -a, --attenuation INTEGER       Set background file attenuation in dB.
                                  [default: 0]
  --fi, --fadein INTEGER          Set fade-in duration in milliseconds.
                                  [default: 3000]
  --fo, --fadeout INTEGER         Set fade-out duration in milliseconds.
                                  [default: 6000]
  -s, --slow                      Generate speech at half-speed.
  -r, --region [AU|CA|IE|IN|UK|US|ZA]
                                  Regional accent to apply to generated
                                  speech.  [default: US]
  -b, --book-mode                 Operates on plain-text file without
                                  phrase/pause formatting.
  -H, --hide, --hide-progress-bar
                                  Do not display progress bar during
                                  execution.
  -v, --version                   Show version and exit.
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  -h, --help                      Show this message and exit.
```

# Prerequisites
Either:
 * Python (3.7+)
 * [pip](https://pypi.org/project/pip/) (option 1)
 * [git](https://git-scm.com/) + [poetry](https://python-poetry.org/) (option 2)
 * Local installation of [ffmpeg](https://www.ffmpeg.org/) (to save results in formats other than .wav)

Or:
 * [docker](https://www.docker.com/)

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
    - `poetry install --no-dev`
    - `poetry shell`
- Once this is done, you will have an "apg" executable available in your terminal. You can type `apg` for basic help, or `apg --help` for full instructions.
- Exit the poetry virtual environment when finished:
    - `exit`

## With `docker`:
- Clone the repo and cd into the directory:
    - `git clone https://github.com/jeffwright13/audio_program_generator.git`
    - `cd audio_program_generator`
- Execute `make apg-build` (builds Docker image)
- Place your <phrase_file> and any <sound_file> in the `apgfiles` subdirectory; docker will be looking for them there
- Execute `make apg args=<args>` (runs container with specified arguments; if using multiple arguments, wrap them all in quotes)
- Results from `make apg` will be available locally in the `/apgfiles` folder, even after the container is stopped
- Examples:
    - `make apg args=--help`
    - `make apg args=-V`
    - `make apg args="apgfiles/program.txt apgfiles/river.wav -a 0 -t co.in"`
    - `make apg args="apgfiles/program.txt -slow -t co.in"`

## With `flask`:
- There is a [sister project](https://github.com/jeffwright13/apg_flask) that wraps the apg module in a bare-bones Flask app. This can be hosted locally, or in a cloud provider such as Heroku, Digital Ocean, or AWS. This method is considered experimental at the moment, and is not officially supported.

# Detailed Usage
*Assumes you are using the provided `apg` command line interface, installed with one of the methods above.  Refer to the source code if you are importing this code as a module/package.*

- Populate a semicolon-separated text file with plain-text phrases, each followed by an inter-phrase duration (see example below). Each line of the file is comprised of:
   - a phrase to be spoken (in English) *or* an asterisk to indicate silence
   - a semicolon
   - a silence duration (in seconds)
- Provide a sound file for background sound (optional)
- Execute the command: `apg [options] <phrase_file> [sound_file]`

The script will generate and save a single audio file. The base name of the file will be the same as the specified input file. The output file will be saved to the same folder that the input text file was taken from, unless specified otherwise (using the "-o" option). For example, if the script is given input file "phrases.txt", the output file will be "phrases.wav" or "phrases.mp3"  or whatever the output format is set to be (using the "-f" option, which defults to ".wav").

The optional `[sound_file]` parameter, when specified, is used to mix in background sounds/music. This parameter specifies the path/filename of the sound file to be mixed in with the speech generated from the phrase file. If the sound file is shorter in duration than the generated speech file, it will be looped. If it is longer, it will be truncated. The resulting background sound (looped or not) will be faded in and out to ensure a smooth transition (6 seconds at beginning and en). Currently, only .wav files are supported as inputs.

The CLI prints out a progress bar by default. The progress bar may be disabled with the `--no-progress-bar` option.

The `--attenuation` option allows fine-tuning the background sound level so it doesn't drown out the generated speech.

The `--slow` option generates each speech snippet is a slow-spoken style.

The `--tld` option allows the user to select one of several regional 'accents' (English only). For accents, select one from the following list: ["com.au", "co.uk", "com", "ca", "co.in", "ie", "co.za"]

Specifying option `--book-mode` creates a spoken-word program (with or without background soundfile). It does this by reading in a file that does not have inter-phrase durations inserted, as is normally the case.

# Example `<phrase_file>` file format
This example will generate a speech-file that has 3 speech snippets ("Phrase One", "Phrase Two", "Phrase Three").

    Phrase One;2
    Phrase Two;5
    Phrase Three;0
    
# Example `<phrase_file>` file format
This example will generate a speech-file that has 3 speech snippets ("Phrase One", "Phrase Two", "Phrase Three"), with a 3-second silence snippet appearing at the beginning.

    *; 3
    Phrase One; 2
    Phrase Two; 5
    Phrase Three; 0

# Example `--book-mode` file format
    Here we have sentence number one (which is a lovely sentence, and deserves its own paragraph).

    Here is a second paragraph, and this is sentence number one (again) in that paragraph. And this is sentence number two! Then shalt thou count to three - no more, no less. Three shall be the number thou shalt count, and the number of the counting shall be three. Four shalt thou not count, neither count thou two, excepting that thou then proceed to three. Five is right out. Once the number three, being the third number, be reached, then lobbest thou thy Holy Hand Grenade of Antioch towards thy foe, who, being naughty in my sight, shall snuff it.

# Testing
Tests are implemented in pytest. You don't really need to worry about that if all you want to do it run them, but chances are if you want to run them, you're probably some sort of a hacker or coder or programmer, and you want to know the deets. See the [source code](https://github.com/jeffwright13/audio_program_generator/tree/main/tests) for more info.

To execute the tests, do one of the following:
* Fire up your venv (see Installation & Execution section above), cd into the top level of the repo, and type `pytest`.

* Do basically the same thing with poetry:

    `poetry shell`

    `pytest`

* Use docker:

    `make apg-build-test`

    `make test`

# Author:
Jeff Wright <jeff.washcloth@gmail.com>

# Collaborators:
- Bob Belderbos
- Erik OShaughnessy
