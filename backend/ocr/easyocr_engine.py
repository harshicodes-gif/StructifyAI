from pathlib import Path
import tempfile
import traceback

OCR_AVAILABLE = False
reader = None
fitz = None

try:
    import easyocr
    import fitz  # PyMuPDF

    print("=" * 80)
    print("[StructifyAI] Initializing EasyOCR...")
    print("=" * 80)

    reader = easyocr.Reader(
        ["en"],
        gpu=False,
    )

    OCR_AVAILABLE = True

    print("=" * 80)
    print("[StructifyAI] EasyOCR initialized successfully.")
    print("=" * 80)

except Exception:
    print("=" * 80)
    print("[StructifyAI] OCR INITIALIZATION FAILED")
    traceback.print_exc()
    print("=" * 80)


def _ocr_image(image_path: str) -> str:
    """Run OCR on an image."""

    if reader is None:
        raise RuntimeError("EasyOCR reader is not initialized.")

    result = reader.readtext(image_path)

    lines = []

    for _, text, _ in result:
        text = text.strip()

        if text:
            lines.append(text)

    return "\n".join(lines)


def _extract_pdf_text(document) -> str:
    """
    Extract embedded text from a digital PDF.
    """

    pages = []

    for page in document:
        text = page.get_text("text").strip()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def _ocr_pdf(document) -> str:
    """
    OCR scanned PDF pages.
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
    Extract text from images and PDFs.

    Images
        -> EasyOCR

    PDFs
        -> Embedded text
        -> OCR fallback
    """

    if not OCR_AVAILABLE or reader is None:
        return (
            "Document extraction unavailable because OCR failed to initialize.\n"
            "Check the Streamlit logs for the initialization error."
        )

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

            text = _extract_pdf_text(document)

            # Digital PDF
            if len(text.strip()) > 100:
                return text

            # Scanned PDF
            return _ocr_pdf(document)

        finally:
            document.close()

    raise ValueError(f"Unsupported file type: {suffix}")
