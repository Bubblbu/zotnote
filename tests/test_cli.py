import pytest

from zotnote.cli import remove


@pytest.fixture
def config():
    
def test_remove_note_bad_citekey():
    citekey = "ahahaha"

    with pytest.raises(SystemExit):
        remove(citekey)
