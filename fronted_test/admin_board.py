"""
文件职责：
    本项目管理端（Admin Dashboard）的主入口文件，负责定义 Web 路由、页面布局及交互逻辑。
核心功能：
    1. 仪表盘展示：通过 ECharts 实现状态分布（饼图）与数据趋势（柱状图）的可视化。
    2. 实时交互：基于 NiceGUI 的事件驱动机制，实现侧边栏切换、异步数据加载及 UI 局部刷新。
    3. 数据管理：提供带分页、搜索、状态过滤功能的解析记录详情表格。
    4. 异步处理：利用 asyncio 和线程池执行器（run_in_executor）处理耗时的数据查询，确保前端界面不卡顿。
"""

from nicegui import ui
import asyncio
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional
from constants import (
    BODY_STYLE, PLACEHOLDER_OPTION, MODE_SETTINGS, TABLE_COLUMNS, 
    STATUS_MAP, DETAILS_HEAD_HTML, LAYOUT_CONFIG, ACTION_LABELS
)
from components import (
    create_header, render_side_menu, create_pie_chart,
    create_bar_chart, create_statistics_card
)
from services import get_status_statistics, get_summary_statistics, get_cleaned_data

# 配置全局日志
logging.basicConfig(level=logging.INFO)

@dataclass
class ViewState:
    """
    视图状态管理类。
    mode: 当前业务模式（home-初始, status-状态分布, summary-汇总统计）。
    active_view: 侧边栏当前选中的菜单项 ID。
    """
    mode: str = 'home'
    active_view: str = 'home'

@ui.page('/')
async def main_page():
    """
    功能：渲染管理端主仪表盘页面。
    流程：初始化状态对象 -> 构建响应式布局 -> 定义视图更新回调 -> 挂载组件。
    """
    ui.query('body').style(BODY_STYLE)
    client = ui.context.client 
    state = ViewState()
    
    # 存储 UI 元素引用的字典，便于在异步函数中跨作用域操作
    refs = {
        'chart': None, 
        'bar_chart': None, 
        'bar_container': None, 
        'icon_overlay': None, 
        'status_text': None
    }

    async def update_view(new_mode: str, status: str = None) -> None:
        """
        功能：处理视图切换逻辑，包括状态重置、异步数据加载及图表更新。
        入参：
            - new_mode (str): 目标模式标识符。
            - status (str, optional): 若传入此值，则视为跳转至详情页的指令。
        出参：None
        """
        with client: 
            # 外部跳转逻辑：如果带有 status 参数，则在新标签页打开详情视图
            if status:
                ui.run_javascript(f'window.open("/details/{status}", "_blank")')
                return
            
            # 逻辑 1：状态重置（返回首页）
            if new_mode == 'home':
                state.mode, state.active_view = 'home', 'home'
                refs['chart'].options.update(PLACEHOLDER_OPTION) # 恢复占位图表
                refs['bar_container'].set_visibility(False)     # 隐藏副图表
                refs['icon_overlay'].set_visibility(True)      # 显示装饰图层
                refs['status_text'].text = ACTION_LABELS['home']
                refs['chart'].update()
                left_panel.refresh()                           # 刷新侧边栏选中状态
                return

            # 逻辑 2：数据异步加载与视图切换
            state.mode = state.active_view = new_mode
            display_name = MODE_SETTINGS.get(new_mode, {}).get('label', '数据')
            refs['status_text'].text = ACTION_LABELS['sync'].format(display_name)
            
            try:
                loop = asyncio.get_event_loop()
                # 复杂逻辑：使用线程池执行数据库查询 func，避免阻塞 Web 服务的异步主事件循环
                func = lambda: get_status_statistics(status) if new_mode == 'status' else get_summary_statistics()
                raw_data = await loop.run_in_executor(None, func)
                
                # 更新主饼图：根据模式调整内环半径及南丁格尔玫瑰图属性
                refs['chart'].options.update(create_pie_chart(
                    raw_data, 
                    inner_radius='40%' if new_mode == 'status' else '25%', 
                    is_rose=(new_mode == 'summary')
                ))
                # 更新辅助柱状图
                refs['bar_chart'].options.update(create_bar_chart(raw_data))
                
                # UI 状态映射：切换容器可见性
                refs['bar_container'].set_visibility(True)
                refs['icon_overlay'].set_visibility(False)
                refs['status_text'].text = ACTION_LABELS['done'].format(display_name)
            except Exception as e:
                # 异常处理：接口调用失败时回退至首页并弹出提示，确保页面不处于持续 Loading 或错乱状态
                logging.error(f"View update failed: {e}")
                ui.notify('终端连接超时，请重试', type='negative')
                await update_view('home')
            
            # 手动触发 ECharts 渲染更新
            refs['chart'].update()
            refs['bar_chart'].update()
            left_panel.refresh()

    # 布局构建
    create_header(on_home_click=lambda: update_view('home'))
    with ui.row().classes('w-full max-w-7xl mx-auto mt-28 p-8 gap-12 justify-between items-start'):
        @ui.refreshable
        def left_panel(): 
            render_side_menu(state.mode, update_view, active_view=state.active_view)
        
        left_panel()
        # 统计卡片组件会返回内部生成的图表对象引用
        refs.update(create_statistics_card(placeholder_option=PLACEHOLDER_OPTION))

