# 📁 RAG作文教学系统 - 代码架构详解

## 🏗️ 项目整体结构

```
article-rag/                    # 项目根目录
├── src/                        # 源代码目录
│   ├── core/                   # 🔧 核心基础模块
│   │   ├── __init__.py        #    模块导出
│   │   ├── config.py          #    系统配置管理
│   │   ├── models.py          #    数据模型定义
│   │   └── utils.py           #    通用工具函数
│   ├── knowledge/              # 📚 知识库管理模块
│   │   ├── __init__.py        #    模块导出
│   │   ├── base.py            #    知识库基础接口
│   │   ├── local_kb.py        #    本地文件知识库实现
│   │   └── loader.py          #    数据加载器
│   ├── retrieval/              # 🔍 检索模块
│   │   ├── __init__.py        #    模块导出
│   │   ├── embedding.py       #    文本向量化
│   │   ├── vector_store.py    #    向量数据库
│   │   └── hybrid_retriever.py #   混合检索器
│   ├── generation/             # ⚡ 生成模块
│   │   ├── __init__.py        #    模块导出
│   │   └── llm_generator.py   #    LLM生成器
│   ├── api/                    # 🌐 Web API模块
│   │   ├── __init__.py        #    模块导出
│   │   └── main.py            #    FastAPI服务
│   └── rag_system.py          # 🎯 RAG主系统类
├── data/                       # 📁 数据存储
│   ├── knowledge/              #    知识库文件
│   ├── essays/                 #    范文存储
│   └── vectordb/              #    向量数据库
├── examples/                   # 📖 使用示例
│   └── quick_start.py         #    快速开始示例
├── tests/                      # 🧪 测试文件
│   └── test_rag_system.py     #    系统测试
├── main.py                     # 🚀 主程序入口
├── simple_demo.py             # 🎮 简化演示版本
├── start_server.py            # 🌐 Web服务启动
└── requirements.txt           # 📦 依赖包列表
```

## 🔍 各模块功能详解

### 1. 核心模块 (src/core/)

这是整个系统的基础，提供数据模型、配置管理和通用工具。

#### config.py - 配置管理
```python
# 作用：管理系统的所有配置参数
class Settings:
    openai_api_key: str        # OpenAI API密钥
    embedding_model: str       # 嵌入模型名称
    vector_db_path: str        # 向量数据库路径
    knowledge_base_path: str   # 知识库路径
    # ... 其他配置
```

#### models.py - 数据模型
```python
# 作用：定义系统中使用的所有数据结构
class EssayPrompt:             # 作文题目
    title: str                 # 题目标题
    essay_type: EssayType      # 作文类型(记叙文/议论文)
    difficulty_level: str      # 难度等级

class WritingMaterial:         # 写作素材
    title: str                 # 素材标题
    content: str               # 素材内容
    category: str              # 素材分类

class WritingGuidance:         # 写作指导
    theme_analysis: str        # 主题分析
    structure_suggestion: List # 结构建议
    writing_tips: List         # 写作技巧
```

#### utils.py - 工具函数
```python
# 作用：提供文本处理、文件操作等通用功能
def clean_text(text):          # 文本清理
def extract_keywords(text):    # 关键词提取
def calculate_similarity():    # 相似度计算
def chunk_text(text):          # 文本分块
```

### 2. 知识库模块 (src/knowledge/)

管理作文素材和范文的存储和检索。

#### base.py - 基础接口
```python
# 作用：定义知识库的统一接口规范
class BaseKnowledgeBase(ABC):
    def add_material():        # 添加素材
    def search_materials():    # 搜索素材
    def add_essay():           # 添加范文
    def search_essays():       # 搜索范文
```

#### local_kb.py - 本地实现
```python
# 作用：基于本地JSON文件的知识库实现
class LocalKnowledgeBase:
    def __init__(knowledge_path):
        self.materials_file    # 素材文件路径
        self.essays_file       # 范文文件路径

    def _load_materials():     # 加载素材数据
    def _save_materials():     # 保存素材数据
    def search_materials():    # 基于关键词搜索
```

#### loader.py - 数据加载
```python
# 作用：加载和初始化知识库数据
class KnowledgeLoader:
    def load_sample_data():    # 加载示例数据
    def load_from_directory(): # 从目录批量加载
```

### 3. 检索模块 (src/retrieval/)

实现文本的向量化和相似度检索。

#### embedding.py - 向量化
```python
# 作用：将文本转换为数值向量
class EmbeddingModel:
    def encode(texts):         # 文本编码为向量
    def similarity():          # 计算向量相似度
    def _simple_encode():      # 简单TF-IDF编码(备用)
```

#### vector_store.py - 向量存储
```python
# 作用：管理向量数据库，存储和检索向量
class VectorStore:
    def add_documents():       # 添加文档向量
    def search():              # 向量相似度搜索
    def _search_chromadb():    # ChromaDB搜索
    def _search_memory():      # 内存搜索(备用)
```

#### hybrid_retriever.py - 混合检索
```python
# 作用：结合关键词和向量检索，提供更准确的结果
class HybridRetriever:
    def retrieve_for_prompt(): # 为题目检索相关内容
    def _keyword_retrieval():  # 关键词检索
    def _semantic_retrieval(): # 语义向量检索
    def _combine_results():    # 结果融合和排序
```

