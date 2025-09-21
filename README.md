

## 1. 基础使用示例

```python
from src.backend.core.character_comprehension import get_character_response

# 基本用法 - 非流式
response = get_character_response("吗", "practice", stream=False)
print(f"Character: {response.character}")
print(f"Source: {response.source.value}")
print(f"Content: {response.get_content()}")
print(f"Reasoning: {response.get_reasoning_content()}")
```

## 2. 流式响应示例

```python
# 流式响应
stream_response = get_character_response("吗", "practice", stream=True)

if stream_response.is_streaming:
    print("Streaming both content and reasoning:")
    for chunk_data in stream_response.stream_content():
        if "reasoning_content" in chunk_data:
            print(f"[推理] {chunk_data['reasoning_content']}", end="", flush=True)
        if "content" in chunk_data:
            print(f"[内容] {chunk_data['content']}", end="", flush=True)
    print()  # 换行
```

## 3. 仅获取特定内容

```python
# 仅获取推理内容
stream_response = get_character_response("水", "practice", stream=True)
print("仅推理过程:")
for reasoning in stream_response.stream_reasoning_only():
    print(reasoning, end="", flush=True)

# 仅获取回答内容  
print("\n仅回答内容:")
for content in stream_response.stream_content_only():
    print(content, end="", flush=True)
```

## 4. 数据库vs LLM响应处理

```python
response = get_character_response("林", "practice")

if response.source.value == "database":
    print("来自数据库的缓存结果:")
    print(f"内容: {response.get_content()}")
    # 数据库结果没有推理内容
elif response.source.value == "llm":
    print("来自LLM的新生成结果:")
    print(f"内容: {response.get_content()}")
    print(f"推理过程: {response.get_reasoning_content()}")
```

## 5. 转换为字典格式

```python
response = get_character_response("火", "practice")
response_dict = response.to_dict()

print("字典格式:")
for key, value in response_dict.items():
    if key in ['content', 'reasoning_content']:
        print(f"{key}: {str(value)[:50]}...")  # 截断长内容
    else:
        print(f"{key}: {value}")
```

## 6. 图片OCR示例

```python
# 使用图片路径（需要有效的图片文件）
try:
    image_response = get_character_response("/path/to/chinese_char.jpg", "practice")
    print(f"从图片识别的汉字: {image_response.character}")
    print(f"内容: {image_response.get_content()}")
except ValueError as e:
    print(f"图片处理错误: {e}")
```

## 7. 错误处理示例

```python
# 处理无效输入
try:
    response = get_character_response("invalid123", "practice")
except ValueError as e:
    print(f"输入错误: {e}")

# 处理无效场景
try:
    response = get_character_response("木", "invalid_scenario")
except ValueError as e:
    print(f"场景错误: {e}")

# 错误使用流式方法
try:
    non_stream = get_character_response("金", "practice", stream=False)
    for chunk in non_stream.stream_content():  # 会抛出异常
        print(chunk)
except ValueError as e:
    print(f"流式使用错误: {e}")
```

## 8. 在Jupyter Notebook中的完整示例

```python
# 在你的notebook中可以这样使用
%load_ext autoreload
%autoreload 2

from src.backend.core.character_comprehension import get_character_response

# 测试非流式
response = get_character_response("山", "practice", stream=False)
print(f"汉字: {response.character}")
print(f"来源: {response.source.value}")
print(f"内容长度: {len(response.get_content())}")

# 测试流式
stream_response = get_character_response("水", "practice", stream=True)
print(f"\n流式响应 - 汉字: {stream_response.character}")
print("实时输出:")
for chunk in stream_response.stream_content():
    if "content" in chunk:
        print(chunk["content"], end="", flush=True)
print("\n完成!")
```

这些示例展示了如何使用统一的`CharacterResponse`接口处理不同数据源（数据库/LLM）和不同模式（流式/非流式）的响应。