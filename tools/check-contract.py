#!/usr/bin/env python3
"""Cross-repo check for two of the three MySuite contracts.

Reads the three sibling apps' stylesheets and fails if they disagree on a value
that spec/sidebar-footer.md or spec/app-name-label.md pins. It never renders
anything: it compares source text and resolved custom properties, which is what
lets it catch the one class of breakage no browser test can see.

    ../mycal    ../mymail    ../mynotes

spec/app-logo.md is NOT checked here, at all. Neither is the app-name-label
contract's PLACEMENT, which is not a declared value in any of the three apps and
cannot be read statically by anything. Both are stated in the caveat block, which
prints on every terminating path — read it, because a green run means less than
it looks like it does.

Python 3, standard library only: no package manager, no network, no build step.
The app repos have a standing rule against npm/npx and this must not become a
dependency they would have to adopt.

Usage:  tools/check-contract.py [--repos DIR] [--quiet] [--self-test]
Exit:   0 all pinned values agree · 1 a pinned value disagrees · 2 cannot check
"""

from __future__ import annotations

import argparse
import os
import re
import sys

SPEC = "spec/sidebar-footer.md"
SPEC_LABEL = "spec/app-name-label.md"
SPECS = (SPEC, SPEC_LABEL)

# ─── Which rules hold the contract in each app ──────────────────────────────
#
# Selector strings are matched exactly, after collapsing whitespace. They differ
# per app by design (§5.2: names are local, values are shared), so this table is
# also the record of where the contract lives in each repo.

APPS = {
    "mycal": {
        "css": ["web/static/app.css"],
        "tokens": ["web/static/app.css"],
        "brandrow": ".brand",
        "bodytext": "body",
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
        "brandrow": ".sidebar-header",   # MyMail's brand row — NOT MyNotes' .sidebar-header
        "bodytext": "html, body",
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
        "brandrow": ".brand",
        "bodytext": "body",
    },
}

# ─── app-name-label roles ───────────────────────────────────────────────────
#
# "brandrow" is the flex row holding the badge and the app-name label. In all
# three apps the label's typography is declared THERE and inherited, and not one
# of the three declares it on the label itself (two of them have no element for
# the label at all — spec/app-name-label.md §1). So this is the rule to read.
#
# That the three do it the same way is a fact about today's implementations, not
# a requirement: an app declaring the size on the label would conform and would
# report "rule not found" here. Loud, not silent, and the caveat block says so.
#
# NOTE the collision hazard: `.sidebar-header` is MyMail's brand row and MyNotes'
# OUTER header (brand + tab strip + actions) — the same class name for different
# elements. The table above is what keeps them apart; do not "simplify" it by
# matching on the class.
#
# "bodytext" is where the font stack is declared in each app — `body` in MyCal and
# MyNotes, `html, body` in MyMail. Nothing nearer the label declares a family in
# any of the three (spec/app-name-label.md §3.1), which is exactly why this reads
# a whole-application rule and why that check is the weaker of the two.

LIGHT_SCOPES = (":root",)
DARK_SCOPES = ('[data-theme="dark"]', ':root[data-theme="dark"]')

# ─── The contract ───────────────────────────────────────────────────────────
#
# (rule, property, expected, mode, spec-section)
#
#   mode "text"   compare the declaration's source text exactly. This is what
#                 catches `0.80rem` -> `0.8rem`: identical computed AND serialised,
#                 so no rendering test can ever see it (§9.2).
#   mode "resolve" follow var() chains through the app's own tokens and compare
#                 the RESOLVED value — a colour or a length. Token *names* are
#                 per-project and are never compared (§5.2); the number of hops
#                 to reach a literal is local too, which is why this resolves
#                 rather than matching names.

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
    ("button", "border-radius",   "6px",                      "resolve", "§2"),
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

