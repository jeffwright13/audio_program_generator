import pytest
import sys
from pathlib import Path
from audio_program_generator.__main__ import cli as apg_main


def test_apg_main_without_arguments():
    with pytest.raises(SystemExit):
        apg_main()


def test_apg_main_help(capsys):
    sys.argv = ["apg", "-h"]
    try:
        apg_main()
    except SystemExit:
        std_out = capsys.readouterr().out
        assert "Usage" in std_out
        assert "Arguments" in std_out
        assert "Options" in std_out


def test_apg_main_version(capsys, APG):
    sys.argv = ["apg", "-v"]
    try:
        apg_main()
    except SystemExit:
        std_out = capsys.readouterr().out
        assert "version" in std_out
        assert APG.__version__ in std_out


def test_apg_main_with_args_no_options(
    clean, phrase_path: Path, sound_path: Path, output_path: Path
):
    sys.argv = ["apg", str(phrase_path), str(sound_path)]
    try:
        apg_main()
    except SystemExit:
        assert output_path.exists()
        assert output_path.is_file()
        assert output_path.suffix == ".wav"
        assert len(output_path.read_bytes()) > 0


@pytest.mark.parametrize(
    "format, expected_filetype",
    [
        ("wav", ".wav"),
        ("mp3", ".mp3"),
        ("ogg", ".ogg"),
        ("acc", ".aac"),
        ("flac", ".flac"),
    ],
)
def test_apg_main_specify_output_filetypes(
    clean,
    phrase_path: Path,
    sound_path: Path,
    output_paths: dict,
    format,
    expected_filetype,
):
    sys.argv = ["apg", str(phrase_path), str(sound_path), "-f", format]
    try:
        apg_main()
    except SystemExit:
        print("f")
        for output_path in output_paths.values():
            if output_path.suffix.endswith(format):
                assert output_path.exists()
                assert output_path.is_file()
                assert output_path.suffix == expected_filetype
                assert len(output_path.read_bytes()) > 0


@pytest.mark.parametrize(
    "input_format",
    [
        (".wav"),
        (".mp3"),
        (".ogg"),
        (".mp4"),
        (".flac"),
    ],
)
def test_apg_main_different_input_filetypes(
    clean,
    phrase_path: Path,
    sound_path: Path,
    output_path,
    input_format
):
    sys.argv = ["apg", str(phrase_path), str(sound_path)]
    expected_filetype = ".wav"
    try:
        apg_main()
    except SystemExit:
        print("f")
        assert output_path.exists()
        assert output_path.is_file()
        assert output_path.suffix == expected_filetype
        assert len(output_path.read_bytes()) > 0
