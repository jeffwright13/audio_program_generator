"""Fixtures for testing AudioProgramGenerator
"""
import io
import pytest
import audio_program_generator.apg as apg
from pathlib import Path
from unittest.mock import MagicMock


@pytest.fixture(scope="session")
def phrase_path() -> Path:
    """pathlib.Path to a known good phrase file.

    Beginning lyrics of the song "Black Sunshin e" by White Zombie.
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
    path = Path(phrase_path.with_suffix(".mp3").name)
    yield path
    path.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def APG(phrase_file, sound_file) -> apg.AudioProgramGenerator:
    """An AudioProgramGenerator created with `phrase_file` and `sound_file`."""
    return apg.AudioProgramGenerator(phrase_file, sound_file)


#########################
# Mocks & Static Objects
#########################
@pytest.fixture(scope="session")
def static_phrase_file() -> io.StringIO:
    return io.StringIO("Static Phrase File: StringIO")


@pytest.fixture(scope="session")
def static_sound_file() -> io.BytesIO:
    return io.BytesIO(b"Static Sound File: BytesIO")


class MockObject:
    """
    A generic mock object that takes an arbitrary list of keyword=value
    pairs, and creates a MagicMock instance which has attributes with
    names/values for each kw/val pair presented.
    """

    def __init__(self, **kwargs) -> None:
        from unittest.mock import MagicMock

        self.mock = MagicMock()
        for key, val in kwargs.items():
            exec(f"self.mock.{key} = '{val}'")


def mock_anything(**kwargs) -> MagicMock:
    """ """
    mock_thing = MagicMock()
    for key, val in kwargs.items():
        exec(f"mock_thing.{key} = '''{val}'''")
    return mock_thing


@pytest.fixture(scope="session")
def mock_gTTS(**kwargs) -> MagicMock:
    """
    Mock AudioProgramGenerator instance.
    <phrase_file> and <sound_file> are hard-coded (static).
    User passes in arbitrary keyword args; MagicMock is returned with
    attributes named as kwargs elements.
    """
    mockApg = MagicMock()
    mockApg.phrase_file = static_phrase_file()
    mockApg.sound_file = static_sound_file()

    for key, val in kwargs.items():
        exec(f"mockApg.{key} = '''{val}'''")

    return mockApg


@pytest.fixture(scope="session")
def mock_APG(phrase_file: io.StringIO, sound_file: io.BytesIO, **kwargs) -> MagicMock:
    """
    Mock AudioProgramGenerator instance.
    <phrase_file> and <sound_file> are hard-coded (static).
    User passes in arbitrary keyword args; MagicMock is returned with
    attributes named as kwargs elements.
    """
    mockApg = MagicMock()
    mockApg.phrase_file = static_phrase_file()
    mockApg.sound_file = static_sound_file()

    for key, val in kwargs.items():
        exec(f"mockApg.{key} = '{val}'")

    return mockApg
