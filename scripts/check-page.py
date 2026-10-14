#!/usr/bin/env python3
"""Validate the redirect page to the projects hub without contacting external services."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

HUB = "https://projects.cristian-nichifor.com/"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.errors = []
        self.lang = False
        self.title = False
        self.heading = False
        self.refresh = None
        self.canonical = None
        self.robots = None

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == "html": self.lang = bool(attrs.get("lang"))
        if tag == "title": self.title = True
        if tag == "h1": self.heading = True
        if tag == "meta" and (attrs.get("http-equiv") or "").lower() == "refresh":
            self.refresh = attrs.get("content") or ""
        if tag == "meta" and attrs.get("name") == "robots":
            self.robots = attrs.get("content") or ""
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if "id" in attrs:
            if attrs["id"] in self.ids: self.errors.append("duplicate id: " + attrs["id"])
            self.ids.add(attrs["id"])
        if tag == "a":
            if not attrs.get("href"): self.errors.append("anchor without destination")
            else: self.links.append(attrs["href"])


def check(root):
    page = Path(root).resolve() / "index.html"
    parser = Page()
    parser.feed(page.read_text())
    for value, message in [(parser.lang, "missing page language"), (parser.title, "missing title"), (parser.heading, "missing main heading")]:
        if not value: parser.errors.append(message)
    match = re.fullmatch(r"\s*0\s*;\s*url=(\S+)\s*", parser.refresh or "", re.IGNORECASE)
    if not match or match.group(1) != HUB:
        parser.errors.append("meta refresh must send visitors to " + HUB)
    if parser.canonical != HUB:
        parser.errors.append("canonical link must be " + HUB)
    if "noindex" not in (parser.robots or "").replace(" ", "").split(","):
        parser.errors.append("robots meta must include noindex")
    if HUB not in parser.links:
        parser.errors.append("visible link to " + HUB + " is missing")
    for href in parser.links:
        if not href.startswith("https://"):
            parser.errors.append("unexpected link: " + href)
    return parser.errors, len(parser.links), page.name


if __name__ == "__main__":
    errors, count, name = check(sys.argv[1] if len(sys.argv) > 1 else ".")
    if errors:
        sys.exit("\n".join(errors))
    print(f"Validated redirect to {HUB} and {count} links in {name}")
