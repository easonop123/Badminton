#!/usr/bin/env python3
"""
Builds preview.html: a set of clean "page" cards that show off the guide's
diagrams and structure, for use as Ko-fi preview images. Screenshot each card.
Reuses the diagram SVGs from build_pdf.py so they stay in sync.
"""
import build_pdf as b

OUT = "preview.html"

CARDS = [
    ("Part 2 · Smash Power", "Where your smash power actually comes from",
     "Power isn't in the wrist. It's a chain that builds from the ground up and "
     "accelerates into the shuttle — finishing with forearm <b>pronation</b>, not a flick.",
     b.svg_kineticchain()),
    ("Part 1 · Injury", "Where badminton players actually break down",
     "Almost none of these are protected by a generic gym program. The guide targets each "
     "one with specific eccentric and isometric work.",
     b.svg_injurymap()),
    ("Part 4 · Footwork", "Train the six court corners",
     "Move explosively from base to each corner and recover — with a real split-step — "
     "instead of running pre-set ladder patterns that don't transfer.",
     b.svg_court6()),
    ("Part 8 · Tactics", "Reading the hall drift",
     "The same swing carries deep with the drift behind you but drops short into it. "
     "Spotting this in the knock-up is free points most club players miss.",
     b.svg_drift()),
]

PLAN_TABLE = """
<table>
<thead><tr><th>Day</th><th>On-Court</th><th>Off-Court</th><th>Focus</th></tr></thead>
<tbody>
<tr><td><b>Mon</b></td><td>Skills/drills</td><td>Mobility 10 min</td><td>Technical, fresh legs</td></tr>
<tr><td><b>Tue</b></td><td>&mdash;</td><td>Strength S1 + power throws</td><td>Power &amp; posterior chain</td></tr>
<tr><td><b>Wed</b></td><td>Match practice</td><td>Reactive ghosting</td><td>Decision speed</td></tr>
<tr><td><b>Thu</b></td><td>&mdash;</td><td>Strength S2 + tendon iso</td><td>Single-leg &amp; shoulder</td></tr>
<tr><td><b>Fri</b></td><td>Light hitting</td><td>Mobility + visualisation</td><td>Prime for weekend</td></tr>
<tr><td><b>Sat</b></td><td>Matches</td><td>&mdash;</td><td>Compete</td></tr>
<tr><td><b>Sun</b></td><td>&mdash;</td><td>Easy aerobic + sleep</td><td>Genuine recovery</td></tr>
</tbody></table>
"""

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #cbd5e1; font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
       padding: 30px; display: flex; flex-direction: column; align-items: center; gap: 34px; }
.page { background: #fff; width: 720px; max-width: 96vw; border-radius: 12px;
        box-shadow: 0 12px 40px rgba(0,0,0,.25); padding: 34px 38px 40px; }
.ph { font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; color: #16a34a;
      font-weight: 700; margin-bottom: 8px; }
.page h2 { font-size: 1.7rem; color: #0b3d2e; line-height: 1.12; margin-bottom: 10px; }
.page p { color: #334155; font-size: 1.02rem; line-height: 1.55; margin-bottom: 18px; }
.page b { color: #0b3d2e; }
.fig svg { width: 100%; height: auto; border: 1px solid #e2e8f0; border-radius: 10px; padding: 8px; background:#fff; }
.brand { text-align: right; margin-top: 16px; font-size: 0.78rem; color: #94a3b8; font-style: italic; }
table { border-collapse: collapse; width: 100%; font-size: 0.92rem; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,.08); }
th { background: #0b3d2e; color: #fff; text-align: left; padding: 9px 11px; }
td { border: 1px solid #e2e8f0; padding: 8px 11px; }
tr:nth-child(even) td { background: #f6faf8; }
.hint { color:#475569; font-size:0.9rem; max-width:720px; text-align:center; }
"""

def card(ph, title, desc, svg):
    return (f'<div class="page"><div class="ph">{ph}</div><h2>{title}</h2>'
            f'<p>{desc}</p><div class="fig">{svg}</div>'
            f'<div class="brand">The Off-Court Edge &mdash; by Ben</div></div>')

def main():
    parts = ['<div class="hint">Screenshot each card below (crop to the white page) '
             'to use as Ko-fi preview images.</div>']
    for ph, title, desc, svg in CARDS:
        parts.append(card(ph, title, desc, svg))
    # planning card
    parts.append(f'<div class="page"><div class="ph">Part 10 · Planning</div>'
                 f'<h2>A periodised weekly plan</h2>'
                 f'<p>The guide ends with a ready-to-use weekly structure and badminton-specific '
                 f'fitness tests &mdash; so you train with a plan, not at random.</p>{PLAN_TABLE}'
                 f'<div class="brand">The Off-Court Edge &mdash; by Ben</div></div>')
    doc = (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width, initial-scale=1">'
           f'<title>The Off-Court Edge — Previews</title><style>{CSS}</style></head>'
           f'<body>{"".join(parts)}</body></html>')
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Wrote {OUT} ({len(doc):,} bytes) with {len(CARDS)+1} preview cards")

if __name__ == "__main__":
    main()
