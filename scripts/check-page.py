#!/usr/bin/env python3
"""Validate local page structure and links without contacting external services."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.errors = []
        self.lang = False
        self.title = False
        self.heading = False
    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == "html": self.lang = bool(attrs.get("lang"))
        if tag == "title": self.title = True
        if tag == "h1": self.heading = True
        if "id" in attrs:
            if attrs["id"] in self.ids: self.errors.append("duplicate id: " + attrs["id"])
            self.ids.add(attrs["id"])
        if tag == "a":
            if not attrs.get("href"): self.errors.append("anchor without destination")
            else: self.links.append(attrs["href"])

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
page = root / "index.html"
parser = Page()
parser.feed(page.read_text())
for value, message in [(parser.lang, "missing page language"), (parser.title, "missing title"), (parser.heading, "missing main heading"), (parser.links, "empty directory")]:
    if not value: parser.errors.append(message)
for href in parser.links:
    url = urlsplit(href)
    if url.scheme in ("https", "http"):
        if not url.netloc: parser.errors.append("invalid external URL: " + href)
    elif url.scheme == "mailto":
        if "@" not in url.path: parser.errors.append("invalid contact URL: " + href)
    elif url.scheme or url.netloc:
        parser.errors.append("unexpected URL scheme: " + href)
    else:
        path = (root / unquote(url.path).lstrip("/")).resolve() if url.path else page
        if not path.is_relative_to(root) or not path.exists(): parser.errors.append("missing local destination: " + href)
        if path == page and url.fragment and unquote(url.fragment) not in parser.ids: parser.errors.append("missing fragment: " + href)
if parser.errors:
    sys.exit("\n".join(parser.errors))
print(f"Validated {len(parser.links)} links and page landmarks in {page.name}")
