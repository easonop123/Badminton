#!/usr/bin/env python3
"""
Converts The-Off-Court-Edge.md into a polished, print-ready HTML file.
Open the resulting HTML in a browser and choose Print -> Save as PDF.
No external dependencies required.
"""
import html
import re
import sys

SRC = "The-Off-Court-Edge.md"
OUT = "The-Off-Court-Edge.html"

CSS = """
@page { size: A4; margin: 20mm 18mm; }
* { box-sizing: border-box; }
body {
  font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #1f2933; line-height: 1.6; max-width: 820px; margin: 0 auto;
  padding: 24px; font-size: 16px;
}
h1 { font-size: 2.4rem; color: #0b3d2e; margin: 0 0 4px; line-height: 1.15; }
h2 { font-size: 1.5rem; color: #0b3d2e; margin-top: 2.2rem; padding-bottom: 6px;
     border-bottom: 3px solid #16a34a; page-break-after: avoid; }
h3 { font-size: 1.15rem; color: #15543f; margin-top: 1.4rem; page-break-after: avoid; }
p { margin: 0.6rem 0; }
em { color: #475569; }
strong { color: #0b3d2e; }
ul, ol { margin: 0.5rem 0 0.9rem; padding-left: 1.4rem; }
li { margin: 0.25rem 0; }
hr { border: none; border-top: 1px solid #d6dee2; margin: 1.8rem 0; }
blockquote {
  margin: 1rem 0; padding: 0.6rem 1rem; background: #f0fdf4;
  border-left: 4px solid #16a34a; color: #14532d; border-radius: 4px;
}
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.93rem;
        page-break-inside: avoid; }
th { background: #0b3d2e; color: #fff; text-align: left; padding: 8px 10px; }
td { border: 1px solid #d6dee2; padding: 7px 10px; vertical-align: top; }
tr:nth-child(even) td { background: #f6faf8; }
.subtitle { font-size: 1.15rem; color: #15543f; font-weight: 600; margin-top: 0; }
.tagline { color: #64748b; font-style: italic; }
@media print { body { padding: 0; } a { color: inherit; text-decoration: none; } }
"""


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def split_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def convert(md):
    lines = md.split("\n")
    out = []
    i = 0
    n = len(lines)
    list_stack = None  # 'ul' or 'ol'

    def close_list():
        nonlocal list_stack
        if list_stack:
            out.append(f"</{list_stack}>")
            list_stack = None

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Table detection: a line with | followed by a separator line
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i + 1]) and "-" in lines[i + 1]:
            close_list()
            header = split_row(line)
            out.append("<table><thead><tr>")
            out.extend(f"<th>{inline(c)}</th>" for c in header)
            out.append("</tr></thead><tbody>")
            i += 2
            while i < n and "|" in lines[i] and lines[i].strip():
                row = split_row(lines[i])
                out.append("<tr>")
                out.extend(f"<td>{inline(c)}</td>" for c in row)
                out.append("</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        if not stripped:
            close_list()
            i += 1
            continue

        if stripped == "---":
            close_list()
            out.append("<hr>")
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            close_list()
            level = len(m.group(1))
            content = inline(m.group(2))
            cls = ""
            if level == 3 and i > 0 and lines[max(0, i - 2)].startswith("# "):
                pass
            out.append(f"<h{level}>{content}</h{level}>")
            i += 1
            continue

        if stripped.startswith(">"):
            close_list()
            quote = inline(stripped.lstrip(">").strip())
            out.append(f"<blockquote>{quote}</blockquote>")
            i += 1
            continue

        om = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if om:
            if list_stack != "ol":
                close_list()
                out.append("<ol>")
                list_stack = "ol"
            out.append(f"<li>{inline(om.group(2))}</li>")
            i += 1
            continue

        um = re.match(r"^[-*]\s+(.*)$", stripped)
        if um:
            if list_stack != "ul":
                close_list()
                out.append("<ul>")
                list_stack = "ul"
            out.append(f"<li>{inline(um.group(1))}</li>")
            i += 1
            continue

        close_list()
        # Subtitle / tagline styling for the top of the doc
        if stripped.startswith("*") and stripped.endswith("*") and "·" in stripped:
            out.append(f'<p class="tagline">{inline(stripped.strip("*"))}</p>')
        else:
            out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_list()
    return "\n".join(out)


def main():
    with open(SRC, encoding="utf-8") as f:
        md = f.read()
    body = convert(md)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Off-Court Edge</title>
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Wrote {OUT} ({len(doc):,} bytes)")


if __name__ == "__main__":
    main()
