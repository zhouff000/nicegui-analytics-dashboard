from typing import Dict, Any

# 全局布局魔法值
LAYOUT_CONFIG = {
    'SIDE_MENU_WIDTH': 'w-full md:w-[500px]',
    'SIDE_MENU_MARGIN': 'ml-[-140px] mt-[-20px]',
    'STAT_CARD_WIDTH': 'w-full md:w-[480px]',
    'STAT_CARD_MARGIN': '-mt-25 -mr-16',
    'CHART_HEIGHT_MAIN': 'h-[300px]',
    'CHART_HEIGHT_BAR': 'h-[280px]',
}

# 全局背景
BODY_STYLE = '''
    background-color: #f8faff;
    background-image: radial-gradient(#e1e7f0 1px, transparent 1px);
    background-size: 24px 24px;
'''

CARD_BASE_STYLE = (
    'w-full py-10 px-8 rounded-[40px] shadow-lg hover:shadow-2xl '
    'hover:scale-[1.02] cursor-pointer border-none transition-all duration-300'
)

COLOR_MAP = {
    '已发布': '#3b82f6',
    '草稿箱': '#94a3b8',
    '待审核': '#22c55e',
    '已拒绝': '#ef4444',
    '核心样本': '#0f172a',
    '新增数据': '#334155',
    '历史归档': '#64748b',
    '暂无数据': '#e2e8f0'
}

THEME_CONFIG = {
    'status': {
        'active': 'bg-blue-600 text-white',
        'icon_color': 'blue-600',
        'sub_btn_bg': 'bg-blue-100/50',
        'sub_icon_color': 'blue-800',
        'sub_text_color': 'text-blue-900',
        'title': '汉字解析记录',
        'subtitle': 'REAL-TIME ANALYTICS',
        'icon': 'analytics'
    },
    'summary': {
        'active': 'bg-teal-600 text-white',
        'icon_color': 'teal-500',
        'sub_btn_bg': 'bg-teal-100/50',
        'sub_icon_color': 'teal-800',
        'sub_text_color': 'text-teal-900',
        'title': '汉字等级',
        'subtitle': 'DATA AGGREGATION',
        'icon': 'database'
    },
    'default': 'bg-white text-slate-800'
}

CHART_UI = {
    'pie': {
        'animationDuration': 800,
        'animationEasing': 'cubicOut',
        'itemStyle': {'borderRadius': 10, 'borderColor': '#fff', 'borderWidth': 4},
        'label': {
            'show': True, 'position': 'outside', 'formatter': '{b}\n{d}%',
            'fontSize': 13, 'fontWeight': 'bold', 'color': '#334155'
        }
    },
    'bar': {
        'animationDuration': 1000,
        'grid': {'top': '20%', 'bottom': '15%', 'left': '18%', 'right': '10%'},
        'axisLineColor': '#e2e8f0',
        'labelColor': '#64748b',
        'splitLineColor': '#f1f5f9',
        'yAxisName': '单位：个',
        'yAxisNameStyle': {'color': '#94a3b8', 'fontSize': 11, 'padding': [0, 0, 0, -30]}
    }
}

PIE_CHART_TEMPLATE = {
    'animationDuration': CHART_UI['pie']['animationDuration'],
    'animationEasing': CHART_UI['pie']['animationEasing'],
    'tooltip': {'trigger': 'item'},
    'series': [{
        'type': 'pie',
        'center': ['50%', '50%'],
        'avoidLabelOverlap': True,
        'itemStyle': CHART_UI['pie']['itemStyle'],
        'label': CHART_UI['pie']['label']
    }]
}

BAR_CHART_TEMPLATE = {
    'animationDuration': CHART_UI['bar']['animationDuration'],
    'grid': CHART_UI['bar']['grid'],
    'xAxis': {
        'type': 'category',
        'axisLine': {'lineStyle': {'color': CHART_UI['bar']['axisLineColor']}},
        'axisLabel': {'color': CHART_UI['bar']['labelColor'], 'fontWeight': 'bold'}
    },
    'yAxis': {
        'type': 'value',
        'name': CHART_UI['bar']['yAxisName'],
        'nameTextStyle': CHART_UI['bar']['yAxisNameStyle'],
        'splitLine': {'lineStyle': {'type': 'dashed', 'color': CHART_UI['bar']['splitLineColor']}},
        'axisLabel': {'color': '#94a3b8'}
    },
    'series': [{
        'type': 'bar',
        'barWidth': '40%',
        'showBackground': True,
        'backgroundStyle': {'color': 'rgba(180, 180, 180, 0.1)', 'borderRadius': 6}
    }]
}

PLACEHOLDER_OPTION = {
    'series': [{
        'type': 'pie', 
        'radius': ['65%', '66%'], 
        'silent': True, 
        'label': {'show': False}, 
        'data': [{'value': 1, 'itemStyle': {'color': '#e2e8f0'}}]
    }]
}

MODE_SETTINGS = {
    'status': {
        'label': '解析记录',
        'sub_items': [
            ('草稿', 'menu_book'), 
            ('待审草稿', 'translate'), 
            ('已拒绝草稿', 'short_text'), 
            ('已发布汉字', 'segment')
        ]
    },
    'summary': {
        'label': '汉字等级',
        'sub_items': [
            ('汉字等级说明', 'description'), 
        ]
    }
}