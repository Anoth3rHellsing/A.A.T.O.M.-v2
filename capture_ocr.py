from __future__ import annotations

from PIL import ImageGrab, Image
import pytesseract


def capture_and_ocr(region: tuple[int, int, int, int] | None = None) -> str:
    """Capture the screen and run OCR.

    Parameters
    ----------
    region: tuple[int, int, int, int] | None, optional
        Bounding box (left, upper, right, lower) to capture. If ``None`` the
        entire screen is captured.

    Returns
    -------
    str
        The recognized text.
    """
    # Capture screenshot (full screen if region is None)
    img = ImageGrab.grab(bbox=region)

    # Convert to grayscale and upscale to roughly 300 DPI
    img = img.convert("L")
    scale = 300 / 96  # typical screen DPI
    new_size = (int(img.width * scale), int(img.height * scale))
    img = img.resize(new_size, Image.Resampling.LANCZOS)

    # Run OCR with Spanish and English language models
    text = pytesseract.image_to_string(img, lang="spa+eng")
    return text.strip()


if __name__ == "__main__":
    try:
        captured_text = capture_and_ocr()
        print(captured_text[:500])
    except Exception as exc:
        # Print the exception to help debugging in environments without GUI or OCR
        print(f"Error capturing or processing screen: {exc}")

