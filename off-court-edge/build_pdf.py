#!/usr/bin/env python3
"""
Converts The-Off-Court-Edge.md into a polished, illustrated, print-ready HTML file.
Open the resulting HTML in a browser and choose Print -> Save as PDF.
No external dependencies, no network, no image files required: all diagrams are
generated as inline SVG so they render and print crisply anywhere.

Diagram placeholders in the markdown look like:   [[DIAGRAM:name|Caption text]]
"""
import html
import re

SRC = "The-Off-Court-Edge.md"
OUT = "The-Off-Court-Edge.html"

# ---- palette ----
DARK = "#0b3d2e"
GREEN = "#16a34a"
LIGHT = "#dcfce7"
MID = "#86efac"
GREY = "#64748b"
WARN = "#ef4444"
AIR = "#0ea5e9"

CSS = """
@page { size: A4; margin: 16mm 16mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #1f2933; line-height: 1.62; max-width: 840px; margin: 0 auto;
  padding: 24px; font-size: 15.5px; background: #fff;
}
h1 { font-size: 2.3rem; color: #0b3d2e; margin: 0 0 4px; line-height: 1.12; }
h2 {
  font-size: 1.45rem; color: #0b3d2e; margin: 2.4rem 0 1rem; padding: 10px 0 10px 16px;
  border-left: 8px solid #16a34a; background: linear-gradient(90deg,#f0fdf4,#ffffff);
  page-break-before: always; page-break-after: avoid; border-radius: 0 6px 6px 0;
}
h2:first-of-type { page-break-before: avoid; }
h3 { font-size: 1.12rem; color: #15543f; margin-top: 1.5rem; page-break-after: avoid; }
p { margin: 0.55rem 0; }
em { color: #475569; }
strong { color: #0b3d2e; }
ul, ol { margin: 0.5rem 0 0.9rem; padding-left: 1.3rem; }
li { margin: 0.28rem 0; }
li::marker { color: #16a34a; font-weight: 700; }
hr { border: none; border-top: 1px solid #d6dee2; margin: 1.6rem 0; }
blockquote {
  margin: 1.1rem 0; padding: 0.7rem 1rem 0.7rem 2.4rem; background: #ecfdf5;
  border-left: 4px solid #16a34a; color: #14532d; border-radius: 6px; position: relative;
  page-break-inside: avoid;
}
blockquote::before {
  content: "i"; position: absolute; left: 12px; top: 50%; transform: translateY(-50%);
  width: 18px; height: 18px; background: #16a34a; color: #fff; border-radius: 50%;
  font-style: italic; font-weight: 700; font-size: 12px; text-align: center; line-height: 18px;
}
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.9rem;
        page-break-inside: avoid; box-shadow: 0 1px 3px rgba(0,0,0,.07); border-radius: 6px; overflow: hidden; }
th { background: #0b3d2e; color: #fff; text-align: left; padding: 9px 11px; font-size: 0.86rem; }
td { border: 1px solid #e2e8f0; padding: 8px 11px; vertical-align: top; }
tr:nth-child(even) td { background: #f6faf8; }

/* Figures / diagrams */
figure { margin: 1.4rem auto; max-width: 660px; page-break-inside: avoid; text-align: center; }
figure svg { width: 100%; height: auto; display: block;
             border: 1px solid #e2e8f0; border-radius: 10px; background: #fff; padding: 8px; }
figcaption { font-size: 0.82rem; color: #64748b; margin-top: 8px; font-style: italic; line-height: 1.4; }

/* Cover */
.cover { page-break-after: always; min-height: 250mm; display: flex; flex-direction: column;
         align-items: center; justify-content: center; text-align: center; padding: 30px 20px;
         background: radial-gradient(120% 90% at 50% 0%, #0b3d2e 0%, #0f5132 45%, #052e1c 100%);
         color: #fff; border-radius: 14px; }
.cover-icon { width: 96px; height: 96px; margin-bottom: 18px; }
.kicker { letter-spacing: 4px; font-size: 0.8rem; color: #86efac; font-weight: 600; margin-bottom: 10px; }
.cover-title { font-size: 3.4rem; color: #fff; line-height: 1.05; margin: 0; text-shadow: 0 2px 12px rgba(0,0,0,.3); }
.cover-sub { font-size: 1.25rem; color: #d1fae5; font-weight: 600; margin: 14px 0 6px; max-width: 600px; }
.cover-tag { color: #a7f3d0; font-style: italic; max-width: 560px; margin: 8px auto 24px; font-size: 0.98rem; }
.cover-rule { width: 80px; height: 4px; background: #16a34a; border-radius: 2px; margin: 6px 0 24px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; max-width: 620px; }
.chips span { background: rgba(255,255,255,.12); border: 1px solid rgba(134,239,172,.5);
              color: #ecfdf5; padding: 6px 13px; border-radius: 999px; font-size: 0.82rem; font-weight: 600; }

@media print { body { padding: 0; } a { color: inherit; text-decoration: none; } }
"""