# ─── spec/app-name-label.md ─────────────────────────────────────────────────
#
# Two pins, and they are NOT of equal strength. The output says which is which on
# the line itself, not in a footer, because a reader who sees two green lines will
# otherwise assume they mean the same thing.
#
#   font-size   STRONG. `1.1rem` -> `1.10rem` or `-> 17.6px` is identical computed
#               at the 16px root every e2e suite runs at, and `1.10rem` is
#               identical serialised as well. NOTHING RENDERED CAN SEE EITHER
#               EDIT, in any of the three apps. This line is the only guard that
#               exists for it (§3.2, §7.1).
#
#   font stack  WEAK, and labelled WEAK in the output. It reads `body`'s
#               declaration in each app. It does NOT check the cascade between
#               `body` and the label, so a rule overriding the family for the
#               brand row passes here. And it says nothing about which FACE
#               renders: `system-ui` resolves per machine by definition, so no
#               check anywhere can make that claim (§3.1).
#
# mode "stack" compares font-family lists with quote style and spacing
# normalised. MyCal and MyMail write 'Segoe UI', MyNotes writes "Segoe UI" — a
# difference no browser can see, and a `text` comparison would report it as drift.

LABEL_PINS = [
    ("brandrow", "font-size",   "1.1rem", "text",  "§3.2", "STRONG"),
    ("bodytext", "font-family",
     "system-ui, -apple-system, segoe ui, roboto, sans-serif", "stack", "§3.1",
     "WEAK: body's stack, not the label's; the cascade between them is NOT "
     "checked, and nothing here says which face renders"),
]

# (rule, property, light, dark, section) — compared as resolved values.
COLOURS = [
    ("button", "color",         "#6b7280", "#9ca3af", "§5.1 resting text"),
    ("hover",  "color",         "#1f2937", "#f3f4f6", "§5.1 hover text"),
    ("hover",  "background",    "#f3f4f6", "#374151", "§5.1 hover background"),
    ("hover",  "border-color",  "#9ca3af", "#6b7280", "§5.1 hover border"),
]

# ─── Recorded per-app values (§5.3, §5.1) ───────────────────────────────────
#
# The backdrop behind the controls is no longer one shared colour. The owner
# ruled that the three apps may differ there, so what this checks is that each
# app matches the value the CONTRACT RECORDS for it — not that the three agree.
#
# That distinction is the whole reason §5.3 writes the values down. A rule
# saying "any opaque colour" would be checkable by nothing; recording them keeps
# a changed backdrop a change to the spec first, exactly as it was before.
#
# (light, dark) — spec/sidebar-footer.md §5.3.
BACKDROPS = {
    "mycal":   ("#f3f4f6", "#111827"),   # --bg: the left column's own background
    "mymail":  ("#ffffff", "#1f2937"),   # --surface
    "mynotes": ("#f9fafb", "#1f2937"),   # --surface
}

# Sanctioned departures from COLOURS, per app and theme (§5.1's deviation table).
# A value is allowed to differ ONLY where that app's own backdrop makes the
# shared value fail a stated threshold, and only with the measurement recorded
# in the spec. Anything not listed here is still expected to be shared, so an
# unlisted difference is drift and fails.
#
# (app, rule, property, theme) -> resolved value
DEVIATIONS = {
    # MyCal's light backdrop is #f3f4f6, not #ffffff:
    #   shared #6b7280 label  -> 4.393:1, FAILS WCAG 1.4.3 (needs 4.5:1)
    #   local  #4b5563 label  -> 6.867:1
    ("mycal", "button", "color", "light"): "#4b5563",
    #   shared #f3f4f6 fill IS the backdrop -> 1.000:1, an absent fill
    #   local  #e5e7eb fill   -> 1.125:1, clearing §5.1's 1.053 floor
    ("mycal", "hover", "background", "light"): "#e5e7eb",
}

