import gradio as gr
from utils.i18n_utils import I18N
from src.web.pages.home import home_page
from src.web.pages.sidebar import sidebar


def load_header(path="src/web/static/html/header.html"):
    with open(path, "r") as header_file:
        header = header_file.read()
    return header


i18n = I18N("locales", "en")

with gr.Blocks(
    theme=gr.themes.Soft(),
) as demo:
    gr.HTML(load_header())

    home_page = home_page(i18n)
    sidebar = sidebar(i18n, [home_page])

demo.launch()
