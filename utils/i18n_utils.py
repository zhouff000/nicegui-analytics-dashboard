import json
import os
from functools import lru_cache


class I18N:
    """
    A class for handling internationalization (i18n).
    It loads all translation files in the specified directory and provides methods to retrieve translated text.
    """

    def __init__(self, locales_dir: str = "locales", default_lang: str = "zh"):
        """Initialize the I18N class.

        Args:
            locales_dir (str): Save and load translation JSON files from this directory.
            default_lang (str): language code.
            scope (str, optional): The scope for translations (e.g., 'login', 'home'). Defaults to None.
        """
        self.locales_dir = locales_dir
        self.default_lang = default_lang
        self.scope = None

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
        # print(f"I18N: Loaded translations: {list(translations.keys())}")
        return translations

    def _get_translator(self, lang_code: str):
        """Private method to get a translator function based on the language code."""
        lang_dict = self.translations.get(
            lang_code, self.translations.get(self.default_lang, {})
        )
        scope_dict = lang_dict.get(self.scope, {}) if self.scope else {}

        def t(key: str) -> str:
            # First, try to get the translation from the specified scope
            if self.scope and key in scope_dict:
                return scope_dict.get(key, f"<{key}>")
            # If not found in scope or no scope is defined, fall back to the global scope
            return lang_dict.get(key, f"<{key}>")

        return t

    def set_scope(self, scope: str):
        """
        Set the scope for translations (e.g., 'login', 'home').
        If the scope is not found in the current language, it will fall back to the global scope.
        """
        if scope == "global":
            self.scope = None
        self.scope = scope
        self.translator = self._get_translator(self.lang_code)

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
    # 1. 初始化一个 i18n 实例，默认语言为中文
    i18n = I18N(locales_dir="locales", default_lang="zh")
    print("--- 默认 (zh) ---")
    print(f"全局 'ok': {i18n('ok')}")

    # 2. 切换作用域到 'login'
    i18n.set_scope("login")
    print("\n--- 切换到 'login' 作用域 (zh) ---")
    print(f"'login' 作用域的 'login_button': {i18n('login_button')}")
    print(f"回退到全局的 'cancel': {i18n('cancel')}")

    # 3. 切换语言到 'en'
    i18n.set_lang("en")
    print("\n--- 保持 'login' 作用域, 切换语言到 'en' ---")
    print(f"'login' 作用域的 'login_button': {i18n('login_button')}")
    print(f"回退到全局的 'cancel': {i18n('cancel')}")

    # 4. 切换到另一个作用域 'sidebar'
    i18n.set_scope("sidebar")
    print("\n--- 切换到 'sidebar' 作用域 (en) ---")
    print(f"'sidebar' 作用域的 'choose_function': {i18n('choose_function')}")

    # 5. 直接通过构造函数创建带作用域的实例
    print("\n--- 直接创建 'home' 作用域实例 (en) ---")
    i18n_home = I18N(locales_dir="locales", default_lang="zh", scope="home")
    i18n_home.set_lang("en")
    print(f"'home' 作用域的 'welcome_message': {i18n_home('welcome_message')}")
