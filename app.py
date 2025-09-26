from nicegui import app,ui
from src.frontend.pages import dashboard


app.include_router(dashboard.router)

ui.run(
    title="重庆师范大学对外汉语教育大模型 ",
    favicon="📚",
    dark=None,
    reload=True,
)
