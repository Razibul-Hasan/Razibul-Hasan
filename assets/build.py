"""Builds every light/dark SVG used by the profile README.

Edit the copy or colors here, then run:  python assets/build.py
(Needs internet once per run to pull icon shapes from simpleicons.org.)
"""

import re
import urllib.request
from html import escape
from pathlib import Path

OUT = Path(__file__).parent

THEMES = {
    "light": {
        "card": "#f6f8fa", "panel": "#ffffff", "line": "#d0d7de",
        "fg": "#1f2328", "muted": "#59636e", "faint": "#818b98",
        "accent": "#3858e9", "ok": "#1a7f37",
        "kw": "#cf222e", "fn": "#8250df", "str": "#0a3069",
    },
    "dark": {
        "card": "#151b23", "panel": "#0d1117", "line": "#3d444d",
        "fg": "#f0f6fc", "muted": "#9198a1", "faint": "#6e7681",
        "accent": "#7b93ff", "ok": "#3fb950",
        "kw": "#ff7b72", "fn": "#d2a8ff", "str": "#a5d6ff",
    },
}

FONTS = (
    ".sans{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif}"
    ".mono{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace}"
)


def svg(w, h, title, body, c, gutter=0, side="right"):
    """A card of w×h. `gutter` adds transparent space on one side so two
    half-width cards can sit edge to edge in the README with a gap between."""
    dx = gutter if side == "left" else 0
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w + gutter}" height="{h}" viewBox="0 0 {w + gutter} {h}" '
        f'role="img" aria-labelledby="t" fill="none">\n'
        f"  <title id=\"t\">{escape(title)}</title>\n"
        f"  <style>{FONTS}</style>\n"
        f'  <g transform="translate({dx} 0)">\n'
        f'  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="{c["card"]}" stroke="{c["line"]}"/>\n'
        f"{body}  </g>\n</svg>\n"
    )


def text(x, y, s, size, fill, cls="sans", weight=None, spacing=None, anchor=None):
    attrs = f'class="{cls}" x="{x}" y="{y}" font-size="{size}" fill="{fill}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    if spacing:
        attrs += f' letter-spacing="{spacing}"'
    if anchor:
        attrs += f' text-anchor="{anchor}"'
    return f"  <text {attrs}>{escape(s)}</text>\n"


def eyebrow(x, y, s, c):
    return text(x, y, s.upper(), 15, c["faint"], "mono", spacing=1.5)


def chips(x, y, items, c):
    out = ""
    for item in items:
        w = round(len(item) * 9.2 + 28)  # sized for the widest common mono font
        out += (
            f'  <rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="31" rx="15.5" '
            f'fill="{c["panel"]}" stroke="{c["line"]}"/>\n'
        )
        out += text(x + w / 2, y + 21, item, 15, c["muted"], "mono", anchor="middle")
        x += w + 8
    return out


def arrow(x, y, c):
    """A small north-east arrow; (x, y) is its top-right corner."""
    return (
        f'  <path d="M{x - 14} {y + 14} L{x} {y} M{x - 10} {y} H{x} V{y + 10}" '
        f'stroke="{c["faint"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n'
    )


# ── Banner ────────────────────────────────────────────────────────────────

CODE = [
    [("<?php", "kw")],
    [("/**", "faint")],
    [(" * ", "faint"), ("Plugin Name:", "accent"), (" Razibul Hasan", "fg")],
    [(" * ", "faint"), ("Description:", "accent"), (" Plugins, themes & stores.", "fg")],
    [(" * ", "faint"), ("Author URI:", "accent"), ("  bestwebexpert.com", "fg")],
    [(" */", "faint")],
    [],
    [("add_action", "fn"), ("( ", "fg"), ("'init'", "str"), (", ", "fg"), ("'ship_it'", "str"), (" );", "fg")],
]


