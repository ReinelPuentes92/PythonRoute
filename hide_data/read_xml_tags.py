from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
import xml.etree.ElementTree as ET


@dataclass
class TagStats:
    count_with_text: int = 0
    total_length: int = 0
    max_length: int = 0
    samples: list[str] = field(default_factory=list)

    def add_text(self, value: str, sample_limit: int) -> None:
        text_length = len(value)
        self.count_with_text += 1
        self.total_length += text_length
        self.max_length = max(self.max_length, text_length)
        if len(self.samples) < sample_limit:
            self.samples.append(value)

    @property
    def avg_length(self) -> float:
        if self.count_with_text == 0:
            return 0.0
        return self.total_length / self.count_with_text


def local_name(tag: str) -> str:
    """Return tag name without namespace."""
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def iter_tag_stats(
    xml_path: Path,
    sample_limit: int = 3,
    sample_chars: int = 80,
) -> tuple[dict[str, TagStats], int]:
    """Parse XML in streaming mode and collect text statistics per tag."""
    stats: dict[str, TagStats] = {}
    processed_nodes = 0

    context = ET.iterparse(str(xml_path), events=("end",))
    for _, elem in context:
        processed_nodes += 1
        tag = local_name(elem.tag)

        text = (elem.text or "").strip()
        if text:
            if tag not in stats:
                stats[tag] = TagStats()
            stats[tag].add_text(text[:sample_chars], sample_limit)

        # Keep memory usage stable for very large XML files.
        elem.clear()

    return stats, processed_nodes


def sorted_rows(stats: dict[str, TagStats]) -> list[tuple[str, TagStats]]:
    return sorted(
        stats.items(),
        key=lambda item: (item[1].count_with_text, item[0]),
        reverse=True,
    )


def print_report(rows: Iterable[tuple[str, TagStats]], top: int) -> None:
    print("tag,count_with_text,avg_length,max_length,samples")
    for idx, (tag, tag_stats) in enumerate(rows):
        if idx >= top:
            break
        samples = " | ".join(tag_stats.samples)
        print(
            f"{tag},{tag_stats.count_with_text},{tag_stats.avg_length:.1f},"
            f"{tag_stats.max_length},{samples}"
        )


def write_csv(rows: list[tuple[str, TagStats]], csv_path: Path) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["tag", "count_with_text", "avg_length", "max_length", "samples"])
        for tag, tag_stats in rows:
            writer.writerow(
                [
                    tag,
                    tag_stats.count_with_text,
                    f"{tag_stats.avg_length:.1f}",
                    tag_stats.max_length,
                    " | ".join(tag_stats.samples),
                ]
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read XML in streaming mode and list tags containing text.",
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to XML input file.",
    )
    parser.add_argument(
        "--top",
        default=200,
        type=int,
        help="Number of tags to print in console report (default: 200).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Optional CSV output path with full tag statistics.",
    )
    parser.add_argument(
        "--sample-limit",
        default=3,
        type=int,
        help="Maximum number of samples saved per tag (default: 3).",
    )
    parser.add_argument(
        "--sample-chars",
        default=80,
        type=int,
        help="Maximum length of every sample text (default: 80).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    stats, processed_nodes = iter_tag_stats(
        xml_path=args.input,
        sample_limit=args.sample_limit,
        sample_chars=args.sample_chars,
    )
    rows = sorted_rows(stats)

    print(f"processed_nodes={processed_nodes}")
    print(f"unique_tags_with_text={len(rows)}")
    print_report(rows, top=args.top)

    if args.out:
        write_csv(rows, args.out)
        print(f"csv_written={args.out}")


if __name__ == "__main__":
    main()
