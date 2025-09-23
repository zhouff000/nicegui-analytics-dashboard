from gradio import Button, Row
from ...utils.i18n_utils import I18N


__all__ = ["dashboard"]


def dashboard(i18n: I18N):
    i18n.set_scope("home")
    components = {
        "page": None,
        "btn_1": None,
        "btn_2": None,
    }
    with Row() as page:
        components["page"] = page
        btn1 = Button(
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

    return components
