from explainer_kit.words import diff_words, sentence


def test_diff_words_keeps_shared_words():
    old = sentence("Make sure that the reservoir is full.")
    new = sentence("Fill the reservoir.")
    kept, removed, added = diff_words(old, new)
    assert [old[i].word for i, _ in kept] == ["the", "reservoir"]  # "reservoir" matches "reservoir." (punctuation ignored)
    assert [old[i].word for i in removed] == ["Make", "sure", "that", "is", "full."]
    assert [new[j].word for j in added] == ["Fill"]
