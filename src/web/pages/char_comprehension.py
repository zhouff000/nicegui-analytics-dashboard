from gradio import (
    Column,
    ChatInterface,
    Chatbot,
    Textbox,
)
from src.web.utils.i18n_utils import I18N


def _slow_echo(message: str, history: list):
    return f"You said: {message} " * 10


def char_comprehend_page(i18n: I18N = I18N("locales", "en")):
    with Column() as page:
        ChatInterface(
            fn=_slow_echo,
            title=None,
            chatbot=Chatbot(height=600, type="messages"),  # 可以自定义聊天框的高度
            textbox=Textbox(placeholder="问我任何问题...", container=False, scale=7),
            type="messages",
        )
    return page


if __name__ == "__main__":
    # uv python gradio src/web/pages/char_comprehend.py && cl
    char_comprehend_page().launch()
