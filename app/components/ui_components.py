"""
文件职责：
    UI 组件层 (ui_components.py)。
    负责定义所有可视化原子组件。
"""

from nicegui import ui
import copy
from typing import Callable, List, Dict, Any, Optional
# 修改点 1：修改导入路径，指向重构后的 config 目录
from app.config.constants import (
    CARD_BASE_STYLE, THEME_CONFIG, COLOR_MAP,
    PIE_CHART_TEMPLATE, BAR_CHART_TEMPLATE,
    MODE_SETTINGS, CHART_UI, LAYOUT_CONFIG
)
# 修改点 2：引入 utils 里的跳转工具
from app.utils.page_utils import open_new_tab

def create_header(on_home_click: Callable) -> None:
    """渲染全局顶部导航栏 - 保持原样"""
    with ui.header().classes('bg-white/80 backdrop-blur-md border-b border-slate-100 px-8 py-4 justify-between items-center shadow-none'):
        with ui.row().classes('items-center gap-3'):
            ui.icon('history_edu', color='slate-700', size='34px')
            with ui.column().classes('gap-0 cursor-pointer').on('click', on_home_click):
                ui.label('师道汉韵').classes('text-2xl font-black text-slate-800 tracking-widest')
                ui.label('SHIDAO HANYUN').classes('text-[10px] font-bold text-slate-400 tracking-[0.3em] -mt-1')
        
        with ui.row().classes('items-center gap-4'):
            with ui.element('div').classes('px-4 py-1.5 rounded-full bg-slate-100 border border-slate-200 flex items-center gap-2'):
                ui.element('div').classes('w-2 h-2 rounded-full bg-emerald-500 animate-pulse')
                ui.label('管理者界面').classes('text-sm font-bold text-slate-600')
            ui.avatar('admin_panel_settings', color='slate-700', text_color='white').props('size=32px')

def render_side_menu(current_mode: str, update_fn: Callable, active_view: str = 'home') -> None:
    """渲染左侧菜单 - 保持原逻辑"""
    with ui.column().classes(f"{LAYOUT_CONFIG['SIDE_MENU_WIDTH']} gap-4 {LAYOUT_CONFIG['SIDE_MENU_MARGIN']}"):
        for mode_key, config in THEME_CONFIG.items():
            if mode_key == 'default': continue
            menu_card(mode_key, config['title'], config['subtitle'], config['icon'], current_mode, lambda m=mode_key: update_fn(m))
            
            if current_mode == mode_key:
                sub_items = MODE_SETTINGS.get(mode_key, {}).get('sub_items', [])
                if sub_items:
                    with ui.column().classes('w-full px-6 gap-3 -mt-2 mb-2 animate-fade-in'):
                        for name, icon, status_key in sub_items:
                            sub_menu_button(name, icon, mode_key, lambda n=name: update_fn(mode_key, n))

def create_statistics_card(
    placeholder_option: dict, 
    title: str = "数据分析", 
    sub_title: str = "DATA ANALYTICS", 
    icon: str = "analytics",
    is_active: bool = False,       # 新增：是否激活状态
    on_click: callable = None,      # 新增：点击回调
    view_all_text: str = ""         # 新增：底部跳转文字
) -> dict:
    """
    功能：创建主统计分析卡片。
    修改点：支持动态标题、激活状态切换及点击事件。
    """
    # 动态背景色：激活时使用深色/蓝色背景，未激活使用白色
    card_bg = "bg-white" 
    text_main = "text-slate-800" # 文字保持深色
    text_sub = "text-blue-600" if is_active else "text-slate-400" # 激活时图标变蓝色

    with ui.card().on('click', on_click).classes(
        f"{LAYOUT_CONFIG['STAT_CARD_WIDTH']} min-h-[680px] p-8 rounded-[50px] shadow-2xl "
        f"{card_bg} border-none items-center relative {LAYOUT_CONFIG['STAT_CARD_MARGIN']} "
        f"z-10 overflow-hidden ml-auto cursor-pointer transition-all duration-500"
    ):
        
        # 装饰性背景文字
        ui.label(sub_title).classes(
            f'absolute right-4 top-32 font-black text-6xl [writing-mode:vertical-rl] '
            f'select-none -z-10 tracking-[0.2em] opacity-10 {text_main}'
        )

        with ui.column().classes('w-full gap-2 items-center'):
            # 中文标题行
            with ui.row().classes('items-center gap-3 mb-4'):
                ui.icon(icon, size='28px').classes(text_sub)
                ui.label(title).classes(f'text-2xl font-black {text_main} tracking-wider')

            # 主图表区域
            with ui.element('div').classes(f"relative w-full {LAYOUT_CONFIG['CHART_HEIGHT_MAIN']} flex items-center justify-center"):
                chart = ui.echart(options=placeholder_option).classes('w-full h-full')
                icon_overlay = ui.icon(icon, size='80px').classes(f'absolute opacity-5 {text_main}')
            
            # 副图表区域 (柱状图)
            with ui.element('div').classes(f"w-full {LAYOUT_CONFIG['CHART_HEIGHT_BAR']} mt-4") as bar_container:
                bar_container.set_visibility(False)
                ui.label('数值明细对比').classes(f'{text_sub} text-[10px] font-bold mb-1 ml-6 tracking-widest')
                bar_chart = ui.echart(options={}).classes('w-full h-full')

        # 底部终端状态栏
        with ui.column().classes('w-full mt-auto gap-4'):
            if view_all_text:
                ui.label(view_all_text).classes(f'text-xs {text_sub} font-bold cursor-pointer hover:underline text-right w-full px-4')
            
            ui.separator().classes('opacity-20')
            with ui.row().classes('items-center gap-4 px-2 mb-2'):
                ui.element('div').classes('w-1.5 h-8 bg-blue-500 rounded-full shadow-lg')
                with ui.column().classes('gap-0'):
                    ui.label('TERMINAL STATUS').classes(f'opacity-40 font-black text-[9px] tracking-tighter {text_main}')
                    status_text = ui.label('等待系统指令加载数据视图').classes(f'font-bold text-[12px] {text_main} opacity-80')
    
    return {
        'chart': chart, 
        'bar_chart': bar_chart, 
        'bar_container': bar_container, 
        'icon_overlay': icon_overlay, 
        'status_text': status_text
    }
