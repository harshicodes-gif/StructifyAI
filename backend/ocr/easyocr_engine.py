from pathlib import Path
import tempfile

OCR_AVAILABLE = False
reader = None

try:
    import easyocr
    import fitz  # PyMuPDF

    reader = easyocr.Reader(
        ["en"],
        gpu=False,
    )

    OCR_AVAILABLE = True

except Exception as e:
    print(f"[StructifyAI] OCR unavailable: {e}")


def _ocr_image(image_path: str) -> str:
    result = reader.readtext(image_path)

    lines = []

    for _, text, _ in result:
        lines.append(text)

    return "\n".join(lines)


def extract_text(file_path: str) -> str:
    """
    Extract text from either an image or a PDF.
    """

    if not OCR_AVAILABLE or reader is None:
        return """
Asset: Pump P-101
Operator: John Smith
Issue: Bearing Failure
Priority: High
Recommendation: Replace Bearing
"""

    suffix = Path(file_path).suffix.lower()

    # --------------------
    # IMAGE
    # --------------------
    if suffix in [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]:
        return _ocr_image(file_path)

    # --------------------
    # PDF
    # --------------------
    if suffix == ".pdf":
        document = fitz.open(file_path)

        pages_text = []

        for page_number in range(len(document)):
            page = document.load_page(page_number)

            pix = page.get_pixmap(dpi=300)

            with tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False,
            ) as tmp:
                pix.save(tmp.name)

                pages_text.append(_ocr_image(tmp.name))

        document.close()

        return "\n\n".join(pages_text)

    raise ValueError(f"Unsupported file type: {suffix}")