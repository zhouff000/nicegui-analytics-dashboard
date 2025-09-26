# -----------------------------------------------------------------------------
# hanzi_analyzer.py - 模块一：汉字解析页面
#
# 职责:
# 1. 定义 "/hanzi" 路由的页面。
# 2. 提供UI界面，让用户可以输入单个汉字并查询。
# 3. 调用业务逻辑层(service)获取汉字数据。
# 4. 将查询结果友好地展示给用户。
# -----------------------------------------------------------------------------

from nicegui import ui
import asyncio


# 导入业务逻辑层的服务。UI层不直接处理数据获取，而是委托给Service层。


async def get_hanzi_details_mock(char: str) -> dict:
    """一个模拟的Service函数，实际应在 analysis_service.py 中实现"""
    await asyncio.sleep(1)  # 模拟网络延迟
    if char == "好":
        return {
            "char": "好",
            "pinyin": "hǎo, hào",
            "radical": "女",
            "strokes": 6,
            "definition": "优点多或使人满意的，与“坏”相对。",
        }
    return {}


@ui.page("/hanzi", title="汉字解析 - 汉风")
def page_hanzi_analyzer():
    # --- 页面状态管理 ---
    # 使用一个字典来存储当前查询的汉字信息，便于UI更新
    result_data = {
        "char": "",
        "pinyin": "",
        "radical": "",
        "strokes": 0,
        "definition": "",
    }

    # --- 核心交互逻辑 ---
    async def analyze_character():
        """点击查询按钮后触发的异步函数"""
        char_to_analyze = input_char.value.strip()

        # 1. 输入验证
        if not char_to_analyze or len(char_to_analyze) > 1:
            ui.notify("请输入一个汉字进行查询！", color="warning")
            return

        # 2. 显示加载状态，并调用Service层获取数据
        spinner.set_visibility(True)
        result_card.set_visibility(False)  # 查询新字时先隐藏旧结果
        try:
            # 这是与后端逻辑交互的关键点
            analysis_result = await get_hanzi_details_mock(char_to_analyze)

            # 3. 更新UI
            if analysis_result:
                result_data.update(analysis_result)
                result_char.set_text(result_data["char"])
                result_pinyin.set_text(f"拼音: {result_data['pinyin']}")
                result_radical.set_text(f"部首: {result_data['radical']}")
                result_strokes.set_text(f"笔画: {result_data['strokes']}")
                result_definition.set_content(f"**释义:** {result_data['definition']}")
                result_card.set_visibility(True)
            else:
                ui.notify(
                    f'未能查询到汉字 "{char_to_analyze}" 的信息。', color="negative"
                )

        except Exception as e:
            print(f"Error fetching Hanzi details: {e}")
            ui.notify("查询时发生网络或服务器错误，请稍后再试。", color="negative")
        finally:
            # 无论成功失败，都隐藏加载动画
            spinner.set_visibility(False)

    # --- UI 界面定义 ---
    with ui.column().classes("w-full max-w-2xl mx-auto items-center gap-8 py-8"):
        ui.label("汉字深度解析").classes("text-4xl font-bold")

        # 输入区域
        with ui.row().classes("w-full items-center justify-center"):
            input_char = (
                ui.input(placeholder="输入单个汉字，如“好”")
                .props("outlined rounded")
                .classes("w-64")
                .on("keydown.enter", analyze_character)
            )
            ui.button("查询", on_click=analyze_character).classes("h-14")

        # 加载动画 (默认隐藏)
        spinner = ui.spinner("dots", size="lg", color="primary").set_visibility(False)

        # 结果展示卡片 (默认隐藏)
        with (
            ui.card()
            .classes("w-full")
            .bind_visibility_from(result_data, "char") as result_card
        ):
            result_char = ui.label().classes("text-8xl font-serif self-center")
            ui.separator()
            with ui.card_section():
                result_pinyin = ui.label().classes("text-xl")
                result_radical = ui.label().classes("text-xl")
                result_strokes = ui.label().classes("text-xl")
                result_definition = ui.markdown().classes("text-lg mt-4")


# --- 业务逻辑层(Service)的占位符 ---
# 提示: 你需要在 app/services/analysis_service.py 中实现真正的逻辑。
# 这里提供一个模拟函数，以便当前文件可以独立理解和运行。


# 在实际代码中，你应该 `from app.services import analysis_service`
# 然后调用 `analysis_service.get_hanzi_details(char)`
