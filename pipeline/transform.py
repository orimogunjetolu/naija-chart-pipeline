"""TRANSFORM: turn messy nested JSON into clean, flat rows.

Each row = one song's position on one day's chart.
"""
import json
from pathlib import Path


def clean_rows(raw_file: Path) -> list[dict]:
    payload = json.loads(Path(raw_file).read_text())
    chart_date = payload["chart_date"]
    rows = []
    for position, t in enumerate(payload["tracks"], start=1):
        rows.append({
            "chart_date": chart_date,
            "position": position,
            "track_id": t["id"],
            "title": (t.get("title") or "").strip(),
            "artist": (t.get("artist", {}).get("name") or "").strip(),
            "album": (t.get("album", {}).get("title") or "").strip(),
            "duration_sec": int(t.get("duration") or 0),
            "deezer_rank": int(t.get("rank") or 0),
            "explicit": bool(t.get("explicit_lyrics")),
        })
    # basic data-quality checks: fail loudly instead of loading bad data
    assert rows, "no rows extracted"
    assert len({r["track_id"] for r in rows}) == len(rows), "duplicate tracks"
    assert all(r["title"] and r["artist"] for r in rows), "missing title/artist"
    return rows
