"""
command-line interface for audio program generator

"""
import typer
from io import StringIO
from typing import Optional
from pathlib import Path
from enum import Enum
from audio_program_generator.apg import AudioProgramGenerator

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

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


class OutputFormat(str, Enum):
    wav: str = "wav"
    mp3: str = "mp3"
    ogg: str = "ogg"
    aac: str = "aac"
    flac: str = "flac"


def version_callback(value: bool):
    if value:
        __version__ = AudioProgramGenerator(StringIO(None)).__version__
        typer.echo(f"Audio Program Generator (apg) version {__version__}")
        raise typer.Exit()


@cli.command(context_settings=CONTEXT_SETTINGS)
def generate_subcommand(
    phrase_path: Path = typer.Argument(
        ..., help="Absolute or relative path to phrase file."
    ),
    sound_path: Path = typer.Argument(
        None,
        help="Path to .wav file to mix with generated speech. [optional]",
    ),
    output_path: Path = typer.Option(
        None,
        "-o",
        "--output-path",
        show_default=True,
        help="Path to store resulting audio file.",
    ),
    output_format: OutputFormat = typer.Option(
        OutputFormat.wav.value,
        "-f",
        "--format",
        "--output-format",
        show_default=True,
        help="File format for output file.",
    ),
    attenuation: int = typer.Option(
        0,
        "-a",
        "--attenuation",
        show_default=True,
        help="Set background file attenuation in dB.",
    ),
    slow: bool = typer.Option(
        False,
        "-s",
        "--slow",
        is_flag=True,
        show_default=True,
        help="Generate speech at half-speed.",
    ),
    regional_accent: RegionalAccent = typer.Option(
        RegionalAccent.US.value,
        "-r",
        "--region",
        show_default=True,
        help="Regional accent to apply to generated speech.",
    ),
    book_mode: bool = typer.Option(
        False,
        "-b",
        "--book-mode",
        is_flag=True,
        show_default=True,
        help="Operates on plain-text file without phrase/pause formatting.",
    ),
    hide_progress_bar: bool = typer.Option(
        False,
        "-H",
        "--hide-progress-bar",
        is_flag=True,
        show_default=True,
        help="Do not display progress bar during execution.",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "-v",
        "--version",
        help="Show version and exit.",
        callback=version_callback,
    ),
) -> None:

    try:
        sound_file = sound_path.open("rb")
    except (AttributeError, FileNotFoundError):
        sound_file = None

    with phrase_path.open("r") as phrase_file:
        Apg = AudioProgramGenerator(
            phrase_file,
            sound_file,
            slow=slow,
            attenuation=attenuation,
            tld=RegionalAccent.get_tld(regional_accent),
            hide_progress_bar=hide_progress_bar,
            book_mode=book_mode,
            output_format=output_format.value,
        )
        audio_data = Apg.invoke()

    if not output_path:
        output_path = phrase_path.with_suffix(f".{output_format.value}")
    with output_path.open("wb") as output_file:
        output_file.write(audio_data.read())


if __name__ == "__main__":
    cli()
