#!/usr/bin/env python3
"""
update_bib.py — Automatically update _bibliography/papers.bib
from Google Scholar and DBLP profiles listed in _data/members.yml

Usage:
    python scripts/update_bib.py [OPTIONS]

Options:
    --dry-run        Print new entries without modifying papers.bib
    --min-year INT   Only include papers from this year onward (default: 2020)
    --max-per INT    Maximum papers per author (default: 10, 0 = unlimited)
    --source STR     Data source: "semantic_scholar" | "dblp" | "all" (default: all)

Requirements:
    pip install pyyaml requests semanticscholar

For Google Scholar (optional, may be rate-limited):
    pip install scholarly
"""

import argparse
import re
import sys
import time
from pathlib import Path

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MEMBERS_YML = REPO_ROOT / "_data" / "members.yml"
PAPERS_BIB = REPO_ROOT / "_bibliography" / "papers.bib"

# ── Helpers ──────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Create a safe BibTeX key from arbitrary text."""
    text = text.lower()
    text = re.sub(r"[àáâãäå]", "a", text)
    text = re.sub(r"[èéêë]", "e", text)
    text = re.sub(r"[ìíîï]", "i", text)
    text = re.sub(r"[òóôõö]", "o", text)
    text = re.sub(r"[ùúûü]", "u", text)
    text = re.sub(r"[^a-z0-9]", "", text)
    return text


def make_key(first_author_last: str, year: int, title_word: str) -> str:
    """e.g. 'lee2025iclr'"""
    last = slugify(first_author_last)[:10]
    word = slugify(title_word)[:8]
    return f"{last}{year}{word}"


def first_last_name(author_str: str) -> str:
    """Extract last name of first author from 'Last, First and ...' or 'First Last and ...'."""
    first_author = author_str.split(" and ")[0].strip()
    if "," in first_author:
        return first_author.split(",")[0].strip()
    parts = first_author.strip().split()
    return parts[-1] if parts else "unknown"


