from nicegui import APIRouter, ui
from ..shared_components.navigation import navigation


router = APIRouter()


@router.page("/hanzi-resolution", title="汉字解析")
def hanzi_resolution_page():
    navigation()
    ui.label("汉字解析页面，正在建设中...").classes("text-h4 font-bold m-5")
