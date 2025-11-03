from typing import Optional
from fastapi.responses import RedirectResponse
from nicegui import APIRouter, app, ui
from ..utils.i18n import SUPPORTED_LANGUAGES

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
            # 获取语言代码（从显示名称反向查找）
            lang_code = next(
                (
                    code
                    for code, name in SUPPORTED_LANGUAGES.items()
                    if name == language.value
                ),
                "zh",
            )
            app.storage.user.update(
                {
                    "username": username.value,
                    "authenticated": True,
                    "language": lang_code,
                }
            )
            ui.navigate.to(redirect_to)
        else:
            ui.notify("用户名或密码错误", color="negative")

    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")
    with ui.card().classes("absolute-center w-96"):
        ui.label("请登录").classes("text-lg font-medium self-center mb-2")
        
        current_lang_code = app.storage.user.get("language", "zh")
        current_lang_name = SUPPORTED_LANGUAGES.get(current_lang_code, "中文")

        language = (
            ui.select(
                options=list(SUPPORTED_LANGUAGES.values()),
                value=current_lang_name,
                label="语言 / Language",
            )
            .classes("w-full mb-4")
            .bind_value(app.storage.user, "language")
        )
        username = (
            ui.input("用户名").on("keydown.enter", try_login).classes("w-full mb-4")
        )
        password = (
            ui.input("密码", password=True, password_toggle_button=True)
            .on("keydown.enter", try_login)
            .classes("w-full mb-4")
        )
        ui.button("登录", on_click=try_login).props("class=mt-4")
    return None
