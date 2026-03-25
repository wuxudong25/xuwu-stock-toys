#!/usr/bin/env python3
"""Fetch yesterday's GOLD daily K-line from AllTick HTTP API."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request
import uuid

API_URL = "https://quote.alltick.co/quote-b-api/kline"


def build_query_payload(code: str, kline_type: int, query_kline_num: int) -> dict:
    return {
        "trace": str(uuid.uuid4()),
        "data": {
            "code": code,
            "kline_type": kline_type,
            "kline_timestamp_end": 0,
            "query_kline_num": query_kline_num,
            "adjust_type": 0,
        },
    }


def fetch_kline(token: str, code: str, timeout: int = 15) -> dict:
    payload = build_query_payload(code=code, kline_type=8, query_kline_num=2)
    encoded_query = urllib.parse.quote(json.dumps(payload, separators=(",", ":"), ensure_ascii=False))
    url = f"{API_URL}?token={token}&query={encoded_query}"

    with urllib.request.urlopen(url, timeout=timeout) as response:
        body = response.read().decode("utf-8")
    return json.loads(body)


def _to_utc_date(ts: str) -> dt.date:
    timestamp = int(ts)
    return dt.datetime.utcfromtimestamp(timestamp).date()


def extract_yesterday_bar(resp_data: dict) -> dict:
    if resp_data.get("ret") != 200:
        raise RuntimeError(f"API returned error: ret={resp_data.get('ret')} msg={resp_data.get('msg')}")

    kline_list = (resp_data.get("data") or {}).get("kline_list") or []
    if len(kline_list) < 2:
        raise RuntimeError(f"Expected at least 2 bars, got {len(kline_list)}")

    sorted_bars = sorted(kline_list, key=lambda x: int(x["timestamp"]))
    return sorted_bars[-2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch yesterday's GOLD daily K-line via AllTick API")
    parser.add_argument("--token", default=os.getenv("ALLTICK_TOKEN"), help="AllTick API token (or env ALLTICK_TOKEN)")
    parser.add_argument("--code", default="GOLD", help="Product code, defaults to GOLD")
    parser.add_argument("--raw", action="store_true", help="Print full API response JSON")
    args = parser.parse_args()

    if not args.token:
        print("Missing token. Pass --token or set ALLTICK_TOKEN.", file=sys.stderr)
        return 2

    try:
        resp = fetch_kline(token=args.token, code=args.code)
        if args.raw:
            print(json.dumps(resp, ensure_ascii=False, indent=2))

        yesterday_bar = extract_yesterday_bar(resp)
        bar_date = _to_utc_date(yesterday_bar["timestamp"])

        print("Yesterday GOLD daily K-line (UTC date based on returned timestamp):")
        print(json.dumps({
            "code": args.code,
            "date": bar_date.isoformat(),
            "open": yesterday_bar["open_price"],
            "high": yesterday_bar["high_price"],
            "low": yesterday_bar["low_price"],
            "close": yesterday_bar["close_price"],
            "volume": yesterday_bar.get("volume"),
            "turnover": yesterday_bar.get("turnover"),
            "timestamp": yesterday_bar["timestamp"],
        }, ensure_ascii=False, indent=2))
        return 0
    except urllib.error.URLError as exc:
        print(f"HTTP error: {exc}", file=sys.stderr)
    except (KeyError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Parse/API error: {exc}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
