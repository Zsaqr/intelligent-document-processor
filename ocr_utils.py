# ocr_utils.py

import os
from typing import Optional

import cv2
import numpy as np
from PIL import Image
import pytesseract
from pytesseract import TesseractError

# ثبيت مسارات Tesseract على ويندوز
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"


def preprocess_image(pil_image: Image.Image) -> np.ndarray:
    """
    Converts a PIL image to an OpenCV format and applies basic preprocessing
    to improve OCR quality.
    """
    # Convert PIL image (RGB) to OpenCV (BGR)
    image = np.array(pil_image)
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Denoise a bit
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Binarization using Otsu threshold
    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh


def ocr_image(pil_image: Image.Image, lang: str = "eng") -> str:
    """
    Runs Tesseract OCR on a PIL image after preprocessing.
    """
    processed = preprocess_image(pil_image)
    config = "--oem 3 --psm 6"

    try:
        text = pytesseract.image_to_string(processed, lang=lang, config=config)
        return text.strip()
    except TesseractError as e:
        # ترجع رسالة نصية بدل ما تبوّظ البرنامج كله
        return f"[OCR ERROR] Could not load language '{lang}'. Details: {e}"


def set_tesseract_cmd(path: Optional[str] = None) -> None:
    """
    Optional helper for Windows: set the Tesseract executable path.
    Example:
        set_tesseract_cmd(r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
    """
    if path:
        pytesseract.pytesseract.tesseract_cmd = path