def banner(c):
    b = ""
    # status
    b += f'  <circle cx="71" cy="85" r="11" fill="{c["ok"]}" fill-opacity=".18"/>\n'
    b += f'  <circle cx="71" cy="85" r="5" fill="{c["ok"]}"/>\n'
    b += text(94, 91, "Available for freelance & remote work", 17, c["muted"], "mono")
    # identity
    b += text(60, 182, "Razibul Hasan", 76, c["fg"], weight=700, spacing=-2)
    b += text(64, 234, "WordPress Developer", 32, c["accent"], weight=600, spacing=-.3)
    b += text(64, 286, "Gazipur, Bangladesh  ·  UTC+6", 17, c["muted"], "mono")

    # editor panel
    px, py, pw, ph = 660, 40, 500, 280
    b += f'  <rect x="{px + .5}" y="{py + .5}" width="{pw - 1}" height="{ph - 1}" rx="12" fill="{c["panel"]}" stroke="{c["line"]}"/>\n'
    for i in range(3):
        b += f'  <circle cx="{px + 24 + i * 20}" cy="{py + 22}" r="5.5" fill="{c["line"]}"/>\n'
    b += text(px + pw / 2, py + 27, "razibul-hasan.php", 14, c["faint"], "mono", anchor="middle")
    b += f'  <path d="M{px} {py + 44.5} H{px + pw}" stroke="{c["line"]}"/>\n'
    for i, tokens in enumerate(CODE):
        y = py + 78 + i * 26
        b += text(px + 42, y, str(i + 1), 15, c["faint"], "mono", anchor="end")
        if tokens:
            spans = "".join(f'<tspan fill="{c[k]}">{escape(s)}</tspan>' for s, k in tokens)
            b += f'  <text class="mono" x="{px + 64}" y="{y}" font-size="16" xml:space="preserve">{spans}</text>\n'
    return svg(1200, 360, "Razibul Hasan — WordPress Developer", b, c)


# ── Selected work ─────────────────────────────────────────────────────────

FLOW = [
    ("1", "Package", "session type, package, add-ons"),
    ("2", "Details", "grouped checkout fields"),
    ("3", "Contract", "optional e-signature"),
    ("4", "Payment", "embedded WooCommerce checkout"),
    ("✓", "Booked", "no reloads, no redirects"),
]


def snapbook(c):
    b = eyebrow(48, 76, "Featured · WordPress plugin", c)
    b += arrow(608, 62, c)
    b += text(46, 134, "SnapBook", 46, c["fg"], weight=700, spacing=-1)
    for i, line in enumerate([
        "Booking engine for photography studios.",
        "Packages, add-ons, availability, e-signed",
        "contracts and deposits — all on one page.",
    ]):
        b += text(48, 180 + i * 28, line, 20, c["muted"])
    b += chips(48, 264, ["PHP", "WooCommerce", "JavaScript"], c)

    px, py, pw, ph = 656, 32, 512, 296
    b += f'  <rect x="{px + .5}" y="{py + .5}" width="{pw - 1}" height="{ph - 1}" rx="12" fill="{c["panel"]}" stroke="{c["line"]}"/>\n'
    b += f'  <text class="mono" x="{px + 28}" y="{py + 38}" font-size="15"><tspan fill="{c["accent"]}">[snapbook]</tspan><tspan fill="{c["faint"]}">  one shortcode, the whole flow</tspan></text>\n'
    b += f'  <path d="M{px} {py + 58.5} H{px + pw}" stroke="{c["line"]}"/>\n'
    cx, top, step = px + 42, py + 94, 44
    b += f'  <path d="M{cx} {top} V{top + step * (len(FLOW) - 1)}" stroke="{c["line"]}" stroke-width="2"/>\n'
    for i, (mark, name, note) in enumerate(FLOW):
        y = top + i * step
        last = i == len(FLOW) - 1
        fill, stroke, ink = (c["accent"], c["accent"], c["panel"]) if last else (c["panel"], c["line"], c["muted"])
        b += f'  <circle cx="{cx}" cy="{y}" r="13" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>\n'
        b += text(cx, y + 5, mark, 13, ink, "mono", weight=700 if last else None, anchor="middle")
        b += text(px + 72, y + 6, name, 18, c["fg"], weight=600)
        b += text(px + 182, y + 6, note, 17, c["muted"])
    return svg(1200, 360, "SnapBook — booking engine for photography studios", b, c)


def half_card(tag, title, lines, stack, c, side):
    b = eyebrow(40, 62, tag, c)
    b += arrow(552, 48, c)
    b += text(39, 110, title, 30, c["fg"], weight=700, spacing=-.6)
    for i, line in enumerate(lines):
        b += text(40, 152 + i * 28, line, 19, c["muted"])
    b += chips(40, 232, stack, c)
    return svg(592, 296, title, b, c, gutter=8, side=side)


