"""Regression tests for ddddocr 1.5.6 constrained probability output."""
from unittest.mock import Mock
import pytest
from Euserv_Renewal import RenewalBot

@pytest.mark.parametrize(
    ("recognized", "expected"),
    [("6+1=", "7"), ("6-6=", "0"), ("6x6=", "36"), ("11+1=", "12"), ("05", "05"), ("", None)],
)
def test_constrained_ocr_decodes_probability_output(recognized, expected):
    chars = list("0123456789+-x/=")
    ocr = Mock()
    # Ordinary classification ignores the configured range in version 1.5.6.
    def classify(image, probability=False):
        if not probability:
            return "pkq8yp"
        return {
            "charsets": chars,
            "probability": [
                [0.99 if candidate == character else 0.001 for candidate in chars]
                for character in recognized
            ],
        }
    ocr.classification.side_effect = classify
    bot = RenewalBot()
    bot._ocr = ocr
    assert bot._solve_captcha_local(b"synthetic-fixture") == expected
    ocr.set_ranges.assert_called_once_with("0123456789+-x/=")
