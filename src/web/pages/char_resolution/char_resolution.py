from gradio import Column, ChatInterface, Chatbot, Textbox
from ...utils.i18n_utils import I18N
# from src.backend.core.character_comprehension import get_character_response
# from src.backend.core.dataclass import DataSource

__all__ = ["char_comprehend_page"]


def slow_echo(message: str, history: list):
    import time

    full_response = f"This is a placeholder response for {message}."  # Placeholder for actual response logic
    response = ""

    for char in full_response:
        response += char
        time.sleep(0.01)
        yield response

    # full_response = get_character_response(message, "stroke", stream=True, locale="en")
    # response = ""
    # reasoning = "> "
    # if full_response.source == DataSource.DATABASE:
    #     for char in full_response.get_content():
    #         response += char
    #         time.sleep(0.01)
    #         yield response
    # else:
    #     for chunk in full_response.stream_content():
    #         if "reasoning_content" in chunk:
    #             reasoning += chunk["reasoning_content"]
    #             yield response
    #         if "content" in chunk:
    #             response += chunk["content"]
    #             yield reasoning + "\n\n" + response


def char_comprehend_page(i18n: I18N):
    i18n.set_scope("char_resolution")
    components = {
        "page": None,
        "chat_interface": None,
    }
    with Column(visible=False) as page:
        components["page"] = page
        components["chat_interface"] = ChatInterface(
            # visiable=False,
            fn=slow_echo,
            title=None,
            chatbot=Chatbot(
                placeholder="<strong>chatbot_placeholder</strong>", type="messages"
            ),
            textbox=Textbox(
                placeholder=f"{i18n('input_prompt')}",
                container=False,
                scale=3,
            ),
            type="messages",
            fill_height=True,
        )
    return components
