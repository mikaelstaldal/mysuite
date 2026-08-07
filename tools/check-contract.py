#!/usr/bin/env python3
"""Cross-repo check for the MySuite sidebar-footer contract.

Reads the three sibling apps' stylesheets and fails if they disagree on a value
that spec/sidebar-footer.md pins. It never renders anything: it compares source
text and resolved custom properties, which is what lets it catch the one class of
breakage no browser test can see.

    ../mycal    ../mymail    ../mynotes

See spec/sidebar-footer.md. What this cannot check is printed on every run —
read it, because a green run means less than it looks like it does.

Python 3, standard library only: no package manager, no network, no build step.
The app repos have a standing rule against npm/npx and this must not become a
dependency they would have to adopt.

Usage:  tools/check-contract.py [--repos DIR] [--quiet]
Exit:   0 all pinned values agree · 1 a pinned value disagrees · 2 cannot check
"""

from __future__ import annotations

import argparse
import os
import re
import sys

SPEC = "spec/sidebar-footer.md"

# ─── Which rules hold the contract in each app ──────────────────────────────
#
# Selector strings are matched exactly, after collapsing whitespace. They differ
# per app by design (§5.2: names are local, values are shared), so this table is
# also the record of where the contract lives in each repo.

APPS = {
    "mycal": {
        "css": ["web/static/app.css"],
        "tokens": ["web/static/app.css"],
        "button": ".sidebar-footer-btn",
        "hover": ".sidebar-footer-btn:hover",
        "focus": ".sidebar-footer-btn:focus-visible",
        "row": ".sidebar-footer-actions",
        "footer": ".sidebar-footer",
        "panel": ".left-sidebar",
    },
    "mymail": {
        "css": ["web/static/app.css"],
        "tokens": ["web/static/app.css"],
        "button": ".sidebar-theme-toggle, .sidebar-settings-link",
        "hover": ".sidebar-theme-toggle:hover, .sidebar-settings-link:hover",
        "focus": ".sidebar-theme-toggle:focus-visible, .sidebar-settings-link:focus-visible",
        "row": ".sidebar-footer",  # in MyMail the footer *is* the flex row
        "footer": ".sidebar-footer",
        "panel": ".sidebar",
    },
    "mynotes": {
        "css": ["web/static/app.css"],
        # MyNotes' palette lives in the render kit, not app.css (§5.2).
        "tokens": ["web/static/render/note.css"],
        "button": ".sidebar-footer-actions .theme-toggle, .sidebar-footer-actions .settings-open",
        "hover": ".sidebar-footer-actions .theme-toggle:hover:not(:disabled), "
                 ".sidebar-footer-actions .settings-open:hover:not(:disabled)",
        "focus": ".sidebar-footer-actions .theme-toggle:focus-visible, "
                 ".sidebar-footer-actions .settings-open:focus-visible",
        "row": ".sidebar-footer-actions",
        "footer": ".sidebar-footer",
        "panel": ".sidebar",
    },
}

LIGHT_SCOPES = (":root",)
DARK_SCOPES = ('[data-theme="dark"]', ':root[data-theme="dark"]')

# ─── The contract ───────────────────────────────────────────────────────────
#
# (rule, property, expected, mode, spec-section)
#
#   mode "text"   compare the declaration's source text exactly. This is what
#                 catches `0.80rem` -> `0.8rem`: identical computed AND serialised,
#                 so no rendering test can ever see it (§9.2).
#   mode "colour" resolve var() through the app's own tokens, compare the hex.
#                 Token *names* are per-project and are not compared (§5.2).

PINS = [
    # rule      property          expected                    mode      section
    ("button", "display",         "inline-flex",              "text",   "§2"),
    ("button", "align-items",     "center",                   "text",   "§2"),
    ("button", "gap",             "6px",                      "text",   "§2"),
    ("button", "padding",         "4px 8px",                  "text",   "§2"),
    ("button", "font-family",     "inherit",                  "text",   "§4"),
    ("button", "font-size",       "0.80rem",                  "text",   "§2.1"),
    ("button", "line-height",     "1.5",                      "text",   "§2"),
    ("button", "white-space",     "nowrap",                   "text",   "§2"),
    ("button", "cursor",          "pointer",                  "text",   "§2"),
    ("button", "background",      "none",                     "text",   "§2"),
    ("button", "border-radius",   "6px",                      "colour", "§2"),
    ("button", "transition",
     "background 0.12s, color 0.12s, border-color 0.12s",     "text",   "§6.1"),
    # The §3.1 class: deleting any of these changes nothing observable in the app
    # where the value already arrives by another route, so rendering cannot
    # defend them. A text comparison across three repos can.
    ("button", "font-weight",     "400",                      "text",   "§3"),
    ("button", "font-style",      "normal",                   "text",   "§3"),
    ("button", "text-align",      "center",                   "text",   "§3"),
    ("button", "flex-shrink",     "0",                        "text",   "§2.3"),

    ("row",    "display",         "flex",                     "text",   "§2"),
    ("row",    "flex-wrap",       "nowrap",                   "text",   "§2"),
    ("row",    "gap",             "6px",                      "text",   "§2"),

    ("focus",  "outline-offset",  "2px",                      "text",   "§6.2"),
]