# ----------------------------------------------------------------------------
# Inline SVG diagram generators
# ----------------------------------------------------------------------------

def _txt(x, y, s, size=12, fill="#1f2933", weight="400", anchor="middle", style=""):
    return (f'<text x="{x}" y="{y}" font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}" {style}>{html.escape(s)}</text>')


def svg_workrest():
    p = [f'<svg viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img">']
    p.append(_txt(360, 30, "Work : Rest \u2248 1 : 2 \u2013 1 : 3", 17, DARK, "700"))
    # axis
    p.append(f'<line x1="30" y1="155" x2="690" y2="155" stroke="#94a3b8" stroke-width="2"/>')
    p.append(f'<polygon points="690,150 702,155 690,160" fill="#94a3b8"/>')
    p.append(_txt(672, 178, "time \u2192", 11, GREY))
    x = 40
    rally_w, rest_w = 70, 140
    for i in range(3):
        p.append(f'<rect x="{x}" y="70" width="{rally_w}" height="65" rx="5" fill="{GREEN}"/>')
        p.append(_txt(x + rally_w/2, 98, "RALLY", 12, "#fff", "700"))
        p.append(_txt(x + rally_w/2, 116, "~7s max", 10, "#eafff2"))
        x += rally_w
        p.append(f'<rect x="{x}" y="70" width="{rest_w}" height="65" rx="5" fill="{LIGHT}" stroke="{MID}"/>')
        p.append(_txt(x + rest_w/2, 98, "RECOVER", 12, DARK, "700"))
        p.append(_txt(x + rest_w/2, 116, "~15s", 10, "#15803d"))
        x += rest_w
    p.append('</svg>')
    return "".join(p)


def svg_kineticchain():
    segs = [("Ground", "push off"), ("Legs", "drive up"), ("Hips", "rotate"),
            ("Trunk", "rotate+flex"), ("Shoulder", "internal rot."),
            ("Forearm", "PRONATION"), ("Fingers", "snap @ contact")]
    p = [f'<svg viewBox="0 0 740 250" xmlns="http://www.w3.org/2000/svg" role="img">']
    p.append('<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">'
             f'<path d="M0,0 L7,3 L0,6 Z" fill="{GREEN}"/></marker></defs>')
    # speed arc
    p.append(f'<path d="M40,100 C 260,58 500,48 700,44" fill="none" stroke="{GREEN}" '
             f'stroke-width="2.5" stroke-dasharray="6 5" marker-end="url(#ah)"/>')
    p.append(_txt(360, 34, "racket-head speed builds \u2192", 12, GREEN, "600"))
    bx, bw, gap, step = 28, 92, 6, 98
    for i, (name, sub) in enumerate(segs):
        x = bx + i * step
        op = 0.30 + (i / 6) * 0.70
        tcol = "#ffffff" if op > 0.55 else DARK
        p.append(f'<rect x="{x}" y="112" width="{bw}" height="54" rx="8" fill="{GREEN}" fill-opacity="{op:.2f}" stroke="{DARK}" stroke-opacity="0.35"/>')
        bold = "700" if sub == "PRONATION" else "600"
        p.append(_txt(x + bw/2, 144, name, 12.5, tcol, bold))
        scol = GREEN if sub == "PRONATION" else GREY
        p.append(_txt(x + bw/2, 186, sub, 9.5, scol, "700" if sub == "PRONATION" else "400"))
        if i < len(segs) - 1:
            ax = x + bw + 1
            p.append(f'<polygon points="{ax},132 {ax+6},138 {ax},144" fill="{DARK}" fill-opacity="0.4"/>')
    p.append(_txt(370, 222, "Power passes UP the chain \u2014 the wrist mainly stabilises; the forearm delivers the snap.",
                  11, GREY, "400", "middle", 'font-style="italic"'))
    p.append('</svg>')
    return "".join(p)


