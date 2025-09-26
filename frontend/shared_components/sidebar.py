from nicegui import ui


def sidebar():
    with ui.left_drawer() as drawer:
        ui.label("导航栏").classes("text-h6")
        ui.link("首页", "/").classes("block my-2")
        ui.link("关于", "/about").classes("block my-2")
        ui.link("物品列表", "/items").classes("block my-2")
    return drawer
