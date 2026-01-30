"""
文件职责：
    UI 组件库模块 (components.py)。
    负责定义“师道汉韵”管理后台的所有可视化原子组件与复合组件。
核心功能：
    - 导航与布局：提供响应式 Header 和带动画效果的折叠式侧边菜单。
    - 数据可视化：封装 ECharts 配置逻辑，生成符合项目视觉风格的饼图（Pie）和柱状图（Bar）。
    - 状态管理映射：根据业务模式（Mode）动态调整组件样式（颜色、图标、阴影）。
"""

from nicegui import ui
import copy
from typing import Callable, List, Dict, Any, Optional
from constants import (
    CARD_BASE_STYLE, THEME_CONFIG, COLOR_MAP,
    PIE_CHART_TEMPLATE, BAR_CHART_TEMPLATE,
    MODE_SETTINGS, CHART_UI, LAYOUT_CONFIG
)

def create_header(on_home_click: Callable) -> None:
    """
    功能：渲染全局顶部导航栏。
    入参：
        - on_home_click: 点击标题时的回调函数（通常用于返回首页或重置状态）。
    """
    with ui.header().classes('bg-white/80 backdrop-blur-md border-b border-slate-100 px-8 py-4 justify-between items-center shadow-none'):
        # 品牌标识区
        with ui.row().classes('items-center gap-3'):
            ui.icon('history_edu', color='slate-700', size='34px')
            with ui.column().classes('gap-0 cursor-pointer').on('click', on_home_click):
                ui.label('师道汉韵').classes('text-2xl font-black text-slate-800 tracking-widest')
                ui.label('SHIDAO HANYUN').classes('text-[10px] font-bold text-slate-400 tracking-[0.3em] -mt-1')
        
        # 用户状态区
        with ui.row().classes('items-center gap-4'):
            with ui.element('div').classes('px-4 py-1.5 rounded-full bg-slate-100 border border-slate-200 flex items-center gap-2'):
                ui.element('div').classes('w-2 h-2 rounded-full bg-emerald-500 animate-pulse') # 呼吸灯效果，暗示系统在线
                ui.label('管理者界面').classes('text-sm font-bold text-slate-600')
            ui.avatar('admin_panel_settings', color='slate-700', text_color='white').props('size=32px')

def render_side_menu(current_mode: str, update_fn: Callable, active_view: str = 'home') -> None:
    """
    功能：渲染左侧折叠式功能菜单。
    入参：
        - current_mode: 当前选中的主业务模式（如 'status', 'summary'）。
        - update_fn: 菜单点击后的状态更新回调。
        - active_view: 当前处于激活状态的视图 ID。
    """
    with ui.column().classes(f"{LAYOUT_CONFIG['SIDE_MENU_WIDTH']} gap-4 {LAYOUT_CONFIG['SIDE_MENU_MARGIN']}"):
        # 遍历主题配置生成一级菜单卡片
        for mode_key, config in THEME_CONFIG.items():
            if mode_key == 'default': continue
            
            # 渲染大卡片按钮
            menu_card(mode_key, config['title'], config['subtitle'], config['icon'], current_mode, lambda m=mode_key: update_fn(m))
            
            # 复杂逻辑：如果当前卡片被激活，则展开其子菜单项（带淡入动画）
            if current_mode == mode_key:
                sub_items = MODE_SETTINGS.get(mode_key, {}).get('sub_items', [])
                if sub_items:
                    with ui.column().classes('w-full px-6 gap-3 -mt-2 mb-2 animate-fade-in'):
                        for name, icon, status_key in sub_items:
                            sub_menu_button(name, icon, mode_key, lambda n=name: update_fn(mode_key, n))

def create_statistics_card(placeholder_option: dict) -> dict:
    """
    功能：创建右侧主统计分析容器，包含两个图表插槽。
    入参：
        - placeholder_option: 初始空状态时显示的 ECharts 配置。
    出参：
        - dict: 包含各 UI 元素引用的字典，便于父页面后续通过 .update() 更新内容。
    """
    with ui.card().classes(f"{LAYOUT_CONFIG['STAT_CARD_WIDTH']} min-h-[680px] p-8 rounded-[50px] shadow-2xl bg-white border-none items-center relative {LAYOUT_CONFIG['STAT_CARD_MARGIN']} z-10 overflow-hidden ml-auto"):
        # 装饰性背景文字：利用绝对定位和垂直排列营造科技感
        ui.label('DATA ANALYTICS').classes('absolute right-4 top-32 text-slate-50 font-black text-6xl [writing-mode:vertical-rl] select-none -z-10 tracking-[0.2em]')

        with ui.column().classes('w-full gap-2 items-center'):
            # 主图表区域（饼图/玫瑰图）
            with ui.element('div').classes(f"relative w-full {LAYOUT_CONFIG['CHART_HEIGHT_MAIN']} flex items-center justify-center"):
                chart = ui.echart(options=placeholder_option).classes('w-full h-full')
                icon_overlay = ui.icon('analytics', size='80px').classes('absolute text-slate-50') # 中间装饰图标
            
            # 副图表区域（柱状图）：默认隐藏，数据加载后展示
            with ui.element('div').classes(f"w-full {LAYOUT_CONFIG['CHART_HEIGHT_BAR']} mt-4") as bar_container:
                bar_container.set_visibility(False)
                ui.label('数值明细对比').classes('text-slate-400 text-[10px] font-bold mb-1 ml-6 tracking-widest')
                bar_chart = ui.echart(options={}).classes('w-full h-full')

        # 底部终端状态栏
        with ui.column().classes('w-full mt-auto gap-4'):
            ui.separator().classes('opacity-50')
            with ui.row().classes('items-center gap-4 px-2 mb-2'):
                ui.element('div').classes('w-1.5 h-8 bg-blue-500 rounded-full shadow-[0_0_10px_rgba(59,130,246,0.3)]')
                with ui.column().classes('gap-0'):
                    ui.label('TERMINAL STATUS').classes('text-slate-300 font-black text-[9px] tracking-tighter')
                    status_text = ui.label('等待系统指令加载数据视图').classes('text-slate-500 font-bold text-[12px]')
    
    return {'chart': chart, 'bar_chart': bar_chart, 'bar_container': bar_container, 'icon_overlay': icon_overlay, 'status_text': status_text}

