import sys
import os
import logging
from typing import List, Dict, Any

# 确保能找到 backend_test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend_test.manager_api import fetch_resolutions_stats
except ImportError:
    # 降级处理：如果没有后端环境，返回模拟数据
    def fetch_resolutions_stats():
        return [{"name": "未连接", "value": 0}]

def get_status_statistics() -> List[Dict[str, Any]]:
    """获取解析状态统计数据"""
    try:
        data = fetch_resolutions_stats()
        return data if data else [{'value': 0, 'name': '暂无数据'}]
    except Exception as e:
        logging.error(f"Failed to fetch resolution stats: {e}")
        return [{'value': 0, 'name': '数据加载异常'}]

def get_summary_statistics() -> List[Dict[str, Any]]:
    """获取等级汇总统计数据"""
    # 模拟从数据库获取
    return [
        {'value': 50, 'name': '等级一'},
        {'value': 40, 'name': '等级二'},
        {'value': 30, 'name': '等级三'}
    ]