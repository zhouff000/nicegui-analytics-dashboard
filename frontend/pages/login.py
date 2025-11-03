from typing import Optional
from fastapi.responses import RedirectResponse
from nicegui import APIRouter, app, ui


router = APIRouter()
credentials = {"1": "1", "user2": "pass2"}


def verify_password(plain: str, hashed: str) -> bool:
    return plain == hashed


@router.page("/login")
def login(redirect_to: str = "/") -> Optional[RedirectResponse]:
    def try_login() -> None:
        if username.value in credentials and verify_password(
            password.value, credentials[username.value]
        ):
            app.storage.user.update({"username": username.value, "authenticated": True})
            ui.navigate.to(redirect_to)
        else:
            ui.notify("用户名或密码错误", color="negative")

    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")
    with ui.card().classes("absolute-center w-96"):
        ui.label("请登录").classes("text-lg font-medium self-center mb-2")
        username = ui.input("用户名").on("keydown.enter", try_login)
        password = ui.input("密码", password=True, password_toggle_button=True).on(
            "keydown.enter", try_login
        )
        ui.button("登录", on_click=try_login).props("class=mt-4")
    return None