# (rule, property, light, dark, section) — compared as resolved values.
COLOURS = [
    ("button", "color",         "#6b7280", "#9ca3af", "§5.1 resting text"),
    ("hover",  "color",         "#1f2937", "#f3f4f6", "§5.1 hover text"),
    ("hover",  "background",    "#f3f4f6", "#374151", "§5.1 hover background"),
    ("hover",  "border-color",  "#9ca3af", "#6b7280", "§5.1 hover border"),
]

# Declarations that must NOT be present — §6.2 names both explicitly.
FORBIDDEN = [
    ("focus", "outline", "none", "§6.2 — never restore `outline: none`"),
]


# ─── A small CSS reader ─────────────────────────────────────────────────────

def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def top_level_rules(css: str):
    """Yield (selector, body) for rules at the top level only.

    Rules nested inside an at-rule (@media, @supports) are skipped deliberately:
    a media-query override is a different value under different conditions, and
    folding it in here would make the comparison lie.
    """
    i, n, sel = 0, len(css), []
    while i < n:
        c = css[i]
        if c == "{":
            selector = "".join(sel).strip()
            depth, j = 1, i + 1
            while j < n and depth:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            if not selector.startswith("@"):
                yield normalise(selector), css[i + 1:j - 1]
            i, sel = j, []
        elif c == "}":
            i, sel = i + 1, []
        else:
            sel.append(c)
            i += 1


def normalise(selector: str) -> str:
    return re.sub(r"\s*,\s*", ", ", " ".join(selector.split()))


def declarations(body: str) -> dict[str, str]:
    """property -> source text of its value, last wins (as the cascade does)."""
    out, depth, buf = {}, 0, []
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == ";" and depth == 0:
            take(out, "".join(buf))
            buf = []
        else:
            buf.append(ch)
    take(out, "".join(buf))
    return out


def take(out: dict[str, str], chunk: str) -> None:
    if ":" not in chunk:
        return
    prop, _, value = chunk.partition(":")
    prop = prop.strip().lower()
    if prop and not prop.startswith("--"):
        out[prop] = " ".join(value.split())


def custom_properties(css: str, scopes) -> dict[str, str]:
    props = {}
    for selector, body in top_level_rules(css):
        if selector not in scopes:
            continue
        for chunk in re.split(r";", body):
            if ":" in chunk and chunk.strip().startswith("--"):
                name, _, value = chunk.partition(":")
                props.setdefault(name.strip(), " ".join(value.split()))
    return props


def resolve(value: str, props: dict[str, str], hops: int = 6) -> str:
    """Follow var(--x) chains. Token names are local; only the value is shared."""
    for _ in range(hops):
        m = re.search(r"var\(\s*(--[\w-]+)\s*(?:,[^)]*)?\)", value)
        if not m:
            return value.strip()
        replacement = props.get(m.group(1))
        if replacement is None:
            return value.strip()
        value = value[:m.start()] + replacement + value[m.end():]
    return value.strip()


# ─── Loading an app ─────────────────────────────────────────────────────────

class App:
    def __init__(self, name: str, root: str):
        self.name, self.root, self.problems = name, root, []
        cfg = APPS[name]
        self.rules, self.sources = {}, {}
        css = self._read(cfg["css"])
        for selector, body in top_level_rules(css):
            self.rules.setdefault(selector, {}).update(declarations(body))
        token_css = css if cfg["tokens"] == cfg["css"] else self._read(cfg["tokens"])
        self.light = custom_properties(token_css, LIGHT_SCOPES)
        # The dark scope only *overrides*: a token it does not redefine still
        # resolves through :root, and aliases (`--text: var(--fg)`) are usually
        # declared once in :root while the value they point at is what changes.
        # Layering matches the cascade; reading the dark block alone would leave
        # every alias unresolved and report a false disagreement.
        self.dark = {**self.light, **custom_properties(token_css, DARK_SCOPES)}
        self.cfg = cfg

    def _read(self, rel_paths) -> str:
        out = []
        for rel in rel_paths:
            path = os.path.join(self.root, rel)
            try:
                with open(path, encoding="utf-8") as fh:
                    out.append(strip_comments(fh.read()))
            except OSError as exc:
                self.problems.append(f"cannot read {rel}: {exc.strerror}")
        return "\n".join(out)

    def where(self, rule: str) -> str:
        return f"{self.cfg[rule]}  in  {self.cfg['css'][0]}"

    def backdrop(self):
        """(raw background value, selector it came from) — footer first, else panel.

        §5.3 pins the colour behind the controls, not the element declaring it.
        """
        for rule in ("footer", "panel"):
            selector = self.cfg[rule]
            block = self.rules.get(selector) or {}
            if "background" in block:
                return block["background"], selector
            if "background-color" in block:
                return block["background-color"], selector
        return None, None

    def declared(self, rule: str, prop: str):
        selector = self.cfg[rule]
        block = self.rules.get(selector)
        if block is None:
            return None, f"rule `{selector}` not found"
        if prop not in block:
            return None, f"`{prop}` not declared on `{selector}`"
        return block[prop], None


