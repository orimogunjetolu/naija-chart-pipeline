"""Run the whole ETL: Extract -> Transform -> Load -> build SQL models."""
from pathlib import Path

import duckdb

from pipeline.extract import extract
from pipeline.load import DB_PATH, load
from pipeline.transform import clean_rows


def build_models(db_path: str = DB_PATH) -> None:
    con = duckdb.connect(db_path)
    for sql_file in sorted(Path("sql").glob("*.sql")):
        con.execute(sql_file.read_text())
        print(f"model: built {sql_file.stem}")
    con.close()


if __name__ == "__main__":
    raw = extract()
    load(clean_rows(raw))
    build_models()
