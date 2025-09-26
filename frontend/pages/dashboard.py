from nicegui import APIRouter, ui
from ..shared_components.sidebar import sidebar

router = APIRouter()



@router.page("/")
def home_page():
    sidebar()

    with ui.column():
        ui.label("仪表盘").classes("ml-5 mt-6 text-h4 font-bold")
        ui.label("欢迎回来！开始今天的汉语学习之旅吧。").classes(
            "ml-5 text-h5 font-medium text-gray-500"
        )

    # 统计数据卡片
    with ui.row().classes("w-full p-8 gap-6"):
        # 学习时长卡片
        with ui.card().classes(
            "flex-1 rounded-3xl shadow-lg hover:shadow-xl transition-all duration-300 p-6"
        ):
            with ui.row().classes("items-center gap-4"):
                ui.icon("schedule", color="primary").classes("text-4xl")
                with ui.column().classes("gap-1"):
                    ui.label("7.5 小时").classes("text-2xl font-bold")
                    ui.label("本周学习时长").classes("text-gray-500")

        # 已掌握词汇卡片
        with ui.card().classes(
            "flex-1 rounded-3xl shadow-lg hover:shadow-xl transition-all duration-300 p-6"
        ):
            with ui.row().classes("items-center gap-4"):
                ui.icon("library_books", color="primary").classes("text-4xl")
                with ui.column().classes("gap-1"):
                    ui.label("280").classes("text-2xl font-bold")
                    ui.label("已掌握词汇").classes("text-gray-500")

        # 对话练习卡片
        with ui.card().classes(
            "flex-1 rounded-3xl shadow-lg hover:shadow-xl transition-all duration-300 p-6"
        ):
            with ui.row().classes("items-center gap-4"):
                ui.icon("chat", color="primary").classes("text-4xl")
                with ui.column().classes("gap-1"):
                    ui.label("12 次").classes("text-2xl font-bold")
                    ui.label("对话练习").classes("text-gray-500")
    ui.separator()
    # 快速开始区域
    with ui.column().classes("w-full px-8"):
        ui.label("快速开始").classes("text-h5 font-bold mb-4")

        with ui.row().classes("w-full gap-6"):
            # 新的情景对话卡片
            with ui.card().classes(
                "flex-1 rounded-3xl shadow-lg hover:translate-y-1 hover:shadow-xl transition-all duration-300 p-6 cursor-pointer"
            ):
                ui.icon("chat_bubble", color="primary").classes("text-4xl mb-4")
                ui.label("新的情景对话").classes("text-xl font-bold mb-2")
                ui.label(
                    "选择一个校园生活场景，与AI进行实时对话，提升你的口语交流能力。"
                ).classes("text-gray-600 mb-4")
                with ui.row().classes("items-center gap-2 text-primary cursor-pointer"):
                    ui.label("开始练习").classes("font-medium")
                    ui.icon("arrow_forward")

            # 复习今日词汇卡片
            with ui.card().classes(
                "flex-1 rounded-3xl shadow-lg hover:translate-y-1 hover:shadow-xl transition-all duration-300 p-6 cursor-pointer"
            ):
                ui.icon("book", color="primary").classes("text-4xl mb-4")
                ui.label("复习今日词汇").classes("text-xl font-bold mb-2")
                ui.label(
                    "根据艾宾浩斯遗忘曲线，智能复习今天应该掌握的词汇和短语。"
                ).classes("text-gray-600 mb-4")
                with ui.row().classes("items-center gap-2 text-primary cursor-pointer"):
                    ui.label("开始复习").classes("font-medium")
                    ui.icon("arrow_forward")

            # 提交作文批改卡片
            with ui.card().classes(
                "flex-1 rounded-3xl shadow-lg hover:translate-y-1 hover:shadow-xl transition-all duration-300 p-6 cursor-pointer"
            ):
                ui.icon("edit", color="primary").classes("text-4xl mb-4")
                ui.label("提交作文批改").classes("text-xl font-bold mb-2")
                ui.label(
                    "上传你的中文作文，AI将从语法、词汇和流畅度等方面为你提供修改建议。"
                ).classes("text-gray-600 mb-4")
                with ui.row().classes("items-center gap-2 text-primary cursor-pointer"):
                    ui.label("开始写作").classes("font-medium")
                    ui.icon("arrow_forward")
