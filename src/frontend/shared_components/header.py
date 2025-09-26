# -----------------------------------------------------------------------------
# header.py - 网站共享页头组件
#
# 职责:
# 1. 创建一个在所有页面顶部显示的导航栏。
# 2. 提供清晰的网站标题或Logo。
# 3. 包含到各个主要功能模块的导航链接。
# -----------------------------------------------------------------------------

from nicegui import ui

# 定义导航链接的菜单项
# 格式为: (显示名称, 路由路径)
# 这样做的好处是便于未来统一修改或增加菜单项
MENU_ITEMS = [
    ("汉字解析", "/hanzi"),
    ("语法纠错", "/grammar"),
    ("句子纠错", "/sentence"),
    ("词汇理解", "/vocab"),
    ("对话练习", "/dialogue"),
]


def create_header():
    """创建一个带有Logo和导航链接的页头"""
    with ui.header(elevated=True).classes(
        "items-center justify-between bg-primary text-white"
    ):
        # 网站标题
        ui.label("汉风 HanFlow").classes("text-2xl font-semibold")

        # 导航链接
        with ui.row(wrap=False).classes("items-center"):
            for item_name, target_path in MENU_ITEMS:
                # 使用 ui.button 创建链接，并通过 on_click 事件导航
                ui.button(
                    item_name, on_click=lambda path=target_path: ui.navigate.to(path)
                ).props("flat color=white text-lg")
