import pytest

from wordstats import avg_sentence_length, reading_time_minutes, sentences, tokenize, top_words, word_freq


def test_tokenize_basic_and_case():
    assert tokenize("Hello, World! 42") == ["hello", "world", "42"]


def test_tokenize_apostrophes():
    assert tokenize("don't 'quoted' ''") == ["don't", "quoted"]


def test_tokenize_stopwords():
    assert tokenize("The cat and the hat", keep_stopwords=False) == ["cat", "hat"]
    assert tokenize("The cat", keep_stopwords=True) == ["the", "cat"]
    assert tokenize("it is in to of or an a and") == ["it", "is", "in", "to", "of", "or", "an", "a", "and"]
    assert tokenize("it is in to of or an a and the", keep_stopwords=False) == []


def test_word_freq():
    assert word_freq("a b a") == {"a": 2, "b": 1}
    assert word_freq("a b a", keep_stopwords=False) == {"b": 1}
    assert word_freq("") == {}


def test_top_words_order_and_ties():
    assert top_words("zeta alpha alpha beta beta zeta gamma", n=3) == [("alpha", 2), ("beta", 2), ("zeta", 2)]
    assert top_words("x y y z z z") == [("z", 3), ("y", 2), ("x", 1)]


def test_top_words_n_and_default_stopwords():
    assert top_words("a b c d", n=0) == []
    assert top_words("b c d", n=2) == [("b", 1), ("c", 1)]
    assert top_words("the the cat") == [("cat", 1)]
    assert top_words("the the cat", keep_stopwords=True) == [("the", 2), ("cat", 1)]
    with pytest.raises(ValueError):
        top_words("a", n=-1)


def test_sentences():
    assert sentences("One. Two! Three?  Four") == ["One.", "Two!", "Three?", "Four"]
    assert sentences("   ") == []
    assert sentences("Mr.Smith went. Home") == ["Mr.Smith went.", "Home"]
    assert sentences("What? Yes") == ["What?", "Yes"]


def test_avg_sentence_length():
    assert avg_sentence_length("") == 0.0
    assert avg_sentence_length("One two. Three four five six.") == 3.0
    assert avg_sentence_length("a b c") == 3.0
    assert avg_sentence_length("a b. c d e.") == 2.5


def test_reading_time():
    assert reading_time_minutes("") == 0
    assert reading_time_minutes("word") == 1
    assert reading_time_minutes("w " * 200) == 1
    assert reading_time_minutes("w " * 201) == 2
    assert reading_time_minutes("w " * 100, wpm=50) == 2
    assert reading_time_minutes("w " * 100, wpm=1) == 100
    with pytest.raises(ValueError):
        reading_time_minutes("x", wpm=0)
    with pytest.raises(ValueError):
        reading_time_minutes("x", wpm=-5)
