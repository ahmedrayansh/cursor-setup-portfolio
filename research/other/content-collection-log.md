# Content Collection Log

Collected: 2026-04-18

## Request

Collect recent content for:
- Dave Gerhardt
- Chris Walker
- Justin Welsh
- Amanda Natividad
- Ross Simmonds
- Devin Reed
- Anthony Pierri
- Guillaume Moubeche
- Gaetano DiNardi
- Lara Acosta

Target folders:
- `research/sources.md`
- `research/linkedin-posts/`
- `research/youtube-transcripts/`
- `research/other/`

## LinkedIn Collection

Method:
- Public LinkedIn post pages and public search-result snippets were used.
- Where a direct LinkedIn `activity-` URL was available, the activity ID was decoded to get an exact UTC date.
- Where LinkedIn only exposed a company-feed repost snippet, the company feed URL and visible relative date were recorded.

Limitations:
- LinkedIn does not reliably expose every recent post without login or API access.
- Some "latest" public results may be snippets or reposts rather than direct author post URLs.
- The files therefore use the phrase "publicly visible" when the post was found through a public page/feed, not a private authenticated scrape.

## YouTube Transcript Collection

Method:
- Public YouTube captions / free transcript-fetching methods were used where captions were available.
- The repo stores cleaned transcript-style notes, not full verbatim caption dumps.
- For newer additions where a full public caption fetch was not available, the notes use public video pages, episode descriptions, and related official pages; those files state the limitation directly.

Files:
- `research/youtube-transcripts/amanda-natividad-zero-click-content-notes.md`
- `research/youtube-transcripts/chris-walker-content-framework-notes.md`
- `research/youtube-transcripts/devin-reed-reed-between-the-lines-trailer-notes.md`
- `research/youtube-transcripts/anthony-pierri-b2b-homepage-positioning-notes.md`
- `research/youtube-transcripts/guillaume-moubeche-why-no-longer-ceo-notes.md`
- `research/youtube-transcripts/justin-welsh-growth-decoded-transcript.md`
- `research/youtube-transcripts/lara-acosta-strategic-storytelling-linkedin-notes.md`
- `research/youtube-transcripts/ross-simmonds-b2b-content-distribution-masterclass-transcript.md`

Dave Gerhardt note:
- A relevant public podcast source was found and retained under `research/other/`.
- A reliable free public YouTube transcript source for Dave was not found during this pass.

Gaetano DiNardi note:
- A strong public AI search webinar source was found on Clearscope and retained under `research/other/`.
- A reliable public YouTube transcript source for Gaetano was not found during this pass.
