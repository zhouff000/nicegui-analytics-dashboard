from nicegui import ui
import asyncio
import logging
from dataclasses import dataclass
from app.config.constants import BODY_STYLE, PLACEHOLDER_OPTION, MODE_SETTINGS, ACTION_LABELS
from app.components.ui_components import (
    create_header, render_side_menu, create_pie_chart, 
    create_bar_chart, create_statistics_card
)
from app.services.data_service import get_status_statistics, get_summary_statistics

@dataclass
class ViewState:
    """管理首页的交互状态"""
    mode: str = 'home'
    active_view: str = 'home'

async def render_main_content():
    """渲染主页内容，保持原有的布局、装饰和逻辑完全不变"""
    ui.query('body').style(BODY_STYLE)
    client = ui.context.client 
    state = ViewState()
    
    # 引用字典，用于跨作用域操作 UI 元素
    refs = {
        'chart': None, 
        'bar_chart': None, 
        'bar_container': None, 
        'icon_overlay': None, 
        'status_text': None
    }

    async def update_view(new_mode: str, status: str = None) -> None:
        """处理侧边栏点击后的视图切换逻辑"""
        with client: 
            if status:
                ui.run_javascript(f'window.open("/details/{status}", "_blank")')
                return
            
            # 首页重置逻辑
            if new_mode == 'home':
                state.mode, state.active_view = 'home', 'home'
                refs['chart'].options.update(PLACEHOLDER_OPTION)
                refs['bar_container'].set_visibility(False)
                refs['icon_overlay'].set_visibility(True)
                refs['status_text'].text = ACTION_LABELS['home']
                refs['chart'].update()
                left_panel.refresh()
                return

            # 数据同步逻辑
            state.mode = state.active_view = new_mode
            display_name = MODE_SETTINGS.get(new_mode, {}).get('label', '数据')
            refs['status_text'].text = ACTION_LABELS['sync'].format(display_name)
            
            try:
                loop = asyncio.get_event_loop()
                # 异步执行耗时查询
                func = lambda: get_status_statistics(status) if new_mode == 'status' else get_summary_statistics()
                raw_data = await loop.run_in_executor(None, func)
                
                # 更新图表配置
                refs['chart'].options.update(create_pie_chart(
                    raw_data, 
                    inner_radius='40%' if new_mode == 'status' else '25%', 
                    is_rose=(new_mode == 'summary')
                ))
                refs['bar_chart'].options.update(create_bar_chart(raw_data))
                
                refs['bar_container'].set_visibility(True)
                refs['icon_overlay'].set_visibility(False)
                refs['status_text'].text = ACTION_LABELS['done'].format(display_name)
            except Exception as e:
                logging.error(f"View update failed: {e}")
                ui.notify('终端连接超时，请重试', type='negative')
                await update_view('home')
            
            refs['chart'].update()
            refs['bar_chart'].update()
            left_panel.refresh()

    # --- 布局编排 (保持原 class 样式字符串不动) ---
    create_header(on_home_click=lambda: update_view('home'))
    
    with ui.row().classes('w-full max-w-7xl mx-auto mt-28 p-8 gap-12 justify-between items-start'):
        @ui.refreshable
        def left_panel(): 
            render_side_menu(state.mode, update_view, active_view=state.active_view)
        
        left_panel()

        # 右侧容器
        with ui.column().classes('flex-1 gap-8'):
            # 1. 创建统计卡片
            sum_refs = create_statistics_card(
                placeholder_option=PLACEHOLDER_OPTION,
                title='解析记录', 
                sub_title='SUMMARY STATS', 
                icon='pie_chart', 
                is_active=True, 
                on_click=lambda: update_view('summary'),
                view_all_text='' 
            )

            # 【重要修正】：refs.update 必须和 sum_refs 在同一个缩进层级
            # 确保它在 with ui.column() 内部执行
            refs.update(sum_refs)

    # 【重要修正】：ui.timer 应该在 render_main_content 函数的最末尾
    # 确保它在 with ui.row() 布局完成后启动
    #ui.timer(0.1, lambda: update_view('summary'), once=True)