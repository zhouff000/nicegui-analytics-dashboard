from gradio import Button, Row, HTML, Column, Markdown
from ...utils.i18n_utils import I18N
from .config import _BUTTON_CONFIGS

__all__ = ["dashboard"]


def dashboard(i18n: I18N):
    i18n.set_scope("home")
    components = {
        "page": None,
        "function_buttons": {
            "character_resolution_col": None,
            "character_resolution_btn": None,
        },
    }
    with Column() as page:
        components["page"] = page
        components["welcome_message"] = HTML(
            f"<h1 style='font-size: 36px; font-weight: bold;'>{i18n('dashboard')}</h1><p style='font-size: 16px; color: gray;'>{i18n('welcome_message')}</p>"
        )
        components["separator"] = Markdown("---")

        for cfg in _BUTTON_CONFIGS:
            with Row(scale=1, variant="panel") as col:
                components["function_buttons"][f"{cfg['key']}_col"] = col
                components["function_buttons"][f"{cfg['key']}_btn"] = Button(
                    value=i18n(cfg["key"]),
                    size=cfg["size"],
                    variant=cfg["variant"],
                )

    return components