def create_pie_chart(data: List[Dict], inner_radius: str = '35%', outer_radius: str = '50%', is_rose: bool = False) -> Dict:
    """
    功能：生成 ECharts 饼图/南丁格尔玫瑰图配置字典。
    入参：
        - data: 格式为 [{'name': '...', 'value': 10}, ...] 的列表。
        - inner_radius/outer_radius: 控制环形图厚度。
        - is_rose: 是否启用面积模式（玫瑰图）。
    """
    # 状态映射：根据常量文件中的 COLOR_MAP 为不同业务状态匹配固定颜色
    for item in data:
        if item['name'] in COLOR_MAP: 
            item['itemStyle'] = {'color': COLOR_MAP[item['name']]}
            
    conf = copy.deepcopy(PIE_CHART_TEMPLATE)
    conf['series'][0].update({
        'radius': [inner_radius, outer_radius], 
        'roseType': 'area' if is_rose else False, 
        'data': data
    })
    return conf

def create_bar_chart(raw_data: List[Dict]) -> Dict:
    """
    功能：生成 ECharts 柱状图配置字典。
    入参：
        - raw_data: 原始数据列表。
    """
    # 样式映射：为柱状图添加圆角和颜色
    chart_data = [{
        'value': item['value'], 
        'itemStyle': {
            'color': COLOR_MAP.get(item['name'], '#3b82f6'), 
            'borderRadius': CHART_UI['bar'].get('borderRadius', [6, 6, 0, 0])
        }
    } for item in raw_data]
    
    conf = copy.deepcopy(BAR_CHART_TEMPLATE)
    conf['xAxis']['data'] = [item['name'] for item in raw_data]
    conf['series'][0]['data'] = chart_data
    return conf

def menu_card(mode_key: str, title: str, sub_title: str, icon: str, current_mode: str, on_click: Callable) -> None:
    """
    功能：渲染侧边栏一级大卡片按钮。
    """
    is_active = (current_mode == mode_key)
    view_all_text = MODE_SETTINGS.get(mode_key, {}).get('view_all')
    cfg = THEME_CONFIG[mode_key]
    
    # 根据是否激活动态计算 CSS 类名
    card_style = f'{CARD_BASE_STYLE} {cfg["active"] if is_active else THEME_CONFIG["default"]}'
    
    with ui.card().classes(card_style).on('click', on_click):
        with ui.row().classes('w-full items-center justify-between'):
            with ui.row().classes('items-center gap-8'):
                # 激活状态时反转 Avatar 颜色以突出显示
                ui.avatar(icon, color='white' if is_active else cfg['icon_color'], text_color=cfg['icon_color'] if is_active else 'white').props('size=64px')
                with ui.column().classes('gap-0'):
                    ui.label(title).classes(f'text-3xl font-black {"text-white" if is_active else "text-slate-800"}')
                    with ui.row().classes('items-center gap-2'):
                        ui.label(sub_title).classes('text-xs tracking-widest opacity-60')
                        
                        # 仅在激活状态下显示“查看全量”链接，并防止点击事件冒泡到父级卡片
                        if is_active and view_all_text:
                            ui.label('|').classes('opacity-30 text-xs')
                            ui.label(view_all_text).classes('text-[10px] font-bold underline cursor-pointer hover:text-white transition-colors').on('click.stop', lambda: ui.navigate.to('/details', new_tab=True))
            
            ui.icon('expand_more' if not is_active else 'expand_less', size='32px')

def sub_menu_button(name: str, icon: str, mode_key: str, on_click: Callable) -> None:
    """
    功能：渲染二级细分按钮。
    """
    cfg = THEME_CONFIG[mode_key]
    with ui.button(on_click=on_click).props('flat').classes(f'w-full py-4 {cfg["sub_btn_bg"]} rounded-2xl hover:bg-opacity-80 transition-colors'):
        with ui.row().classes('w-full items-center gap-4 px-4'):
            ui.icon(icon, color=cfg['sub_icon_color'], size='24px')
            ui.label(name).classes(f'{cfg["sub_text_color"]} font-bold text-lg')