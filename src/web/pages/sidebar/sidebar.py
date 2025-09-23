from gradio import Button, Markdown, Sidebar, Image
from ...utils.i18n_utils import I18N
from .config import _BUTTON_CONFIGS, _STATIC_FILE_MAPPING

__all__ = ["sidebar"]


def sidebar(
    i18n: I18N,
):
    i18n.set_scope("sidebar")
    with Sidebar(position="left", open=True) as sidebar:
        components = {
            "sidebar": sidebar,
            "header_image": None,
            "choose_function_md": None,
            "separator_md_1": None,
            "separator_md_2": None,
            "dashboard": None,
        }
        components["sidebar"] = sidebar
        components["header_image"] = Image(
            _STATIC_FILE_MAPPING["sidebar_header"],
            container=False,
            show_label=False,
            interactive=False,
            show_download_button=False,
            show_fullscreen_button=False,
        )
        components["choose_function_md"] = Markdown(f"## {i18n('choose_function')}")
        components["separator_md_1"] = Markdown("---")
        components["dashboard"] = Button(
            value=i18n("dashboard"),
            size="lg",
            variant="primary",
        )

        components["separator_md_2"] = Markdown("---")

        for cfg in _BUTTON_CONFIGS:
            components[cfg["key"]] = Button(
                value=i18n(cfg["key"]),
                size=cfg["size"],
                variant=cfg["variant"],
            )
    return components


if __name__ == "__main__":
    pass