def load_existing_keys(bib_path: Path) -> set:
    """Return the set of BibTeX keys already in papers.bib."""
    keys = set()
    if not bib_path.exists():
        return keys
    for line in bib_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^@\w+\{(\S+),", line.strip())
        if m:
            keys.add(m.group(1).rstrip(","))
    return keys


def append_entries(bib_path: Path, entries: list[str]) -> None:
    """Append new BibTeX entries to papers.bib."""
    with bib_path.open("a", encoding="utf-8") as f:
        for entry in entries:
            f.write("\n" + entry + "\n")


# ── DBLP source ──────────────────────────────────────────────────────────────

def fetch_dblp(dblp_id: str, min_year: int, max_per: int) -> list[dict]:
    """
    Fetch publications from DBLP using the author pid.
    dblp_id example: "255/6568"
    Returns list of dicts with keys: title, authors, year, venue, type, url, doi
    """
    url = f"https://dblp.org/pid/{dblp_id}.xml"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  [DBLP] Request failed for {dblp_id}: {e}", file=sys.stderr)
        return []

    import xml.etree.ElementTree as ET
    root = ET.fromstring(resp.text)

    papers = []
    for pub in root.findall(".//{http://www.w3.org/1999/xhtml}li"):
        pass  # DBLP XML is more complex; use the search API instead

    # Simpler: use DBLP search API
    search_url = "https://dblp.org/search/publ/api"
    params = {
        "q": f"author_pid:{dblp_id}",
        "format": "json",
        "h": max_per if max_per > 0 else 100,
    }
    try:
        resp = requests.get(search_url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  [DBLP] Search API failed for {dblp_id}: {e}", file=sys.stderr)
        return []

    hits = data.get("result", {}).get("hits", {}).get("hit", [])
    for hit in hits:
        info = hit.get("info", {})
        year = int(info.get("year", 0))
        if year < min_year:
            continue
        authors_raw = info.get("authors", {}).get("author", [])
        if isinstance(authors_raw, dict):
            authors_raw = [authors_raw]
        author_names = [a.get("text", "") for a in authors_raw]
        papers.append({
            "title":   info.get("title", "").rstrip("."),
            "authors": " and ".join(author_names),
            "year":    year,
            "venue":   info.get("venue", ""),
            "type":    info.get("type", ""),
            "url":     info.get("ee", ""),
            "doi":     info.get("doi", ""),
        })

    return papers[:max_per] if max_per > 0 else papers


# ── Semantic Scholar source ───────────────────────────────────────────────────

def search_semantic_scholar_author(name_en: str) -> str | None:
    """Find Semantic Scholar author ID by name."""
    url = "https://api.semanticscholar.org/graph/v1/author/search"
    params = {"query": name_en, "fields": "name,affiliations", "limit": 5}
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        for author in data.get("data", []):
            affiliations = [a.get("name", "").lower() for a in author.get("affiliations", [])]
            if any("jbnu" in a or "jeonbuk" in a or "chonbuk" in a or "전북" in a for a in affiliations):
                return author["authorId"]
        # Fall back to first result if no affiliation match
        if data.get("data"):
            return data["data"][0]["authorId"]
    except Exception as e:
        print(f"  [S2] Author search failed for '{name_en}': {e}", file=sys.stderr)
    return None


def fetch_semantic_scholar(name_en: str, min_year: int, max_per: int) -> list[dict]:
    """Fetch papers for an author from Semantic Scholar."""
    author_id = search_semantic_scholar_author(name_en)
    if not author_id:
        print(f"  [S2] Author not found: {name_en}", file=sys.stderr)
        return []

    url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
    fields = "title,authors,year,venue,externalIds,openAccessPdf,publicationTypes"
    params = {"fields": fields, "limit": max_per if 0 < max_per <= 100 else 100}
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  [S2] Papers fetch failed for '{name_en}' (id={author_id}): {e}", file=sys.stderr)
        return []

    papers = []
    for p in data.get("data", []):
        year = p.get("year") or 0
        if year < min_year:
            continue
        author_names = [a.get("name", "") for a in p.get("authors", [])]
        doi = p.get("externalIds", {}).get("DOI", "")
        arxiv = p.get("externalIds", {}).get("ArXiv", "")
        pdf_url = ""
        if p.get("openAccessPdf"):
            pdf_url = p["openAccessPdf"].get("url", "")
        papers.append({
            "title":   p.get("title", "").rstrip("."),
            "authors": " and ".join(author_names),
            "year":    year,
            "venue":   p.get("venue", ""),
            "type":    (p.get("publicationTypes") or [""])[0],
            "url":     pdf_url or (f"https://doi.org/{doi}" if doi else ""),
            "doi":     doi,
            "arxiv":   arxiv,
        })

    papers.sort(key=lambda x: x["year"], reverse=True)
    return papers[:max_per] if max_per > 0 else papers


# ── Google Scholar source (optional) ─────────────────────────────────────────

def fetch_google_scholar(scholar_id: str, min_year: int, max_per: int) -> list[dict]:
    """
    Fetch papers from Google Scholar using the `scholarly` library.
    Install: pip install scholarly
    Note: Google Scholar blocks automated requests — use a proxy or limit calls.
    """
    try:
        from scholarly import scholarly as gs  # type: ignore
    except ImportError:
        print("  [GS] scholarly not installed. Run: pip install scholarly", file=sys.stderr)
        return []

    try:
        author = gs.search_author_id(scholar_id)
        gs.fill(author, sections=["publications"])
    except Exception as e:
        print(f"  [GS] Failed for scholar_id={scholar_id}: {e}", file=sys.stderr)
        return []

    papers = []
    for pub in author.get("publications", []):
        bib = pub.get("bib", {})
        year = int(bib.get("pub_year", 0) or 0)
        if year < min_year:
            continue
        papers.append({
            "title":   bib.get("title", ""),
            "authors": bib.get("author", ""),
            "year":    year,
            "venue":   bib.get("journal") or bib.get("conference") or bib.get("venue", ""),
            "type":    "JournalArticle" if bib.get("journal") else "Conference",
            "url":     pub.get("pub_url", ""),
            "doi":     "",
            "arxiv":   "",
        })
        if max_per > 0 and len(papers) >= max_per:
            break

    return papers


# ── BibTeX formatting ─────────────────────────────────────────────────────────

CONFERENCE_KEYWORDS = {
    "cvpr", "iccv", "eccv", "neurips", "nips", "icml", "iclr", "aaai",
    "acm mm", "acm chi", "uist", "iccv", "uai", "aistats", "iros", "wacv",
    "miccai", "accv", "ijcai", "cases", "lctes",
}

JOURNAL_KEYWORDS = {
    "ieee transactions", "transactions on", "journal of", "letters",
    "pattern recognition", "information sciences", "computer vision",
    "image understanding", "systems", "access",
}


def guess_entry_type(pub: dict) -> str:
    ptype = (pub.get("type") or "").lower()
    if "journal" in ptype:
        return "article"
    if any(k in ptype for k in ("conference", "proceedings")):
        return "inproceedings"
    venue = pub.get("venue", "").lower()
    if any(k in venue for k in CONFERENCE_KEYWORDS):
        return "inproceedings"
    if any(k in venue for k in JOURNAL_KEYWORDS):
        return "article"
    return "inproceedings"  # default


def format_bibtex(pub: dict, key: str, abbr: str = "") -> str:
    etype = guess_entry_type(pub)
    venue_field = "booktitle" if etype == "inproceedings" else "journal"

    lines = [f"@{etype}{{{key},"]
    if abbr:
        lines.append(f"  abbr      = {{{abbr}}},")
    lines.append(f"  title     = {{{{{pub['title']}}}}},")
    lines.append(f"  author    = {{{pub['authors']}}},")
    lines.append(f"  {venue_field:<9} = {{{pub['venue']}}},")
    lines.append(f"  year      = {{{pub['year']}}},")
    if pub.get("doi"):
        lines.append(f"  doi       = {{{pub['doi']}}},")
    if pub.get("url") and not pub.get("doi"):
        lines.append(f"  url       = {{{pub['url']}}},")
    if pub.get("arxiv"):
        lines.append(f"  pdf       = {{https://arxiv.org/abs/{pub['arxiv']}}},")
    lines.append("  selected  = {false},")
    lines.append("}")
    return "\n".join(lines)


def venue_abbr(venue: str) -> str:
    """Derive a short abbreviation from venue name."""
    v = venue.strip()
    # Check common names
    table = {
        "IEEE Transactions on Image Processing": "IEEE TIP",
        "IEEE Transactions on Pattern Analysis and Machine Intelligence": "IEEE TPAMI",
        "IEEE Transactions on Neural Networks and Learning Systems": "IEEE TNNLS",
        "IEEE Transactions on Multimedia": "IEEE TMM",
        "IEEE Transactions on Geoscience and Remote Sensing": "IEEE TGRS",
        "IEEE Signal Processing Letters": "IEEE SPL",
        "IEEE Access": "IEEE Access",
        "Neural Information Processing Systems": "NeurIPS",
        "Advances in Neural Information Processing Systems": "NeurIPS",
        "International Conference on Machine Learning": "ICML",
        "International Conference on Learning Representations": "ICLR",
        "Conference on Computer Vision and Pattern Recognition": "CVPR",
        "International Conference on Computer Vision": "ICCV",
        "European Conference on Computer Vision": "ECCV",
        "AAAI Conference on Artificial Intelligence": "AAAI",
        "International Joint Conference on Artificial Intelligence": "IJCAI",
        "ACM International Conference on Multimedia": "ACM MM",
        "CHI Conference on Human Factors in Computing Systems": "ACM CHI",
        "ACM Conference on Human Factors in Computing Systems": "ACM CHI",
        "AISTATS": "AISTATS",
        "Uncertainty in Artificial Intelligence": "UAI",
        "Medical Image Computing and Computer Assisted Intervention": "MICCAI",
        "Winter Conference on Applications of Computer Vision": "WACV",
        "ACM Transactions on Intelligent Systems and Technology": "ACM TIST",
        "Computer Vision and Image Understanding": "CVIU",
    }
    for full, short in table.items():
        if full.lower() in v.lower():
            return short
    # Fallback: uppercase initials of capitalized words
    words = [w for w in v.split() if w[0].isupper() and len(w) > 2]
    if words:
        return "".join(w[0] for w in words[:4])
    return ""


# ── Main ──────────────────────────────────────────────────────────────────────

def load_members(yml_path: Path) -> list[dict]:
    data = yaml.safe_load(yml_path.read_text(encoding="utf-8"))
    members = []
    for group in ("professors", "associate_professors", "assistant_professors"):
        members.extend(data.get(group, []))
    return members


def process_member(member: dict, args: argparse.Namespace) -> list[str]:
    name_en = member.get("name_en", "")
    links = member.get("links", {}) or {}
    scholar_id = links.get("scholar_id", "")
    dblp_id = links.get("dblp_id", "")

    if not scholar_id and not dblp_id:
        print(f"  Skipping {name_en}: no scholar_id or dblp_id")
        return []

    print(f"\nFetching: {member['name']} ({name_en})")
    papers: list[dict] = []

    if dblp_id and args.source in ("dblp", "all"):
        print(f"  → DBLP pid={dblp_id}")
        papers = fetch_dblp(dblp_id, args.min_year, args.max_per)
        time.sleep(0.5)

    if not papers and scholar_id and args.source in ("semantic_scholar", "all"):
        print(f"  → Semantic Scholar (searching by name: {name_en})")
        papers = fetch_semantic_scholar(name_en, args.min_year, args.max_per)
        time.sleep(1.0)

    if not papers and scholar_id and args.source == "google_scholar":
        print(f"  → Google Scholar scholar_id={scholar_id}")
        papers = fetch_google_scholar(scholar_id, args.min_year, args.max_per)
        time.sleep(2.0)

    print(f"  Found {len(papers)} papers (year >= {args.min_year})")
    return papers


def main() -> None:
    parser = argparse.ArgumentParser(description="Update papers.bib from member profiles")
    parser.add_argument("--dry-run", action="store_true", help="Print entries, don't write")
    parser.add_argument("--min-year", type=int, default=2020, metavar="YEAR")
    parser.add_argument("--max-per", type=int, default=10, metavar="N",
                        help="Max papers per author (0 = unlimited)")
    parser.add_argument("--source", choices=["semantic_scholar", "dblp", "google_scholar", "all"],
                        default="all")
    args = parser.parse_args()

    members = load_members(MEMBERS_YML)
    existing_keys = load_existing_keys(PAPERS_BIB)
    print(f"Existing BibTeX keys: {len(existing_keys)}")

    new_entries: list[str] = []
    new_keys: set[str] = set()

    for member in members:
        papers = process_member(member, args)
        for pub in papers:
            if not pub.get("title") or not pub.get("year"):
                continue
            # Build a candidate key
            first_last = first_last_name(pub.get("authors", ""))
            title_words = pub["title"].split()
            key_word = title_words[0] if title_words else "paper"
            candidate = make_key(first_last, pub["year"], key_word)
            # Deduplicate
            base = candidate
            suffix = 0
            while candidate in existing_keys or candidate in new_keys:
                suffix += 1
                candidate = f"{base}{chr(96 + suffix)}"  # a, b, c ...

            abbr = venue_abbr(pub.get("venue", ""))
            entry = format_bibtex(pub, candidate, abbr)

            if args.dry_run:
                print(entry)
                print()
            else:
                new_entries.append(entry)
                new_keys.add(candidate)

    if not args.dry_run:
        if new_entries:
            # Add a section comment
            section = f"\n%% ── Auto-updated {__import__('datetime').date.today()} ─────────────────────────────────────────\n"
            with PAPERS_BIB.open("a", encoding="utf-8") as f:
                f.write(section)
            append_entries(PAPERS_BIB, new_entries)
            print(f"\nAdded {len(new_entries)} new entries to {PAPERS_BIB}")
        else:
            print("\nNo new entries to add.")
    else:
        print(f"\n[dry-run] Would add {len(new_entries)} entries.")


if __name__ == "__main__":
    main()
