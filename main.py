from nicegui import ui
from app.routes.main import init_routes

# 1. 注册路由
init_routes()

# 2. 启动服务（确保不要在 ui.run 里乱填图标名）
ui.run(
    title='师道汉韵管理后台',
    port=8080,
    show=True
)