def menu_card(mode_key: str, title: str, sub_title: str, icon: str, current_mode: str, on_click: Callable) -> None:
    """渲染一级大卡片按钮 - 修改跳转逻辑"""
    is_active = (current_mode == mode_key)
    view_all_text = MODE_SETTINGS.get(mode_key, {}).get('view_all')
    cfg = THEME_CONFIG[mode_key]
    
    card_style = f'{CARD_BASE_STYLE} {cfg["active"] if is_active else THEME_CONFIG["default"]}'
    
    with ui.card().classes(card_style).on('click', on_click):
        with ui.row().classes('w-full items-center justify-between'):
            with ui.row().classes('items-center gap-8'):
                ui.avatar(icon, color='white' if is_active else cfg['icon_color'], text_color=cfg['icon_color'] if is_active else 'white').props('size=64px')
                with ui.column().classes('gap-0'):
                    ui.label(title).classes(f'text-3xl font-black {"text-white" if is_active else "text-slate-800"}')
                    with ui.row().classes('items-center gap-2'):
                        ui.label(sub_title).classes('text-xs tracking-widest opacity-60')
                        
                        if is_active and view_all_text:
                            ui.label('|').classes('opacity-30 text-xs')
                            # 修改点 3：使用 open_new_tab 工具函数，代替 ui.navigate
                            ui.label(view_all_text).classes('text-[10px] font-bold underline cursor-pointer hover:text-white transition-colors').on('click.stop', lambda: open_new_tab('/details'))
            
            ui.icon('expand_more' if not is_active else 'expand_less', size='32px')

# 其余辅助函数 (sub_menu_button, create_pie_chart, create_bar_chart) 保持不变，仅需确认它们使用的常量能正确通过导入获取
def sub_menu_button(name: str, icon: str, mode_key: str, on_click: Callable) -> None:
    cfg = THEME_CONFIG[mode_key]
    with ui.button(on_click=on_click).props('flat').classes(f'w-full py-4 {cfg["sub_btn_bg"]} rounded-2xl hover:bg-opacity-80 transition-colors'):
        with ui.row().classes('w-full items-center gap-4 px-4'):
            ui.icon(icon, color=cfg['sub_icon_color'], size='24px')
            ui.label(name).classes(f'{cfg["sub_text_color"]} font-bold text-lg')

def create_pie_chart(data: List[Dict], inner_radius: str = '35%', outer_radius: str = '50%', is_rose: bool = False) -> Dict:
    for item in data:
        if item['name'] in COLOR_MAP: 
            item['itemStyle'] = {'color': COLOR_MAP[item['name']]}
    conf = copy.deepcopy(PIE_CHART_TEMPLATE)
    conf['series'][0].update({'radius': [inner_radius, outer_radius], 'roseType': 'area' if is_rose else False, 'data': data})
    return conf

def create_bar_chart(raw_data: List[Dict]) -> Dict:
    chart_data = [{'value': item['value'], 'itemStyle': {'color': COLOR_MAP.get(item['name'], '#3b82f6'), 'borderRadius': CHART_UI['bar'].get('borderRadius', [6, 6, 0, 0])}} for item in raw_data]
    conf = copy.deepcopy(BAR_CHART_TEMPLATE)
    conf['xAxis']['data'] = [item['name'] for item in raw_data]
    conf['series'][0]['data'] = chart_data
    return conf