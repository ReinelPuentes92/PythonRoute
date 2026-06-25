from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.sax import handler, make_parser
from xml.sax.saxutils import XMLGenerator


def mask_by_length(value: str, mask_char: str = "X") -> str:
    """Mask non-whitespace content preserving character count."""
    if not value.strip():
        return value
    return "".join(mask_char if not ch.isspace() else ch for ch in value)


def normalize_tag(name: tuple[str | None, str]) -> str:
    """Return local tag name for namespace-aware SAX events."""
    return name[1] if name[1] else ""


def parse_mask_tags(raw_tags: str | None, tags_file: Path | None) -> set[str]:
    tags: set[str] = set()

    if raw_tags:
        tags.update(tag.strip() for tag in raw_tags.split(",") if tag.strip())

    if tags_file:
        for line in tags_file.read_text(encoding="utf-8").splitlines():
            clean = line.strip()
            if clean and not clean.startswith("#"):
                tags.add(clean)

    return tags


@dataclass
class AnonymizationStats:
    elements_seen: int = 0
    elements_masked: int = 0
    text_nodes_masked: int = 0


class MaskingHandler(handler.ContentHandler):
    def __init__(self, writer: XMLGenerator, tags_to_mask: set[str], mask_char: str) -> None:
        super().__init__()
        self.writer = writer
        self.tags_to_mask = tags_to_mask
        self.mask_char = mask_char
        self.mask_stack: list[bool] = []
        self.stats = AnonymizationStats()

    def startDocument(self) -> None:
        self.writer.startDocument()

    def endDocument(self) -> None:
        self.writer.endDocument()

    def startPrefixMapping(self, prefix: str, uri: str) -> None:
        self.writer.startPrefixMapping(prefix, uri)

    def endPrefixMapping(self, prefix: str) -> None:
        self.writer.endPrefixMapping(prefix)

    def startElementNS(
        self,
        name: tuple[str | None, str],
        qname: str | None,
        attrs,
    ) -> None:
        self.stats.elements_seen += 1
        local = normalize_tag(name)
        should_mask = local in self.tags_to_mask
        self.mask_stack.append(should_mask)
        if should_mask:
            self.stats.elements_masked += 1
        self.writer.startElementNS(name, qname, attrs)

    def endElementNS(self, name: tuple[str | None, str], qname: str | None) -> None:
        self.writer.endElementNS(name, qname)
        self.mask_stack.pop()

    def characters(self, content: str) -> None:
        if self.mask_stack and self.mask_stack[-1]:
            masked = mask_by_length(content, self.mask_char)
            if masked != content:
                self.stats.text_nodes_masked += 1
            self.writer.characters(masked)
            return
        self.writer.characters(content)

    def ignorableWhitespace(self, whitespace: str) -> None:
        self.writer.ignorableWhitespace(whitespace)

    def processingInstruction(self, target: str, data: str) -> None:
        self.writer.processingInstruction(target, data)


def anonymize_xml(
    input_path: Path,
    output_path: Path,
    tags_to_mask: set[str],
    mask_char: str = "X",
) -> AnonymizationStats:
    """Anonymize selected tags in XML using SAX streaming processing."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, True)

    with output_path.open("w", encoding="utf-8", newline="") as out_file:
        writer = XMLGenerator(out_file, encoding="utf-8", short_empty_elements=True)
        sax_handler = MaskingHandler(writer, tags_to_mask, mask_char)
        parser.setContentHandler(sax_handler)
        parser.parse(str(input_path))
        return sax_handler.stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Anonymize XML values by masking selected tag text by length.",
    )
    parser.add_argument("--input", required=True, type=Path, help="Path to input XML file.")
    parser.add_argument("--output", required=True, type=Path, help="Path to output XML file.")
    parser.add_argument(
        "--tags",
        type=str,
        default="",
        help="Comma-separated tag names to anonymize, e.g. Name,Email,Phone.",
    )
    parser.add_argument(
        "--tags-file",
        type=Path,
        help="Optional text file with one tag per line. Lines starting with # are ignored.",
    )
    parser.add_argument(
        "--mask-char",
        type=str,
        default="X",
        help="Single character used for masking (default: X).",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    if args.tags_file and not args.tags_file.exists():
        raise FileNotFoundError(f"Tags file not found: {args.tags_file}")

    if not args.mask_char or len(args.mask_char) != 1:
        raise ValueError("--mask-char must be exactly one character")


def main() -> None:
    args = parse_args()
    validate_args(args)

    tags_to_mask = parse_mask_tags(args.tags, args.tags_file)
    if not tags_to_mask:
        raise ValueError("Provide at least one tag via --tags or --tags-file")

    stats = anonymize_xml(
        input_path=args.input,
        output_path=args.output,
        tags_to_mask=tags_to_mask,
        mask_char=args.mask_char,
    )

    print(f"elements_seen={stats.elements_seen}")
    print(f"elements_masked={stats.elements_masked}")
    print(f"text_nodes_masked={stats.text_nodes_masked}")
    print(f"output_xml={args.output}")


if __name__ == "__main__":
    main()