@ui.page('/details/{status}', title='解析记录视图 | 师道汉韵') 
@ui.page('/details', title='解析记录全量视图 | 师道汉韵')    
async def details_page(status: str = None):
    """
    功能：渲染数据详情表格页面。
    入参：
        - status (str, optional): 路由参数，用于根据特定状态过滤初始数据。
    """
    ui.query('body').style(BODY_STYLE)
    ui.add_head_html(DETAILS_HEAD_HTML)

    with ui.column().classes('w-full p-8 gap-6 items-center'):
        with ui.card().classes('w-full max-w-7xl p-8 rounded-[30px] shadow-2xl bg-white border-none overflow-hidden'):
            # 顶部标题栏区域
            with ui.row().classes('w-full items-center justify-between mb-8'):
                with ui.row().classes('items-center gap-4'):
                    ui.element('div').classes('w-1.5 h-8 bg-blue-600 rounded-full')
                    with ui.column().classes('gap-1'):
                        ui.label('解析记录详情').classes('text-3xl font-black text-slate-800')
                        total_label = ui.label('DATABASE TOTAL: LOADING...').classes('text-[11px] text-blue-500/70 font-bold tracking-widest')
                with ui.row().classes('gap-3 items-center'):
                    search_input = ui.input(placeholder='检索词条...').props('rounded outlined dense').classes('w-80')
                    ui.button('导出 Excel', icon='download').props('elevated').classes('bg-blue-600 text-white px-6')

            # 表格主体：定义插槽逻辑
            table = ui.table(columns=TABLE_COLUMNS, rows=[], row_key='id').classes('w-full border-none shadow-none').props('flat no-data-label=" 暂无数据..." loading-label="正在努力加载中..." ')
            
            # 复杂前端样式：根据状态文本进行条件色块映射（使用 Quasar 样式语法）
            table.add_slot('body-cell-status', '''<q-td :props="props" class="text-center"><span :style="{'background-color': props.value?.includes('发布') ? '#ecfdf5' : props.value?.includes('拒绝') ? '#fef2f2' : props.value?.includes('审核') ? '#fff7ed' : '#f1f5f9', 'color': props.value?.includes('发布') ? '#059669' : props.value?.includes('拒绝') ? '#dc2626' : props.value?.includes('审核') ? '#d97706' : '#64748b', 'border': '1px solid currentColor', 'padding': '4px 12px', 'border-radius': '8px', 'font-weight': 'bold', 'display': 'inline-block', 'font-size': '12px', 'min-width': '80px'}">{{ props.value }}</span></q-td>''')
            table.add_slot('body-cell-actions', '''<q-td :props="props" class="text-center"><q-btn flat round color="blue-6" icon="manage_search" @click="$parent.$emit('view_details', props.row)"><q-tooltip class="bg-blue-800 text-white">查看解析详情</q-tooltip></q-btn></q-td>''')

            # 分页控件区域
            with ui.row().classes('w-full justify-end mt-8 items-center gap-4 px-4'):
                pagination = ui.pagination(min=1, max=1, direction_links=True).props('flat color=blue-7 size=md active-design=outline max-pages=5')
                with ui.row().classes('items-center gap-2 text-slate-500'):
                    ui.label('跳至').classes('text-sm')
                    jump_input = ui.number(value=1).props('outlined dense hide-bottom-space').classes('w-14 h-8 text-center bg-white')
                    ui.label('页').classes('text-sm')

    # 信号量控制，防止由于并发导致的分页请求抖动
    loading_lock = False

    async def load_data(page: int = 1):
        """
        功能：执行分页数据获取及表格更新。
        入参：page (int): 目标页码。
        """
        nonlocal loading_lock
        if loading_lock:
            return
        
        # 简单入参校验
        try:
            target_page = int(page)
        except (ValueError, TypeError):
            target_page = 1

        try:
            loading_lock = True
            table.props('loading') 
            table.update()
            
            # 获取后端清理后的结构化数据
            result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: get_cleaned_data(page=target_page, status=status)
            )
            
            # 复杂逻辑：补全前端连续序号（index_id = (当前页-1) * 每页数量 + 行索引 + 1）
            page_size = LAYOUT_CONFIG.get('PAGE_SIZE', 15)
            for i, row in enumerate(result['rows']):
                row['index_id'] = (target_page - 1) * page_size + i + 1
            
            table.rows[:] = result['rows']
            total_label.text = f"DATABASE TOTAL: {result['total']} RECORDS"
            
            # 逻辑计算：向上取整计算最大页码
            max_p = max(1, (result['total'] + page_size - 1) // page_size)
            pagination.max = max_p
            
            # 【重要】状态同步：仅当组件值与目标值不一致时更新，避免触发死循环
            if pagination.value != target_page:
                pagination.value = target_page 
            
            table.update()
        except Exception as e:
            # 异常处理：数据加载失败时仅通知用户，不破坏已有表格数据（兜底策略）
            logging.error(f"Load data error: {e}")
            ui.notify('数据加载失败', type='negative')
        finally: 
            table.props(remove='loading')
            table.update()
            loading_lock = False

    # --- 事件绑定 ---
    
    # 监听分页器点击事件
    pagination.on('update:modelValue', lambda e: load_data(page=e.args))

    async def on_jump():
        """处理跳转输入框的回车事件，执行页码范围校验"""
        if jump_input.value is None:
            return
        val = int(jump_input.value)
        if 1 <= val <= pagination.max:
            await load_data(page=val) 
        else:
            ui.notify(f'请输入 1-{pagination.max} 之间的页码')

    jump_input.on('keydown.enter', on_jump)
    
    # 初始加载：延迟 0.1s 确保前端容器已挂载完毕
    ui.timer(0.1, lambda: load_data(page=1), once=True)

# 生产环境运行配置
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='师道汉韵·管理终端', port=8080)