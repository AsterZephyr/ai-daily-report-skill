#!/usr/bin/env python3
"""
AI Daily Report Cache Manager

Maintains a deduplicated cache of crawled content.
Two operations:
  - get [--date YYYY-MM-DD] : retrieve cached entries, optionally filtered by date
  - put <json>              : add an entry, skip if duplicate (by url or title)

Storage: ~/.cache/ai-daily-report/cache.json
Format: {"entries": [{"url": "...", "title": "...", "date": "...", ...}]}
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent.parent / "data"
CACHE_FILE = CACHE_DIR / "cache.json"

# Entries older than this are auto-pruned on write
MAX_AGE_DAYS = 90


def _load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {"entries": []}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_cache(data: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _is_duplicate(existing: list[dict], entry: dict) -> bool:
    """Check duplicate by url (primary) or title (fallback)."""
    url = entry.get("url", "").strip()
    title = entry.get("title", "").strip()
    for e in existing:
        if url and e.get("url", "").strip() == url:
            return True
        if title and e.get("title", "").strip() == title:
            return True
    return False


def _prune_old(entries: list[dict]) -> list[dict]:
    """Remove entries older than MAX_AGE_DAYS."""
    cutoff = (datetime.now() - timedelta(days=MAX_AGE_DAYS)).strftime("%Y-%m-%d")
    return [e for e in entries if e.get("date", "9999-99-99") >= cutoff]


def cmd_get(date: str | None) -> None:
    """
    Retrieve cached entries.
    - If date is provided: return only entries matching that date.
    - If date is None: return entries from the last 14 days.
    """
    cache = _load_cache()
    entries = cache.get("entries", [])

    if date:
        filtered = [e for e in entries if e.get("date") == date]
    else:
        cutoff = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
        filtered = [e for e in entries if e.get("date", "0000-00-00") >= cutoff]

    json.dump(filtered, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_put(entry_json: str) -> None:
    """
    Add one or more entries to the cache. Skip duplicates.
    Accepts a single JSON object or a JSON array.
    """
    try:
        payload = json.loads(entry_json)
    except json.JSONDecodeError as exc:
        print(f'{{"error": "invalid JSON: {exc}"}}', file=sys.stderr)
        sys.exit(1)

    entries_to_add = payload if isinstance(payload, list) else [payload]

    cache = _load_cache()
    existing = cache.get("entries", [])
    added = 0
    skipped = 0

    for entry in entries_to_add:
        if not entry.get("date"):
            entry["date"] = datetime.now().strftime("%Y-%m-%d")

        if _is_duplicate(existing, entry):
            skipped += 1
            continue

        existing.append(entry)
        added += 1

    existing = _prune_old(existing)
    cache["entries"] = existing
    _save_cache(cache)

    result = {"added": added, "skipped_duplicates": skipped, "total": len(existing)}
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def main():
    parser = argparse.ArgumentParser(description="AI Daily Report Cache Manager")
    sub = parser.add_subparsers(dest="command", required=True)

    get_p = sub.add_parser("get", help="Retrieve cached entries")
    get_p.add_argument("--date", help="Filter by date (YYYY-MM-DD). Omit for last 14 days.")

    put_p = sub.add_parser("put", help="Add entry/entries to cache")
    put_p.add_argument("data", help="JSON string: object or array of objects")

    args = parser.parse_args()

    if args.command == "get":
        cmd_get(args.date)
    elif args.command == "put":
        cmd_put(args.data)


if __name__ == "__main__":
    main()
