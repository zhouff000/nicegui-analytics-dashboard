# -----------------------------------------------------------------------------
# sidebar.py - 网站共享侧边栏导航组件
#
# 职责:
# 1. 创建一个在所有页面左侧固定显示的导航栏。
# 2. 提供清晰的网站标题或Logo。
# 3. 垂直排列到各个主要功能模块的导航链接。
# -----------------------------------------------------------------------------

from nicegui import ui

# 导航菜单项的数据保持不变
MENU_ITEMS = [
    ("汉字解析", "/hanzi"),
    ("语法纠错", "/grammar"),
    ("句子纠错", "/sentence"),
    ("词汇理解", "/vocab"),
    ("对话练习", "/dialogue"),
]


def create_sidebar():
    """创建一个固定在左侧的侧边栏导航"""
    with ui.left_drawer(
        value=True,
        fixed=False,
        bordered=True,
        elevated=True,
        top_corner=True,
        bottom_corner=True,
    ).classes("bg-gray-100 dark:bg-gray-800 w-64"):
        # 侧边栏顶部标题
        with ui.row().classes("w-full p-4 items-center"):
            ui.icon("translate", size="lg", color="primary")
            ui.label("汉风 HanFlow").classes("text-2xl font-semibold")

        ui.separator().classes("my-2")

        # 垂直排列的导航链接
        # 使用 ui.link 更适合导航，它会生成标准的 <a> HTML 标签
        for item_name, target_path in MENU_ITEMS:
            ui.link(item_name, target_path).classes(
                "w-full px-4 py-3 text-lg text-gray-700 dark:text-gray-200 "
                "hover:bg-primary hover:text-white rounded-md"
            )
