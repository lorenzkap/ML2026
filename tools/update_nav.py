"""Regenerate the prev/next navigation in every workshop notebook.

Adds two things to each notebook, both idempotent (re-run any time):

  * a **header line** right under the Colab badge:
        [⬅ Previous] · [🗺️ Course index] · **Notebook 03 of the course** · [Next ➡]
  * a **footer cell** at the very end — the "next button": a big Colab badge that
    opens the next notebook, plus small previous/index links.

The order and the notebook titles are read from the course-index table in
00_START_HERE.ipynb, so that table stays the single source of truth: add a row
there, re-run this script, and the navigation follows.

    python tools/update_nav.py            # rewrite the notebooks
    python tools/update_nav.py --check    # exit 1 if anything is out of date
"""
import io
import json
import os
import re
import sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_NB = "00_START_HERE.ipynb"
REPO_URL = "https://colab.research.google.com/github/lorenzkap/ML2026/blob/main"
GITHUB_URL = "https://github.com/lorenzkap/ML2026"
COLAB_BADGE = "https://colab.research.google.com/assets/colab-badge.svg"

HEADER_MARK = "<!-- nav-header -->"
FOOTER_MARK = "<!-- nav-footer -->"
# the hand-written header line this script replaces, from before nav existed
LEGACY_HEADER = re.compile(r"^\[⬅ Back to the course index\]\(.*?\) · \*\*Notebook .*$",
                           re.MULTILINE)


def colab(fname):
    return f"{REPO_URL}/{fname}"


def raw(fname):
    with io.open(os.path.join(WS, fname), encoding="utf-8", newline="") as fh:
        return fh.read()


def read(fname):
    return json.loads(raw(fname))


def md_cell(text, cell_id, like=None):
    """A markdown cell in nbformat's own on-disk shape (keep the id: nbformat 4.5
    requires one, and a stable id keeps re-executions from churning the diff)."""
    lines = text.split("\n")
    source = [ln + "\n" for ln in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    cell = {"cell_type": "markdown", "id": cell_id,
            "metadata": (like or {}).get("metadata", {}), "source": source}
    return cell


def course_order():
    """[(number, filename, title), ...] parsed from the index table in 00_START_HERE."""
    row = re.compile(r"^\|\s*(\d{2})\s*\|\s*\[([^\]]+)\]\([^)]*/([0-9A-Za-z_]+\.ipynb)\)")
    chapters = []
    for cell in read(INDEX_NB)["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        for line in "".join(cell["source"]).split("\n"):
            m = row.match(line.strip())
            if m:
                num, title, fname = m.group(1), m.group(2).strip(), m.group(3)
                chapters.append((num, fname, title))
    if not chapters:
        sys.exit("❌ could not parse the course-index table in " + INDEX_NB)
    return [("00", INDEX_NB, "Start here")] + chapters


def plain(title):
    """Title without a leading emoji — nicer inside a sentence."""
    return re.sub(r"^[^\w(]+\s*", "", title).strip()


def index_link(i):
    """On notebook 00 the index *is* this notebook — point at the repo instead."""
    if i == 0:
        return f"[📁 The course on GitHub]({GITHUB_URL})"
    return f"[🗺️ Course index]({colab(INDEX_NB)})"


def header_line(i, order):
    num, _, _ = order[i]
    bits = []
    if i > 0:
        bits.append(f"[⬅ Previous]({colab(order[i - 1][1])})")
    bits.append(index_link(i))
    bits.append(f"**Notebook {num} of the course**")
    if i + 1 < len(order):
        nxt = order[i + 1]
        bits.append(f"[Next: {nxt[0]} — {plain(nxt[2])} ➡]({colab(nxt[1])})")
    return HEADER_MARK + "\n" + " · ".join(bits)


def footer_text(i, order):
    prev_link = f"[⬅ Back to Notebook {order[i - 1][0]}]({colab(order[i - 1][1])})" if i > 0 else None
    repo_link = f"[📁 The course on GitHub]({GITHUB_URL})" if i > 0 else None

    if i + 1 < len(order):
        num, fname, title = order[i + 1]
        body = (
            f"### ➡️ Next up — Notebook {num}: {plain(title)}\n"
            f"\n"
            f'<a href="{colab(fname)}" target="_parent">'
            f'<img src="{COLAB_BADGE}" alt="Open Notebook {num} in Colab" height="32"/>'
            f"</a>\n"
            f"\n"
            f"👉 **[Continue to Notebook {num} — {plain(title)}]({colab(fname)})**"
        )
    else:
        body = (
            "### 🎓 That's the end of the course\n"
            "\n"
            f'<a href="{colab(INDEX_NB)}" target="_parent">'
            f'<img src="{COLAB_BADGE}" alt="Back to the course index" height="32"/>'
            f"</a>\n"
            "\n"
            f"👉 **[Back to the course index]({colab(INDEX_NB)})** — every notebook stays open to you."
        )

    tail = " · ".join(x for x in (prev_link, index_link(i), repo_link) if x)
    return f"{FOOTER_MARK}\n---\n\n{body}\n\n{tail}"


def navigated(fname, i, order):
    """Return the notebook with its navigation regenerated (does not write)."""
    nb = read(fname)
    cells = nb["cells"]

    # ---- header -------------------------------------------------------------
    want = header_line(i, order)
    first = "".join(cells[0]["source"])
    if HEADER_MARK in first:
        head, _, _ = first.partition(HEADER_MARK)
        new_first = head.rstrip("\n") + "\n\n" + want + "\n"
    elif LEGACY_HEADER.search(first):
        new_first = LEGACY_HEADER.sub(want, first, count=1)
    else:                                   # no nav yet: put it after the Colab badge
        new_first = first.rstrip("\n") + "\n\n" + want + "\n"
    if new_first != first:
        cells[0] = md_cell(new_first, cells[0].get("id", "nav-header"), like=cells[0])

    # ---- footer -------------------------------------------------------------
    cells[:] = [c for c in cells
                if not (c["cell_type"] == "markdown" and FOOTER_MARK in "".join(c["source"]))]
    while cells and not "".join(cells[-1]["source"]).strip():
        cells.pop()
    cells.append(md_cell(footer_text(i, order), "nav-footer"))
    return nb


def main():
    check_only = "--check" in sys.argv
    order = course_order()
    stale = []
    for i, (num, fname, title) in enumerate(order):
        before = raw(fname)
        crlf = "\r\n" in before
        text = json.dumps(navigated(fname, i, order), ensure_ascii=False, indent=1) + "\n"
        if crlf:
            text = text.replace("\n", "\r\n")
        changed = text != before
        if changed:
            stale.append(fname)
            if not check_only:
                with io.open(os.path.join(WS, fname), "w", encoding="utf-8", newline="") as fh:
                    fh.write(text)
        where = f"next: {order[i + 1][1]}" if i + 1 < len(order) else "end of course"
        mark = ("❌" if check_only else "✏️") if changed else "✅"
        print(f"  {mark} {num} {fname} → {where}")
    if check_only and stale:
        sys.exit("\n❌ navigation out of date in: " + ", ".join(stale))
    print("\n✅ navigation up to date in %d notebooks" % len(order))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
