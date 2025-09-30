from nicegui import APIRouter, ui


router = APIRouter()


@ui.page("/character_resolution", title="汉字解析")
def character_resolution_page():
    ui.label("汉字解析页面，正在建设中...").classes("text-h4 font-bold m-5")