def svg_court6():
    p = ['<svg viewBox="0 0 360 470" xmlns="http://www.w3.org/2000/svg" role="img">']
    p.append('<defs><marker id="ca" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">'
             f'<path d="M0,0 L7,3 L0,6 Z" fill="{GREEN}"/></marker></defs>')
    # court
    p.append(f'<rect x="50" y="45" width="260" height="380" fill="#f0fdf4" stroke="{DARK}" stroke-width="2"/>')
    p.append(f'<line x1="180" y1="45" x2="180" y2="425" stroke="{MID}" stroke-width="1.5"/>')
    p.append(f'<line x1="50" y1="45" x2="310" y2="45" stroke="{DARK}" stroke-width="3" stroke-dasharray="7 5"/>')
    p.append(_txt(180, 33, "NET", 12, DARK, "700"))
    base = (180, 250)
    corners = [(95, 100, "Net"), (265, 100, "Net"),
               (72, 250, "Mid"), (288, 250, "Mid"),
               (95, 388, "Rear"), (265, 388, "Rear")]
    for cx, cy, lbl in corners:
        p.append(f'<line x1="{base[0]}" y1="{base[1]}" x2="{cx}" y2="{cy}" stroke="{GREEN}" '
                 f'stroke-width="2" stroke-dasharray="4 3" marker-end="url(#ca)"/>')
    for cx, cy, lbl in corners:
        p.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{GREEN}"/>')
        ly = cy - 16 if cy < 200 else (cy + 26 if cy > 300 else cy - 16)
        p.append(_txt(cx, ly, lbl, 11, DARK, "600"))
    p.append(f'<circle cx="{base[0]}" cy="{base[1]}" r="11" fill="{DARK}" stroke="#fff" stroke-width="2"/>')
    p.append(_txt(base[0] + 36, base[1] + 4, "BASE", 11, DARK, "700"))
    p.append('</svg>')
    return "".join(p)


def svg_injurymap():
    p = ['<svg viewBox="0 0 470 470" xmlns="http://www.w3.org/2000/svg" role="img">']
    # body (light green thick strokes)
    g = (f'stroke="{MID}" stroke-linecap="round" fill="none"')
    p.append(f'<circle cx="210" cy="50" r="22" fill="{MID}"/>')                 # head
    p.append(f'<line x1="210" y1="82" x2="210" y2="228" {g} stroke-width="48"/>')  # torso/hips
    p.append(f'<line x1="170" y1="106" x2="250" y2="106" {g} stroke-width="20"/>') # shoulders
    p.append(f'<line x1="172" y1="110" x2="150" y2="205" {g} stroke-width="17"/>') # L arm
    p.append(f'<line x1="248" y1="110" x2="288" y2="200" {g} stroke-width="17"/>') # R arm (racket)
    p.append(f'<line x1="196" y1="225" x2="190" y2="338" {g} stroke-width="23"/>') # L thigh
    p.append(f'<line x1="190" y1="338" x2="184" y2="430" {g} stroke-width="19"/>') # L shin
    p.append(f'<line x1="224" y1="225" x2="230" y2="338" {g} stroke-width="23"/>') # R thigh
    p.append(f'<line x1="230" y1="338" x2="236" y2="430" {g} stroke-width="19"/>') # R shin

    def hot(dot, lab, lx, anchor):
        s = []
        s.append(f'<line x1="{dot[0]}" y1="{dot[1]}" x2="{lx}" y2="{dot[1]}" stroke="{WARN}" stroke-width="1.2" stroke-dasharray="3 2"/>')
        s.append(f'<circle cx="{dot[0]}" cy="{dot[1]}" r="7" fill="{WARN}" stroke="#fff" stroke-width="2"/>')
        tx = lx + 6 if anchor == "start" else lx - 6
        s.append(_txt(tx, dot[1] + 4, lab, 12, "#b91c1c", "600", anchor))
        return "".join(s)

    p.append(hot((250, 108), "Smash shoulder (cuff)", 320, "start"))
    p.append(hot((286, 165), "Elbow & forearm", 320, "start"))
    p.append(hot((232, 380), "Achilles & calf", 320, "start"))
    p.append(hot((210, 165), "Lower back", 150, "end"))
    p.append(hot((190, 338), "Patellar tendon (knee)", 150, "end"))
    p.append(hot((184, 425), "Ankle (sprains)", 150, "end"))
    p.append('</svg>')
    return "".join(p)


