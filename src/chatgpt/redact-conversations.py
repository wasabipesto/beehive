#!/usr/bin/env python3
# This script takes ./conversations-full.csv (relative to this script's location),
# then removes some columns and writes the output to ./conversations.csv.
#
# Keep columns:
# - score
# - date
# - msg_count
# - word_count
# - category
# - topic
#
# Derived columns:
# - kept (bool): True if decision starts with "Keep", False otherwise
#
# Remove columns:
# - title
# - id
# - first_message
# - decision

import csv
from pathlib import Path

KEEP_COLUMNS = ["score", "date", "msg_count", "word_count", "category", "topic", "kept"]

script_dir = Path(__file__).parent
input_path = script_dir / "conversations-full.csv"
output_path = script_dir / "conversations.csv"

with (
    open(input_path, newline="", encoding="utf-8") as infile,
    open(output_path, "w", newline="", encoding="utf-8") as outfile,
):
    reader = csv.DictReader(infile)

    missing = [
        col
        for col in [
            "score",
            "date",
            "msg_count",
            "word_count",
            "category",
            "topic",
            "decision",
        ]
        if col not in (reader.fieldnames or [])
    ]
    if missing:
        raise ValueError(f"Missing expected columns in input: {missing}")

    writer = csv.DictWriter(outfile, fieldnames=KEEP_COLUMNS, extrasaction="ignore")
    writer.writeheader()

    rows_written = 0
    for row in reader:
        row["kept"] = row["decision"].lower().startswith("keep")
        writer.writerow(row)
        rows_written += 1

print(f"Wrote {rows_written} rows to {output_path}")
