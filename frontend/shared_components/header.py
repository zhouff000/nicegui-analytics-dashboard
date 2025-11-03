from nicegui import ui, app


def header():
    with ui.header(elevated=True).classes("row items-center justify-between"):
        ui.label("重庆师范大学对外汉语教育平台 - 教学资源采集系统").classes(
            "ml-4 text-h4"
        )
        with ui.row().classes("mr-4 gap-1"):
            ui.link("首页", "/").classes(
                "px-4 py-2 hover:bg-blue-500 rounded-xl text-lg no-underline text-white"
            )
            ui.link("汉字解析", "/hanzi-resolution").classes(
                "px-4 py-2 hover:bg-blue-500 rounded-xl text-lg no-underline text-white"
            )
            with ui.button(icon="menu").classes("ml-4"):
                with ui.menu() as menu:
                    ui.button(
                        f"用户: {app.storage.user.get('username', '访客')}",
                        icon="account_circle",
                    )
                    ui.menu_item(
                        "个人信息", on_click=lambda: ui.notify("个人信息功能待实现")
                    )
                    ui.menu_item(
                        "登出",
                        on_click=lambda: (
                            app.storage.user.clear(),
                            ui.navigate.to("/login"),
                        ),
                    )
                    ui.separator()
                    ui.menu_item("关闭", menu.close)
