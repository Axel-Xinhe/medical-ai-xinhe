import dashscope
import json
from http import HTTPStatus

text = "通用多模态表征模型示例"
input = [{'text': text}]
# 调用模型接口
resp = dashscope.MultiModalEmbedding.call(
    model="multimodal-embedding-v1",
    input=input,
    api_key="sk-f5601aa8f3cb46b3ae0405a86af9b939"
)

if resp.status_code == HTTPStatus.OK:
    result = {
        "status_code": resp.status_code,
        "request_id": getattr(resp, "request_id", ""),
        "code": getattr(resp, "code", ""),
        "message": getattr(resp, "message", ""),
        "output": resp.output,
        "usage": resp.usage
    }
    print(json.dumps(result, ensure_ascii=False, indent=4))