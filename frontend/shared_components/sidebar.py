from nicegui import ui
from .config import MENU_ITEMS


def sidebar():
    with ui.left_drawer(
        value=True,
        bordered=True,
        elevated=True,
        top_corner=True,
        bottom_corner=True,
    ).props("width=250 bordered") as drawer:
        with ui.column().classes("w-full items-center"):
            for name, link in MENU_ITEMS:
                ui.link(name, link).classes(
                    "justify-center"
                    "w-full px-4 py-3 my-1 rounded-lg "
                    "hover:bg-blue-100 hover:text-blue-600 "
                    "transition-colors duration-200 "
                    "text-gray-700"
                )
    with ui.header():
        ui.button("≡", on_click=drawer.toggle())

    # toggle_button.on("click", lambda _: drawer.toggle())
