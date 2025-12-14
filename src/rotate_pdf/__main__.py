# src/rotate_pdf/__main__.py
import argparse
import os
import sys
from typing import NoReturn

from pypdf.errors import PdfReadError

from .rotation import process_pdf


def main() -> NoReturn:
    parser = argparse.ArgumentParser(
        description="Rotate every page of a PDF file by 90, 180, or 270 degrees, clockwise or counterclockwise."
    )
    parser.add_argument("input_path", help="Path to the input PDF file")
    parser.add_argument(
        "output_path",
        nargs="?",
        help="Path to the output rotated PDF file (optional; defaults to input_path with '_out' suffix)",
    )
    parser.add_argument(
        "--degrees",
        type=int,
        default=90,
        choices=[90, 180, 270],
        help="Degrees to rotate (default: 90)",
    )
    parser.add_argument(
        "--direction",
        type=int,
        default=0,
        choices=[0, 1],
        help="Direction: 0 for counterclockwise (default), 1 for clockwise",
    )

    args = parser.parse_args()

    # Set default output path if not provided
    if not args.output_path:
        base, ext = os.path.splitext(args.input_path)
        args.output_path = f"{base}_out{ext}"

    # Input validation
    if not os.path.exists(args.input_path):
        parser.error(f"Error: The input file '{args.input_path}' does not exist.")

    if not os.path.isfile(args.input_path):
        parser.error(f"Error: The input path '{args.input_path}' is not a file.")

    if os.path.abspath(args.input_path) == os.path.abspath(args.output_path):
        parser.error(
            "Error: The output path cannot be the same as the input path (would overwrite the original)."
        )

    # Map direction number to name and sign
    direction_name = "counterclockwise" if args.direction == 0 else "clockwise"
    rotation_angle = -args.degrees if args.direction == 0 else args.degrees

    try:
        num_pages = process_pdf(args.input_path, args.output_path, rotation_angle)
        print(f"Successfully rotated all {num_pages} pages by {args.degrees}° {direction_name}.")
        print(f"Output saved to: {args.output_path}")
    except PdfReadError:
        print("Error: Unable to read the PDF (invalid or corrupted file?).")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: Permission denied - {e}")
        sys.exit(1)
    except OSError as e:
        print(f"Error: File system error - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
