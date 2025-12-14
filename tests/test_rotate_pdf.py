# tests/test_rotate_pdf.py
import os
import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError

from rotate_pdf import process_pdf  # Clean import (works after `uv pip install -e .`)


def create_sample_pdf(
    path: Path,
    pages: int = 1,
    initial_rotation: int = 0,
    width: float = 400,
    height: float = 600,
) -> None:
    """Helper to create a sample PDF with blank pages and optional initial rotation."""
    writer = PdfWriter()
    for _ in range(pages):
        page = writer.add_blank_page(width=width, height=height)
        page.rotation = initial_rotation % 360  # Ensure normalized
    with open(path, "wb") as f:
        writer.write(f)


@pytest.fixture
def sample_input_pdf(tmp_path: Path) -> Path:
    pdf_path = tmp_path / "input.pdf"
    create_sample_pdf(pdf_path)
    return pdf_path


def test_process_basic_counterclockwise_90(tmp_path: Path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    create_sample_pdf(input_pdf)

    process_pdf(str(input_pdf), str(output_pdf), -90)

    reader_out = PdfReader(output_pdf)
    assert reader_out.pages[0].rotation == 270

    # Input file unchanged
    reader_in = PdfReader(input_pdf)
    assert reader_in.pages[0].rotation == 0


def test_process_clockwise_90(tmp_path: Path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    create_sample_pdf(input_pdf)

    process_pdf(str(input_pdf), str(output_pdf), 90)

    reader = PdfReader(output_pdf)
    assert reader.pages[0].rotation == 90


def test_process_180(tmp_path: Path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    create_sample_pdf(input_pdf)

    process_pdf(str(input_pdf), str(output_pdf), 180)  # +180 or -180 both result in 180

    reader = PdfReader(output_pdf)
    assert reader.pages[0].rotation == 180


def test_process_multiple_pages(tmp_path: Path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    create_sample_pdf(input_pdf, pages=3)

    process_pdf(str(input_pdf), str(output_pdf), -90)

    reader = PdfReader(output_pdf)
    for page in reader.pages:
        assert page.rotation == 270


def test_process_initial_rotation(tmp_path: Path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    create_sample_pdf(input_pdf, initial_rotation=90)

    process_pdf(str(input_pdf), str(output_pdf), 90)

    reader_out = PdfReader(output_pdf)
    assert reader_out.pages[0].rotation == 180

    reader_in = PdfReader(input_pdf)
    assert reader_in.pages[0].rotation == 90  # unchanged


def test_process_empty_pdf(tmp_path: Path):
    input_pdf = tmp_path / "input.pdf"
    create_sample_pdf(input_pdf, pages=0)
    output_pdf = tmp_path / "output.pdf"

    with pytest.raises(ValueError, match="no pages"):
        process_pdf(str(input_pdf), str(output_pdf), 90)


def test_process_invalid_pdf(tmp_path: Path):
    input_pdf = tmp_path / "invalid.pdf"
    input_pdf.write_text("this is not a PDF")
    output_pdf = tmp_path / "output.pdf"

    with pytest.raises(PdfReadError):
        process_pdf(str(input_pdf), str(output_pdf), 90)


# CLI integration tests
def test_cli_input_not_exist():
    result = subprocess.run(
        [sys.executable, "-m", "rotate_pdf", "nonexistent.pdf"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "does not exist" in result.stderr


def test_cli_overwrite_attempt(tmp_path: Path):
    input_pdf = tmp_path / "test.pdf"
    create_sample_pdf(input_pdf)

    result = subprocess.run(
        [sys.executable, "-m", "rotate_pdf", str(input_pdf), str(input_pdf)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "same as" in result.stderr.lower()


def test_cli_default_behavior(tmp_path: Path):
    input_pdf = tmp_path / "input.pdf"
    create_sample_pdf(input_pdf)
    expected_output = tmp_path / "input_out.pdf"

    result = subprocess.run(
        [sys.executable, "-m", "rotate_pdf", str(input_pdf)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Successfully rotated" in result.stdout
    assert os.path.exists(expected_output)

    reader = PdfReader(expected_output)
    assert reader.pages[0].rotation == 270  # default: 90° counterclockwise

    # Input unchanged
    reader_in = PdfReader(input_pdf)
    assert reader_in.pages[0].rotation == 0


def test_cli_clockwise(tmp_path: Path):
    input_pdf = tmp_path / "input.pdf"
    create_sample_pdf(input_pdf)
    output_pdf = tmp_path / "output.pdf"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "rotate_pdf",
            str(input_pdf),
            str(output_pdf),
            "--direction",
            "1",
            "--degrees",
            "90",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    reader = PdfReader(output_pdf)
    assert reader.pages[0].rotation == 90
