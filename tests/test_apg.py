import pytest
from tempfile import TemporaryFile
import audio_program_generator.apg as apg

# Test existence of module functions
def test_module_functions_exist():
    assert "main" in dir(apg)
    assert "parse_textfile" in dir(apg)


# Test that all expected class methods are there
def test_all_class_methods_exist(capsys):
    with capsys.disabled():
        fh = TemporaryFile()
        A = apg.AudioProgramGenerator(fh)
        assert "_gen_speech" in dir(A)
        assert "_mix" in dir(A)
        assert "invoke" in dir(A)


# Test the regex parser
@pytest.mark.parametrize(
    "instring, expected",
    [
        ("", []),
        (" - ", []),
        (";", []),
        ("hi ;", []),
        (";10", []),
        (" ^ & Hello ;  99 (", [("Hello", "99")]),
        ("\n\nbig *bad _ bear; 10<>", [("big bad  bear", "10")]),
    ],
)
def test_parse_textfile(instring, expected):
    assert apg.parse_textfile(instring) == expected
