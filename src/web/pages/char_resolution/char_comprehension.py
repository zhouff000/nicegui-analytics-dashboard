from gradio import (
    Column,
    ChatInterface,
    Chatbot,
    Textbox,
)
from ...utils.i18n_utils import I18N

__all__ = ["char_comprehend_page"]


def slow_echo(message: str, history: list):
    return f"You said: {message} " * 10


def char_comprehend_page(i18n: I18N = I18N("locales", "en")):
    with Column() as page:
        ChatInterface(
            fn=slow_echo,
            title=None,
            chatbot=Chatbot(height=600, type="messages"),
            textbox=Textbox(placeholder="问我任何问题...", container=False, scale=7),
            type="messages",
        )
    return page

