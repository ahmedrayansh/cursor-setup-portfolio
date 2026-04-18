from __future__ import annotations

import os
import re
import textwrap
from datetime import date
from pathlib import Path
from typing import Any

import requests


API_URL = "https://api.supadata.ai/v1/transcript"
TRANSLATE_URL = "https://api.supadata.ai/v1/youtube/transcript/translate"
API_KEY = os.getenv("SUPADATA_API_KEY", "sd_d467b0a3e46f958e44d3f0387776ce15")

OUTPUT_DIR = Path("research/youtube-transcripts")

VIDEOS = [
    {
        "person": "Dave Gerhardt",
        "title": "Life is Too Short to Work for a CEO Who Doesn't Get Marketing",
        "url": None,
        "output": OUTPUT_DIR / "dave-gerhardt-youtube-transcript.md",
    },
    {
        "person": "Chris Walker",
        "title": "How To Take Your Content Strategy To The Next Level",
        "url": "https://www.youtube.com/watch?v=z624BxQVHH4",
        "output": OUTPUT_DIR / "chris-walker-content-framework-notes.md",
    },
    {
        "person": "Justin Welsh",
        "title": "Interview with Justin Welsh - Increasing productivity by creating systems",
        "url": "https://www.youtube.com/watch?v=NWNR7BJ1qy8",
        "output": OUTPUT_DIR / "justin-welsh-video1.md",
    },
    {
        "person": "Amanda Natividad",
        "title": "MicroConf Refresh: The New Way of Marketing - Mastery of Zero-Click Content",
        "url": "https://www.youtube.com/watch?v=Z-OJiMGYL74",
        "output": OUTPUT_DIR / "amanda-natividad-zero-click-content-notes.md",
    },
    {
        "person": "Ross Simmonds",
        "title": "B2B Content Distribution Masterclass: Live with Ross Simmonds",
        "url": "https://www.youtube.com/watch?v=GiI2UaY6HTI",
        "output": OUTPUT_DIR / "ross-simmonds-b2b-content-distribution-masterclass-transcript.md",
    },
    {
        "person": "Devin Reed",
        "title": "The #1 mistake brands make with B2B creators (Aneesh Lal, Wishly)",
        "url": "https://www.youtube.com/watch?v=9i-4lp4Y8d4",
        "output": OUTPUT_DIR / "devin-reed-reed-between-the-lines-trailer-notes.md",
    },
    {
        "person": "Anthony Pierri",
        "title": "How to Perfectly Position Your B2B Brand in 34 Minutes",
        "url": "https://www.youtube.com/watch?v=ivZ4HRKEc20",
        "output": OUTPUT_DIR / "anthony-pierri-b2b-homepage-positioning-notes.md",
    },
    {
        "person": "Guillaume Moubeche",
        "title": "Why I'm no longer CEO of lemlist (and what I'm doing now...)",
        "url": "https://www.youtube.com/watch?v=VEUxgjUUBBU",
        "output": OUTPUT_DIR / "guillaume-moubeche-why-no-longer-ceo-notes.md",
        "translate_to": "en",
    },
    {
        "person": "Gaetano DiNardi",
        "title": "The Dark SEO Funnel | AirOps & Gaetano DiNardi",
        "url": "https://www.youtube.com/watch?v=0XWc3NfMIUc",
        "output": OUTPUT_DIR / "gaetano-dinardi-dark-seo-funnel-transcript.md",
    },
    {
        "person": "Lara Acosta",
        "title": "The Power of Strategic Storytelling for Your Personal Brand on LinkedIn",
        "url": "https://www.youtube.com/watch?v=dC_CxCi44KE",
        "output": OUTPUT_DIR / "lara-acosta-strategic-storytelling-linkedin-notes.md",
    },
]


def fetch_transcript(video_url: str, lang: str = "en", mode: str = "auto") -> dict[str, Any]:
    response = requests.get(
        API_URL,
        headers={"x-api-key": API_KEY},
        params={"url": video_url, "lang": lang, "text": "true", "mode": mode},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def translate_transcript(video_url: str, lang: str = "en") -> dict[str, Any]:
    response = requests.get(
        TRANSLATE_URL,
        headers={"x-api-key": API_KEY},
        params={"url": video_url, "lang": lang, "text": "true"},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def extract_text(payload: dict[str, Any]) -> str:
    for key in ("text", "transcript", "content"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    segments = payload.get("segments") or payload.get("snippets") or payload.get("captions")
    if isinstance(segments, list):
        parts = []
        for segment in segments:
            if isinstance(segment, dict):
                text = segment.get("text") or segment.get("content")
                if text:
                    parts.append(str(text))
            elif isinstance(segment, str):
                parts.append(segment)
        if parts:
            return " ".join(parts).strip()

    raise ValueError(f"Could not find transcript text in API response keys: {sorted(payload.keys())}")


def clean_transcript(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?<!\n)\s+(\[[^\]]+\])", r"\n\n\1", text)
    return text.strip()


def to_markdown(person: str, title: str, url: str, transcript: str, collection_method: str) -> str:
    wrapped = "\n\n".join(
        textwrap.fill(paragraph.strip(), width=100)
        for paragraph in transcript.split("\n\n")
        if paragraph.strip()
    )
    return (
        f"# {person} - YouTube Transcript\n\n"
        f"Video Title: {title}\n\n"
        f"Link: {url}\n\n"
        f"Collected: {date.today().isoformat()}\n\n"
        f"Collection method: {collection_method}\n\n"
        "## Transcript\n\n"
        f"{wrapped}\n"
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for video in VIDEOS:
        person = video["person"]
        title = video["title"]
        url = video["url"]
        output = video["output"]
        translate_to = video.get("translate_to")

        if not url:
            print(f"\n--- {person} ---")
            print("Skipped: no regular YouTube watch URL is available in this project yet.")
            continue

        print(f"\n--- {person} ---")
        print(f"Fetching: {url}")

        try:
            if translate_to:
                payload = translate_transcript(url, translate_to)
                collection_method = (
                    f"Supadata YouTube transcript translation endpoint, translated to {translate_to}."
                )
            else:
                payload = fetch_transcript(url)
                collection_method = "Supadata transcript API, preferring English captions when available."
            transcript = clean_transcript(extract_text(payload))
            markdown = to_markdown(person, title, url, transcript, collection_method)
            output.write_text(markdown, encoding="utf-8")
            print(transcript)
            print(f"\nSaved: {output}")
        except requests.HTTPError as error:
            body = error.response.text if error.response is not None else ""
            print(f"Failed: {error}\n{body}")
        except Exception as error:
            print(f"Failed: {error}")


if __name__ == "__main__":
    main()
