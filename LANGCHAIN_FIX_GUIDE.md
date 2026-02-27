# LangChain 导入问题解决方案

## 问题描述

在运行系统时，出现以下警告信息：
```
langchain 相关库未安装，OpenAI功能不可用
```

## 原因分析

这个问题的根本原因是 **LangChain 版本更新导致的API变更**：

1. **旧版本导入方式**（LangChain < 1.0）：
```python
from langchain.schema import HumanMessage, SystemMessage, AIMessage
```

2. **新版本导入方式**（LangChain >= 1.0）：
```python
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
```

## 解决方案

### 方法一：更新导入语句（推荐）

将代码中的导入语句从：
```python
try:
    from langchain_openai import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("langchain 相关库未安装，OpenAI功能不可用")
```

更新为：
```python
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("langchain 相关库未安装，OpenAI功能不可用")
```

### 方法二：兼容性导入（备选）

如果需要同时支持新旧版本，可以使用兼容性导入：
```python
try:
    from langchain_openai import ChatOpenAI
    try:
        # 尝试新版本导入路径
        from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    except ImportError:
        # 降级到旧版本导入路径
        from langchain.schema import HumanMessage, SystemMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("langchain 相关库未安装，OpenAI功能不可用")
```

### 方法三：版本固定

在 `requirements.txt` 中指定兼容的版本：
```
langchain>=1.0.0
langchain-openai>=1.0.0
langchain-core>=1.0.0
```

## 验证修复

运行以下命令验证修复是否成功：

```bash
cd /Users/admin/Desktop/Work/ggame/article-rag
python -c "
from src.generation.llm_generator import LANGCHAIN_AVAILABLE
print(f'✅ LANGCHAIN_AVAILABLE: {LANGCHAIN_AVAILABLE}')
"
```

如果输出 `✅ LANGCHAIN_AVAILABLE: True`，说明修复成功。

## LangChain 版本变更历史

| 版本范围 | 消息类导入路径 | 状态 |
|---------|----------------|------|
| < 0.1.0 | `langchain.schema` | 已废弃 |
| 0.1.0 - 0.9.x | `langchain.schema` | 兼容 |
| >= 1.0.0 | `langchain_core.messages` | 当前 |

## 常见错误和解决

### 错误1：No module named 'langchain.schema'
**原因**: 使用了新版本LangChain但用旧的导入路径
**解决**: 更新导入语句为 `from langchain_core.messages import ...`

### 错误2：No module named 'langchain_core'
**原因**: LangChain版本太旧，没有 `langchain_core` 包
**解决**: 升级到 `langchain>=1.0.0`

### 错误3：ImportError: cannot import name 'HumanMessage'
**原因**: 版本不兼容或导入路径错误
**解决**: 检查版本兼容性，使用正确的导入路径

## 最佳实践

1. **使用版本范围**: 在 `requirements.txt` 中使用 `>=` 而不是 `==`
2. **兼容性测试**: 在CI/CD中测试多个版本
3. **文档更新**: 及时更新文档说明依赖版本要求
4. **日志监控**: 监控导入错误日志，及时发现版本问题

## 相关链接

- [LangChain 官方文档](https://python.langchain.com/)
- [LangChain 迁移指南](https://python.langchain.com/docs/guides/migration/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)

---

**注意**: 这个修复已经在当前系统中应用，无需额外操作。
