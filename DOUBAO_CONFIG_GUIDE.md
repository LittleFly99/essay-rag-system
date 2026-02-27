# 火山引擎豆包API配置指南

## 1. 获取API密钥

### 注册和登录
1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 注册并登录您的账户
3. 进入 [Ark大模型服务](https://console.volcengine.com/ark/region:ark+cn-beijing/model)

### 创建API密钥
1. 在左侧导航栏选择 "模型推理" → "在线推理"
2. 点击右上角 "API密钥管理"
3. 创建新的API密钥
4. 复制并保存API密钥（请妥善保管，不要泄露）

### 获取接入点
1. 在模型列表中选择要使用的模型（如 doubao-pro-4k）
2. 点击模型名称进入详情页
3. 在 "接入指南" 中找到API接入点URL

## 2. 配置环境变量

编辑 `.env` 文件，添加以下配置：

```bash
# LLM 提供商选择
LLM_PROVIDER=doubao

# 火山引擎豆包 API 配置
DOUBAO_API_KEY=your_actual_api_key_here
DOUBAO_ENDPOINT=https://ark.cn-beijing.volces.com/api/v3
DOUBAO_MODEL=doubao-pro-4k
```

### 配置说明

#### LLM_PROVIDER
- `doubao`: 使用火山引擎豆包模型
- `openai`: 使用OpenAI模型

#### DOUBAO_API_KEY
- 在火山引擎控制台获取的API密钥
- 格式通常为：`ak-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

#### DOUBAO_ENDPOINT
- 火山引擎API服务的接入点
- 常见地址：
  - 北京：`https://ark.cn-beijing.volces.com/api/v3`
  - 上海：`https://ark.cn-shanghai.volces.com/api/v3`

#### DOUBAO_MODEL
支持的模型列表：

| 模型名称 | 上下文长度 | 说明 |
|---------|-----------|------|
| doubao-lite-4k | 4K | 轻量版，适合简单任务 |
| doubao-pro-4k | 4K | 标准版，平衡性能和成本 |
| doubao-pro-32k | 32K | 长文本版，支持更长上下文 |
| doubao-pro-128k | 128K | 超长文本版，适合复杂任务 |

## 3. 测试配置

### 方法一：使用测试脚本
```bash
cd /Users/admin/Desktop/Work/ggame/article-rag
python -c "
from src.generation.llm_generator import LLMGenerator
from src.core.models import EssayPrompt, EssayType, DifficultyLevel

# 创建测试题目
prompt = EssayPrompt(
    title='我的梦想',
    essay_type=EssayType.NARRATIVE,
    difficulty_level=DifficultyLevel.MIDDLE
)

# 测试豆包API
generator = LLMGenerator()
guidance = generator.generate_guidance(prompt)
print('API测试成功！')
print(f'主题分析: {guidance.theme_analysis[:50]}...')
"
```

### 方法二：使用简单演示
```bash
python simple_demo.py
```

## 4. API调用限制

### 请求频率限制
- 免费版：10 QPS（每秒查询数）
- 付费版：根据套餐不同有不同限制

### 令牌消耗
- 按输入和输出令牌数计费
- 1个中文字符 ≈ 1.5-2个令牌
- 1个英文单词 ≈ 1.3个令牌

### 单次请求限制
- 输入+输出令牌总数不能超过模型的上下文长度
- 建议保留一定缓冲，避免截断

## 5. 错误处理

### 常见错误和解决方案

#### 401 Unauthorized
```
原因：API密钥无效或过期
解决：检查.env文件中的DOUBAO_API_KEY是否正确
```

#### 403 Forbidden
```
原因：没有访问指定模型的权限
解决：确认模型名称正确，或联系客服开通权限
```

#### 429 Too Many Requests
```
原因：请求频率过高
解决：添加请求间隔，或升级API套餐
```

#### 500 Internal Server Error
```
原因：服务端临时错误
解决：稍后重试，或检查请求参数格式
```

### 系统级错误处理
系统已内置以下错误处理机制：

1. **自动重试**：网络错误时自动重试
2. **降级处理**：API失败时使用模拟生成
3. **超时保护**：设置60秒请求超时
4. **日志记录**：详细记录错误信息

## 6. 性能优化建议

### 提示词优化
- 使用清晰具体的指令
- 提供足够的上下文信息
- 要求结构化输出（如JSON格式）

### 请求优化
- 批量处理多个请求
- 缓存常用的响应结果
- 控制输入文本长度

### 成本控制
- 选择合适的模型版本
- 监控令牌使用量
- 设置合理的max_tokens限制

## 7. 安全注意事项

### API密钥安全
- 不要在代码中硬编码API密钥
- 使用环境变量存储敏感信息
- 定期轮换API密钥
- 限制API密钥的使用范围

### 数据安全
- 不要发送敏感个人信息
- 遵守数据隐私法规
- 考虑数据本地化需求

## 8. 监控和日志

### 日志查看
```bash
# 查看实时日志
tail -f logs/app.log

# 查看错误日志
grep "ERROR" logs/app.log

# 查看API调用日志
grep "豆包API" logs/app.log
```

### 性能监控
- 监控API响应时间
- 跟踪令牌消耗情况
- 观察错误率变化

## 9. 故障排除

### 检查清单
- [ ] API密钥是否正确
- [ ] 接入点URL是否正确
- [ ] 模型名称是否正确
- [ ] 网络连接是否正常
- [ ] 请求格式是否符合API规范

### 调试技巧
```python
# 开启详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 测试网络连接
import requests
response = requests.get("https://ark.cn-beijing.volces.com")
print(response.status_code)

# 测试API调用
from src.generation.llm_generator import DoubaoClient
client = DoubaoClient(api_key="your_key", endpoint="your_endpoint", model="doubao-pro-4k")
result = client.chat_completion([{"role": "user", "content": "你好"}])
print(result)
```

## 10. 高级配置

### 自定义参数
```python
# 在llm_generator.py中可以调整以下参数：
- temperature: 0.1-1.0 (创造性，越高越随机)
- max_tokens: 最大输出令牌数
- timeout: 请求超时时间(秒)
```

### 多模型切换
```bash
# 在.env文件中快速切换模型
DOUBAO_MODEL=doubao-lite-4k    # 快速便宜
DOUBAO_MODEL=doubao-pro-4k     # 平衡性能
DOUBAO_MODEL=doubao-pro-32k    # 长文本
```

---

如需更多帮助，请参考：
- [火山引擎官方文档](https://www.volcengine.com/docs/82379)
- [Ark大模型API文档](https://www.volcengine.com/docs/82379/1263475)
- [系统错误日志](logs/app.log)
