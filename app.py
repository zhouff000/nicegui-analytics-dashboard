from nicegui import app, ui
from frontend.pages import dashboard,character_resolution
from frontend.utils.css import load_css

# ui.add_head_html(load_css("frontend/static/css/app.css"))

app.include_router(dashboard.router)
app.include_router(character_resolution.router)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="重庆师范大学对外汉语教育大模型 ",
        favicon="📚",
        dark=False,
        reload=True,
        storage_secret="your_secret_key",
    )
