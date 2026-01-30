"""
文件职责：
    数据服务与清洗模块 (services.py)。
    作为前端 UI 层与后端 API 层之间的适配器，负责业务逻辑处理、数据格式标准化及异常降级。
核心功能：
    - 统计聚合：获取状态分布、等级分布等图表所需数据。
    - 分页列表：对接解析记录列表，支持按状态过滤、分页偏移计算。
    - 数据清洗（ETL）：统一处理空值兜底、时间格式化、ID 截断及状态码映射，确保前端展示的一致性。
"""

import logging
from typing import List, Dict, Any
from app.config.constants import STATUS_MAP, STATUS_DISPLAY_MAP, LAYOUT_CONFIG

# --- 修改这里：导入你真正的 API 函数 ---
try:
    from .backend_api import fetch_resolutions_stats, fetch_resolutions_list
    logging.info("成功连接到后端 API 模块")
except ImportError:
    logging.warning("未找到后端 API 模块，启用 Mock 降级数据")

try:
    # 尝试从业务后端模块导入 API 函数
    from backend_test.manager_api import fetch_resolutions_stats, fetch_resolutions_list
except ImportError:
    # 异常处理注释：当后端模块不可用时启用 Mock 降级方案，确保前端演示流程不中断
    def fetch_resolutions_stats(status=None):
        mock_data = [
            {"name": "草稿箱", "value": 120}, 
            {"name": "待审核", "value": 45}, 
            {"name": "已拒绝", "value": 12}, 
            {"name": "已发布", "value": 850}
        ]
        return [d for d in mock_data if d['name'] in status] if status else mock_data
        


def get_status_statistics(status: str = None) -> List[Dict[str, Any]]:
    """
    功能：获取并格式化解析状态的分布统计数据（用于饼图）。
    入参：status (str, 可选): 指定过滤的状态名称。
    出参：包含 'name' 和 'value' 的字典列表。
    """
    try:
        data = fetch_resolutions_stats(status=status)
        return data if data else [{'value': 0, 'name': '暂无数据'}]
    except Exception as e:
        # 异常捕获后的兜底：接口调用失败时返回“异常提示”项，避免图表组件报错
        logging.error(f"统计数据加载异常: {e}")
        return [{'value': 0, 'name': '数据加载异常'}]

def get_summary_statistics() -> List[Dict[str, Any]]:
    """
    功能：获取系统概览或等级分布的统计数据。
    出参：固定格式的等级分布列表（当前为静态数据，后期可对接接口）。
    """
    return [
        {'value': 50, 'name': '等级一'}, 
        {'value': 40, 'name': '等级二'}, 
        {'value': 30, 'name': '等级三'}
    ]

def _format_data_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    功能：【内部工具】将单条后端原始数据格式化为前端 UI 专用结构。
    入参：item (Dict): 后端返回的原始字典对象。
    出参：清洗后的字典，包含 id, word, pinyin, status 等前端字段。
    """
    raw_status = item.get('status')
    # 确保 pinyin_data 始终是字典
    pinyin_data = item.get('pronunciation') or {}
    if not isinstance(pinyin_data, dict): pinyin_data = {} 
    
    return {
        'id': item.get('id') or item.get('_id', '-'),
        'word': item.get('word', '-'),
        'pinyin': pinyin_data.get('pinyin', '-'),
        'status': STATUS_DISPLAY_MAP.get(raw_status, '待审核'),
        # 增加空值判断再截取
        'creator_id': str(item.get('creator_id'))[:8] if item.get('creator_id') else 'system',
        'created_at': (item.get('created_at') or '').replace('T', ' ')[:16],
        'review_comment': item.get('review_comment') if item.get('review_comment') not in ["string", None, ""] else "无"
    }

def get_cleaned_data(page: int = 1, status: str = None) -> Dict[str, Any]:
    """
    功能：分页获取解析记录并执行全量数据清洗。
    入参：
        - page (int): 当前请求的页码。
        - status (str, 可选): 前端传入的状态过滤标识。
    出参：包含 'rows' (清洗后的数据列表) 和 'total' (总记录数) 的字典。
    """
    # 复杂逻辑（分页计算）：根据全局配置计算跳过的记录数 (Skip)
    page_size = LAYOUT_CONFIG.get('PAGE_SIZE', 15)
    skip = (page - 1) * page_size
    
    # 1. 状态映射处理：将前端的“友好标签”转换为后端 API 识别的“业务编码”
    backend_status = None
    if status and status != "EXCLUDE_DRAFT":
        backend_status = STATUS_MAP.get(status, status)

    try:
        # 2. 调用后端异步/线程安全接口
        raw = fetch_resolutions_list(skip=skip, limit=page_size, status=backend_status)
       # ✅ 增加更多兼容性判断
        if isinstance(raw, list):
            items = raw
            total = len(raw)
        elif isinstance(raw, dict):
            # 尝试所有可能的键名：items, data, 或直接是列表
            items = raw.get('items') or raw.get('data') or []
            total = raw.get('total') or len(items)
        else:
            items, total = [], 0
        
        # 4. 批量数据清洗：应用标准化格式化函数
        processed = [_format_data_item(item) for item in items]
        
        return {'rows': processed, 'total': total}
        
    except Exception as e:
        # 异常处理注释：接口调用失败时返回空列表及 0 总数，防止前端表格加载无限 Loading 或崩溃
        logging.error(f"解析记录列表加载失败: {e}")
        return {'rows': [], 'total': 0}