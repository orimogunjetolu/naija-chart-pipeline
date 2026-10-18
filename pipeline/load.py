"""LOAD: write clean rows into a DuckDB database (a free, file-based SQL warehouse).

Loading is idempotent: re-running the same day replaces that day's rows
instead of creating duplicates.
"""
import duckdb

DB_PATH = "data/charts.duckdb"

DDL = """
CREATE TABLE IF NOT EXISTS chart_entries (
    chart_date   DATE,
    position     INTEGER,
    track_id     BIGINT,
    title        VARCHAR,
    artist       VARCHAR,
    album        VARCHAR,
    duration_sec INTEGER,
    deezer_rank  INTEGER,
    explicit     BOOLEAN,
    PRIMARY KEY (chart_date, track_id)
);
"""


def load(rows: list[dict], db_path: str = DB_PATH) -> int:
    con = duckdb.connect(db_path)
    con.execute(DDL)
    chart_date = rows[0]["chart_date"]
    con.execute("DELETE FROM chart_entries WHERE chart_date = ?", [chart_date])
    con.executemany(
        "INSERT INTO chart_entries VALUES (?,?,?,?,?,?,?,?,?)",
        [tuple(r.values()) for r in rows],
    )
    n = con.execute("SELECT count(*) FROM chart_entries").fetchone()[0]
    con.close()
    print(f"load: {len(rows)} rows for {chart_date}; table now has {n} rows")
    return n
