from nicegui import ui, app
from .config import MENU_ITEMS


def navigation():
    with (
        ui.left_drawer(
            value=True,
            bordered=False,
            elevated=False,
            top_corner=True,
            bottom_corner=True,
        )
        .props("width=260")
        .classes("bg-gradient-to-b from-blue-50 to-blue-100") as drawer
    ):
        # 侧边栏标题区域
        with ui.column().classes("w-full p-6 mb-4"):
            ui.icon("school", size="xl").classes("text-blue-500 mb-2")
            ui.label("教学资源采集").classes(
                "text-xl font-bold text-blue-900 text-center"
            )
            ui.label("系统导航").classes("text-sm text-blue-600 text-center mt-1")

        ui.separator().classes("bg-blue-200 opacity-50")

        # 菜单项容器
        with ui.column().classes("w-full px-4 py-6 gap-2"):
            for name, link in MENU_ITEMS:
                # 扁平圆角卡片式菜单项
                with ui.link(target=link).classes("no-underline w-full"):
                    with ui.row().classes(
                        "items-center gap-3 px-5 py-4 rounded-2xl "
                        "bg-white hover:bg-blue-500 "
                        "shadow-sm hover:shadow-md "
                        "transition-all duration-300 ease-in-out "
                        "hover:scale-105 cursor-pointer "
                        "border border-blue-100 hover:border-blue-500"
                    ):
                        ui.icon("arrow_forward_ios", size="sm").classes(
                            "text-blue-400 group-hover:text-white"
                        ).style("transition: all 0.3s")
                        ui.label(name).classes(
                            "text-gray-700 font-medium hover:text-white"
                        ).style("transition: all 0.3s")

    with ui.header(elevated=True).classes("row items-center justify-between"):
        with ui.row().classes("items-center gap-4"):
            ui.button("≡", on_click=drawer.toggle).classes("ml-2")
            ui.label("重庆师范大学对外汉语教育平台 - 教学资源采集系统").classes(
                "text-h4"
            )

        with ui.row().classes("mr-4 gap-1 items-center"):
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

    return drawer


def header():
    pass


def sidebar():
    pass
