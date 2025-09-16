import gradio as gr


def char_comprehend_page():
    with gr.Blocks() as page:
        gr.Markdown("### 汉字解析页面")
        gr.Textbox(label="输入汉字")
        gr.Button("解析")
    return page


if __name__ == "__main__":
    # uv python gradio src/web/pages/char_comprehend.py && cl
    char_comprehend_page().launch()
