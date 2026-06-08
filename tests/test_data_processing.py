from src.data_processing import clean_text


def test_clean_text_preserves_portuguese_characters():
    text = "A Educação é ótima: ação, saúde e cidadania!"

    assert clean_text(text) == "a educação é ótima ação saúde e cidadania"


def test_clean_text_handles_non_string_values():
    assert clean_text(None) == ""
