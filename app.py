import gradio as gr
from src.web.utils.i18n_utils import I18N
from src.web.pages.dashboard.dashboard import dashboard
from src.web.pages.sidebar import sidebar


i18n = I18N("locales", "zh")


def load_header(path="src/web/static/html/header.html"):
    with open(path, "r") as header_file:
        header = header_file.read()
    return header


def setup_component_interactions(sidebar_interface, home_interface): ...


with gr.Blocks(
    theme=gr.themes.Soft(),
    css_paths=["src/web/static/css/home.css"],
) as demo:
    header = gr.HTML(load_header())

    home_interface = dashboard(i18n)
    sidebar = sidebar(i18n)
    setup_component_interactions(sidebar, home_interface)

demo.launch()
