import os

from pypdf import PdfReader, PdfWriter


def process_pdf(input_path: str, output_path: str, rotation: int) -> int:
    """
    Rotate all pages in the input PDF by the given rotation angle (relative),
    ensuring the final /Rotate value is normalized to 0, 90, 180, or 270.
    Returns the number of pages processed.
    """
    reader = PdfReader(input_path)
    num_pages = len(reader.pages)

    if num_pages == 0:
        raise ValueError("The input PDF has no pages to rotate.")

    writer = PdfWriter()

    for page in reader.pages:
        # Directly compute and set the new normalized rotation
        page.rotation = (page.rotation + rotation) % 360
        writer.add_page(page)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    return num_pages
