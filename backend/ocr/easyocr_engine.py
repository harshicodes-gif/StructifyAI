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
    """Run OCR on an image."""

    result = reader.readtext(image_path)

    lines = []

    for _, text, _ in result:
        text = text.strip()

        if text:
            lines.append(text)

    return "\n".join(lines)


def _extract_pdf_text(document) -> str:
    """
    Try extracting embedded text from a PDF.

    This is much faster and more accurate than OCR for
    digitally-created PDFs.
    """

    pages = []

    for page in document:
        text = page.get_text("text").strip()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def _ocr_pdf(document) -> str:
    """
    OCR every page of a scanned PDF.
    """

    pages = []

    for page in document:

        pix = page.get_pixmap(dpi=300)

        with tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=True,
        ) as tmp:

            pix.save(tmp.name)

            pages.append(_ocr_image(tmp.name))

    return "\n\n".join(pages)


def extract_text(file_path: str) -> str:
    """
    Extract text from an image or PDF.

    Strategy:

    Images
        -> EasyOCR

    PDFs
        -> Embedded text extraction
        -> OCR fallback
    """

    if not OCR_AVAILABLE or reader is None:

        return """
Document extraction unavailable because OCR is not installed.
"""

    suffix = Path(file_path).suffix.lower()

    # ---------------------------------------------------
    # Images
    # ---------------------------------------------------

    if suffix in {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tif",
        ".tiff",
    }:
        return _ocr_image(file_path)

    # ---------------------------------------------------
    # PDFs
    # ---------------------------------------------------

    if suffix == ".pdf":

        document = fitz.open(file_path)

        try:
            # First try embedded text
            text = _extract_pdf_text(document)

            # If enough text exists, don't OCR
            if len(text.strip()) > 100:
                return text

            # Otherwise OCR
            return _ocr_pdf(document)

        finally:
            document.close()

    raise ValueError(f"Unsupported file type: {suffix}")