### 4. 生成模块 (src/generation/)

基于检索结果生成写作指导内容。

#### llm_generator.py - LLM生成器
```python
# 作用：使用大语言模型生成写作指导
class LLMGenerator:
    def generate_guidance():        # 生成写作指导
    def _generate_with_llm():       # 使用真实LLM
    def _generate_mock_guidance():  # 模板生成(备用)
    def _build_system_prompt():     # 构建系统提示词
    def _parse_llm_response():      # 解析LLM响应
```

### 5. RAG主系统 (src/rag_system.py)

整合所有模块，提供统一的业务接口。

```python
# 作用：RAG系统的核心控制器
class RAGSystem:
    def __init__():
        self.knowledge_base    # 知识库实例
        self.vector_store      # 向量存储实例
        self.retriever         # 混合检索器
        self.generator         # LLM生成器

    def initialize():          # 系统初始化
    def process_request():     # 处理RAG请求
    def add_material():        # 添加新素材
    def get_system_status():   # 获取系统状态
```

### 6. API模块 (src/api/)

提供Web服务接口。

#### main.py - FastAPI服务
```python
# 作用：提供RESTful API接口
@app.post("/generate-guidance") # 生成写作指导
@app.post("/add-material")      # 添加素材
@app.get("/search-materials")   # 搜索素材
@app.get("/system-status")      # 系统状态
```

## 🔄 系统工作流程

### 1. 初始化流程
```
1. 加载配置 (config.py)
2. 初始化知识库 (LocalKnowledgeBase)
3. 加载示例数据 (KnowledgeLoader)
4. 构建向量索引 (VectorStore + HybridRetriever)
5. 初始化生成器 (LLMGenerator)
```

### 2. 请求处理流程
```
用户输入作文题目
    ↓
构建RAGRequest对象 (models.py)
    ↓
混合检索相关内容 (HybridRetriever)
    ├── 关键词检索 (LocalKnowledgeBase)
    └── 向量检索 (VectorStore)
    ↓
结果融合排序
    ↓
生成写作指导 (LLMGenerator)
    ↓
返回RAGResponse对象
```

### 3. 数据流向
```
原始文本 → 文本清理 → 关键词提取 → 向量编码
    ↓
存储到知识库 (JSON) + 向量库 (ChromaDB/Memory)
    ↓
检索时：查询 → 匹配 → 排序 → 返回Top-K结果
    ↓
生成时：结果 + 提示词 → LLM → 结构化指导
```

## 💡 核心设计模式

### 1. 策略模式
- 多种检索策略：关键词 + 向量 + 混合
- 多种存储策略：本地文件 + 向量数据库 + 内存

### 2. 适配器模式
- 统一的知识库接口，支持不同存储后端
- 统一的向量存储接口，支持不同向量数据库

### 3. 模板方法模式
- 检索流程的标准化步骤
- 生成流程的标准化步骤

### 4. 工厂模式
- 根据配置创建不同的组件实例

## 🎯 关键技术点

### 1. 文本相似度计算
```python
# 简单方法：基于词汇重叠的Jaccard相似度
def calculate_similarity(text1, text2):
    words1 = set(segment_chinese_text(text1))
    words2 = set(segment_chinese_text(text2))
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union)
```

### 2. 混合检索策略
```python
# 结合多种检索方法
final_score = (
    keyword_score * keyword_weight +
    semantic_score * semantic_weight
)
```

### 3. 结果生成模板
```python
# 根据作文类型生成不同的指导模板
if essay_type == "narrative":
    # 记叙文模板
elif essay_type == "argumentative":
    # 议论文模板
```

## 🚀 使用示例

### 简单使用
```python
# 1. 初始化系统
system = RAGSystem()
system.initialize()

# 2. 创建题目
prompt = EssayPrompt(
    title="我的老师",
    essay_type="narrative"
)

# 3. 生成指导
response = system.process_request(RAGRequest(prompt=prompt))
print(response.guidance.theme_analysis)
```

### Web API使用
```bash
# 启动服务
python start_server.py

# 调用API
curl -X POST "http://localhost:8000/generate-guidance" \
     -H "Content-Type: application/json" \
     -d '{"title": "我的老师", "essay_type": "narrative"}'
```

## 🔧 扩展点

### 1. 新增检索策略
```python
class SemanticRetriever(BaseRetriever):
    def retrieve(self, query):
        # 实现新的检索逻辑
        pass
```

### 2. 新增存储后端
```python
class DatabaseKnowledgeBase(BaseKnowledgeBase):
    def __init__(self, db_connection):
        # 实现数据库存储
        pass
```

### 3. 新增生成策略
```python
class AdvancedGenerator(BaseGenerator):
    def generate(self, context):
        # 实现高级生成逻辑
        pass
```

这个架构的优势：
- 📦 **模块化**: 每个模块职责单一，便于测试和维护
- 🔌 **可扩展**: 通过接口设计，便于添加新功能
- 🎯 **专业化**: 针对作文教学场景优化
- 🛡️ **稳健性**: 多重备用方案，确保系统稳定运行

希望这个详细的架构解析能帮助您理解整个RAG系统的设计思路和实现细节！
