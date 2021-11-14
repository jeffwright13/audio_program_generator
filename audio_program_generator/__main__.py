""" command-line interface

"""

from pathlib import Path
from enum import Enum

import typer

from .apg import AudioProgramGenerator

cli = typer.Typer()


class RegionalAccent(str, Enum):
    AU: str = "AU"
    CA: str = "CA"
    IE: str = "IE"
    IN: str = "IN"
    UK: str = "UK"
    US: str = "US"
    ZA: str = "ZA"

    @classmethod
    def get_tld(cls, region: str) -> str:
        return {
            "au": "com.au",
            "ca": "ca",
            "ie": "ie",
            "in": "co.in",
            "uk": "co.uk",
            "us": "com",
            "za": "co.za",
        }.get(region.lower())


@cli.command()
def generate_subcommand(
    phrase_path: Path,
    output_path: Path = typer.Option(
        None,
        "--output-path",
        "-o",
        show_default=True,
        help="Path to store resulting MP3 audio file.",
    ),
    sound_path: Path = typer.Option(
        None,
        "--sound-path",
        "-s",
        show_default=True,
        help="Path for an optional WAV to mix with the generated speech.",
    ),
    attenuation: int = typer.Option(
        0,
        "--attenuation",
        "-a",
        show_default=True,
        help="Set background file attenuation in dB",
    ),
    slow: bool = typer.Option(
        False,
        "--slow",
        is_flag=True,
        show_default=True,
        help="Generate speech at half-speed.",
    ),
    regional_accent: RegionalAccent = typer.Option(
        RegionalAccent.US.value,
        "--region",
        "-r",
        show_default=True,
        help="Regional accent to apply to generated speech.",
    ),
    book_mode: bool = typer.Option(
        False,
        "--book-mode",
        "-B",
        is_flag=True,
        show_default=True,
        help="Operates on plain text without phrase pause formatting.",
    ),
    hide_progress_bar: bool = typer.Option(
        False,
        "--hide-progress-bar",
        is_flag=True,
        show_default=True,
        help="Do not display progress bar during execution.",
    ),
) -> None:
    """Generate audio program of spoken phrases, with optional background
    sound file mixed in.

    The user supplies a semicolon-separated text file with plain-text
    phrases, each followed by an inter-phrase duration. Each line of
    the file is comprised of:

    - one phrase to be spoken
    - a semicolon
    - a silence duration (specified in seconds)

    The script generates and saves a single MP3 file. If a path for
    the output file is not given, the output file will have the same
    base name as the input file with the suffix ".mp3" in the current
    working directory.
    """

    if not output_path:
        output_path = Path.cwd() / phrase_path.with_suffix(".mp3").name

    try:
        sound_file = sound_path.open("rb")
    except AttributeError:
        sound_file = None

    with phrase_path.open("r") as phrase_file:
        apGen = AudioProgramGenerator(
            phrase_file,
            sound_file,
            slow=slow,
            attenuation=attenuation,
            tld=RegionalAccent.get_tld(regional_accent),
            hide_progress_bar=hide_progress_bar,
            book_mode=book_mode,
        )
        audio_data = apGen.invoke()

    with output_path.open("wb") as output_file:
        output_file.write(audio_data.read())
        
if __name__ == "__main__":
    cli()