def svg_drift():
    p = ['<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg" role="img">']
    p.append('<defs>'
             f'<marker id="da" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{AIR}"/></marker>'
             f'<marker id="dg" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{GREEN}"/></marker>'
             f'<marker id="do" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#ea580c"/></marker>'
             '</defs>')
    p.append(f'<rect x="40" y="80" width="640" height="170" fill="#f0fdf4" stroke="{DARK}" stroke-width="2"/>')
    p.append(f'<line x1="360" y1="80" x2="360" y2="250" stroke="{MID}" stroke-width="2" stroke-dasharray="7 5"/>')
    p.append(_txt(360, 72, "NET", 11, DARK, "700"))
    p.append(_txt(90, 72, "END A", 11, GREY, "600"))
    p.append(_txt(630, 72, "END B", 11, GREY, "600"))
    # air drift arrows ->
    for ay in (100, 240):
        p.append(f'<line x1="70" y1="{ay}" x2="300" y2="{ay}" stroke="{AIR}" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#da)" opacity="0.85"/>')
        p.append(f'<line x1="420" y1="{ay}" x2="650" y2="{ay}" stroke="{AIR}" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#da)" opacity="0.85"/>')
    p.append(_txt(180, 290, "air drifts this way \u2192", 11, AIR, "600"))
    # trajectories from net center
    p.append(f'<path d="M360,150 Q520,60 650,205" fill="none" stroke="{GREEN}" stroke-width="3" marker-end="url(#dg)"/>')
    p.append(_txt(560, 240, "WITH drift: carries DEEP", 11.5, "#15803d", "700"))
    p.append(f'<path d="M360,150 Q270,80 175,205" fill="none" stroke="#ea580c" stroke-width="3" marker-end="url(#do)"/>')
    p.append(_txt(170, 240, "INTO drift: drops SHORT", 11.5, "#c2410c", "700"))
    p.append(f'<circle cx="360" cy="150" r="5" fill="{DARK}"/>')
    p.append(_txt(360, 135, "same swing", 10, GREY, "400", "middle", 'font-style="italic"'))
    p.append('</svg>')
    return "".join(p)


def shuttle_icon():
    return (f'<svg class="cover-icon" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
            f'<polygon points="38,66 62,66 80,16 20,16" fill="#ffffff" fill-opacity="0.92" stroke="#86efac" stroke-width="2"/>'
            f'<line x1="50" y1="66" x2="50" y2="16" stroke="#86efac" stroke-width="1.5"/>'
            f'<line x1="44" y1="66" x2="34" y2="16" stroke="#86efac" stroke-width="1.5"/>'
            f'<line x1="56" y1="66" x2="66" y2="16" stroke="#86efac" stroke-width="1.5"/>'
            f'<line x1="30" y1="40" x2="70" y2="40" stroke="#86efac" stroke-width="1.2"/>'
            f'<ellipse cx="50" cy="74" rx="15" ry="13" fill="#16a34a"/>'
            f'<ellipse cx="50" cy="71" rx="15" ry="9" fill="#22c55e"/>'
            f'</svg>')