# ─── Checking ───────────────────────────────────────────────────────────────

class Report:
    def __init__(self):
        self.failures, self.lines = [], []

    def ok(self, label: str, detail: str = "") -> None:
        self.lines.append(("  ok  ", label, [detail] if detail else []))

    def fail(self, label: str, details: list[str]) -> None:
        # Failure detail is never suppressed, including under --quiet: a failure
        # a reader cannot act on is barely better than no failure at all.
        self.lines.append((" FAIL ", label, details))
        self.failures.append((label, details))


def site(app: App, rule: str) -> str:
    """Where a reader should go to fix it: repo, file, selector."""
    return f"{app.name:<8} {app.cfg['css'][0]}   in rule `{app.cfg[rule]}`"


def check(apps: dict[str, App], report: Report) -> None:
    for rule, prop, expected, mode, section in PINS:
        label = f"{section:<7} {rule}.{prop}"
        bad = []
        for name, app in apps.items():
            raw, err = app.declared(rule, prop)
            if err:
                bad.append(f"{site(app, rule)}\n           {err}")
                continue
            actual = resolve(raw, app.light) if mode == "colour" else raw
            if actual != expected:
                got = f"`{prop}: {raw}`"
                if actual != raw:
                    got += f" (resolves to `{actual}`)"
                bad.append(f"{site(app, rule)}\n"
                           f"           found {got}, expected `{expected}`")
        if bad:
            report.fail(label, bad)
        else:
            report.ok(label, f"`{expected}` in all {len(apps)}")

    for rule, prop, light, dark, section in COLOURS:
        for theme, expected in (("light", light), ("dark", dark)):
            label = f"{section:<26} [{theme}]"
            bad = []
            for name, app in apps.items():
                raw, err = app.declared(rule, prop)
                if err:
                    bad.append(f"{site(app, rule)}\n           {err}")
                    continue
                props = app.light if theme == "light" else app.dark
                actual = resolve(raw, props).lower()
                if actual != expected:
                    bad.append(f"{site(app, rule)}\n"
                               f"           `{prop}: {raw}` resolves to `{actual}` "
                               f"in {theme}, expected `{expected}`")
            if bad:
                report.fail(label, bad)
            else:
                report.ok(label, f"`{expected}` in all {len(apps)}")

    for rule, prop, banned, why in FORBIDDEN:
        bad = []
        for name, app in apps.items():
            raw, err = app.declared(rule, prop)
            if not err and raw.strip().lower() == banned:
                bad.append(f"{site(app, rule)}\n"
                           f"           `{prop}: {raw}` is present and must not be")
        if bad:
            report.fail(why, bad)
        else:
            report.ok(why, "absent in all 3")

    # §5.3 — the RESOLVED backdrop, not which element declares it. An app whose
    # panel already paints --surface needs nothing on the footer (MyNotes); an
    # app with a sticky footer needs it there regardless (§8.3). Checking the
    # footer alone would fail a correct repo, which is worse than admitting a gap.
    #
    # This is the WEAK form and is labelled as such in the output. It assumes the
    # painting element is either the footer or the one panel named in APPS — true
    # of all three today, required by nothing. An app painting --surface three
    # levels up would satisfy the contract and fail here. The robust form is a
    # browser walking up from the button to the first ancestor whose computed
    # backgroundColor is not transparent; that is out of reach for a static
    # reader, so this says which form it ran rather than implying more.
    for theme in ("light", "dark"):
        label = f"§5.3 backdrop is --surface   [{theme}]  (STATIC approximation)"
        bad = []
        for name, app in apps.items():
            props = app.light if theme == "light" else app.dark
            want = resolve("var(--surface)", props).lower()
            raw, source = app.backdrop()
            if raw is None:
                bad.append(f"{app.name:<8} {app.cfg['css'][0]}\n"
                           f"           no background on `{app.cfg['footer']}` or "
                           f"`{app.cfg['panel']}` — cannot determine the backdrop statically")
                continue
            actual = resolve(raw, props).lower()
            if actual != want:
                bad.append(f"{app.name:<8} {app.cfg['css'][0]}   in rule `{source}`\n"
                           f"           `background: {raw}` resolves to `{actual}` in {theme}, "
                           f"expected --surface `{want}`")
        if bad:
            report.fail(label, bad)
        else:
            report.ok(label, f"--surface behind the controls in all {len(apps)}")

    # The focus outline is one declaration in every app, but its colour comes
    # from a token, so shape and resolved colour are checked together per theme.
    for theme, expected in (("light", "#2563eb"), ("dark", "#3b82f6")):
        label = f"§6.2 focus outline           [{theme}]"
        want, bad = f"2px solid {expected}", []
        for name, app in apps.items():
            raw, err = app.declared("focus", "outline")
            if err:
                bad.append(f"{site(app, 'focus')}\n           {err}")
                continue
            props = app.light if theme == "light" else app.dark
            actual = resolve(raw, props).lower()
            if actual != want:
                bad.append(f"{site(app, 'focus')}\n"
                           f"           `outline: {raw}` resolves to `{actual}` "
                           f"in {theme}, expected `{want}`")
        if bad:
            report.fail(label, bad)
        else:
            report.ok(label, f"`{want}` in all {len(apps)}")


