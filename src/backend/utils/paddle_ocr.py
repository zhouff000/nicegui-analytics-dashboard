import base64
import requests
from typing import List
import tomllib
import os
from pathlib import Path
from functools import lru_cache

__all__ = [
    "PaddleOCR",
    "call_ocr",
]

# Configuration paths
_PROJECT_CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"
_PADDLE_OCR_CONFIG_PATH = Path(
    os.getenv("PADDLE_OCR_CONFIG_TOML_PATH", _PROJECT_CONFIG_DIR / "config.toml")
)


@lru_cache(maxsize=1)
def _load_paddle_ocr_config() -> dict:
    """Load PaddleOCR configuration from TOML file."""
    try:
        with open(_PADDLE_OCR_CONFIG_PATH, "rb") as f:
            return tomllib.load(f)["paddle_ocr"]
    except (FileNotFoundError, KeyError, tomllib.TOMLDecodeError) as e:
        raise RuntimeError(f"Failed to load PaddleOCR config: {e}")


class PaddleOCR:
    """PaddleOCR client for calling OCR service"""

    def __init__(self, base_url: str = None):
        """
        Initialize OCR client

        Args:
            base_url: Base URL of the OCR service. If None, loads from config.
        """
        if base_url is None:
            config = _load_paddle_ocr_config()
            base_url = config["base_url"]

        self.base_url = base_url.rstrip("/")
        self.ocr_endpoint = f"{self.base_url}/ocr"

    def extract_text_from_file(self, file_path: str, file_type: int = 1) -> List[str]:
        """
        Extract text from image file

        Args:
            file_path: Path to the image file
            file_type: File type, default is 1

        Returns:
            List of extracted text strings

        Raises:
            FileNotFoundError: File does not exist
            requests.RequestException: Network request exception
            ValueError: OCR service returns error
        """
        try:
            with open(file_path, "rb") as file:
                file_bytes = file.read()
                file_data = base64.b64encode(file_bytes).decode("ascii")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            raise
        except Exception as e:
            print(f"Failed to read file: {e}")
            raise

        return self._call_ocr_api(file_data, file_type)[0]

    def extract_text_from_bytes(
        self, image_bytes: bytes, file_type: int = 1
    ) -> List[str]:
        """
        Extract text from image byte data

        Args:
            image_bytes: Image byte data
            file_type: File type, default is 1

        Returns:
            List of extracted text strings
        """
        file_data = base64.b64encode(image_bytes).decode("ascii")
        return self._call_ocr_api(file_data, file_type)

    def _call_ocr_api(self, file_data: str, file_type: int) -> List[str]:
        """
        Call OCR API

        Args:
            file_data: Base64 encoded file data
            file_type: File type

        Returns:
            List of extracted text strings
        """
        payload = {"file": file_data, "fileType": file_type}

        try:
            response = requests.post(self.ocr_endpoint, json=payload, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"OCR API call failed: {e}")
            raise

        try:
            result = response.json()["result"]
            texts = []
            for i, res in enumerate(result["ocrResults"]):
                texts.extend(res["prunedResult"]["rec_texts"])
            return texts
        except (KeyError, TypeError) as e:
            print(f"Failed to parse OCR response: {e}")
            raise ValueError(f"OCR service returned invalid format: {e}")


# Backward compatible function
def call_ocr(
    url: str = "http://10.248.137.210:8080/ocr",
    file_path: str = "src/web/static/test/hupu.png",
) -> List[str]:
    """
    Backward compatible OCR function (deprecated, please use PaddleOCR class)
    """
    base_url = url.replace("/ocr", "")
    ocr_client = PaddleOCR(base_url)
    return ocr_client.extract_text_from_file(file_path)[0]


if __name__ == "__main__":
    # Use class instance
    ocr_client = PaddleOCR()
    try:
        texts = ocr_client.extract_text_from_file("src/web/static/test/hupu.png")
        print("Extracted text:", texts)
    except Exception as e:
        print(f"OCR failed: {e}")
