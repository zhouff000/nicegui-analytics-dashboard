from nicegui import ui
from app.pages.main_page import render_main_content
from app.pages.details_page import render_details_content

def init_routes():
    @ui.page('/')
    async def index():
        await render_main_content()

    @ui.page('/details')
    async def details_all():
        await render_details_content()

    @ui.page('/details/{status}')
    async def details_filter(status: str):
        await render_details_content(status)