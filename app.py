from nicegui import app, ui
from frontend.pages import dashboard, character_resolution, login
from frontend.shared_components.authmiddleware import AuthMiddleware

app.add_middleware(AuthMiddleware)
app.include_router(login.router)
app.include_router(dashboard.router)
app.include_router(character_resolution.router)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="重庆师范大学对外汉语教育大模型 ",
        favicon="📚",
        dark=False,
        reload=True,
        storage_secret="sadfafa",
    )
