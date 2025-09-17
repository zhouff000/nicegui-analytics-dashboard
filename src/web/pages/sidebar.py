from utils.i18n_utils import I18N
from gradio import Sidebar, Column, Markdown, Button, update
from typing import List

STATIC_FILE_MAPPING = {
    "character": "src/web/static/icon/patterns_character_icon.ico",
    "pronunciation": "src/web/static/icon/patterns_character_icon.ico",
}


def sidebar(i18n: I18N, control_component: List = [Column]):
    i18n.set_scope("sidebar")
    with Sidebar(position="left", open=True) as sidebar:
        # with Column():
        Markdown(f"## {i18n('choose_function')}")
        Markdown("---")

        Button(
            icon=STATIC_FILE_MAPPING["character"],
            value=i18n("character_resolution"),
            size="md",
            variant="secondary",
        ).click(
            fn=lambda: update(visible=True),
            inputs=[],
            outputs=control_component,
        )
        Button(
            icon=STATIC_FILE_MAPPING["pronunciation"],
            value=i18n("vocabulary_comprehension"),
            size="md",
            variant="secondary",
        ).click(
            fn=lambda: update(visible=False),
            inputs=[],
            outputs=control_component,
        )
        Button(
            icon=STATIC_FILE_MAPPING["pronunciation"],
            value=i18n("grammar_learning"),
            size="md",
            variant="secondary",
        ).click(
            fn=lambda: update(visible=False),
            inputs=[],
            outputs=control_component,
        )
    return sidebar
