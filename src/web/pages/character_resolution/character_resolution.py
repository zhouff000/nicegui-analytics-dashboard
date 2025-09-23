from gradio import Column, Chatbot, MultimodalTextbox, Blocks, Navbar
import gradio as gr
from ...utils.i18n_utils import I18N
# from src.backend.core.character_comprehension import get_character_response
# from src.backend.core.dataclass import DataSource


with Blocks() as character_resolution_page:

    i18n = I18N("locales", "zh")
    i18n.set_scope("character_resolution")

    print(gr.BrowserState())
    with Column(visible=True, elem_classes="chat-container") as page:
        navbar = Navbar(visible=False)
        Chatbot(
            container=True,
            show_label=False,
            type="messages",
            show_share_button=False,
            elem_classes="chatbot",
        )
    with Column(visible=True, elem_classes="input-container"):
        MultimodalTextbox(
            lines=1,
            placeholder=f"{i18n('input_prompt')}",
            container=True,
            show_label=False,
            submit_btn=True,
            autofocus=True,
        )
