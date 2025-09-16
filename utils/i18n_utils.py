import json
import os
from functools import lru_cache


class I18N:
    """
    A class for handling internationalization (i18n).
    It loads all translation files in the specified directory and provides methods to retrieve translated text.
    """

    def __init__(self, locales_dir: str = "locales", default_lang: str = "en"):
        """Initialize the I18N class.

        Args:
            locales_dir (str): Save and load translation JSON files from this directory.
            default_lang (str): language code.
        """
        self.locales_dir = locales_dir
        self.default_lang = default_lang

        self.translations = self._load_translations()
        self.supported_langs = list(self.translations.keys())

        self.lang_code = default_lang
        self.translator = self._get_translator(self.lang_code)

    @lru_cache(maxsize=None)
    def _load_translations(self) -> dict:
        """Private method to scan the locales directory and load all language JSON files."""
        translations = {}
        path = self.locales_dir
        for f in os.listdir(path):
            if f.endswith(".json"):
                lang = os.path.splitext(f)[0]
                with open(os.path.join(path, f), "r", encoding="utf-8") as file:
                    translations[lang] = json.load(file)
        print(f"I18N: Loaded translations: {list(translations.keys())}")
        return translations

    def _get_translator(self, lang_code: str):
        """Private method to get a translator function based on the language code."""
        lang_dict = self.translations.get(
            lang_code, self.translations.get(self.default_lang, {})
        )

        def t(key: str) -> str:
            return lang_dict.get(key, f"<{key}>")

        return t

    def set_lang(self, lang_code: str):
        """
        Set current language by language code.
        If the language code is not supported, it will fall back to the default language.
        """
        if lang_code in self.supported_langs:
            self.lang_code = lang_code
            self.translator = self._get_translator(lang_code)
        else:
            print(
                f"Warning: Unsupported language '{lang_code}'. Falling back to default '{self.default_lang}'."
            )
            self.set_lang(self.default_lang)

    def t(self, key: str) -> str:
        """Get the translated text for the given key in the current language. This is the most commonly used public method.

        Args:
            key (str): The key to be translated.

        Returns:
            str: The translated text.
        """
        return self.translator(key)

    __call__ = t


if __name__ == "__main__":
    i18n = I18N(locales_dir="locales", default_lang="cn-zh")
    print(i18n("goodbye"))