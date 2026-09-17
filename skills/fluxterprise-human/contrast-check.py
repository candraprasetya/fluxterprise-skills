#!/usr/bin/env python3
"""WCAG 2.x contrast checker, home of the fluxterprise-human contrast checker.

Usage:
    python3 contrast-check.py "#FFFFFF" "#777777"
    python3 contrast-check.py FFFFFF 777777
    python3 contrast-check.py --aaa "#FFFFFF" "#777777"
    python3 contrast-check.py --selftest
    python3 contrast-check.py --file palette.json
    python3 contrast-check.py --json "#FFFFFF" "#777777"

Prints the contrast ratio and a PASS/FAIL verdict for normal text (4.5:1)
and large text (3:1, 18px+ per fluxterprise FG-25). Exit code 0 only when both
verdicts pass, so scripts can chain on it.

--selftest parses the reference table out of the SKILL.md next to this script
(the skill doc is the source of truth, not a list copied into this script) and
recomputes every row with the formula, checking the ratio and both verdicts.

--aaa checks WCAG AAA thresholds (7:1 normal, 4.5:1 large) instead of AA.

--file reads a JSON file with color pairs and checks all of them.

--json outputs results as JSON for CI integration.
"""

import json
import os
import re
import sys

REFERENCE_HEADER = "| Pairing (text on background) | Ratio | Normal text (4.5) | Large text (3.0) |"
NAMED_COLORS = {
    "black": (0, 0, 0), "white": (255, 255, 255),
    "red": (255, 0, 0), "green": (0, 128, 0), "blue": (0, 0, 255),
    "yellow": (255, 255, 0), "cyan": (0, 255, 255), "magenta": (255, 0, 255),
    "orange": (255, 165, 0), "purple": (128, 0, 128), "pink": (255, 192, 203),
    "grey": (128, 128, 128), "gray": (128, 128, 128),
    "lightgrey": (211, 211, 211), "lightgray": (211, 211, 211),
    "darkgrey": (169, 169, 169), "darkgray": (169, 169, 169),
    "navy": (0, 0, 128), "teal": (0, 128, 128), "maroon": (128, 0, 0),
    "olive": (128, 128, 0), "lime": (0, 255, 0), "aqua": (0, 255, 255),
    "silver": (192, 192, 192), "fuchsia": (255, 0, 255),
}


def parse_color(value):
    """Parse a color value. Supports hex (#RRGGBB, #RGB, RRGGBB, RGB), rgb(r, g, b), rgba(r, g, b, a), and named CSS colors."""
    value = value.strip()

    # rgb() / rgba() format
    rgb_match = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", value)
    if rgb_match:
        return tuple(int(rgb_match.group(i)) for i in (1, 2, 3))

    # Named CSS color
    if value.lower() in NAMED_COLORS:
        return NAMED_COLORS[value.lower()]

    # Hex format
    return parse_hex(value)


def parse_hex(value):
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", value):
        raise ValueError(f"expected a hex color like #FFFFFF, got {value!r}")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def parse_pairing(pairing):
    """Turn 'White on #333333' or '#555555 on black' into two RGB tuples."""
    colors = []
    for token in re.split(r"\s+on\s+", pairing):
        token = token.strip()
        match = re.search(r"#[0-9A-Fa-f]{3,6}", token)
        if match:
            colors.append(parse_hex(match.group(0)))
        elif token.lower() in NAMED_COLORS:
            colors.append(NAMED_COLORS[token.lower()])
        else:
            raise ValueError(f"cannot parse {token!r} from pairing {pairing!r}")
    if len(colors) != 2:
        raise ValueError(f"expected two colors in pairing {pairing!r}")
    return tuple(colors)


