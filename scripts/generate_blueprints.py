#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOKEN_RE = re.compile(r"\[\[([a-zA-Z0-9_.-]+)\]\]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render localized blueprint YAML files from a template and i18n dictionaries."
    )
    parser.add_argument("--template", default="template.yaml", help="Path to template YAML.")
    parser.add_argument("--i18n-dir", default="languages", help="Directory with <lang>.json files.")
    parser.add_argument("--output-dir", default="dist", help="Output directory for generated files.")
    parser.add_argument(
        "--default-lang",
        default="en",
        help="Fallback language code. Must exist in languages directory.",
    )
    parser.add_argument(
        "--filename",
        default="adaptive_lighting.yaml",
        help="Filename used for each generated blueprint.",
    )
    parser.add_argument(
        "--write-root-default",
        action="store_true",
        help="Also write fallback language output at repository root filename.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit(f"Expected object at top-level in {path}")

    out: dict[str, str] = {}
    for key, value in data.items():
        if not isinstance(key, str):
            raise SystemExit(f"Non-string key in {path}: {key!r}")
        if not isinstance(value, str):
            raise SystemExit(f"Value for key {key!r} in {path} must be a string")
        out[key] = value
    return out


def render_template(template: str, values: dict[str, str]) -> str:
    errors: list[str] = []

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            errors.append(key)
            return match.group(0)

        value = values[key]
        if "\n" not in value:
            return value

        line_start = template.rfind("\n", 0, match.start()) + 1
        indent = template[line_start : match.start()]
        lines = value.splitlines()
        if not lines:
            return ""
        return lines[0] + "\n" + "\n".join(indent + line for line in lines[1:])

    rendered = TOKEN_RE.sub(repl, template)
    if errors:
        missing = ", ".join(sorted(set(errors)))
        raise SystemExit(f"Missing placeholder values for keys: {missing}")
    return rendered


def main() -> int:
    args = parse_args()

    template_path = Path(args.template)
    i18n_dir = Path(args.i18n_dir)
    output_dir = Path(args.output_dir)

    if not template_path.exists():
        raise SystemExit(f"Template not found: {template_path}")
    if not i18n_dir.exists() or not i18n_dir.is_dir():
        raise SystemExit(f"i18n directory not found: {i18n_dir}")

    template = template_path.read_text(encoding="utf-8")
    template_keys = set(TOKEN_RE.findall(template))
    if not template_keys:
        raise SystemExit("No placeholders found in template.")

    dictionaries: dict[str, dict[str, str]] = {}
    for path in sorted(i18n_dir.glob("*.json")):
        dictionaries[path.stem] = load_json(path)

    if not dictionaries:
        raise SystemExit("No i18n dictionaries found.")

    if args.default_lang not in dictionaries:
        raise SystemExit(
            f"Fallback language '{args.default_lang}' not found in {i18n_dir}."
        )

    default_dict = dictionaries[args.default_lang]
    missing_default = sorted(template_keys - set(default_dict))
    if missing_default:
        raise SystemExit(
            "Fallback dictionary is missing keys required by template: "
            + ", ".join(missing_default)
        )

    unknown_in_default = sorted(set(default_dict) - template_keys)
    if unknown_in_default:
        raise SystemExit(
            f"Fallback dictionary has unknown keys not used by template: {', '.join(unknown_in_default)}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    for lang, local_dict in dictionaries.items():
        unknown_keys = sorted(set(local_dict) - template_keys)
        if unknown_keys:
            raise SystemExit(
                f"Dictionary '{lang}' has unknown keys not used by template: {', '.join(unknown_keys)}"
            )

        values = default_dict | local_dict
        rendered = render_template(template, values)

        lang_out_dir = output_dir / lang
        lang_out_dir.mkdir(parents=True, exist_ok=True)
        (lang_out_dir / args.filename).write_text(rendered, encoding="utf-8")

    default_output = output_dir / args.default_lang / args.filename
    if args.write_root_default:
        Path(args.filename).write_text(default_output.read_text(encoding="utf-8"), encoding="utf-8")

    print(
        f"Rendered {len(dictionaries)} language(s) to '{output_dir}'. "
        f"Fallback language: '{args.default_lang}'."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
