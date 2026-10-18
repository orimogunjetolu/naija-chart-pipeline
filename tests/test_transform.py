import json

import pytest

from pipeline.transform import clean_rows


def _raw(tmp_path, tracks):
    f = tmp_path / "raw.json"
    f.write_text(json.dumps({"chart_date": "2026-10-17", "tracks": tracks}))
    return f


def _track(i, title="Song"):
    return {"id": i, "title": title, "artist": {"name": "Artist"},
            "album": {"title": "Album"}, "duration": 180, "rank": 5000}


def test_positions_follow_order(tmp_path):
    rows = clean_rows(_raw(tmp_path, [_track(1), _track(2)]))
    assert [r["position"] for r in rows] == [1, 2]


def test_rejects_duplicates(tmp_path):
    with pytest.raises(AssertionError):
        clean_rows(_raw(tmp_path, [_track(1), _track(1)]))


def test_rejects_missing_title(tmp_path):
    with pytest.raises(AssertionError):
        clean_rows(_raw(tmp_path, [_track(1, title="")]))
