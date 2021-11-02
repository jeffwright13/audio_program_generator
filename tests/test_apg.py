import io
import pytest
from tempfile import TemporaryFile
import audio_program_generator.apg as apg


@pytest.mark.parametrize(
    "kwargs",
    [
        ({}),
        # add more kwargs here that would work
    ],
)
def test_create_audio_program_generator_success(phrase_file, sound_file, kwargs):
    instance = apg.AudioProgramGenerator(phrase_file, sound_file, **kwargs)
    assert isinstance(instance, apg.AudioProgramGenerator)


@pytest.mark.parametrize(
    "phrase_file,sound_file,kwargs,expected_error",
    [
        (None, None, {}, AttributeError),
        # add more busted argument combinations here
    ],
)
def test_create_audio_program_generator_failure(
    phrase_file, sound_file, kwargs, expected_error
):
    with pytest.raises(expected_error):
        apg.AudioProgramGenerator(phrase_file, sound_file, **kwargs)


def test_audio_program_generator_invoke(APG):
    buf = APG.invoke()
    assert isinstance(buf, io.BytesIO)


# Test existence of module functions
def test_module_functions_exist():
    assert "main" in dir(apg)
    assert "parse_textfile" in dir(apg)


# Test that all expected class methods are there
def test_all_class_methods_exist(APG):
    assert "_gen_speech" in dir(APG)
    assert "_mix" in dir(APG)
    assert "invoke" in dir(APG)


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
