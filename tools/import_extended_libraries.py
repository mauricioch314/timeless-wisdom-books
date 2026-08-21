#!/usr/bin/env python3
"""Import the English Atkinson/Verne libraries and smaller Spanish collections."""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit

SOURCE = Path("/Users/peps/Documents/website")
TARGET = Path(__file__).resolve().parents[1]

SMALL_SPANISH = [
    "biblioteca-exito.html", "biblioteca-esoterica.html",
    "biblioteca-clasica.html", "biblioteca-biografia.html",
    "biblioteca-haanel.html", "biblioteca-james-allen.html",
    "biblioteca-marden.html", "biblioteca-napoleon-hill.html",
    "biblioteca-shinn.html", "biblioteca-wattles.html",
]

PROTECTED = {"index.html", "biblioteca-es.html", "biblioteca-atkinson.html", "biblioteca-verne.html", "novelas.html"}

HTML_SOURCES = [
    SOURCE / "biblioteca-atkinson-en.html",
    SOURCE / "biblioteca-verne-ingles.html",
    SOURCE / "tesla.html",
    *sorted(SOURCE.glob("atkinson-[0-9][0-9][0-9]-en.html")),
    *sorted(SOURCE.glob("verne-*-en.html")),
    *(SOURCE / name for name in SMALL_SPANISH),
]

ATTR_RE = re.compile(r'''(?:src|href)=["']([^"']+)["']''', re.I)
CSS_URL_RE = re.compile(r'''url\(["']?([^"')]+)["']?\)''', re.I)


def adapt_html(text: str, filename: str) -> str:
    text = "\n".join(
        line for line in text.splitlines()
        if not ("mauriciochavesmesen.com" in line and re.search(r'<link rel="(?:canonical|alternate)"', line, re.I))
    ) + "\n"
    text = text.replace(" — Mauricio Chaves-Mesén</title>", " — Timeless Wisdom Books</title>")
    text = text.replace(">Mauricio Chaves-Mesén</a>", ">Timeless Wisdom Books</a>")
    text = text.replace("© Mauricio Chaves-Mesén", "© Timeless Wisdom Books")
    text = text.replace("← Mauricio Chaves-Mesén", "← Timeless Wisdom Books")
    text = text.replace('href="/"', 'href="index.html"')
    text = text.replace('href="/bio-en.html">Bio &amp; More</a>', 'href="library-en.html">English Library</a>')
    text = text.replace('href="/bio-en.html">Bio & More</a>', 'href="library-en.html">English Library</a>')
    text = text.replace('href="/bio-en.html">About the translator</a>', 'href="library-en.html">English Library</a>')
    text = text.replace('href="/bio.html">Bio &amp; más</a>', 'href="biblioteca-es.html">Biblioteca en español</a>')
    text = text.replace('href="/bio.html">Bio & más</a>', 'href="biblioteca-es.html">Biblioteca en español</a>')
    text = text.replace('href="traducciones.html"', 'href="biblioteca-es.html"')
    text = text.replace('href="/traducciones.html"', 'href="biblioteca-es.html"')
    text = text.replace('href="translations.html"', 'href="library-en.html"')
    # Large free-book PDFs remain on the established source host. Copying the
    # whole archive would add roughly 500 MB to every static deployment.
    text = re.sub(
        r'(["\'])/?(traducciones/atkinson/ebooks/[^"\']+)(["\'])',
        r'\1https://mauriciochavesmesen.com/\2\3', text,
    )
    text = re.sub(
        r'(["\'])/?(traducciones/atkinson/guides/[0-9]+-study-guide\.pdf)(["\'])',
        r'\1https://mauriciochavesmesen.com/\2\3', text,
    )
    return text


def local_file(ref: str) -> Path | None:
    parsed = urlsplit(ref)
    if parsed.scheme or parsed.netloc or ref.startswith(("#", "data:", "mailto:", "tel:")):
        return None
    relative = unquote(parsed.path).lstrip("/")
    if not relative or "." not in Path(relative).name:
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
        for ref in CSS_URL_RE.findall(source.read_text(encoding="utf-8")):
            nested = (source.parent / unquote(urlsplit(ref).path)).resolve()
            if nested.is_file() and nested.is_relative_to(SOURCE):
                copy_asset(nested, copied)


def main() -> None:
    copied: set[Path] = set()
    queue = list(dict.fromkeys(HTML_SOURCES))
    seen: set[Path] = set()
    while queue:
        source = queue.pop(0)
        if source in seen or not source.is_file():
            continue
        seen.add(source)
        text = adapt_html(source.read_text(encoding="utf-8"), source.name)
        (TARGET / source.name).write_text(text, encoding="utf-8")
        for ref in ATTR_RE.findall(text):
            item = local_file(ref)
            if not item:
                continue
            if item.suffix.lower() in {".html", ".htm"}:
                if source.name in SMALL_SPANISH and item.name not in PROTECTED:
                    queue.append(item)
            else:
                copy_asset(item, copied)
    print(f"Imported {len(seen)} pages and {len(copied)} referenced assets.")


if __name__ == "__main__":
    main()
