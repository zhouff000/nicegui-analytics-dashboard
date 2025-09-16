import gradio as gr
from src.web.pages.char_comprehend import char_comprehend_page

with open("src/web/static/html/header.html", "r") as header_file:
    header = header_file.read()


history = [
    {"role": "assistant", "content": "I am happy to provide you that report and plot.","path":"documents/report.pdf"},
    {"role": "user", "content": "Please provide a report and plot for the data I am uploading."},
]


with gr.Blocks(
    theme=gr.themes.Soft(),
) as demo:
    gr.HTML(header)

    gr.Chatbot(history, type="messages")

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

demo.launch()
