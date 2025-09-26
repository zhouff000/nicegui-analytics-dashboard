from nicegui import ui
from .config import MENU_ITEMS


def sidebar():
    with ui.left_drawer(
        value=True,
        bordered=True,
        elevated=True,
        top_corner=True,
        bottom_corner=True,
    ).props("width=250 bordered"):
        for name, link in MENU_ITEMS:
            ui.link(name, link).classes("block my-2")
