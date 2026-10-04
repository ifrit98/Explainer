from types import SimpleNamespace

from manim import LEFT, RIGHT, UP, Rectangle, VGroup

from explainer_kit.scene import ExplainerScene, label


def issues(*tops):
    return ExplainerScene.layout_issues(SimpleNamespace(mobjects=list(tops)))


def panel(w=4, h=1.5):
    r = Rectangle(width=w, height=h, stroke_width=0)
    r.set_fill("#000000", opacity=0.9)
    return r


def test_clean_layout_has_no_issues():
    assert issues(label("left").shift(LEFT * 3), label("right").shift(RIGHT * 3)) == []


def test_overlapping_text_is_flagged():
    assert any(i.startswith("overlap:") for i in issues(label("one two"), label("three four")))


def test_panel_from_another_group_covering_text_is_flagged():
    found = issues(label("The ___ sat on the mat."), VGroup(panel(), label("card")))
    assert any("covered: 'The ___ sat on the mat.'" in i for i in found)


def test_panel_with_its_own_text_is_fine():
    assert issues(VGroup(panel(), label("card text"))) == []


def test_intentional_overlay_is_skipped():
    overlay = VGroup(panel(16, 9), label("PAUSE AND PREDICT"))
    overlay.explainer_overlay = True
    assert issues(label("under the overlay"), overlay) == []


def test_off_frame_text_is_flagged():
    assert any(i.startswith("off-frame") for i in issues(label("far away").shift(UP * 5)))


def test_text_that_nearly_touches_is_crowded():
    top = label("n odd numbers")
    below = label("1 = 1").next_to(top, UP * -1, buff=0.02)
    assert any(i.startswith("crowded:") for i in issues(top, below))


def test_text_with_normal_spacing_is_not_crowded():
    top = label("n odd numbers")
    below = label("1 = 1").next_to(top, UP * -1, buff=0.25)
    assert issues(top, below) == []
