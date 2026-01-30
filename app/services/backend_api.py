import logging
from typing import List, Dict, Any, Final
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- 基础配置与常量 ---
# 确保 API_BASE 路径完整，指向具体的 resolutions 资源
API_BASE: Final[str] = "http://47.109.134.91:6001/api/v1/admin/dashboard/resolutions"
TOKEN: Final[str] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4YTMwMmRmMi0xMDM0LTQyOWUtYmYwZC0wZDc5YTE1YjJhYTQiLCJ1c2VyX2lkIjoiOGEzMDJkZjItMTAzNC00MjllLWJmMGQtMGQ3OWExNWIyYWE0IiwidXNlcm5hbWUiOiJzdXBlcl90ZXN0ZXIiLCJ1c2VyX3R5cGUiOiJkYXRhX2VudHJ5IiwiZXhwIjoxNzY5Njk0NjI1fQ.qRNmuHSgAP8i5OPD1amFCCCr-j7SoDQk3ZTiBbIfGA4"
# 配置结构化日志，方便在终端查看详细运行状态
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- 核心网络层配置 ---

def create_http_session(pool_size: int = 10) -> requests.Session:
    """
    创建并配置线程安全的 Session。
    在多线程环境下，每个任务创建独立的 Session 以确保彻底的线程安全。
    """
    session = requests.Session()
    
    # 定义自动重试策略 (仅针对 GET 等幂等方法)
    retry_strategy = Retry(
        total=3,                # 最多重试 3 次
        backoff_factor=1,       # 等待时间 1s, 2s, 4s
        status_forcelist=[429, 500, 502, 503, 504], 
        allowed_methods=["GET", "HEAD", "OPTIONS"] 
    )
    
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=pool_size,
        pool_maxsize=pool_size
    )
    
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # 统一注入 Token
    session.headers.update({
        'accept': 'application/json',
        'Authorization': f'Bearer {TOKEN.strip()}'
    })
    
    return session

def fetch_single_status(status_key: str, status_name: str, timeout: tuple = (3.05, 10)) -> Dict[str, Any]:
    """
    核心函数：获取单个状态的数据数量。
    :param timeout: (连接超时, 读取超时)
    :return: 格式化后的字典 {'name': str, 'value': int}
    """
    # 修复点：每个线程使用专属的独立 Session，解决并发冲突
    with create_http_session() as http_session:
        try:
            # 仅需统计数量，limit 设为 1 减轻后端压力
            params = {'skip': 0, 'limit': 1, 'status': status_key}
            
            response = http_session.get(API_BASE, params=params, timeout=timeout)
            
            # 鉴权状态专门处理
            if response.status_code in (401, 403):
                logger.error(f"鉴权失败 (401/403)！请检查 TOKEN 有效性。状态: {status_name}")
                return {'name': status_name, 'value': 0}
            
            # 若返回 404，通常代表该路径下无数据，视作 0
            if response.status_code == 404:
                logger.warning(f"路径未找到 (404): {status_name}，已设为 0")
                return {'name': status_name, 'value': 0}

            response.raise_for_status() # 抛出其他 4xx/5xx 错误
            
            data = response.json()
            
            # 兼容列表和带有 total 字段的字典
            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict):
                count = data.get('total', len(data.get('items', data.get('data', []))))
            else:
                count = 0
            
            # 强制转换为 int，确保前端图表渲染不报错
            final_value = int(count) if isinstance(count, (int, float)) else 0
            
            logger.info(f"状态【{status_name}】获取成功，数量: {final_value}")
            return {'name': status_name, 'value': final_value}

        except requests.exceptions.RequestException as re:
            logger.error(f"网络请求异常 ({status_name}): {re}")
        except Exception:
            # 记录完整错误堆栈信息，排障神技
            logger.exception(f"处理【{status_name}】数据时发生未知异常")
            
        return {'name': status_name, 'value': 0}

def fetch_resolutions_stats() -> List[Dict[str, Any]]:
    """
    业务主管：并发抓取所有状态并重组结果。
    """
    # 定义前端需要的映射顺序
    status_map: Final[Dict[str, str]] = {
        'published': '已发布',
        'draft': '草稿箱',
        'pending_review': '待审核',
        'rejected': '已拒绝'
    }
    
    # 结果暂存器
    temp_results: Dict[str, Dict[str, Any]] = {}

    try:
        # 限制最大工作线程，避免资源浪费
        with ThreadPoolExecutor(max_workers=min(len(status_map), 4)) as executor:
            # 提交所有统计任务
            future_to_key = {
                executor.submit(fetch_single_status, key, name): key 
                for key, name in status_map.items()
            }
            
            # 异步收集结果
            for future in as_completed(future_to_key):
                key = future_to_key[future]
                temp_results[key] = future.result()

        # 按照业务定义的 key 顺序重组列表，确保前端图例顺序固定
        processed_data = [temp_results[key] for key in status_map.keys() if key in temp_results]

        # 兜底：如果全部数据都为 0，返回暂无数据提示
        if not processed_data or sum(item['value'] for item in processed_data) == 0:
            return [{'name': '暂无数据', 'value': 0}]
            
        return processed_data

    except Exception:
        logger.exception("fetch_resolutions_stats 执行过程中发生致命错误")
        return [{'name': '系统异常', 'value': 0}]
def fetch_resolutions_list(skip: int = 0, limit: int = 15, status: str = None):
    """获取分页列表数据"""
    with create_http_session() as http_session:
        try:
            params = {'skip': skip, 'limit': limit}
            if status:
                params['status'] = status
            
            response = http_session.get(API_BASE, params=params, timeout=10)
            response.raise_for_status()
            return response.json()  # 返回后端原始 JSON
        except Exception as e:
            logger.error(f"列表抓取失败: {e}")
            return {"items": [], "total": 0}
# --- 测试运行入口 ---
# if __name__ == "__main__":
#     print("--- 正在执行后端 API 统计测试 ---")
#     results = fetch_resolutions_stats()
#     print("\n最终汇总结果:")
#     print(results)