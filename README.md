# audio_program_generator
Generates an audio program from a text file containing English sentences

#Description:
    apg.py: Generate audio program of custom phrases

    User populates a text file with plain-text phrases, and accompanying
    inter-phrase durations. Each line of the file constitutes one phrase to be
    spoken, followed by a semicolon, followed by a silence duration in seconds.

    The script generates and saves a single MP3 file ("program.mp3").

    Optionally, the script can play out the entire program (consisting of each
    phrase and its corresponding silence interval), using the "play" option.

#Usage:
    apg <phrase_file> [-p | --play]
    apg -h | --help
    apg -V | --version

#Arguments:
    phrase_file     Name of semi-colon-separated text file
                    containing phrases and silence durations
#Options:
    -p --play       Play the program after generating it
    -h --help       Show this message and exit
    -V --version    Show version info and exit

#Example phrases file format:
    Let's do some qi gong!;2
    Relax your body;60
    Lifting the sky;60
    Shaking the tree;60
    Fireworks;60
    Flowing breeze swaying willow;60
    Flowing stillness;30
    Closing sequence;60
    Good job!;0
