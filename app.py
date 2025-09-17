import gradio as gr
import time


def load_header(path="src/web/static/html/header.html"):
    with open(path, "r") as header_file:
        header = header_file.read()
    return header


def slow_echo(message: str, history: list):
    """
    一个模拟 LLM 响应的函数。
    它会逐字地 "yield" 返回响应，以实现流式输出效果。
    """
    response = ""
    for char in f"You said: {message} " * 10:
        response += char
        # 每 yield 一次，前端的 chatbot 就会更新一次
        yield response
        time.sleep(0.02)


def switch_page():
    return gr.update(visible=False)


with gr.Blocks(
    theme=gr.themes.Soft(),
) as demo:
    gr.HTML(load_header())

    page1 = gr.Column()
    with page1:
        with gr.Tab("发音"):
            gr.ChatInterface(
                fn=slow_echo,
                title=None,
                chatbot=gr.Chatbot(
                    height=600, type="messages"
                ),  # 可以自定义聊天框的高度
                textbox=gr.Textbox(
                    placeholder="问我任何问题...", container=False, scale=7
                ),
                type="messages",
            )
        with gr.Tab("小练习"):
            gr.Image("src/web/static/images/header.png")

    with gr.Sidebar(label="功能切换", position="left"):
        with gr.Column():
            gr.Markdown("## 功能选择")
            gr.Markdown("---")

            page_1 = gr.Button(
                icon="src/web/static/icon/patterns_character_icon_215652.ico",
                value="汉字解析",
                size="lg",
                variant="secondary",
            )
            page_2 = gr.Button(
                value="发音",
                size="lg",
                variant="secondary",
            ).click(
                fn=switch_page,
                inputs=[],
                outputs=[page1],
            )

demo.launch()
