from gradio import Button, Markdown, Sidebar
from utils.i18n_utils import I18N

STATIC_FILE_MAPPING = {
    "character": "src/web/static/icon/patterns_character_icon.ico",
    "pronunciation": "src/web/static/icon/patterns_character_icon.ico",
}

# 定义按钮配置表
BUTTON_CONFIGS = [
    {"key": "character_resolution", "icon": "character", "visible": True},
    {"key": "vocabulary_comprehension", "icon": "pronunciation", "visible": False},
    {"key": "grammar_learning", "icon": "pronunciation", "visible": False},
    {"key": "sentence_correction", "icon": "pronunciation", "visible": False},
]


def sidebar(
    i18n: I18N,
):
    i18n.set_scope("sidebar")
    with Sidebar(position="left", open=True) as sidebar:
        registered_components = {}
        Markdown(f"## {i18n('choose_function')}")
        Markdown("---")
        registered_components["home_page"] = Button(
            icon=STATIC_FILE_MAPPING["pronunciation"],
            value=i18n("home_page"),
            size="lg",
            variant="primary",
        )
        Markdown("---")

        registered_components["sidebar"] = sidebar
        for cfg in BUTTON_CONFIGS:
            btn = Button(
                icon=STATIC_FILE_MAPPING[cfg["icon"]],
                value=i18n(cfg["key"]),
                size="md",
                variant="secondary",
            )
            registered_components[cfg["key"]] = btn
    return registered_components


if __name__ == "__main__":
    pass
