#!/usr/bin/env python3
"""
Fetch channels JSON and convert it to M3U playlist.
"""

import json
import urllib.request
from pathlib import Path

JSON_URL = "https://raw.githubusercontent.com/mdjamsad9/dudetvapi/main/public_decrypted/channels/50008.json"
OUTPUT_FILE = "playlist.m3u"

def main():
    print(f"Downloading: {JSON_URL}")
    with urllib.request.urlopen(JSON_URL) as response:
        channels = json.loads(response.read().decode("utf-8"))

    lines = ["#EXTM3U"]

    for ch in channels:
        title = ch.get("title", "Unknown").strip()
        logo = ch.get("logo", "").strip()
        link = ch.get("link", "").strip()
        api = ch.get("api", "").strip()

        if not link:
            continue

        extinf = f'#EXTINF:-1 tvg-name="{title}"'
        if logo:
            extinf += f' tvg-logo="{logo}"'
        if api:
            extinf += f' catchup-source="{api}"'
        extinf += f',{title}'

        lines.append(extinf)
        lines.append(link)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Created {OUTPUT_FILE} with {len(channels)} channels")

if __name__ == "__main__":
    main()
