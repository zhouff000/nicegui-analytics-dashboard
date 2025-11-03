from nicegui import ui, app
from .config import MENU_ITEMS


def navigation():
    """
    统一的导航组件，整合了 header 和 sidebar 的功能
    通过 drawer 和 header 提供一致的导航体验
    """
    # 创建侧边栏抽屉
    with ui.left_drawer(
        value=True,
        bordered=True,
        elevated=True,
        top_corner=True,
        bottom_corner=True,
    ).props("width=250 bordered") as drawer:
        with ui.column().classes("w-full items-center"):
            # 渲染菜单项
            for name, link in MENU_ITEMS:
                ui.link(name, link).classes(
                    "justify-center "
                    "w-full px-4 py-3 my-1 rounded-lg "
                    "hover:bg-blue-100 hover:text-blue-600 "
                    "transition-colors duration-200 "
                    "text-gray-700"
                )

    # 创建顶部导航栏
    with ui.header(elevated=True).classes("row items-center justify-between"):
        # 左侧：抽屉切换按钮和标题
        with ui.row().classes("items-center gap-4"):
            ui.button("≡", on_click=drawer.toggle).classes("ml-2")
            ui.label("重庆师范大学对外汉语教育平台 - 教学资源采集系统").classes(
                "text-h4"
            )

        # 右侧：导航链接和用户菜单
        with ui.row().classes("mr-4 gap-1 items-center"):
            ui.link("首页", "/").classes(
                "px-4 py-2 hover:bg-blue-500 rounded-xl text-lg no-underline text-white"
            )
            ui.link("汉字解析", "/hanzi-resolution").classes(
                "px-4 py-2 hover:bg-blue-500 rounded-xl text-lg no-underline text-white"
            )
            # 用户菜单
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


# 保持向后兼容：提供独立的 header 和 sidebar 函数
def header():
    """向后兼容的 header 函数，建议使用 navigation() 替代"""
    pass


def sidebar():
    """向后兼容的 sidebar 函数，建议使用 navigation() 替代"""
    pass
