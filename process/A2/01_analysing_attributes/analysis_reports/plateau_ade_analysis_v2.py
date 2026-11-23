#!/usr/bin/env python3
import argparse
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
GML_ID = "{http://www.opengis.net/gml}id"
DEFAULT_UNKNOWN_PATTERN = r"^-?9+$"


@dataclass
class FileResult:
    path: Path
    bldg_count: int = 0
    attr_count: dict[str, int] = field(default_factory=dict)
    bldg_with_attr: dict[str, int] = field(default_factory=dict)
    attr_unknown: dict[str, int] = field(default_factory=dict)
    attr_empty: dict[str, int] = field(default_factory=dict)


@dataclass
class FileError:
    path: Path
    message: str


@dataclass
class FolderSummary:
    total_bldg_count: int = 0
    attr_count: dict[str, int] = field(default_factory=dict)
    bldg_with_attr: dict[str, int] = field(default_factory=dict)
    attr_unknown: dict[str, int] = field(default_factory=dict)
    attr_empty: dict[str, int] = field(default_factory=dict)


def split_tag(tag: str) -> tuple[str, str]:
    if tag.startswith("{"):
        uri, _, local = tag[1:].partition("}")
        return uri, local
    return "", tag


def is_uro_uri(uri: str) -> bool:
    return "/iur/uro/" in uri


def is_bldg_uri(uri: str) -> bool:
    return "/citygml/building/" in uri


def is_group_uri(uri: str) -> bool:
    return "/citygml/cityobjectgroup/" in uri


def is_city_object_member(uri: str, local: str) -> bool:
    return local == "cityObjectMember" and "/citygml/" in uri


def is_ade_leaf(elem: ET.Element, local: str) -> bool:
    if len(elem) != 0:
        return False
    if not local or not local[0].islower():
        return False
    if local.endswith("Attribute"):
        return False
    return True


def find_parent_id(city_obj: ET.Element) -> str | None:
    for el in city_obj.iter():
        if not isinstance(el.tag, str):
            continue
        uri, local = split_tag(el.tag)
        if local == "parent" and is_group_uri(uri):
            href = el.get(XLINK_HREF)
            if href:
                return href.rsplit("#", 1)[-1]
            return None
    return None


def analyze_file(path: Path, unknown_re: re.Pattern[str]) -> FileResult:
    attr_count: defaultdict[str, int] = defaultdict(int)
    attr_unknown: defaultdict[str, int] = defaultdict(int)
    attr_empty: defaultdict[str, int] = defaultdict(int)
    building_attr_sets: list[set[str]] = []
    building_ids: dict[str, int] = {}
    groups: list[tuple[str | None, set[str]]] = []
    bldg_count = 0
    members = 0

    context = ET.iterparse(str(path), events=("start", "end"))
    root = None

    for event, elem in context:
        if root is None:
            root = elem
            continue
        if event != "end":
            continue
        if not isinstance(elem.tag, str):
            continue

        uri, local = split_tag(elem.tag)
        if not is_city_object_member(uri, local):
            continue

        member_attrs: set[str] = set()
        for el in elem.iter():
            if not isinstance(el.tag, str):
                continue
            euri, elocal = split_tag(el.tag)
            if not is_uro_uri(euri) or not is_ade_leaf(el, elocal):
                continue

            attr_count[elocal] += 1
            text = (el.text or "").strip()
            if text == "":
                if XLINK_HREF not in el.attrib:
                    attr_empty[elocal] += 1
            elif unknown_re.fullmatch(text):
                attr_unknown[elocal] += 1
            member_attrs.add(elocal)

        city_obj = None
        for child in elem:
            if isinstance(child.tag, str):
                city_obj = child
                break

        if city_obj is not None:
            curi, clocal = split_tag(city_obj.tag)
            if clocal == "Building" and is_bldg_uri(curi):
                bldg_count += 1
                idx = len(building_attr_sets)
                building_attr_sets.append(member_attrs)
                gid = city_obj.get(GML_ID)
                if gid:
                    building_ids[gid] = idx
            elif clocal == "CityObjectGroup" and is_group_uri(curi):
                groups.append((find_parent_id(city_obj), member_attrs))

        members += 1
        elem.clear()
        if members % 1000 == 0:
            root.clear()

    for parent_id, attrs in groups:
        if parent_id is None:
            continue
        idx = building_ids.get(parent_id)
        if idx is not None:
            building_attr_sets[idx].update(attrs)

    bldg_with_attr: defaultdict[str, int] = defaultdict(int)
    for attrs in building_attr_sets:
        for attr in attrs:
            bldg_with_attr[attr] += 1

    return FileResult(
        path=path,
        bldg_count=bldg_count,
        attr_count=dict(attr_count),
        bldg_with_attr=dict(bldg_with_attr),
        attr_unknown=dict(attr_unknown),
        attr_empty=dict(attr_empty),
    )


