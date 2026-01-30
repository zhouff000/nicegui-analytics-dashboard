import requests
import json

# --- 配置区 ---
TEST_URL = "http://47.109.134.91:6001/api/v1/admin/dashboard/activities"
YOUR_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4YTMwMmRmMi0xMDM0LTQyOWUtYmYwZC0wZDc5YTE1YjJhYTQiLCJ1c2VyX2lkIjoiOGEzMDJkZjItMTAzNC00MjllLWJmMGQtMGQ3OWExNWIyYWE0IiwidXNlcm5hbWUiOiJzdXBlcl90ZXN0ZXIiLCJ1c2VyX3R5cGUiOiJkYXRhX2VudHJ5IiwiZXhwIjoxNzY5Njk0NjI1fQ.qRNmuHSgAP8i5OPD1amFCCCr-j7SoDQk3ZTiBbIfGA4"

def test_api_connection():
    print("--- 开始 API 连接测试 ---")
    
    params = {'status': 'published'} 

    # 注意：这里要用你上面定义的 YOUR_TOKEN 和 TEST_URL
    headers = {
        "Authorization": f"Bearer {YOUR_TOKEN}",
        "Content-Type": "application/json"
    }

    print(f"正在请求 URL: {TEST_URL}")

    try:
        # 注意：这里要把 url 改成 TEST_URL
        response = requests.get(TEST_URL, headers=headers, params=params, timeout=10)
        
        print(f"状态码: {response.status_code}")
        
        if response.text:
            print("返回内容:")
            try:
                parsed_json = response.json()
                print(json.dumps(parsed_json, indent=4, ensure_ascii=False))
            except:
                print(response.text)
        else:
            print("警告：服务器返回内容完全为空 (Empty Response)")

    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {e}")

    print("--- 脚本执行结束 ---")

# ==========================================
# 关键点：这一行必须写！只有调用了函数，代码才会执行
# ==========================================
if __name__ == "__main__":
    test_api_connection()