from gradio import (
    Column,
    Markdown,
)
from utils.i18n_utils import I18N


def home_page(i18n: I18N):
    i18n.set_scope("home")
    with Column() as page:
        Markdown(f"# {i18n('welcome_message')}")
        Markdown(f"## {i18n('choose_function')}")
    # print(type(page))
    return page
