import gradio as gr
from src.web.utils.i18n_utils import I18N
from src.web.pages.dashboard.dashboard import dashboard
from src.web.pages.sidebar.sidebar import sidebar
from src.web.pages.char_resolution.char_resolution import char_comprehend_page

i18n = I18N("locales", "zh")


def load_header(path="src/web/static/html/header.html"):
    with open(path, "r") as header_file:
        header = header_file.read()
    return header


def setup_component_interactions(components):
    components["sidebar"]["dashboard"].click(
        fn=lambda: (
            gr.update(visible=True),
            gr.update(open=False),
            gr.update(visible=False),
        ),
        inputs=[],
        outputs=[
            components["dashboard"]["page"],
            components["sidebar"]["sidebar"],
            components["char_resolution"]["page"],
        ],
    )

    components["sidebar"]["character_resolution"].click(
        fn=lambda: (
            gr.update(visible=True),
            gr.update(open=True),
            gr.update(visible=False),
        ),
        inputs=[],
        outputs=[
            components["char_resolution"]["page"],
            components["sidebar"]["sidebar"],
            components["dashboard"]["page"],
        ],
    )

    components["dashboard"]["function_buttons"]["character_resolution_btn"].click(
        fn=lambda: (gr.update(visible=True), gr.update(visible=False)),
        inputs=[],
        outputs=[
            components["char_resolution"]["page"],
            components["dashboard"]["page"],
        ],
    )

    ...


with gr.Blocks(
    theme=gr.themes.Soft(),
    css_paths=["src/web/static/css/home.css"],
) as demo:
    header = gr.HTML(load_header())
    components = {
        "header": header,
        "sidebar": sidebar(i18n),
        "dashboard": dashboard(i18n),
        "char_resolution": char_comprehend_page(i18n),
    }
    setup_component_interactions(components)

demo.launch()