def looks_like_building_citygml(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            head = handle.read(131072)
    except OSError:
        return False
    return b"citygml/building" in head


def aggregate_results(results: list[FileResult]) -> FolderSummary:
    attr_count: defaultdict[str, int] = defaultdict(int)
    bldg_with_attr: defaultdict[str, int] = defaultdict(int)
    attr_unknown: defaultdict[str, int] = defaultdict(int)
    attr_empty: defaultdict[str, int] = defaultdict(int)
    total_bldg_count = 0

    for result in results:
        total_bldg_count += result.bldg_count
        for attr, count in result.attr_count.items():
            attr_count[attr] += count
        for attr, count in result.bldg_with_attr.items():
            bldg_with_attr[attr] += count
        for attr, count in result.attr_unknown.items():
            attr_unknown[attr] += count
        for attr, count in result.attr_empty.items():
            attr_empty[attr] += count

    return FolderSummary(
        total_bldg_count=total_bldg_count,
        attr_count=dict(attr_count),
        bldg_with_attr=dict(bldg_with_attr),
        attr_unknown=dict(attr_unknown),
        attr_empty=dict(attr_empty),
    )


def format_pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{numerator / denominator * 100:.1f}%"


def render_table(result: FileResult) -> str:
    lines = [
        "| attrName | attrCount | bldgWithAttrCount | attrUnkwnCount | attrEmptyCount |",
        "|---|---:|---:|---:|---:|",
    ]
    if not result.attr_count:
        lines.append("| _none_ | 0 | 0 | 0 | 0 |")
        return "\n".join(lines)

    for attr in sorted(result.attr_count):
        lines.append(
            f"| uro:{attr} | {result.attr_count.get(attr, 0)} | "
            f"{result.bldg_with_attr.get(attr, 0)} | "
            f"{result.attr_unknown.get(attr, 0)} | "
            f"{result.attr_empty.get(attr, 0)} |"
        )
    return "\n".join(lines)


def render_folder_table(summary: FolderSummary) -> str:
    lines = [
        "| attrName | attrCount | bldgWithAttrCount | bldgWithAttrCount_pct | "
        "attrUnkwnCount | attrUnkwnCount_pct | attrEmptyCount | attrEmptyCount_pct |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    if not summary.attr_count:
        lines.append("| _none_ | 0 | 0 | 0.0% | 0 | 0.0% | 0 | 0.0% |")
        return "\n".join(lines)

    for attr in sorted(summary.attr_count):
        attr_count = summary.attr_count.get(attr, 0)
        bldg_with_attr = summary.bldg_with_attr.get(attr, 0)
        attr_unknown = summary.attr_unknown.get(attr, 0)
        attr_empty = summary.attr_empty.get(attr, 0)
        lines.append(
            f"| uro:{attr} | {attr_count} | {bldg_with_attr} | "
            f"{format_pct(bldg_with_attr, summary.total_bldg_count)} | "
            f"{attr_unknown} | {format_pct(attr_unknown, attr_count)} | "
            f"{attr_empty} | {format_pct(attr_empty, attr_count)} |"
        )
    return "\n".join(lines)


def render_single(result: FileResult, unknown_pattern: str) -> str:
    return "\n".join(
        [
            "# PLATEAU i-UR ADE Attribute Analysis",
            "",
            f"- Input file: `{result.path}`",
            f"- bldgCount: {result.bldg_count}",
            f"- ADE attributes found: {len(result.attr_count)}",
            f"- Unknown value pattern: `{unknown_pattern}`",
            "",
            "## ADE attributes",
            "",
            render_table(result),
            "",
        ]
    )


def render_folder(
    folder: Path,
    results: list[FileResult],
    skipped: list[Path],
    errors: list[FileError],
    unknown_pattern: str,
) -> str:
    summary = aggregate_results(results)
    lines = [
        "# PLATEAU i-UR ADE Attribute Analysis",
        "",
        f"- Input folder: `{folder}`",
        f"- bldgFileCount: {len(results)}",
        f"- totalBldgCountFolder: {summary.total_bldg_count}",
        f"- totalAttrCountFolder: {len(summary.attr_count)}",
        f"- Unknown value pattern: `{unknown_pattern}`",
        "",
        "## Folder ADE Attribute Summary",
        "",
        render_folder_table(summary),
        "",
        "## Summary",
        "",
        "| file | bldgCount | adeAttributeCount |",
        "|---|---:|---:|",
    ]

    for result in results:
        lines.append(
            f"| `{result.path.name}` | {result.bldg_count} | {len(result.attr_count)} |"
        )

    for result in results:
        lines.extend(
            [
                "",
                f"## File: `{result.path.name}`",
                "",
                f"- Path: `{result.path}`",
                f"- bldgCount: {result.bldg_count}",
                f"- ADE attributes found: {len(result.attr_count)}",
                "",
                render_table(result),
            ]
        )

    if skipped:
        lines.extend(["", "## Skipped files", ""])
        for path in skipped:
            lines.append(f"- `{path}`: no bldg:Building found")

    if errors:
        lines.extend(["", "## Errors", ""])
        for error in errors:
            lines.append(f"- `{error.path}`: {error.message}")

    lines.append("")
    return "\n".join(lines)


def default_output_path(input_path: Path, mode: str) -> Path:
    if mode == "file":
        return input_path.with_name(f"{input_path.stem}_ade_attr_analysis.md")
    name = input_path.name or "folder"
    return input_path / f"{name}_ade_attr_analysis.md"


def write_and_print(report: str, output_path: Path) -> bool:
    content = report.rstrip("\n") + "\n"
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
    except OSError as exc:
        print(
            f"error: could not write report to {output_path}: {exc}",
            file=sys.stderr,
        )
        return False

    sys.stdout.write(content)
    sys.stdout.flush()
    print(f"Report written to {output_path}", file=sys.stderr)
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyse i-UR ADE attributes in PLATEAU CityGML building files."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    file_parser = subparsers.add_parser("file", help="Analyse one CityGML file.")
    file_parser.add_argument("path", type=Path, help="Path to the CityGML file.")
    file_parser.add_argument(
        "--output", type=Path, help="Path to the output Markdown report."
    )
    file_parser.add_argument(
        "--unknown-pattern",
        default=DEFAULT_UNKNOWN_PATTERN,
        help=f"Regex for unknown values (default: {DEFAULT_UNKNOWN_PATTERN}).",
    )

    folder_parser = subparsers.add_parser(
        "folder", help="Analyse all building CityGML files in a folder."
    )
    folder_parser.add_argument("path", type=Path, help="Path to the folder.")
    folder_parser.add_argument(
        "--output", type=Path, help="Path to the output Markdown report."
    )
    folder_parser.add_argument(
        "--unknown-pattern",
        default=DEFAULT_UNKNOWN_PATTERN,
        help=f"Regex for unknown values (default: {DEFAULT_UNKNOWN_PATTERN}).",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        unknown_re = re.compile(args.unknown_pattern)
    except re.error as exc:
        print(f"error: invalid --unknown-pattern: {exc}", file=sys.stderr)
        return 2

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.mode == "file":
        input_path: Path = args.path
        if not input_path.is_file():
            print(f"error: not a file: {input_path}", file=sys.stderr)
            return 2

        print(f"Parsing {input_path} ...", file=sys.stderr)
        try:
            result = analyze_file(input_path, unknown_re)
        except ET.ParseError as exc:
            print(f"error: failed to parse {input_path}: {exc}", file=sys.stderr)
            return 1

        print(
            f"Done: {result.bldg_count} buildings, {len(result.attr_count)} attributes",
            file=sys.stderr,
        )
        report = render_single(result, args.unknown_pattern)
        output_path = args.output or default_output_path(input_path, "file")
        if not write_and_print(report, output_path):
            return 1
        return 0

    folder: Path = args.path
    if not folder.is_dir():
        print(f"error: not a directory: {folder}", file=sys.stderr)
        return 2

    gml_files = sorted(
        (
            path
            for path in folder.iterdir()
            if path.is_file() and path.suffix.lower() == ".gml"
        ),
        key=lambda path: path.name.lower(),
    )
    if not gml_files:
        print(f"error: no .gml files found in {folder}", file=sys.stderr)
        return 1

    candidates = [path for path in gml_files if looks_like_building_citygml(path)]
    if not candidates:
        print(f"error: no building CityGML files found in {folder}", file=sys.stderr)
        return 1

    results: list[FileResult] = []
    skipped: list[Path] = []
    errors: list[FileError] = []

    for index, path in enumerate(candidates, 1):
        print(f"[{index}/{len(candidates)}] Parsing {path.name} ...", file=sys.stderr)
        try:
            result = analyze_file(path, unknown_re)
        except ET.ParseError as exc:
            errors.append(FileError(path, str(exc)))
            print(f"  error: {exc}", file=sys.stderr)
            continue

        if result.bldg_count == 0:
            skipped.append(path)
            print("  skipped: no bldg:Building found", file=sys.stderr)
            continue

        results.append(result)
        print(
            f"  done: {result.bldg_count} buildings, {len(result.attr_count)} attributes",
            file=sys.stderr,
        )

    if not results:
        print(
            "error: no building CityGML files with bldg:Building found",
            file=sys.stderr,
        )
        for error in errors:
            print(f"error: {error.path}: {error.message}", file=sys.stderr)
        return 1

    report = render_folder(folder, results, skipped, errors, args.unknown_pattern)
    output_path = args.output or default_output_path(folder, "folder")
    if not write_and_print(report, output_path):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
