"""EXTRACT: download today's official Deezer 'Top Nigeria' chart and save the raw JSON.

Keeping the untouched raw file means we can always re-run later steps
without calling the API again (a core data engineering habit).
"""
import json
from datetime import date
from pathlib import Path

import requests

CHART_PLAYLIST_ID = 1362516565  # Deezer Charts: "Top Nigeria"
URL = f"https://api.deezer.com/playlist/{CHART_PLAYLIST_ID}/tracks"
RAW_DIR = Path("data/raw")


def extract(run_date: date | None = None) -> Path:
    run_date = run_date or date.today()
    tracks, url = [], URL + "?limit=100"
    while url:  # the API returns pages; follow "next" until done
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        body = resp.json()
        tracks.extend(body.get("data", []))
        url = body.get("next")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / f"top_nigeria_{run_date.isoformat()}.json"
    out.write_text(json.dumps({"chart_date": run_date.isoformat(), "tracks": tracks}))
    print(f"extract: saved {len(tracks)} tracks to {out}")
    return out
