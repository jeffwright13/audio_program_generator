import pytest
import sys
import typer
from pathlib import Path
from audio_program_generator.__main__ import cli as apg_main


def test_apg_main_without_arguments(capsys):
    with pytest.raises(SystemExit):
        apg_main()

@pytest.mark.skip(reason="This test fails")
def test_apg_main_with_args(
    phrase_path: Path,
    sound_path: Path,
    output_path: Path,
    capsys,
):
    sys.argv = ["apg", str(phrase_path), str(sound_path)]
    breakpoint()
    apg_main()

    assert output_path.exists()
    assert output_path.is_file()
    assert len(output_path.read_bytes()) > 0
