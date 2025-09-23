from gradio import Column, Chatbot, MultimodalTextbox
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
        "chatbot": None,
        "textbox": None,
    }
    with Column(visible=False, elem_classes="chat-container") as page:
        components["page"] = page
        components["chatbot"] = Chatbot(
            container=True,
            show_label=False,
            type="messages",
            show_share_button=False,
            elem_classes="chatbot",
        )
        components["textbox"] = MultimodalTextbox(
            file_count="single",
            lines=1,
            placeholder=f"{i18n('input_prompt')}",
            container=True,
            show_label=False,
            submit_btn=True,
            autofocus=True,
        )

    return components
