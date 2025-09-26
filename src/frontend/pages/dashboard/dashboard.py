# -----------------------------------------------------------------------------
# dashboard.py - 应用主页，展示统计数据
# -----------------------------------------------------------------------------
from nicegui import ui


@ui.page("/", title="Dashboard - 汉风")
def page_dashboard():
    """定义主页仪表盘的UI布局和内容"""

    # 模拟一些学习数据
    stats = {
        "今日学习时长 (分钟)": 45,
        "本周掌握词汇": 23,
        "累计完成对话": 8,
        "语法练习正确率": "92%",
    }

    with ui.column().classes("w-full max-w-4xl mx-auto items-center gap-8 py-8"):
        ui.label("我的学习仪表盘").classes("text-4xl font-bold text-primary")

        # 使用栅格系统来展示统计卡片
        with ui.grid(columns=4).classes("w-full gap-4"):
            for key, value in stats.items():
                with ui.card().classes("w-full items-center justify-center"):
                    ui.label(key).classes("text-md text-gray-500")
                    ui.label(value).classes("text-4xl font-semibold")

        # 添加一些其他的图表或快速入口
        ui.separator().classes("w-full my-4")
        ui.label("快速开始").classes("text-2xl font-bold")
        with ui.row():
            ui.button(
                "开始汉字解析",
                on_click=lambda: ui.navigate.to("/tools/hanzi"),
                icon="font_download",
            ).props("size=lg")
            ui.button(
                "进行对话练习",
                on_click=lambda: ui.navigate.to("/tools/dialogue"),
                icon="question_answer",
            ).props("size=lg")
