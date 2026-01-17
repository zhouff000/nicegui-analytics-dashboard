from nicegui import ui
import asyncio
import logging
from dataclasses import dataclass
from typing import Dict, Any
from constants import BODY_STYLE, PLACEHOLDER_OPTION, MODE_SETTINGS
from components import (
    create_header, render_side_menu, create_pie_chart,
    create_bar_chart, create_statistics_card
)
from services import get_status_statistics, get_summary_statistics

logging.basicConfig(level=logging.INFO)

@dataclass
class ViewState:
    """结构化管理页面状态"""
    mode: str = 'home'          # 控制左侧菜单展开/收缩
    active_view: str = 'home'   # 控制右侧实际展示的数据维度

# 1. 应用全局样式
ui.query('body').style(BODY_STYLE)

def create_ui():
    client = ui.context.client 
    state = ViewState()
    
    # 引用字典（已移除 reset_btn，因为它不再需要从外部控制）
    refs: Dict[str, Any] = {
        'chart': None, 
        'bar_chart': None, 
        'bar_container': None,
        'icon_overlay': None, 
        'status_text': None
    }

    async def update_view(new_mode: str) -> None:
        """核心路由控制逻辑"""
        with client: 
            # --- 场景 A: 彻底重置 (点击左侧返回按钮) ---
            if new_mode == 'home':
                state.mode = 'home'
                state.active_view = 'home'
                
                # 清理图表
                refs['chart'].options.clear()
                refs['chart'].options.update(PLACEHOLDER_OPTION)
                refs['bar_container'].set_visibility(False)
                refs['icon_overlay'].set_visibility(True)
                refs['status_text'].text = '等待系统指令加载数据视图'
            
            # --- 场景 B: 二次点击已展开卡片 (仅收缩菜单，保留图表) ---
            elif new_mode == state.mode:
                state.mode = 'home' 
                display_name = MODE_SETTINGS.get(state.active_view, {}).get('label', '')
                refs['status_text'].text = f'✨ 视图锁定：当前正在分析{display_name}'
            
            # --- 场景 C: 加载新维度数据 ---
            else:
                state.mode = new_mode
                state.active_view = new_mode
                display_name = MODE_SETTINGS.get(new_mode, {}).get('label', '数据')
                refs['status_text'].text = f'正在同步{display_name}数据中心...'
                
                try:
                    # 异步获取业务数据
                    loop = asyncio.get_event_loop()
                    fetch_func = get_status_statistics if new_mode == 'status' else get_summary_statistics
                    raw_data = await loop.run_in_executor(None, fetch_func)
                    
                    # 更新图表
                    pie_config = create_pie_chart(
                        raw_data, 
                        inner_radius='40%' if new_mode == 'status' else '25%',
                        is_rose=(new_mode == 'summary')
                    )
                    refs['chart'].options.clear()
                    refs['chart'].options.update(pie_config)
                    
                    refs['bar_chart'].options.clear()
                    refs['bar_chart'].options.update(create_bar_chart(raw_data))
                    
                    # 显隐控制
                    refs['bar_container'].set_visibility(True)
                    refs['icon_overlay'].set_visibility(False)
                    refs['status_text'].text = f'分析完成：当前展示{display_name}'
                    
                except Exception as e:
                    logging.error(f"Sync error: {e}")
                    ui.notify('终端连接超时', type='negative')
                    await update_view('home')

            # 统一刷新图表与左侧面板
            if refs['chart']: refs['chart'].update()
            if refs['bar_chart']: refs['bar_chart'].update()
            left_panel.refresh() 

    # --- UI 渲染布局 ---
    
    create_header(on_home_click=lambda: update_view('home'))

    with ui.row().classes('w-full max-w-7xl mx-auto mt-28 p-8 gap-12 justify-between items-start'):
        
        # 左侧导航：传入 active_view 供智能显示逻辑判断
        @ui.refreshable
        def left_panel():
            render_side_menu(state.mode, update_view, active_view=state.active_view)
        
        left_panel()

        # 右侧统计卡片
        card_refs = create_statistics_card(
            placeholder_option=PLACEHOLDER_OPTION
        )
        
        refs.update(card_refs)

# 启动
if __name__ in {"__main__", "__mp_main__"}:
    create_ui()
    ui.run(title='师道汉韵·管理终端', port=8080)