#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pypdf>=4", "click>=8.1"]
# ///

import dataclasses
import datetime
import re
from pathlib import Path

import click
from pypdf import PdfReader

Date = datetime.date
DATE_RE = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{2})\b")


@dataclasses.dataclass
class ReceiptParseResult:
    date: Date
    vendor: str

    @property
    def is_valid(self):
        return self.date and self.vendor


class ReceiptParseError(RuntimeError):
    pass


def extract_pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    parts: list[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text:
            parts.append(page_text)
    return "\n".join(parts)


def parse_first_date_mmddyy(text: str) -> Date | None:
    def to_date(match: re.Match[str]) -> Date | None:
        mm = int(match.group(1))
        dd = int(match.group(2))
        yy = int(match.group(3))
        yyyy = 2000 + yy
        try:
            return Date(yyyy, mm, dd)
        except ValueError:
            return None

    search_pos = 0
    while match := DATE_RE.search(text, pos=search_pos):
        if date := to_date(match):
            return date
        # keep searching if the match was an invalid date
        search_pos = match.end()


def extract_date_meijer(pdf: Path) -> Date:
    try:
        text = extract_pdf_text(pdf)
    except Exception as e:
        raise ReceiptParseError(f"Could not extract text")

    first_lines_text = "\n".join(
        [line for line in text.split("\n") if line.strip()][:3]
    )
    date = parse_first_date_mmddyy(first_lines_text)
    if not date:
        raise ReceiptParseError(f"Could not find valid MM/DD/YY date")

    return date


def parse_receipt(pdf: Path) -> ReceiptParseResult:
    if pdf.name.startswith("meijer_digital_receipt"):
        return ReceiptParseResult(vendor="meijer", date=extract_date_meijer(pdf))
    else:
        raise ReceiptParseError(f"Unable to determine receipt type from filename")


def rename_receipts(pdfs: list[Path], *, dry_run: bool) -> int:
    if not pdfs:
        click.echo("ERROR: no input files provided", err=True)
        return 2

    for pdf_in in pdfs:
        pdf = pdf_in.expanduser().resolve()

        if pdf.suffix.lower() != ".pdf":
            click.echo(f"WARNING: skipping non-PDF: '{pdf}'")
            continue

        if not pdf.exists():
            click.echo(f"WARNING: file does not exist: '{pdf}'")
            continue

        if not pdf.is_file():
            click.echo(f"WARNING: not a file, skipping: '{pdf}'")
            continue

        try:
            parsed = parse_receipt(pdf)
            if not parsed.is_valid:
                raise ReceiptParseError(f"Invalid parser output: {parsed}")
        except ReceiptParseError as e:
            click.echo(f"WARNING: parse error: {e}: '{pdf}'")
            continue

        vendor = parsed.vendor.lower()  # TODO: normalize more?
        target_name = f"{parsed.date:%Y-%m-%d}-{vendor}.pdf"
        target_path = pdf.with_name(target_name)

        if target_path.exists():
            click.echo(
                f"WARNING: target already exists, skipping: '{pdf.name}' -> '{target_path.name}'"
            )
            continue

        if target_path.resolve() == pdf.resolve():
            # already named correctly
            continue

        if dry_run:
            click.echo(f"[Dry-run] {pdf.name} -> {target_path.name}")
        else:
            pdf.rename(target_path)
            click.echo(f"Renamed: {pdf.name} -> {target_path.name}")

    return 0


def click_exit(code):
    click.get_current_context().exit(code)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli() -> None:
    """Receipt processing tools."""
    pass


@cli.command("rename")
@click.argument(
    "pdfs",
    nargs=-1,
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--dry-run", "-n", is_flag=True, help="Show what would change without renaming"
)
def rename_cmd(pdfs: tuple[Path, ...], dry_run: bool) -> None:
    click_exit(rename_receipts(list(pdfs), dry_run=dry_run))


if __name__ == "__main__":
    cli(standalone_mode=True)
