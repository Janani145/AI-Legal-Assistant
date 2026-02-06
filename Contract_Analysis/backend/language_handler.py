# backend/language_handler.py

from langdetect import detect, DetectorFactory
import argostranslate.translate

DetectorFactory.seed = 0


def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "unknown"


def translate_hindi_to_english(text: str) -> str:
    """
    Offline Hindi → English translation
    Preserves line structure
    """
    translated_lines = []

    for line in text.splitlines():
        if line.strip():
            translated = argostranslate.translate.translate(
                line, "hi", "en"
            )
            translated_lines.append(translated)
        else:
            translated_lines.append("")

    return "\n".join(translated_lines)


def normalize_language(contract_text: str) -> dict:
    detected_lang = detect_language(contract_text)

    if detected_lang == "en":
        return {
            "original_text": contract_text,
            "language": "en",
            "normalized_english_text": contract_text,
            "note": "Original document is already in English"
        }

    if detected_lang == "hi":
        translated_text = translate_hindi_to_english(contract_text)

        return {
            "original_text": contract_text,
            "language": "hi",
            "normalized_english_text": translated_text,
            "note": "Translated from Hindi to English (offline)"
        }

    return {
        "original_text": contract_text,
        "language": detected_lang,
        "normalized_english_text": contract_text,
        "note": "Language detected but translation not applied"
    }


