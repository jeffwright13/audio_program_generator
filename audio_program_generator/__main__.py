""" command-line interface

"""

import errno
import os

from pathlib import Path
from enum import Enum

import pydub
import typer

from .apg import AudioProgramGenerator

from .accent import Accent
from .spoken_program import SpokenProgram


cli = typer.Typer()


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
    accent: Accent = typer.Option(
        Accent.US.value,
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
        if sound_path and not sound_path.exists():
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), str(sound_path)
            )

        program = SpokenProgram.from_file(phrase_path, structured=not book_mode)
        audio = program.render(
            sound_path,
            accent,
            slow,
            attenuation,
            hide_progress_bar=hide_progress_bar,
        )

        audio.export(str(output_path))

        if not hide_progress_bar:
            typer.secho("Wrote output to: ", nl=False)
            typer.secho(str(output_path.absolute()), fg="green")
    except FileNotFoundError as error:
        typer.secho(f"File not found: {error.filename}", fg="red")
    except Exception as error:
        typer.secho(str(error), fg="red")
        raise typer.Exit()


if __name__ == "__main__":
    cli()
