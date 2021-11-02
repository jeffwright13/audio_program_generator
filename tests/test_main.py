import sys
import pytest
from pathlib import Path
from docopt import DocoptExit
from audio_program_generator.apg import main as apg_main


def test_apg_main_without_arguments(capsys):
    """Verify that apg called without args aserts DocOptExit."""
    # with pytest.raises(DocoptExit):
    #     apg_main()
    apg_main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


def test_apg_main_with_args(
    phrase_path: Path,
    sound_path: Path,
    output_path: Path,
):
    """Verify calling main() outputs a file."""
    sys.argv = ["apg", str(phrase_path), str(sound_path)]
    apg_main()

    assert output_path.exists()
    assert output_path.is_file()
    assert len(output_path.read_bytes()) > 0
