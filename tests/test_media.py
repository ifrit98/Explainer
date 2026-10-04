from explainer_kit.render import ffmetadata_chapters, format_srt, format_vtt, parse_srt
from explainer_kit.scene import caption_chunks
from explainer_kit.voice import split_segments
from manim_voiceover.helper import remove_bookmarks


def test_segments_split_at_bookmarks_and_sentences_with_exact_offsets():
    text = "Rule one. Use simple words. <bookmark mark='m'/> Replenished becomes full, mostly. Done!"
    content = remove_bookmarks(text)
    segs = split_segments(text)
    assert [s for s, _ in segs] == ["Rule one.", "Use simple words.", "Replenished becomes full, mostly.", "Done!"]
    for seg, off in segs:
        assert content[off:off + len(seg)] == seg


def test_caption_chunks_keep_sentences_whole():
    chunks = caption_chunks("This is STE-80. It is a writing style for technical text. It uses most of the rules.")
    assert chunks == ["This is STE-80. It is a writing style for technical text.", "It uses most of the rules."]
    assert all(len(c) <= 70 for c in caption_chunks("word " * 40))


def test_srt_vtt_roundtrip():
    cues = [(0.0, 1.5, "One."), (1.6, 3.25, "Two.")]
    srt = format_srt(cues)
    assert parse_srt(srt) == cues
    vtt = format_vtt(cues)
    assert vtt.startswith("WEBVTT") and "00:00:01.600 --> 00:00:03.250" in vtt
    assert parse_srt(vtt.split("\n\n", 1)[1]) == cues


def test_chapters_escape_and_cover_duration():
    meta = ffmetadata_chapters([(0.0, "Start"), (12.5, "Predict: a=b; #1")], 30.0)
    assert "START=12500" in meta and meta.rstrip().endswith(r"title=Predict: a\=b\; \#1")
    assert "END=30000" in meta
