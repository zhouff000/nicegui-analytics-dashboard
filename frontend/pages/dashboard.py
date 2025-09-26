from nicegui import APIRouter, ui
from ..shared_components.sidebar import sidebar

router = APIRouter()


@router.page("/")
def home_page():
    sidebar()
    with ui.column().classes("p-4"):
        ui.label("这是首页").classes("text-2xl")
        ui.label("通过 APIRouter 定义的 / 页面")
