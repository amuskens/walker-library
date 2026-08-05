#!/usr/bin/env python3
"""Small structural validation for the generated static library."""
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
text = (root / "data/books.js").read_text(encoding="utf-8")
match = re.search(r"window\.WALKER_BOOKS\s*=\s*(\[.*\]);?\s*$", text, re.S)
assert match, "books.js does not contain a valid collection assignment"
books = json.loads(match.group(1))
assert books, "no books installed"
for book in books:
    assert book["id"] and book["title"] and book["blocks"] and book["toc"]
    ids = [item["id"] for item in book["toc"]]
    assert len(ids) == len(set(ids)), f"duplicate section IDs in {book['id']}"
    pages = [item["page"] for item in book["blocks"] if item["type"] == "page"]
    assert pages, f"no original page markers in {book['id']}"
    for block in book["blocks"]:
        if block["type"] == "image":
            assert (root / block["src"]).exists(), f"missing image: {block['src']}"
print(f"Validated {len(books)} book(s), {sum(len(b['blocks']) for b in books)} blocks, {sum(len(b['toc']) for b in books)} headings")
