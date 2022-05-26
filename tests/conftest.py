"""fixtures for testing AudioProgramGenerator
"""
import io
import re
import pytest
from pathlib import Path

import audio_program_generator.apg as apg


@pytest.fixture(scope="session")
def clean() -> None:
    """Clean out old test results"""
    resource_location = Path(__file__).absolute().parent
    for fileext in ("wav", "mp3", "ogg", "aac", "flac"):
        file = resource_location / f"resources/phrases.{fileext}"
        file.unlink(missing_ok=True)
    print("f")


@pytest.fixture(scope="session")
def phrase_path() -> Path:
    """pathlib.Path to a known good phrase file.

    Beginning lyrics of the song "Black Sunshine" by White Zombie.
    """
    return Path(__file__).absolute().parent / "resources/phrases.txt"


@pytest.fixture(scope="session")
def sound_path(format=".wav") -> Path:
    """Path to a known good input file.

    mustang4.wav
    Source: https://freesound.org/people/VacekH/sounds/205507/
    License: CC0 1.0
    """
    return Path(__file__).absolute().parent / f"resources/mustang4{format}"


@pytest.fixture(scope="session")
def phrase_file(phrase_path) -> io.StringIO:
    """StringIO loaded with the contents of 'phrase_path'."""
    return io.StringIO(phrase_path.read_text())


@pytest.fixture(scope="session")
def sound_file(sound_path) -> io.BytesIO:
    """BytesIO loaded with the contents of 'sound_path'."""
    return io.BytesIO(sound_path.read_bytes())


@pytest.fixture(scope="session")
def output_path(phrase_path, request) -> Path:
    """Produces pathlib.Path of the expected output file (default: .wav)."""
    path = Path(phrase_path.with_suffix(".wav"))
    yield path
    path.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def output_paths(phrase_path, request) -> Path:
    """Produces dictionary of pathlib.Path for each expected output files."""
    pattern = re.compile(r"(\..*)]")
    paths = {}
    for item in request.session.items:
        name = pattern.search(item.name)
        try:
            filetype = name.groups()[-1]
        except AttributeError:
            continue
        path = Path(phrase_path.with_suffix(filetype))
        paths[filetype[1:]] = path
    yield paths
    for path in paths.values():
        path.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def APG(phrase_file, sound_file) -> apg.AudioProgramGenerator:
    """An AudioProgramGenerator created with 'phrase_file' and 'sound_file'."""
    return apg.AudioProgramGenerator(phrase_file, sound_file)
