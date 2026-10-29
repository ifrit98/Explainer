"""Positive controls for the rederivation test (PRD-002a), without calling the claude CLI."""

import json

from explainer_kit import artifact_eval as ae, controls


def test_controls_follow_the_eligibility_rule():
    c = controls.load_controls()
    dev = {s["id"]: s for s in ae.load("dev")[1] if "rederive" in s}
    assert sorted(c["cuts"]) == ["bloom-filter", "float-sum", "greenhouse", "heat-pump", "key-exchange", "two-tides"]
    assert set(c["cuts"]) | set(c["left_out"]) == set(dev)
    assert not set(c["cuts"]) & set(c["left_out"])
    for sid, spec in c["cuts"].items():
        kinds = [s["kind"] for s in dev[sid]["rederive"]["steps"]]
        assert spec["cut"] not in spec["clean"]
        for i in [spec["cut"], *spec["clean"]]:
            assert kinds[i - 1] == "block"
            for k in (1, 2, 3):   # reliably credited when intact (rule 4)
                g = json.loads((c["baseline"] / "rederive" / f"pass-{k}" / "grades" / f"{sid}.json").read_text())
                assert g["grades"]["principles"]["marks"][i - 1] == "supported", (sid, i, k)
    assert sum(len(s["clean"]) for s in c["cuts"].values()) == 4


def test_the_bar_is_the_prds():
    assert controls.load_controls()["bar"] == {"catch": 0.8, "min_counted": 5, "clean_losses": 1}