DIAGRAMS = {
    "workrest": svg_workrest,
    "kineticchain": svg_kineticchain,
    "court6": svg_court6,
    "injurymap": svg_injurymap,
    "drift": svg_drift,
}

# ----------------------------------------------------------------------------
# Markdown -> HTML
# ----------------------------------------------------------------------------

def inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def convert(md):
    lines = md.split("\n")
    out, i, n, list_stack = [], 0, len(md.split("\n")), None

    def close_list():
        nonlocal list_stack
        if list_stack:
            out.append(f"</{list_stack}>")
            list_stack = None

    while i < n:
        line = lines[i]
        stripped = line.strip()

        m_diag = re.match(r"^\[\[DIAGRAM:(\w+)(?:\|(.*))?\]\]$", stripped)
        if m_diag:
            close_list()
            name, cap = m_diag.group(1), m_diag.group(2)
            if name in DIAGRAMS:
                fig = f"<figure>{DIAGRAMS[name]()}"
                if cap:
                    fig += f"<figcaption>{inline(cap)}</figcaption>"
                fig += "</figure>"
                out.append(fig)
            i += 1
            continue

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
            close_list(); i += 1; continue
        if stripped == "---":
            close_list(); out.append("<hr>"); i += 1; continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            close_list()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1; continue

        if stripped.startswith(">"):
            close_list()
            out.append(f"<blockquote>{inline(stripped.lstrip('>').strip())}</blockquote>")
            i += 1; continue

        om = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if om:
            if list_stack != "ol":
                close_list(); out.append("<ol>"); list_stack = "ol"
            out.append(f"<li>{inline(om.group(2))}</li>"); i += 1; continue

        um = re.match(r"^[-*]\s+(.*)$", stripped)
        if um:
            if list_stack != "ul":
                close_list(); out.append("<ul>"); list_stack = "ul"
            out.append(f"<li>{inline(um.group(1))}</li>"); i += 1; continue

        close_list()
        out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_list()
    return "\n".join(out)


def build_cover(md):
    title = subtitle = tagline = ""
    for line in md.split("\n")[:8]:
        s = line.strip()
        if s.startswith("# ") and not title:
            title = s[2:]
        elif s.startswith("### ") and not subtitle:
            subtitle = s[4:]
        elif s.startswith("*") and s.endswith("*") and not tagline and len(s) > 4:
            tagline = s.strip("*")
    chips = ["Power & Smash", "Braking Strength", "Tendon Health", "Footwork",
             "Interval Conditioning", "Tournament Fuelling", "Recovery", "Tactics & Drift"]
    chip_html = "".join(f"<span>{html.escape(c)}</span>" for c in chips)
    return (f'<div class="cover">{shuttle_icon()}'
            f'<div class="kicker">BADMINTON PERFORMANCE GUIDE</div>'
            f'<h1 class="cover-title">{html.escape(title)}</h1>'
            f'<div class="cover-rule"></div>'
            f'<div class="cover-sub">{html.escape(subtitle)}</div>'
            f'<p class="cover-tag">{html.escape(tagline)}</p>'
            f'<div class="chips">{chip_html}</div></div>')


def main():
    with open(SRC, encoding="utf-8") as f:
        md = f.read()
    cover = build_cover(md)
    # drop the leading title block (up to and including the first '---') from the body
    lines = md.split("\n")
    cut = next((idx for idx, l in enumerate(lines) if l.strip() == "---"), 0)
    body_md = "\n".join(lines[cut + 1:])
    body = convert(body_md)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Off-Court Edge</title>
<style>{CSS}</style>
</head>
<body>
{cover}
{body}
</body>
</html>"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Wrote {OUT} ({len(doc):,} bytes)")


if __name__ == "__main__":
    main()