CANNOT_CHECK = """\
What a green run does NOT mean. This reads CSS source; it never renders anything.

  · Geometry is unverified — the 29.2px height, the (8,8) viewport position, the
    4px outline clearance, overflow and clipping. All need a browser (§2.2, §8).
  · The cascade is unverified. This reads the declarations in the contract's own
    rule. A later rule overriding them, or a selector that matches nothing, looks
    identical to correct here.
  · Markup is unverified — icon size, aria-label wording, the element type, and
    the width-stable label structure all live in TSX, not CSS (§7).
  · Contrast ratios are not computed; only that the colours are the pinned ones.
  · The §5.3 backdrop check is a STATIC APPROXIMATION, labelled as such above. It
    resolves the footer's background, falling back to the panel named in APPS —
    which assumes the painting element is one of those two. That is true of all
    three apps today and required by nothing. A failure there may be this check's
    limitation rather than a real violation; confirm in a browser, by walking up
    from the button to the first ancestor with a non-transparent background.
  · Values inside @media blocks are deliberately skipped: a conditional override
    is a different value under different conditions, not a disagreement.

Rendering and this check are complements, not substitutes. Neither sees what the
other does — and only MyCal has a rendering suite at all."""


def main() -> int:
    ap = argparse.ArgumentParser(description="Check the MySuite sidebar-footer contract.")
    ap.add_argument("--repos", default=None,
                    help="directory holding mycal/ mymail/ mynotes/ (default: this repo's parent)")
    ap.add_argument("--quiet", action="store_true", help="print only failures and the verdict")
    args = ap.parse_args()

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    repos = args.repos or os.path.dirname(here)

    print(f"MySuite contract check — {SPEC}")
    print(f"siblings: {repos}\n")

    # Degrade honestly: two of three agreeing is not a pass.
    missing = [n for n in APPS if not os.path.isdir(os.path.join(repos, n))]
    if missing:
        print(f"CANNOT CHECK: repo(s) not found at {repos}: {', '.join(sorted(missing))}")
        print("This contract is a three-repo agreement; checking a subset would be misleading.")
        return 2

    apps = {}
    for name in APPS:
        app = App(name, os.path.join(repos, name))
        if app.problems:
            print(f"CANNOT CHECK: {name}: " + "; ".join(app.problems))
            return 2
        apps[name] = app

    report = Report()
    check(apps, report)

    for status, label, details in report.lines:
        failed = status.strip() == "FAIL"
        if args.quiet and not failed:
            continue
        print(f"{status} {label}")
        # Detail on a failure always prints: a failure nobody can act on is
        # barely better than no failure. Passing detail is noise under --quiet.
        if failed or not args.quiet:
            for line in details:
                print(f"         {line}")

    print()
    if report.failures:
        print(f"FAILED — {len(report.failures)} pinned value(s) disagree across the three repos.")
        print(f"Every value above is fixed by {SPEC}. Changing one is a change in all three")
        print("repos, or in none — a local 'fix' is the defect this check exists to find.")
        return 1

    print(f"PASSED — every pinned value agrees across {', '.join(sorted(apps))}.")
    print()
    print(CANNOT_CHECK)
    return 0


if __name__ == "__main__":
    sys.exit(main())