# Declarations that must NOT be present. `0` and `none` compute identically, and
# the base button rule is at least as natural a place to add one as :focus-visible,
# so both rules and both spellings are checked.
FORBIDDEN = [
    (("focus", "button"), "outline", {"none", "0"},
     "§6.2 — never restore `outline: none`"),
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
        if c == ";" and not sel_is_open(sel):
            # A statement at-rule — `@import url(...);`, `@charset`, `@layer a, b;`
            # — ends here and declares no block. Without this reset the accumulator
            # runs on into the NEXT selector, the combined string starts with `@`,
            # and the guard below silently drops a rule that is not an at-rule.
            # MyNotes' app.css opens with `@import url("render/note.css");`, so
            # this fired on a real repo: the following `*` rule vanished.
            i, sel = i + 1, []
            continue
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


def sel_is_open(sel) -> bool:
    """True if the accumulated selector has an unclosed `(`, so a `;` inside it
    (e.g. `:is(a;b)` malformed, or a url with a semicolon) is not a statement end."""
    return "".join(sel).count("(") > "".join(sel).count(")")


def normalise(selector: str) -> str:
    return re.sub(r"\s*,\s*", ", ", " ".join(selector.split()))


def declarations(body: str) -> dict[str, str]:
    """property -> source text of its value, last wins (as the cascade does)."""
    out, parens, braces, buf = {}, 0, 0, []
    for ch in body:
        if ch == "(":
            parens += 1
        elif ch == ")":
            parens -= 1
        elif ch == "{":
            # Native CSS nesting. Everything inside belongs to the nested rule,
            # not this one — `&:hover { color: red }` would otherwise attribute a
            # hover colour to the resting rule and fail against the wrong pin.
            braces += 1
            take(out, "".join(buf))   # flush the declaration before the nested block
            buf = []
            continue
        elif ch == "}":
            braces -= 1
            buf = []
            continue
        if braces > 0:
            continue
        if ch == ";" and parens == 0:
            take(out, "".join(buf))
            buf = []
        else:
            buf.append(ch)
    take(out, "".join(buf))
    return out


PROP_RE = re.compile(r"^[a-z-]+$")


def take(out: dict[str, str], chunk: str) -> None:
    if ":" not in chunk:
        return
    prop, _, value = chunk.partition(":")
    prop = prop.strip().lower()
    # A real property name only. Guards against a nested selector fragment
    # (`&`, `.btn { gap`) being recorded as if it were a declaration.
    if PROP_RE.match(prop) and not prop.startswith("--"):
        out[prop] = " ".join(value.split())


def font_stack(value: str) -> str:
    """Normalise a font-family list: the families are the value, the quoting is not.

    `'Segoe UI'` and `"Segoe UI"` are the same font and render identically; the
    three apps happen to disagree on which quote to use (spec/app-name-label.md
    §3.1). Comparing the source text would report that as a divergence, which is
    the check being wrong rather than the repos.
    """
    out = []
    for part in value.split(","):
        part = " ".join(part.split())
        if len(part) >= 2 and part[0] == part[-1] and part[0] in "\"'":
            part = part[1:-1].strip()
        out.append(part.lower())
    return ", ".join(out)


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
    """Where a reader should go to fix it: repo, file(s), selector."""
    files = " / ".join(app.cfg["css"])   # all of them: one entry would be a guess
    return f"{app.name:<8} {files}   in rule `{app.cfg[rule]}`"


def check_label(apps: dict[str, App], report: Report) -> None:
    """spec/app-name-label.md — font size and font stack. Placement is NOT here
    and cannot be: it is a flex remainder, not a declared value in any app."""
    for rule, prop, expected, mode, section, strength in LABEL_PINS:
        label = f"label {section:<6} {rule}.{prop}"
        bad = []
        for app in apps.values():
            raw, err = app.declared(rule, prop)
            if err:
                bad.append(f"{site(app, rule)}\n           {err}")
                continue
            actual = font_stack(raw) if mode == "stack" else raw
            if actual != expected:
                got = f"`{prop}: {raw}`"
                if actual != raw:
                    got += f" (normalises to `{actual}`)"
                bad.append(f"{site(app, rule)}\n"
                           f"           found {got}, expected `{expected}`")
        if bad:
            report.fail(label, bad + [f"[{strength}]"])
        else:
            report.ok(label, f"`{expected}` in all {len(apps)}   [{strength}]")


def check(apps: dict[str, App], report: Report) -> None:
    for rule, prop, expected, mode, section in PINS:
        label = f"{section:<8} {rule}.{prop}"
        bad = []
        for app in apps.values():
            raw, err = app.declared(rule, prop)
            if err:
                bad.append(f"{site(app, rule)}\n           {err}")
                continue
            actual = resolve(raw, app.light).lower() if mode == "resolve" else raw
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
        for theme, shared in (("light", light), ("dark", dark)):
            label = f"{section:<28} [{theme}]"
            bad, deviated = [], []
            for app in apps.values():
                raw, err = app.declared(rule, prop)
                if err:
                    bad.append(f"{site(app, rule)}\n           {err}")
                    continue
                props = app.light if theme == "light" else app.dark
                actual = resolve(raw, props).lower()
                # A recorded deviation (§5.1) is checked against ITS OWN value,
                # not waived. An app that deviates differently from the way the
                # contract says it deviates still fails.
                expected = DEVIATIONS.get((app.name, rule, prop, theme), shared)
                if expected is not shared:
                    deviated.append(f"{app.name} `{expected}`")
                if actual != expected:
                    why = ("expected the recorded deviation" if expected is not shared
                           else "expected the shared value")
                    bad.append(f"{site(app, rule)}\n"
                               f"           `{prop}: {raw}` resolves to `{actual}` "
                               f"in {theme}, {why} `{expected}`")
            if bad:
                report.fail(label, bad)
            elif deviated:
                report.ok(label, f"`{shared}` shared; recorded deviation: "
                                 + ", ".join(deviated))
            else:
                report.ok(label, f"`{shared}` in all {len(apps)}")

    for rules, prop, banned, why in FORBIDDEN:
        bad = []
        for app in apps.values():
            for rule in rules:
                raw, err = app.declared(rule, prop)
                if not err and raw.strip().lower() in banned:
                    bad.append(f"{site(app, rule)}\n"
                               f"           `{prop}: {raw}` is present and must not be")
        if bad:
            report.fail(why, bad)
        else:
            report.ok(why, f"absent in all {len(apps)}")

    # §5.3 — the RESOLVED backdrop, not which element declares it. An app whose
    # panel already paints it needs nothing on the footer (MyNotes); an app with
    # a sticky footer needs it there regardless (§8.3). Checking the footer alone
    # would fail a correct repo, which is worse than admitting a gap.
    #
    # The three apps are NO LONGER expected to agree here — the owner ruled that
    # they may differ, so each is compared against the value BACKDROPS records
    # for it. This still fails on an unrecorded change, which is the point: the
    # colour stopped being shared, the obligation to write it down did not.
    #
    # This is the WEAK form and is labelled as such in the output. It assumes the
    # painting element is either the footer or the one panel named in APPS — true
    # of all three today, required by nothing. An app painting the colour three
    # levels up would satisfy the contract and fail here. The robust form is a
    # browser walking up from the button to the first ancestor whose computed
    # backgroundColor is not transparent; that is out of reach for a static
    # reader, so this says which form it ran rather than implying more.
    for theme in ("light", "dark"):
        label = f"{'§5.3 backdrop is as recorded':<28} [{theme}]  (STATIC approximation)"
        bad = []
        for app in apps.values():
            props = app.light if theme == "light" else app.dark
            want = BACKDROPS.get(app.name, (None, None))[0 if theme == "light" else 1]
            if want is None:
                # An app with no recorded backdrop cannot be checked, and that is
                # a failure rather than a pass. §5.3 requires the value to be
                # written down; not finding one is the contract being incomplete,
                # not the app being fine.
                bad.append(f"{app.name:<8} {SPEC}\n"
                           f"           no backdrop recorded for this app in §5.3 — "
                           f"the contract cannot be checked here, so this is not a pass")
                continue
            raw, source = app.backdrop()
            if raw is None:
                # "Could not look" is never "agrees" — the same rule the e2e walk
                # follows with its non-null assertion (measurement-protocol.md).
                bad.append(f"{app.name:<8} {app.cfg['css'][0]}\n"
                           f"           no background on `{app.cfg['footer']}` or "
                           f"`{app.cfg['panel']}` — cannot determine the backdrop "
                           f"statically, which is a failure and not a pass")
                continue
            actual = resolve(raw, props).lower()
            if actual != want:
                bad.append(f"{app.name:<8} {app.cfg['css'][0]}   in rule `{source}`\n"
                           f"           `background: {raw}` resolves to `{actual}` in {theme}, "
                           f"but §5.3 records `{want}` for {app.name}")
        if bad:
            report.fail(label, bad)
        else:
            recorded = ", ".join(
                f"{n} `{BACKDROPS[n][0 if theme == 'light' else 1]}`" for n in sorted(apps))
            report.ok(label, f"each app matches its recorded value — {recorded}")

    # The focus outline is one declaration in every app, but its colour comes
    # from a token, so shape and resolved colour are checked together per theme.
    for theme, expected in (("light", "#2563eb"), ("dark", "#3b82f6")):
        label = f"{'§6.2 focus outline':<28} [{theme}]"
        want, bad = f"2px solid {expected}", []
        for app in apps.values():
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
What this run does NOT tell you — on a pass OR a failure. It reads CSS source
and never renders anything, so a clean result is narrower than it looks and a
failing one covers less ground than the count suggests.

  · IT CHECKS TWO CONTRACTS OF THREE. spec/ holds THREE binding contracts. This
    script knows about spec/sidebar-footer.md (fully) and spec/app-name-label.md
    (its font size and font stack, and NOTHING else it pins).
    NOTHING HERE LOOKS AT spec/app-logo.md — not the badge box, the fill, the
    glyph size, the mark's extent, the placement, nor the accessibility rules. A
    green run says nothing whatever about it. Note the asymmetry a future checker
    for it must print: a CSS reader can defend the badge box in all three apps
    but the GLYPH SIZE IN MYCAL ONLY, because MyMail sizes its glyph in a TSX
    prop no stylesheet reader can see (app-logo.md §9.4).

  · PLACEMENT IS NOT CHECKED AND CANNOT BE. spec/app-name-label.md pins the
    label's font, font size AND PLACEMENT. Only the first two are above. The
    label's position is not a declared value in ANY of the three apps — it is a
    flex remainder, centred in a row whose height is the row's tallest item — so
    there is nothing for a static reader to read, and no better version of this
    script would help. It is held by three per-app rendered suites, which are
    blind to each other, and by review. See app-name-label.md §4.1 and §7.3.

  · WHICH FONT RENDERS IS NOT CHECKED AND CANNOT BE. The font-stack line compares
    the DECLARED stack — the request made of the platform. `system-ui` resolves
    per machine by definition; all three measuring sandboxes resolved it to a
    monospace face, and CI resolves it ~1.25x wider than a local run. No check
    anywhere can assert the rendered face, and this one does not try.

  · THE TWO app-name-label LINES ARE NOT OF EQUAL STRENGTH, and each says which
    it is. font-size is STRONG: `1.1rem` -> `1.10rem` or `-> 17.6px` is invisible
    to every rendering test in all three repos, so that line is the only guard
    that exists for it. The font stack is WEAK: it reads `body`'s declaration, so
    a rule overriding the family for the brand row passes here.

  · Geometry is unverified — the 29.2px height, the (8,8) viewport position, the
    4px outline clearance, overflow and clipping. All need a browser (§2.2, §8).
  · The cascade is unverified. This reads the declarations in the contract's own
    rule. A later rule overriding them, or a selector that matches nothing, looks
    identical to correct here.
  · Markup is unverified — icon size, aria-label wording, the element type, and
    the width-stable label structure all live in TSX, not CSS (§7).
  · Contrast ratios are not computed; only that the colours are the recorded
    ones. This matters more than it used to: since §5.3 let the three apps have
    DIFFERENT backdrops, agreeing with the record is no longer evidence that a
    colour reads well on what it sits on. The 4.5:1 and 3:1 obligations in §5.4
    and §6.2 are held by hand-measurement and review, not by this script.
  · Recorded per-app deviations (§5.1) are checked against their own values, not
    waived — but this script cannot tell you whether a deviation SHOULD exist.
    An app that quietly stops deviating fails here; an app that deviates for a
    bad reason passes, provided the spec records the same value.
  · A deviation confined to ONE THEME is only half-defended here, and the half
    that is missing was measured rather than assumed. Confining it means the
    other theme must NAME the shared token, which is a claim about the
    declaration — invisible to a resolved-value comparison wherever the two
    tokens agree. Mutation-tested on scratch copies: collapsing MyCal's dark
    label alias IS caught (#d1d5db != #9ca3af); collapsing its dark hover-fill
    alias is NOT (dark --border and --hover-bg are both #374151). Only a CSSOM
    read of the declaration catches that one. See §5.1.
  · The §5.3 backdrop check is a STATIC APPROXIMATION, labelled as such above. It
    resolves the footer's background, falling back to the panel named in APPS —
    which assumes the painting element is one of those two. That is true of all
    three apps today and required by nothing. A failure there may be this check's
    limitation rather than a real violation; confirm in a browser, by walking up
    from the button to the first ancestor with a non-transparent background.
  · WHICH REPOSITORY STATE this read is not reported, because it cannot be: it
    reads files on disk, so a commit, an uncommitted edit and a half-written file
    all look the same, and across three repos there is no atomic snapshot. A run
    against a tree somebody is editing has already produced a red result that
    three runs seconds later did not reproduce. Re-run before reporting a
    failure, and say "green against an uncommitted tree" when that is what it
    was — see measurement-protocol.md.
  · Values inside @media blocks are deliberately skipped: a conditional override
    is a different value under different conditions, not a disagreement.
  · It reads ONE NAMED RULE per app (see APPS). A reordered selector list or a
    renamed class reports "rule not found", not drift — loud, but it is a static
    reader coupled to selector text in a suite whose §5.2 says names are local.
  · Known parser gaps, none firing on the three apps today: `!important` is kept
    in the value text and would read as a disagreement; a `var()` nested inside a
    fallback (`var(--a, var(--b))`) is returned verbatim; comment-stripping is
    string-unaware, so a `"/*"` inside a string would corrupt the rest of the
    file; a custom property whose value contains `;` inside `url()` mis-parses.

Rendering and this check are complements, not substitutes. Neither sees what the
other does — all three apps now have a rendering suite and all three run in CI,
but each sees only its own app. Nothing but this script compares them, and
nobody's CI runs this script."""


# ─── Self-test: prove the guard can still fail ──────────────────────────────
#
# measurement-protocol.md: "a guard is not accepted when it goes green. It is
# accepted when it has been shown to go red for the right reason." That has to
# stay true as this file changes, so the sensitivity checks live with it. Each
# case names the parser behaviour it defends and the finding that motivated it.

SELF_TEST = [
    ("@import does not swallow the next rule",
     lambda: "*" in [s for s, _ in top_level_rules('@import url("x.css");\n* { box-sizing: border-box; }')]),
    ("a top-level ; does not merge selectors",
     lambda: [s for s, _ in top_level_rules('@charset "utf-8";\n.a { color: red }')] == [".a"]),
    ("native nesting does not leak into the parent rule",
     lambda: declarations("gap: 6px; &:hover { color: red; }") == {"gap": "6px"}),
    ("a declaration after a nested block is still read",
     lambda: declarations("&:hover { color: red; } gap: 6px") == {"gap": "6px"}),
    ("paren depth still protects multi-part values",
     lambda: declarations("transition: a 1s, b 2s") == {"transition": "a 1s, b 2s"}),
    ("var() chains resolve to a literal, not a name",
     lambda: resolve("var(--a)", {"--a": "var(--b)", "--b": "#ffffff"}) == "#ffffff"),
    ("a var() cycle terminates instead of hanging",
     lambda: resolve("var(--a)", {"--a": "var(--b)", "--b": "var(--a)"}) is not None),
    ("an unknown token is returned verbatim, not treated as a match",
     lambda: resolve("var(--nope)", {}) == "var(--nope)"),
    ("@media blocks are not read as top-level rules",
     lambda: [s for s, _ in top_level_rules("@media (x) { .a { color: red } }")] == []),
    ("a nested selector fragment is not recorded as a property",
     lambda: "&" not in declarations("gap: 6px; &:hover { color: red; }")),
    # app-name-label §3.1: the three apps disagree on quote style and agree on the
    # font. Normalising too little reports drift no browser can see; normalising
    # too much would swallow a real change. Both directions are checked, because
    # only the second one can fail silently.
    ("font stack: quote style is normalised away",
     lambda: font_stack("system-ui, 'Segoe UI', sans-serif")
             == font_stack('system-ui, "Segoe UI", sans-serif')),
    ("font stack: whitespace and case are normalised away",
     lambda: font_stack("system-ui,   Roboto ,sans-serif")
             == font_stack("System-UI, roboto, sans-serif")),
    ("font stack: a DIFFERENT family is still a difference",
     lambda: font_stack("system-ui, Roboto") != font_stack("system-ui, Helvetica")),
    ("font stack: a dropped family is still a difference",
     lambda: font_stack("system-ui, Roboto, sans-serif")
             != font_stack("system-ui, sans-serif")),
    ("font stack: reordering is still a difference",
     lambda: font_stack("system-ui, Roboto") != font_stack("Roboto, system-ui")),
]


def self_test() -> int:
    print("Self-test — can this guard still fail?\n")
    bad = 0
    for label, fn in SELF_TEST:
        try:
            passed = bool(fn())
        except Exception as exc:                      # a crash is a failure, not a skip
            passed, label = False, f"{label}  [raised {type(exc).__name__}: {exc}]"
        print(f"{'  ok  ' if passed else ' FAIL '} {label}")
        bad += not passed
    print()
    if bad:
        print(f"SELF-TEST FAILED — {bad} case(s). The parser is not behaving as the")
        print("contract checks assume, so a green contract run would prove nothing.")
        return 1
    print(f"Self-test passed — {len(SELF_TEST)} cases. This proves the PARSER still")
    print("behaves as assumed. It does not prove the contract holds; run without")
    print("--self-test for that.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Check the MySuite sidebar-footer contract.")
    ap.add_argument("--repos", default=None,
                    help="directory holding mycal/ mymail/ mynotes/ (default: this repo's parent)")
    ap.add_argument("--quiet", action="store_true", help="print only failures and the verdict")
    ap.add_argument("--self-test", action="store_true",
                    help="check the parser against inline fixtures; prove this guard can still fail")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    repos = args.repos or os.path.dirname(here)

    print("MySuite contract check — " + " + ".join(SPECS))
    print(f"siblings: {repos}\n")

    # Degrade honestly: two of three agreeing is not a pass.
    missing = [n for n in APPS if not os.path.isdir(os.path.join(repos, n))]
    if missing:
        verdict = (f"CANNOT CHECK: repo(s) not found at {repos}: "
                   f"{', '.join(sorted(missing))}")
        print(verdict)
        print("This contract is a three-repo agreement; checking a subset would be misleading.")
        print()
        print(CANNOT_CHECK)
        print(f"\n{verdict}")
        return 2

    apps = {}
    for name in APPS:
        app = App(name, os.path.join(repos, name))
        if app.problems:
            verdict = f"CANNOT CHECK: {name}: " + "; ".join(app.problems)
            print(verdict)
            print()
            print(CANNOT_CHECK)
            print(f"\n{verdict}")
            return 2
        apps[name] = app

    report = Report()
    check(apps, report)
    check_label(apps, report)

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
        verdict = (f"FAILED — {len(report.failures)} pinned value(s) disagree "
                   f"across the three repos.")
        print(verdict)
        print("Every value above is fixed by " + " or ".join(SPECS) + ". Changing one is a")
        print("change in all three")
        print("repos, or in none — a local 'fix' is the defect this check exists to find.")
    else:
        verdict = f"PASSED — every pinned value agrees across {', '.join(sorted(apps))}."
        print(verdict)
    print()
    print(CANNOT_CHECK)
    # The verdict again, last. The caveats above run to three screens, so a reader
    # who tails the output, scrolls to the bottom, or opens a collapsed CI log
    # lands on the epistemics and never sees whether it passed — which happened to
    # a reviewer running the acceptance check, on a `tail -20`. The honesty of that
    # section is what made a truncated read feel complete, so the fix is ordering
    # and repetition, not less of it.
    print(f"\n{verdict}")
    return 1 if report.failures else 0


if __name__ == "__main__":
    sys.exit(main())