def linearize(channel):
    c = channel / 255.0
    if c <= 0.03928:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (linearize(ch) for ch in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(color_a, color_b):
    lum_a, lum_b = luminance(color_a), luminance(color_b)
    lighter, darker = sorted((lum_a, lum_b), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def check_pair(fg, bg, aaa=False):
    """Check a single color pair. Returns a result dict."""
    ratio = contrast_ratio(fg, bg)
    aa_normal = 4.5
    aa_large = 3.0
    aaa_normal = 7.0
    aaa_large = 4.5

    if aaa:
        return {
            "foreground": fg,
            "background": bg,
            "ratio": round(ratio, 2),
            "aa": {
                "normal_text": {"threshold": aa_normal, "pass": ratio >= aa_normal},
                "large_text": {"threshold": aa_large, "pass": ratio >= aa_large},
            },
            "aaa": {
                "normal_text": {"threshold": aaa_normal, "pass": ratio >= aaa_normal},
                "large_text": {"threshold": aaa_large, "pass": ratio >= aaa_large},
            },
        }
    else:
        return {
            "foreground": fg,
            "background": bg,
            "ratio": round(ratio, 2),
            "normal_text": {"threshold": aa_normal, "pass": ratio >= aa_normal},
            "large_text": {"threshold": aa_large, "pass": ratio >= aa_large},
        }


def reference_doc_path():
    here = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(here, "SKILL.md")
    return candidate if os.path.isfile(candidate) else None


def parse_reference_rows(path):
    """Reference table rows from SKILL.md, with the ratio already a float.

    A row that does not split into four cells is dropped silently, not raised.
    """
    rows = []
    with open(path, encoding="utf-8") as handle:
        in_table = False
        for raw in handle:
            line = raw.rstrip("\n")
            if line.startswith(REFERENCE_HEADER):
                in_table = True
                continue
            if not in_table:
                continue
            if not line.startswith("|"):
                break
            if line.startswith("|---"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 4:
                continue
            pairing, ratio, normal, large = cells
            rows.append({
                "pairing": pairing,
                "ratio": float(ratio),
                "normal": normal,
                "large": large,
            })
    return rows


def selftest():
    doc = reference_doc_path()
    if doc is None:
        print("selftest: SKILL.md not found next to the script; cannot check the table")
        return 2
    try:
        rows = parse_reference_rows(doc)
    except (OSError, ValueError) as exc:
        print(f"selftest: could not read the table from SKILL.md: {exc}")
        return 1
    if not rows:
        print("selftest: no reference rows found in SKILL.md")
        return 1

    failures = 0
    for row in rows:
        color_a, color_b = parse_pairing(row["pairing"])
        computed = round(contrast_ratio(color_a, color_b), 2)
        expected_normal = "Pass" if computed >= 4.5 else "Fail"
        expected_large = "Pass" if computed >= 3.0 else "Fail"
        if f"{computed:.2f}" != f"{row['ratio']:.2f}":
            failures += 1
            print(f"selftest: {row['pairing']}: table says {row['ratio']}, the formula says {computed:.2f}")
        if row["normal"] != expected_normal:
            failures += 1
            print(f"selftest: {row['pairing']}: normal text marked {row['normal']}, should be {expected_normal}")
        if row["large"] != expected_large:
            failures += 1
            print(f"selftest: {row['pairing']}: large text marked {row['large']}, should be {expected_large}")

    if failures:
        return 1
    print(f"selftest: {len(rows)} reference pairs OK")
    return 0


def batch_check(file_path, aaa=False, output_json=False):
    """Check all color pairs in a JSON file.

    Expected format:
    {
      "pairs": [
        {"foreground": "#FFFFFF", "background": "#777777", "label": "Header text"},
        {"foreground": "#000000", "background": "#F5F5F5", "label": "Body text"}
      ]
    }
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: could not read {file_path}: {exc}")
        return 2

    pairs = data.get("pairs", [])
    if not pairs:
        print("error: no 'pairs' array found in JSON file")
        return 2

    results = []
    all_pass = True
    for pair in pairs:
        label = pair.get("label", "unlabeled")
        try:
            fg = parse_color(pair["foreground"])
            bg = parse_color(pair["background"])
            result = check_pair(fg, bg, aaa=aaa)
            result["label"] = label
            results.append(result)

            if aaa:
                passed = result["aaa"]["normal_text"]["pass"] and result["aaa"]["large_text"]["pass"]
            else:
                passed = result["normal_text"]["pass"] and result["large_text"]["pass"]

            if not passed:
                all_pass = False
        except (ValueError, KeyError) as exc:
            print(f"error: {label}: {exc}")
            all_pass = False

    if output_json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            label = r.get("label", "unlabeled")
            ratio = r["ratio"]
            if aaa:
                n = r["aaa"]["normal_text"]
                l = r["aaa"]["large_text"]
                print(f"{label}: {ratio}:1 | AAA normal {'PASS' if n['pass'] else 'FAIL'} ({n['threshold']}:1) | AAA large {'PASS' if l['pass'] else 'FAIL'} ({l['threshold']}:1)")
            else:
                n = r["normal_text"]
                l = r["large_text"]
                print(f"{label}: {ratio}:1 | normal {'PASS' if n['pass'] else 'FAIL'} ({n['threshold']}:1) | large {'PASS' if l['pass'] else 'FAIL'} ({l['threshold']}:1)")

    return 0 if all_pass else 1


def main(argv):
    aaa = False
    output_json = False
    file_path = None

    # Parse flags
    args = []
    for arg in argv:
        if arg == "--aaa":
            aaa = True
        elif arg == "--json":
            output_json = True
        elif arg == "--selftest":
            args.append(arg)
        elif arg == "--file":
            args.append(arg)
        elif args and args[-1] == "--file":
            args.append(arg)
            file_path = arg
        else:
            args.append(arg)

    if args and args[0] == "--selftest":
        return selftest()

    if file_path:
        return batch_check(file_path, aaa=aaa, output_json=output_json)

    if len(args) != 2:
        print("usage: python3 contrast-check.py [--aaa] [--json] <hex1> <hex2>")
        print("       python3 contrast-check.py [--aaa] [--json] --file palette.json")
        print("       python3 contrast-check.py --selftest")
        return 2

    try:
        fg = parse_color(args[0])
        bg = parse_color(args[1])
    except ValueError as exc:
        print(f"error: {exc}")
        return 2

    result = check_pair(fg, bg, aaa=aaa)
    ratio = result["ratio"]

    if output_json:
        print(json.dumps(result, indent=2))
        aa_pass = result["normal_text"]["pass"] and result["large_text"]["pass"]
        return 0 if aa_pass else 1

    aa_pass = result["normal_text"]["pass"] and result["large_text"]["pass"]
    print(f"ratio: {ratio}:1")
    print(f"AA normal text (4.5:1): {'PASS' if result['normal_text']['pass'] else 'FAIL'}")
    print(f"AA large text  (3.0:1): {'PASS' if result['large_text']['pass'] else 'FAIL'}")

    if aaa:
        aaa_pass = result["aaa"]["normal_text"]["pass"] and result["aaa"]["large_text"]["pass"]
        print(f"AAA normal text (7.0:1): {'PASS' if result['aaa']['normal_text']['pass'] else 'FAIL'}")
        print(f"AAA large text  (4.5:1): {'PASS' if result['aaa']['large_text']['pass'] else 'FAIL'}")
        return 0 if aa_pass and aaa_pass else 1

    return 0 if aa_pass else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
