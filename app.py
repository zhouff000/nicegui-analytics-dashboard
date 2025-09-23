import gradio as gr
from src.web.utils.i18n_utils import I18N
from src.web.pages.character_resolution.character_resolution import (
    character_resolution_page,
)

_STATIC_FILE_MAPPING = {
    "sidebar_header": "src/web/static/images/sidebar_header.png",
    "character_resolution": "src/web/static/icon/sidebar_character_icon.ico",
}

_BUTTON_CONFIGS = [
    {
        "key": "character_resolution",
        "icon": "character_resolution",
        "size": "md",
        "variant": "secondary",
        "visible": True,
    },
]


def load_header(path="src/web/static/html/header.html"):
    with open(path, "r") as header_file:
        header = header_file.read()
    return header


with gr.Blocks() as demo:
    i18n = I18N("locales", "")
    i18n.set_scope("dashboard")
    i18n.set_lang("en")

    gr.BrowserState(["lang", "en"])


    gr.HTML(load_header())
    navbar = gr.Navbar(value=None, visible=False)
    with gr.Sidebar() as sidebar:
        gr.Image(
            _STATIC_FILE_MAPPING["sidebar_header"],
            show_label=False,
            interactive=False,
            show_download_button=False,
            show_fullscreen_button=False,
            container=False,
        )
        gr.Markdown(f"## {i18n('choose_function')}")
        gr.Markdown("---")
        gr.Button(
            value=i18n("dashboard"),
            size="lg",
            variant="primary",
        )

        gr.Markdown("---")

        for cfg in _BUTTON_CONFIGS:
            gr.Button(
                link="/character_resolution",
                value=i18n(cfg["key"]),
                size=cfg["size"],
                variant=cfg["variant"],
            )

with demo.route(
    f"{i18n('character_resolution')}",
    "/character_resolution",
):
    character_resolution_page.render()

if __name__ == "__main__":
    demo.launch()
