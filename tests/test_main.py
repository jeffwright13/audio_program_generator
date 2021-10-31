from pathlib import Path

import pytest
import sys


from audio_program_generator.apg import main as apg_main
from docopt import DocoptExit


def test_apg_main_without_arguments(capsys):

    with pytest.raises(DocoptExit):
        apg_main()


def test_apg_main_with_args(
    phrase_path: Path,
    sound_path: Path,
    output_path: Path,
    capsys,
):
    sys.argv = ["apg", str(phrase_path), str(sound_path)]

    apg_main()

    assert output_path.exists()
    assert output_path.is_file()
    assert len(output_path.read_bytes()) > 0
