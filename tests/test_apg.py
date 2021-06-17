from pathlib import Path
from tempfile import TemporaryFile
import audio_program_generator.apg as apg


def test_module(capsys):
    with capsys.disabled():
        print("\napg:", dir(apg))
        assert "main" in dir(apg)


def test_class_methods(capsys):
    with capsys.disabled():
        fh = TemporaryFile()
        A = apg.AudioProgramGenerator(fh)
        print("\nA:", dir(A))
        assert "_gen_speech" in dir(A)
        assert "_mix" in dir(A)
