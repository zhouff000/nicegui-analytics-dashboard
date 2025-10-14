from nicegui import APIRouter, ui
from ..shared_components.sidebar import sidebar


router = APIRouter()


@router.page("/character-resolution", title="汉字解析")
def character_resolution_page():
    sidebar()
    ui.label("汉字解析页面，正在建设中...").classes("text-h4 font-bold m-5")
