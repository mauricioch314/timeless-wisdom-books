#!/usr/bin/env python3
"""Import the Spanish Atkinson and Verne catalogues from the author website.

The source remains the editorial master. This script makes the Timeless Wisdom
copy reproducible while removing source-site navigation and SEO metadata.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit


SOURCE = Path("/Users/peps/Documents/website")
TARGET = Path(__file__).resolve().parents[1]

HTML_SOURCES = [
    SOURCE / "biblioteca-atkinson.html",
    SOURCE / "biblioteca-verne.html",
    *sorted(SOURCE.glob("atkinson-[0-9][0-9][0-9].html")),
    *sorted(SOURCE.glob("verne-*-es.html")),
]

ATTR_RE = re.compile(r'''(?:src|href)=["']([^"']+)["']''', re.I)
CSS_URL_RE = re.compile(r'''url\(["']?([^"')]+)["']?\)''', re.I)


def adapt_html(text: str, filename: str) -> str:
    # Canonical and hreflang URLs from the source domain must not survive on an
    # independent site. They can be restored once the production domain is set.
    text = "\n".join(
        line
        for line in text.splitlines()
        if not (
            "mauriciochavesmesen.com" in line
            and re.search(r'<link rel="(?:canonical|alternate)"', line, re.I)
        )
    ) + "\n"
    text = text.replace(" — Mauricio Chaves-Mesén</title>", " — Timeless Wisdom Books</title>")
    text = text.replace(">Mauricio Chaves-Mesén</a>", ">Timeless Wisdom Books</a>")
    text = text.replace('href="/"', 'href="index.html"')
    text = text.replace('href="/biblioteca-verne.html"', 'href="biblioteca-verne.html"')
    text = text.replace('href="/biblioteca-verne"', 'href="biblioteca-verne.html"')
    text = text.replace('href="traducciones.html"', 'href="biblioteca-es.html"')
    text = text.replace('href="/traducciones.html"', 'href="biblioteca-es.html"')
    text = text.replace('href="/bio.html">Bio &amp; más</a>', 'href="biblioteca-es.html">Biblioteca en español</a>')
    text = text.replace('href="/bio.html">Bio & más</a>', 'href="biblioteca-es.html">Biblioteca en español</a>')
    text = text.replace("© Mauricio Chaves-Mesén ·", "© Timeless Wisdom Books ·")
    text = text.replace("← Mauricio Chaves-Mesén", "← Timeless Wisdom Books")

    if filename.startswith("atkinson-") or filename == "biblioteca-atkinson.html":
        text = text.replace(">Traducciones</a>", ">Biblioteca en español</a>")
    if filename.startswith("verne-") or filename == "biblioteca-verne.html":
        text = text.replace("El Mundo de Julio Verne", "Biblioteca de Julio Verne")
        text = text.replace("El Mundo de Verne", "Julio Verne")
        text = text.replace("56 títulos de los Viajes Extraordinarios", "54 títulos de los Viajes Extraordinarios")

    return text


def local_asset(ref: str) -> Path | None:
    parsed = urlsplit(ref)
    if parsed.scheme or parsed.netloc or ref.startswith(("#", "data:", "mailto:")):
        return None
    relative = unquote(parsed.path).lstrip("/")
    if not relative or relative.endswith((".html", ".htm")) or "." not in Path(relative).name:
        return None
    candidate = SOURCE / relative
    return candidate if candidate.is_file() else None


def copy_asset(source: Path, copied: set[Path]) -> None:
    relative = source.relative_to(SOURCE)
    if relative in copied:
        return
    destination = TARGET / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    copied.add(relative)

    if source.suffix.lower() == ".css":
        css = source.read_text(encoding="utf-8")
        for ref in CSS_URL_RE.findall(css):
            nested = source.parent / unquote(urlsplit(ref).path)
            if nested.is_file() and nested.is_relative_to(SOURCE):
                copy_asset(nested.resolve(), copied)


def main() -> None:
    copied: set[Path] = set()
    page_count = 0
    for source in HTML_SOURCES:
        text = adapt_html(source.read_text(encoding="utf-8"), source.name)
        (TARGET / source.name).write_text(text, encoding="utf-8")
        page_count += 1
        for ref in ATTR_RE.findall(text):
            asset = local_asset(ref)
            if asset:
                copy_asset(asset, copied)

    print(f"Imported {page_count} pages and {len(copied)} referenced assets.")


if __name__ == "__main__":
    main()
