"""fixtures for testing AudioProgramGenerator
"""

import io
import pytest
import os

from pathlib import Path

import audio_program_generator.apg as apg


@pytest.fixture(scope="session")
def phrase_path() -> Path:
    """pathlib.Path to a known good phrase file.

    Beginning lyrics of the song "Black Sunshine" by White Zombie.
    """
    return Path(__file__).absolute().parent / "resources/phrases.txt"


@pytest.fixture(scope="session")
def sound_path() -> Path:
    """Path to a known good WAV file.

    mustang4.wav
    Source: https://freesound.org/people/VacekH/sounds/205507/
    License: CC0 1.0
    """
    return Path(__file__).absolute().parent / "resources/mustang4.wav"


@pytest.fixture(scope="session")
def phrase_file(phrase_path) -> io.StringIO:
    """StringIO loaded with the contents of `phrase_path`."""
    return io.StringIO(phrase_path.read_text())


@pytest.fixture(scope="session")
def sound_file(sound_path) -> io.BytesIO:
    """BytesIO loaded with the contents of `sound_path`."""
    return io.BytesIO(sound_path.read_bytes())


@pytest.fixture(scope="session")
def output_path(phrase_path) -> Path:
    """pathlib.Path of the expected output file."""
    path = phrase_path.with_suffix(".mp3")
    yield path
    path.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def APG(phrase_file, sound_file) -> apg.AudioProgramGenerator:
    """An AudioProgramGenerator created with `phrase_file` and `sound_file`."""
    return apg.AudioProgramGenerator(phrase_file, sound_file)