def boilerplate(c):
    return half_card(
        "Plugin starter",
        "WP React Plugin Boilerplate",
        [
            "React admin dashboard, PSR-style autoloader,",
            "REST namespace, webpack + gulp build.",
            "Rename five identifiers and ship.",
        ],
        ["PHP", "React", "REST API", "webpack"],
        c,
        side="right",
    )


def fitlog(c):
    return half_card(
        "Next.js app",
        "FitLog",
        [
            "Workout library and daily planner built on",
            "the App Router. Plans and saved lifts stay",
            "in the browser between visits.",
        ],
        ["Next.js", "TypeScript", "Tailwind", "daisyUI"],
        c,
        side="left",
    )


# ── Stack ─────────────────────────────────────────────────────────────────

STACK = [
    ("CMS & Commerce", [("wordpress", "WordPress"), ("#woo", "WooCommerce"), ("elementor", "Elementor"), ("shopify", "Shopify")]),
    ("Backend", [("php", "PHP"), ("#database", "MySQL"), ("#braces", "REST API")]),
    ("Frontend", [("javascript", "JavaScript"), ("typescript", "TypeScript"), ("react", "React"), ("nextdotjs", "Next.js")]),
    ("Styling", [("tailwindcss", "Tailwind CSS"), ("sass", "SCSS"), ("html5", "HTML & CSS")]),
    ("Workflow", [("git", "Git"), ("figma", "Figma")]),
]

# Hand-drawn 24×24 glyphs for tools whose official marks are wordmarks
# (unreadable at icon size). {c} is replaced with the icon color.
GLYPHS = {
    "#woo": '<path fill="{c}" d="M4 5h16a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3h-5.5l1.5 3.5-5.5-3.5H4a3 3 0 0 1-3-3V8a3 3 0 0 1 3-3z"/>',
    "#database": (
        '<g stroke="{c}" stroke-width="2" stroke-linecap="round"><ellipse cx="12" cy="5.5" rx="8" ry="3"/>'
        '<path d="M4 5.5v13c0 1.66 3.58 3 8 3s8-1.34 8-3v-13M4 12c0 1.66 3.58 3 8 3s8-1.34 8-3"/></g>'
    ),
    "#braces": (
        '<path stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'd="M8 3.5c-2 0-3 1-3 3v2.5c0 1.5-.8 2.5-2.5 3 1.7.5 2.5 1.5 2.5 3v2.5c0 2 1 3 3 3'
        'M16 3.5c2 0 3 1 3 3v2.5c0 1.5.8 2.5 2.5 3-1.7.5-2.5 1.5-2.5 3v2.5c0 2-1 3-3 3"/>'
    ),
}

_icons = {}


def icon(slug, color):
    if slug in GLYPHS:
        return GLYPHS[slug].replace("{c}", color)
    if slug not in _icons:
        req = urllib.request.Request(f"https://cdn.simpleicons.org/{slug}", headers={"User-Agent": "build.py"})
        raw = urllib.request.urlopen(req).read().decode()
        _icons[slug] = re.search(r'<path d="([^"]+)"', raw).group(1)
    return f'<path fill="{color}" d="{_icons[slug]}"/>'


def stack(c):
    b = ""
    col_w = 221
    b += f'  <path d="M48 100.5 H1152" stroke="{c["line"]}"/>\n'
    for i, (label, items) in enumerate(STACK):
        x = 48 + i * col_w
        b += eyebrow(x, 72, label, c)
        for j, (slug, name) in enumerate(items):
            y = 150 + j * 48
            b += f'  <g transform="translate({x} {y - 20}) scale(1.0833)">{icon(slug, c["muted"])}</g>\n'
            b += text(x + 40, y, name, 19, c["fg"])
    return svg(1200, 330, "Tech stack", b, c)


ASSETS = {
    "banner": banner,
    "work-snapbook": snapbook,
    "work-boilerplate": boilerplate,
    "work-fitlog": fitlog,
    "stack": stack,
}

if __name__ == "__main__":
    for name, build in ASSETS.items():
        for theme, palette in THEMES.items():
            path = OUT / f"{name}-{theme}.svg"
            path.write_text(build(palette), encoding="utf-8", newline="\n")
            print("wrote", path.name)
