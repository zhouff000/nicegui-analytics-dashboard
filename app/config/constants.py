from typing import Dict, Any

# --- 全局布局与样式 ---
LAYOUT_CONFIG = {
    'SIDE_MENU_WIDTH': 'w-full md:w-[500px]',
    'SIDE_MENU_MARGIN': 'ml-[-140px] mt-[-20px]',
    'STAT_CARD_WIDTH': 'w-full md:w-[480px]',
    'STAT_CARD_MARGIN': '-mt-25 -mr-16',
    'CHART_HEIGHT_MAIN': 'h-[300px]',
    'CHART_HEIGHT_BAR': 'h-[280px]',
    'PAGE_SIZE': 15
}

BODY_STYLE = '''
    background-color: #f8faff;
    background-image: radial-gradient(#e1e7f0 1px, transparent 1px);
    background-size: 24px 24px;
'''

# 详情页专用 CSS 注入
DETAILS_HEAD_HTML = '''
    <style>
        .q-table thead tr { background-color: #e0f2fe !important; }
        .q-table thead th {
            background-color: #e0f2fe !important;
            color: #1e40af !important; 
            font-weight: 800 !important;
            font-size: 0.9rem;
            border-bottom: 2px solid #bae6fd !important;
        }
        .nicegui-table tbody tr:hover { background-color: #f8fbff !important; }
        .nicegui-table tbody td { border-bottom: 1px solid #f1f5f9 !important; }
    </style>
'''

CARD_BASE_STYLE = (
    'w-full py-10 px-8 rounded-[40px] shadow-lg hover:shadow-2xl '
    'hover:scale-[1.02] cursor-pointer border-none transition-all duration-300'
)

# --- 数据映射 ---
# 统一中文状态到后端 Key 的映射
STATUS_MAP = {
    '待审核': 'pending_review',
    '已发布': 'published',
    '已通过': 'published',  # 兼容性处理
    '已拒绝': 'rejected',
    '草稿': 'draft',
    '草稿箱': 'draft'
}

# 统一后端 Key 到中文显示的映射
STATUS_DISPLAY_MAP = {
    'published': '已发布',
    'rejected': '已拒绝',
    'draft': '草稿箱',
    'pending_review': '待审核'
}

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

# --- 组件配置 ---
TABLE_COLUMNS = [
    {'name': 'index_id', 'label': '序号', 'field': 'index_id', 'align': 'center', 'classes': 'text-slate-400 font-bold'},
    {'name': 'word_info', 'label': '汉字 / 拼音', 'field': 'word', 'align': 'left'},
    {'name': 'status', 'label': '状态', 'field': 'status', 'align': 'center'},
    {'name': 'users', 'label': '人员 (创/审)', 'field': 'creator_id', 'align': 'left'},
    {'name': 'times', 'label': '时间 (创/审)', 'field': 'created_at', 'align': 'left'},
    {'name': 'actions', 'label': '操作', 'field': 'id', 'align': 'center'},
]

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
        'title': '系统日志',
        'subtitle': 'DATA AGGREGATION',
        'icon': 'database'
    },
    'default': 'bg-white text-slate-800'
}

# --- 图表模板 ---
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
        'view_all': '查看全部记录>',
        'sub_items': [
            ('草稿箱', 'menu_book', 'draft'), 
            ('待审核', 'translate', 'pending_review'), 
            ('已拒绝', 'short_text', 'rejected'), 
            ('已发布', 'segment', 'published')
        ]
    },
    'summary': {
        'label': '系统日志',
        'sub_items': [
            ('汉字等级说明', 'description', None), 
        ]
    }
}
def get_status_label(key: str) -> str:
    return STATUS_DISPLAY_MAP.get(key, '未知状态')

# 新增：动作文案映射
ACTION_LABELS = {
    'home': '等待系统指令加载数据视图',
    'sync': '正在同步{}数据中心...',
    'done': '分析完成：当前展示{}'
}