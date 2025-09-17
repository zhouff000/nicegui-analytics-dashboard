import gradio as gr

with open("src/web/static/html/header.html", "r") as header_file:
    header = header_file.read()


history = [
    {
        "role": "assistant",
        "content": "I am happy to provide you that report and plot.",
        "path": "documents/report.pdf",
    },
    {
        "role": "user",
        "content": "Please provide a report and plot for the data I am uploading.",
    },
]


with gr.Blocks(
    theme=gr.themes.Soft(),
) as demo:
    gr.HTML(header,container=True)
    with gr.Tab("发音"):
        gr.Chatbot(
            [
                {
                    "role": "assistant",
                    "content": "I am happy to provide you that report and plot.",
                    "path": "documents/report.pdf",
                },
            ],
            type="messages",
        )
    with gr.Tab("小练习"):
        gr.Chatbot(
            [
                {
                    "role": "user",
                    "content": "Please provide a report and plot for the data I am uploading.",
                },
            ],
            type="messages",
        )

    gr.Textbox(placeholder="Type your message here...", label="Your Message")
    gr.Button("Send")
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
