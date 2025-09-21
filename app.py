import gradio as gr
from src.web.utils.i18n_utils import I18N
from src.web.pages.home import home
from src.web.pages.sidebar import sidebar


i18n = I18N("locales", "zh")


def setup_component_interactions(sidebar_interface, home_interface):
    sidebar_interface["character_resolution"].click(
        fn=lambda: gr.update(visible=False),
        inputs=[],
        outputs=[home_interface["page"]],
    )



with gr.Blocks(
    theme=gr.themes.Soft(),
    css_paths=["src/web/static/css/home.css"],
) as demo:
    home_interface = home(i18n)
    sidebar = sidebar(i18n)
    setup_component_interactions(sidebar, home_interface)
demo.launch()
