from nicegui import app, ui
from frontend.pages import dashboard

with open("frontend/static/css/custom_root.css") as f:
    css = f.read()
ui.add_head_html(f"<style>{css}</style>")

app.include_router(dashboard.router)

ui.run(
    title="重庆师范大学对外汉语教育大模型 ",
    favicon="📚",
    dark=False,
    reload=True,
)
