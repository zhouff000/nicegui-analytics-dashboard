# -----------------------------------------------------------------------------
# main.py - 应用主入口
#
# 职责:
# 1. 初始化应用配置。
# 2. 加载并应用全局样式/主题。
# 3. 注册并显示所有跨页面共享的UI组件 (如页头、页脚)。
# 4. 导入所有独立的页面模块，以便NiceGUI的路由能够发现它们。
# 5. 启动Web服务。
# -----------------------------------------------------------------------------

import os
from nicegui import app, ui

# 导入项目内的模块
# 使用绝对路径导入，确保代码在不同环境下都能正确找到模块
# from app.core import config

from src.frontend.shared_components.sidebar import create_sidebar

# --- 关键步骤：导入所有页面模块 ---
# 尽管这里看起来这些导入的变量没有被直接使用，但这一步是必须的。
# 导入操作会执行每个页面文件中的代码，从而使得 @ui.page 装饰器能够被执行，
# 进而向NiceGUI注册好各个页面的路由。
from src.frontend.pages.character_resolution.character_resolution import (
    page_hanzi_analyzer,
)

# 1. 应用全局主题
# 在所有UI元素被创建之前，首先调用主题设置函数。
# theme.apply_theme()

# 2. 创建共享的UI布局
# 在这里创建的UI元素会出现在每一个页面上。
# 我们将页头作为一个全局共享组件。
# header.create_header()
create_sidebar()
# sidebar()

# 3. 添加页面容器
# 这个容器是必须的，它会作为“占位符”，
# NiceGUI 会将当前访问路由对应的页面内容动态渲染到这个容器中。
# ui.page_container()


# 4. 启动应用服务器
if __name__ in {"__main__", "__mp_main__"}:
    # 注册静态文件目录，这样CSS, JS, 图片等文件才能被浏览器访问
    # 第一个参数是URL路径，第二个参数是本地文件夹路径
    # app.add_static_files("/static", "app/static")

    # 运行NiceGUI应用
    ui.run(
        # 网站标题，会显示在浏览器标签页上
        title="AI-Powered Han-Learning Platform",
        # 从配置文件中读取用于保护用户会session的密钥，非常重要！
        # storage_secret=config.STORAGE_SECRET,
        # 设置网站图标 (可以是emoji, URL, 或者本地文件路径)
        favicon="📚",
        # 设置主题模式，None 表示自动跟随系统设置 (亮色/暗色)
        dark=None,
        # 设置应用运行的端口，可以通过环境变量配置，便于部署
        port=int(os.getenv("PORT", 8080)),
        # 在生产环境中建议设置为 False，可以提升性能
        reload=True,
    )
