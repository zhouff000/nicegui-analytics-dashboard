from nicegui import ui
import copy
from typing import Callable, List, Dict, Any
from constants import (
    CARD_BASE_STYLE, THEME_CONFIG, COLOR_MAP,
    PIE_CHART_TEMPLATE, BAR_CHART_TEMPLATE,
    MODE_SETTINGS, CHART_UI, LAYOUT_CONFIG
)

def create_header(on_home_click: Callable) -> None:
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

def render_side_menu(current_mode: str, update_fn: Callable[[str], Any], active_view: str = 'home') -> None:
    """
    优化布局：
    1. 确保返回按钮文字对齐
    2. 智能显示：仅在非主页状态下显示返回按钮
    """
    with ui.column().classes(f"{LAYOUT_CONFIG['SIDE_MENU_WIDTH']} gap-4 {LAYOUT_CONFIG['SIDE_MENU_MARGIN']}"):
        
        # 1. 遍历配置渲染功能卡片
        for mode_key, config in THEME_CONFIG.items():
            if mode_key == 'default': continue
            
            menu_card(
                mode_key, config['title'], config['subtitle'], 
                config['icon'], current_mode, lambda m=mode_key: update_fn(m)
            )
            
            # 2. 渲染激活状态下的子菜单
            if current_mode == mode_key:
                sub_items = MODE_SETTINGS.get(mode_key, {}).get('sub_items', [])
                if sub_items:
                    with ui.column().classes('w-full px-6 gap-3 -mt-2 mb-2 animate-fade-in'):
                        for name, icon in sub_items:
                            sub_menu_button(name, icon, mode_key)

        # 3. 【核心改动】：智能判定返回按钮
        # 逻辑：只要菜单展开了(current_mode != 'home') 或者 右侧有图表(active_view != 'home')
        if current_mode != 'home' or active_view != 'home':
            with ui.column().classes('w-full px-4 mt-2 animate-fade-in'): # 增加淡入动画
                ui.separator().classes('opacity-10 mb-4')
                
                with ui.button(on_click=lambda: update_fn('home')) \
                    .props('flat no-caps') \
                    .classes('w-full py-4 rounded-2xl hover:bg-slate-100 transition-all border border-dashed border-slate-200 group'):
                    
                    with ui.row().classes('w-full items-center justify-start gap-10 px-6'): 
                        ui.icon('arrow_back', size='28px').classes('text-slate-400 group-hover:text-blue-500')
                        ui.label('返回主概览').classes('text-slate-400 font-bold text-xl group-hover:text-blue-500')
                        
def create_statistics_card(placeholder_option: dict) -> dict:
    """极简化的统计卡片：移除冗余重置功能，聚焦数据展示"""
    with ui.card().classes(f"{LAYOUT_CONFIG['STAT_CARD_WIDTH']} min-h-[680px] p-8 rounded-[50px] shadow-2xl bg-white border-none items-center relative {LAYOUT_CONFIG['STAT_CARD_MARGIN']} z-10 overflow-hidden ml-auto"):
        
        # 顶部标题栏：现在只保留标题，视觉更聚焦
        with ui.row().classes('w-full items-center mb-6 px-2'):
            with ui.column().classes('gap-1'):
                ui.label('统计分析终端').classes('text-blue-500 font-black tracking-[0.4em] text-sm')
                ui.element('div').classes('w-12 h-[3px] bg-blue-100 rounded-full')
            
        # 装饰性背景文字
        ui.label('DATA ANALYTICS').classes('absolute right-4 top-32 text-slate-50 font-black text-6xl [writing-mode:vertical-rl] select-none -z-10 tracking-[0.2em]')

        # 图表容器
        with ui.column().classes('w-full gap-2 items-center'):
            with ui.element('div').classes(f"relative w-full {LAYOUT_CONFIG['CHART_HEIGHT_MAIN']} flex items-center justify-center"):
                chart = ui.echart(options=placeholder_option).classes('w-full h-full')
                icon_overlay = ui.icon('analytics', size='80px').classes('absolute text-slate-50')
            
            with ui.element('div').classes(f"w-full {LAYOUT_CONFIG['CHART_HEIGHT_BAR']} mt-4") as bar_container:
                bar_container.set_visibility(False)
                ui.label('数值明细对比').classes('text-slate-400 text-[10px] font-bold mb-1 ml-6 tracking-widest')
                bar_chart = ui.echart(options={}).classes('w-full h-full')

        # 底部状态栏
        with ui.column().classes('w-full mt-auto gap-4'):
            ui.separator().classes('opacity-50')
            with ui.row().classes('items-center gap-4 px-2 mb-2'):
                ui.element('div').classes('w-1.5 h-8 bg-blue-500 rounded-full shadow-[0_0_10px_rgba(59,130,246,0.3)]')
                with ui.column().classes('gap-0'):
                    ui.label('TERMINAL STATUS').classes('text-slate-300 font-black text-[9px] tracking-tighter')
                    status_text = ui.label('等待系统指令加载数据视图').classes('text-slate-500 font-bold text-[12px]')

    # 返回字典时移除 reset_btn
    return {
        'chart': chart, 'bar_chart': bar_chart, 'bar_container': bar_container,
        'icon_overlay': icon_overlay, 'status_text': status_text
    }
    
