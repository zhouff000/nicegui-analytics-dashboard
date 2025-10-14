from nicegui import APIRouter, ui
from ..shared_components.sidebar import sidebar
from ..utils.i18n import I18N

router = APIRouter()

i18n = I18N()
i18n.set_scope("dashboard")

CARD_BASE = (
    "flex-1 rounded-3xl shadow-lg hover:shadow-xl transition-all duration-300 p-6"
)
CARD_INTERACTIVE = f"{CARD_BASE} hover:translate-y-1 cursor-pointer"

ICON_LARGE = "text-4xl mb-4"

TEXT_TITLE = "text-xl font-bold mb-2"
TEXT_DESCRIPTION = "text-gray-600 mb-4"
TEXT_LINK = "items-center gap-2 text-primary cursor-pointer"


def stat_card(icon: str, value: str, label: str):
    with ui.card().classes(
        "flex-1 rounded-3xl shadow-lg hover:shadow-xl transition-all duration-300 p-6"
    ):
        with ui.row().classes("items-center gap-4"):
            ui.icon(icon, color="primary").classes("text-4xl")
            with ui.column().classes("gap-1"):
                ui.label(value).classes("text-2xl font-bold")
                ui.label(label).classes("text-gray-500")


def action_card(icon: str, title: str, description: str, action_text: str = "开始"):
    with ui.card().classes(
        "flex-1 rounded-3xl shadow-lg hover:translate-y-1 hover:shadow-xl transition-all duration-300 p-6 cursor-pointer"
    ):
        ui.icon(icon, color="primary").classes("text-4xl mb-4")
        ui.label(title).classes("text-xl font-bold mb-2")
        ui.label(description).classes("text-gray-600 mb-4")
        with ui.row().classes("items-center gap-2 text-primary cursor-pointer"):
            ui.label(action_text).classes("font-medium")
            ui.icon("arrow_forward")


@router.page("/")
def dashboard_page():
    sidebar()
    with ui.column():
        ui.label(i18n("dashboard")).classes("ml-5 mt-6 text-h4 font-bold")
        ui.label(i18n("welcome_message")).classes(
            "ml-5 text-h5 font-medium text-gray-500"
        )

    with ui.row().classes("w-full p-8 gap-6"):
        stat_card("schedule", "7.5 小时", "本周学习时长")
        stat_card("library_books", "280", "已掌握词汇")
        stat_card("chat", "12 次", "对话练习")

    ui.separator()

    with ui.column().classes("w-full px-8"):
        ui.label(i18n("quickstart")).classes("text-h5 font-bold mb-4")

        with ui.row().classes("w-full gap-6"):
            action_card(
                "chat_bubble",
                "新的情景对话",
                "选择一个校园生活场景,与AI进行实时对话,提升你的口语交流能力。",
                "开始练习",
            )
            action_card(
                "book",
                "复习今日词汇",
                "根据艾宾浩斯遗忘曲线,智能复习今天应该掌握的词汇和短语。",
                "开始复习",
            )
            action_card(
                "edit",
                "提交作文批改",
                "上传你的中文作文,AI将从语法、词汇和流畅度等方面为你提供修改建议。",
                "开始写作",
            )
