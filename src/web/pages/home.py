from gradio import Button, Row, HTML
from src.web.utils.i18n_utils import I18N



def _load_header(path="src/web/static/html/header.html"):
    with open(path, "r") as header_file:
        header = header_file.read()
    return header


def home(i18n: I18N):
    i18n.set_scope("home")
    header = HTML(_load_header())
    with Row() as page:
        btn1 = Button(
            icon="src/web/static/icon/patterns_character_icon.ico",
            value=i18n("welcome_message"),
            size="lg",
            variant="primary",
            elem_classes="home_button",
        )
        btn2 = Button(
            value=i18n("welcome_message"),
            size="lg",
            variant="primary",
            elem_classes="home_button",
        )
    return {"header": header, "page": page, "btn_1": btn1, "btn_2": btn2}
