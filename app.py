import gradio as gr
from src.web.pages.char_comprehend import char_comprehend_page

with open("src/web/static/html/header.html", "r") as header_file:
    header = header_file.read()


def switch_page(gradio_page):
    gradio_page.update(visible=True)


with gr.Blocks(
    theme=gr.themes.Soft(),
) as demo:
    gr.HTML(header)

    with gr.Sidebar(label="功能切换", position="left"):
        with gr.Column():
            gr.Markdown("## 大模型在线体验平台")
            gr.Markdown("---")

            page = gr.Button(
                icon="src/web/static/icon/patterns_character_icon_215652.ico",
                value="汉字解析",
                size="lg",
                variant="secondary",
            )
            gr.Button(
                icon="src/web/static/icon/patterns_character_icon_215652.ico",
                value="词汇理解",
                size="lg",
                variant="secondary",
            )
            gr.Button(
                icon="src/web/static/icon/patterns_character_icon_215652.ico",
                value="语法学习",
                size="lg",
                variant="secondary",
            )
            gr.Button(
                icon="src/web/static/icon/patterns_character_icon_215652.ico",
                value="句子纠错",
                size="lg",
                variant="secondary",
            )
            gr.Button(
                icon="src/web/static/icon/patterns_character_icon_215652.ico",
                value="汉语对话",
                size="lg",
                variant="secondary",
            )
        char = char_comprehend_page()
        page.click(fn=switch_page, inputs=char, outputs=char)

demo.launch()
