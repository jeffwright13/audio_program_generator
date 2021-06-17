from pathlib import Path
from tempfile import TemporaryFile
import audio_program_generator.apg as apg


def test_module(capsys):
    with capsys.disabled():
        assert "main" in dir(apg)


def test_all_class_methods_exist(capsys):
    with capsys.disabled():
        fh = TemporaryFile()
        A = apg.AudioProgramGenerator(fh)
        assert "_gen_speech" in dir(A)
        assert "_mix" in dir(A)
        assert "invoke" in dir(A)


def test_class_instantiation():