def create_pie_chart(data: List[Dict], inner_radius: str = '35%', outer_radius: str = '50%', is_rose: bool = False) -> Dict:
    for item in data:
        if item['name'] in COLOR_MAP:
            item['itemStyle'] = {'color': COLOR_MAP[item['name']]}

    conf = copy.deepcopy(PIE_CHART_TEMPLATE)
    series = conf['series'][0]
    series.update({
        'radius': [inner_radius, outer_radius],
        'roseType': 'area' if is_rose else False,
        'data': data
    })
    return conf

def create_bar_chart(raw_data: List[Dict]) -> Dict:
    chart_data = []
    for item in raw_data:
        color = COLOR_MAP.get(item['name'], '#3b82f6')
        chart_data.append({
            'value': item['value'],
            'itemStyle': {'color': color, 'borderRadius': CHART_UI['bar'].get('borderRadius', [6, 6, 0, 0])}
        })

    conf = copy.deepcopy(BAR_CHART_TEMPLATE)
    conf['xAxis']['data'] = [item['name'] for item in raw_data]
    conf['series'][0]['data'] = chart_data
    return conf

def menu_card(mode_key: str, title: str, sub_title: str, icon: str, current_mode: str, on_click: Callable) -> None:
    is_active = (current_mode == mode_key)
    cfg = THEME_CONFIG[mode_key]
    bg_style = cfg['active'] if is_active else THEME_CONFIG['default']
    avatar_color = 'white' if is_active else cfg['icon_color']
    text_icon_color = cfg['icon_color'] if is_active else 'white'
    label_color = 'text-white' if is_active else 'text-slate-800'

    with ui.card().classes(f'{CARD_BASE_STYLE} {bg_style}').on('click', on_click):
        with ui.row().classes('w-full items-center justify-between'):
            with ui.row().classes('items-center gap-8'):
                ui.avatar(icon, color=avatar_color, text_color=text_icon_color).props('size=64px')
                with ui.column().classes('gap-0'):
                    ui.label(title).classes(f'text-3xl font-black {label_color}')
                    ui.label(sub_title).classes('text-xs tracking-widest opacity-60')
            ui.icon('expand_more' if not is_active else 'expand_less', size='32px')

def sub_menu_button(name: str, icon: str, mode_key: str) -> None:
    cfg = THEME_CONFIG[mode_key]
    with ui.button(on_click=lambda: ui.notify(f'加载{name}...')) \
        .props('flat').classes(f'w-full py-4 {cfg["sub_btn_bg"]} rounded-2xl hover:bg-opacity-80 transition-colors'):
        with ui.row().classes('w-full items-center gap-4 px-4'):
            ui.icon(icon, color=cfg['sub_icon_color'], size='24px')
            ui.label(name).classes(f'{cfg["sub_text_color"]} font-bold text-lg')