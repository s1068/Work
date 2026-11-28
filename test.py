#!/usr/bin/env python3
"""
Fetch channels JSON and convert it to proper Kodi M3U (ClearKey)
"""

import json
import urllib.request

JSON_URL = "https://raw.githubusercontent.com/mdjamsad9/dudetvapi/main/public_decrypted/channels/50008.json"
OUTPUT_FILE = "playlist.m3u"

def main():
    print(f"Downloading: {JSON_URL}")
    with urllib.request.urlopen(JSON_URL) as response:
        channels = json.loads(response.read().decode("utf-8"))

    lines = ["#EXTM3U"]

    for ch in channels:
        title = ch.get("title", "Unknown").strip()
        logo  = ch.get("logo", "").strip()
        link  = ch.get("link", "").strip()
        key   = ch.get("api", "").strip()          # kid:key

        if not link:
            continue

        # EXTINF
        extinf = f'#EXTINF:-1 tvg-name="{title}"'
        if logo:
            extinf += f' tvg-logo="{logo}"'
        extinf += f',{title}'
        lines.append(extinf)

        # ClearKey properties (correct for this key format)
        if key:
            lines.append("#KODIPROP:inputstream=inputstream.adaptive")
            lines.append("#KODIPROP:inputstream.adaptive.manifest_type=mpd")
            lines.append("#KODIPROP:inputstream.adaptive.license_type=org.w3.clearkey")
            lines.append(f"#KODIPROP:inputstream.adaptive.license_key={key}")

        lines.append(link)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Created {OUTPUT_FILE} with {len(channels)} channels")

if __name__ == "__main__":
    main()
