# RAG作文教学系统详细流程图

## 系统总体架构流程图

```mermaid
graph TB
    %% 用户接口层
    User[👤 用户] --> Demo[🖥️ Streamlit演示界面]
    User --> API[🔌 FastAPI接口]

    %% 核心系统
    Demo --> RAGSystem[🎯 RAG核心系统]
    API --> RAGSystem

    %% 子系统模块
    RAGSystem --> KnowledgeBase[📚 知识库模块]
    RAGSystem --> Retriever[🔍 检索模块]
    RAGSystem --> Generator[🤖 生成模块]

    %% 知识库子模块
    KnowledgeBase --> LocalKB[💾 本地知识库]
    LocalKB --> MaterialsJSON[📄 materials.json]
    LocalKB --> EssaysJSON[📄 essays.json]
    LocalKB --> KBLoader[📥 知识库加载器]

    %% 检索子模块
    Retriever --> HybridRetriever[🔄 混合检索器]
    HybridRetriever --> VectorStore[🗃️ 向量存储]
    HybridRetriever --> KeywordSearch[🔤 关键词检索]
    HybridRetriever --> SemanticSearch[🧠 语义检索]

    %% 生成子模块
    Generator --> LLMGenerator[🤖 LLM生成器]
    LLMGenerator --> OpenAI[🌐 OpenAI API]
    LLMGenerator --> MockGenerator[🎭 模拟生成器]

    %% 数据存储
    VectorStore --> VectorDB[(🗄️ 向量数据库<br/>ChromaDB)]

    %% 配置和工具
    RAGSystem --> Config[⚙️ 配置管理]
    RAGSystem --> Utils[🛠️ 工具函数]

    %% 日志和监控
    RAGSystem --> Logger[📝 日志系统<br/>Loguru]

    style RAGSystem fill:#ff9999
    style KnowledgeBase fill:#99ccff
    style Retriever fill:#99ff99
    style Generator fill:#ffcc99
    style VectorDB fill:#cc99ff
```

## 详细数据流程图

```mermaid
sequenceDiagram
    participant User as 👤 用户
    participant Demo as 🖥️ Streamlit界面
    participant RAG as 🎯 RAG系统
    participant KB as 📚 知识库
    participant Ret as 🔍 检索器
    participant VS as 🗃️ 向量存储
    participant Gen as 🤖 生成器
    participant LLM as 🌐 LLM

    Note over User,LLM: 系统初始化阶段
    Demo->>RAG: 初始化系统
    RAG->>KB: 加载知识库
    KB->>KB: 读取materials.json<br/>读取essays.json
    RAG->>VS: 初始化向量存储
    VS->>VS: 加载/创建向量索引
    RAG->>Ret: 构建混合检索器
    Ret->>VS: 索引知识库内容
    RAG-->>Demo: 初始化完成

    Note over User,LLM: 用户查询阶段
    User->>Demo: 输入作文题目
    Demo->>RAG: 处理RAG请求

    Note over RAG,LLM: 检索阶段
    RAG->>Ret: 执行混合检索
    Ret->>VS: 语义检索
    VS-->>Ret: 返回相关文档块
    Ret->>KB: 关键词检索
    KB-->>Ret: 返回匹配素材
    Ret->>Ret: 合并和重排序结果
    Ret-->>RAG: 返回检索结果

    Note over RAG,LLM: 生成阶段
    RAG->>Gen: 生成写作指导
    Gen->>Gen: 构建提示模板
    Gen->>LLM: 调用LLM生成
    LLM-->>Gen: 返回生成结果
    Gen->>Gen: 解析和验证结果
    Gen-->>RAG: 返回写作指导

    RAG-->>Demo: 返回RAG响应
    Demo-->>User: 显示写作指导
```

## 知识库管理流程图

```mermaid
flowchart TD
    Start([开始]) --> CheckFiles{检查数据文件}
    CheckFiles -->|文件不存在| CreateFiles[创建空的JSON文件]
    CheckFiles -->|文件存在| LoadData[加载数据]

    CreateFiles --> InitEmpty[初始化空结构]
    InitEmpty --> LoadSample{加载示例数据?}

    LoadData --> ParseJSON{解析JSON格式}
    ParseJSON -->|数组格式| DirectLoad[直接加载数组]
    ParseJSON -->|对象格式| ExtractKey[提取materials/essays键]
    ParseJSON -->|格式错误| HandleError[错误处理]

    DirectLoad --> ValidateData[验证数据结构]
    ExtractKey --> ValidateData
    HandleError --> CreateBackup[创建备份]
    CreateBackup --> InitEmpty

    ValidateData --> CreateModels[创建Pydantic模型]
    CreateModels --> IndexContent[建立向量索引]

    LoadSample -->|是| LoadSampleData[加载示例素材和范文]
    LoadSample -->|否| IndexContent
    LoadSampleData --> SaveToKB[保存到知识库]
    SaveToKB --> IndexContent

    IndexContent --> Ready([知识库就绪])

    %% 动态添加流程
    AddMaterial([添加新素材]) --> ValidateInput[验证输入数据]
    ValidateInput --> GenerateID[生成唯一ID]
    GenerateID --> ExtractKeywords[提取关键词]
    ExtractKeywords --> SaveMaterial[保存到materials.json]
    SaveMaterial --> UpdateIndex[更新向量索引]
    UpdateIndex --> Complete([完成])

    style Start fill:#90EE90
    style Ready fill:#90EE90
    style Complete fill:#90EE90
    style HandleError fill:#FFB6C1
    style CreateBackup fill:#FFB6C1
```

## 检索系统详细流程图

```mermaid
flowchart TD
    Query[📝 用户查询] --> BuildQuery[构建查询文本]
    BuildQuery --> ExtractKeywords[提取关键词]

    ExtractKeywords --> ParallelSearch{并行检索}

    %% 关键词检索分支
    ParallelSearch --> KeywordBranch[🔤 关键词检索]
    KeywordBranch --> SearchMaterials[搜索素材库]
    KeywordBranch --> SearchEssays[搜索范文库]
    SearchMaterials --> KeywordScore[关键词匹配评分]
    SearchEssays --> KeywordScore

    %% 语义检索分支
    ParallelSearch --> SemanticBranch[🧠 语义检索]
    SemanticBranch --> Embedding[文本向量化]
    Embedding --> VectorSearch[向量相似度搜索]
    VectorSearch --> SemanticScore[语义相似度评分]

    %% 结果合并
    KeywordScore --> Combine[🔄 结果合并]
    SemanticScore --> Combine
    Combine --> WeightedScore[加权评分<br/>关键词:30% 语义:70%]
    WeightedScore --> Rerank[重新排序]
    Rerank --> TopK[选择Top-K结果]

    %% 结果处理
    TopK --> ProcessChunks[处理文档块]
    ProcessChunks --> GroupBySource[按来源分组]
    GroupBySource --> FilterDuplicates[去重处理]
    FilterDuplicates --> FinalResults[📋 最终检索结果]

    %% 错误处理
    VectorSearch -.->|索引不存在| RebuildIndex[重建向量索引]
    RebuildIndex -.-> VectorSearch

    style Query fill:#E6F3FF
    style FinalResults fill:#E6FFE6
    style RebuildIndex fill:#FFE6E6
```

## 生成系统详细流程图

```mermaid
flowchart TD
    Input[📋 检索结果 + 题目] --> ValidateInput{验证输入}
    ValidateInput -->|有效| BuildPrompt[构建生成提示]
    ValidateInput -->|无效| MockGeneration[使用模拟生成]

    BuildPrompt --> SelectTemplate[选择提示模板]
    SelectTemplate --> FillTemplate[填充模板数据]
    FillTemplate --> FormatPrompt[格式化最终提示]

    FormatPrompt --> CheckLLM{LLM可用?}
    CheckLLM -->|可用| CallLLM[调用OpenAI API]
    CheckLLM -->|不可用| MockGeneration

    CallLLM --> ParseResponse[解析LLM响应]
    ParseResponse --> ValidateJSON{验证JSON格式}

    ValidateJSON -->|有效| CreateGuidance[创建WritingGuidance对象]
    ValidateJSON -->|无效| RetryParse[重试解析]
    RetryParse -->|成功| CreateGuidance
    RetryParse -->|失败| FallbackGeneration[降级生成]

    MockGeneration --> GenerateMock[生成模拟指导]
    FallbackGeneration --> GenerateBasic[生成基础指导]
    GenerateMock --> CreateGuidance
    GenerateBasic --> CreateGuidance

    CreateGuidance --> ValidateModel{验证Pydantic模型}
    ValidateModel -->|通过| LogSuccess[记录成功日志]
    ValidateModel -->|失败| LogError[记录错误日志]

    LogSuccess --> FinalResponse[🎯 最终写作指导]
    LogError --> EmergencyResponse[应急响应]
    EmergencyResponse --> FinalResponse

    %% API调用错误处理
    CallLLM -.->|API错误| HandleAPIError[处理API错误]
    HandleAPIError -.->|重试| CallLLM
    HandleAPIError -.->|放弃| FallbackGeneration

    style Input fill:#E6F3FF
    style FinalResponse fill:#E6FFE6
    style MockGeneration fill:#FFF9E6
    style HandleAPIError fill:#FFE6E6
```

## 错误处理和恢复流程图

```mermaid
flowchart TD
    Error[⚠️ 系统错误] --> ClassifyError{错误分类}

    %% 数据相关错误
    ClassifyError -->|数据错误| DataError[数据相关错误]
    DataError --> CheckFile{文件是否存在?}
    CheckFile -->|不存在| CreateEmpty[创建空文件]
    CheckFile -->|存在| ValidateJSON{JSON格式有效?}
    ValidateJSON -->|无效| BackupCorrupted[备份损坏文件]
    BackupCorrupted --> RestoreDefault[恢复默认数据]
    ValidateJSON -->|有效| CheckStructure{数据结构正确?}
    CheckStructure -->|错误| FixStructure[修复数据结构]
    CheckStructure -->|正确| LoadData[重新加载数据]

    %% 模型相关错误
    ClassifyError -->|模型错误| ModelError[模型验证错误]
    ModelError --> CheckFields{检查必需字段}
    CheckFields --> FixMissingFields[补充缺失字段]
    FixMissingFields --> DefaultValues[使用默认值]
    DefaultValues --> RetryValidation[重试验证]

    %% API相关错误
    ClassifyError -->|API错误| APIError[API调用错误]
    APIError --> CheckConnection{网络连接?}
    CheckConnection -->|正常| CheckAuth{认证有效?}
    CheckConnection -->|异常| WaitRetry[等待重试]
    CheckAuth -->|有效| CheckQuota{配额充足?}
    CheckAuth -->|无效| UseMock[使用模拟生成]
    CheckQuota -->|充足| RetryAPI[重试API调用]
    CheckQuota -->|不足| UseMock

    %% 向量存储错误
    ClassifyError -->|向量错误| VectorError[向量存储错误]
    VectorError --> CheckVectorDB{向量DB可用?}
    CheckVectorDB -->|不可用| ReinitVector[重新初始化]
    CheckVectorDB -->|可用| RebuildIndex[重建索引]

    %% 收敛点
    CreateEmpty --> LoadData
    RestoreDefault --> LoadData
    FixStructure --> LoadData
    LoadData --> LogRecovery[记录恢复日志]

    RetryValidation --> LogRecovery
    DefaultValues --> LogRecovery

    WaitRetry --> RetryAPI
    RetryAPI --> LogRecovery
    UseMock --> LogRecovery

    ReinitVector --> LogRecovery
    RebuildIndex --> LogRecovery

    LogRecovery --> SystemReady[🟢 系统恢复]

    style Error fill:#FFE6E6
    style SystemReady fill:#E6FFE6
    style UseMock fill:#FFF9E6
    style LogRecovery fill:#E6F3FF
```

## API服务流程图

```mermaid
flowchart TD
    Client[📱 客户端请求] --> FastAPI[🔌 FastAPI服务器]
    FastAPI --> ValidateRequest{验证请求}
    ValidateRequest -->|有效| ProcessRequest[处理请求]
    ValidateRequest -->|无效| ErrorResponse[返回错误响应]

    ProcessRequest --> RAGCall[调用RAG系统]
    RAGCall --> CheckInit{系统已初始化?}
    CheckInit -->|否| InitSystem[初始化系统]
    CheckInit -->|是| ProcessRAG[处理RAG请求]

    InitSystem --> InitResult{初始化结果}
    InitResult -->|成功| ProcessRAG
    InitResult -->|失败| ServiceError[服务错误响应]

    ProcessRAG --> RAGResponse[RAG处理结果]
    RAGResponse --> FormatResponse[格式化响应]
    FormatResponse --> SuccessResponse[成功响应]

    %% 并行的演示界面流程
    StreamlitUser[👤 演示用户] --> Streamlit[🖥️ Streamlit界面]
    Streamlit --> LocalRAG[本地RAG调用]
    LocalRAG --> DisplayResults[显示结果]

    %% 错误处理
    RAGCall -.->|异常| CatchException[捕获异常]
    CatchException -.-> LogError[记录错误]
    LogError -.-> ErrorResponse

    ErrorResponse --> ErrorLog[错误日志]
    ServiceError --> ErrorLog
    SuccessResponse --> AccessLog[访问日志]

    style Client fill:#E6F3FF
    style SuccessResponse fill:#E6FFE6
    style ErrorResponse fill:#FFE6E6
    style ServiceError fill:#FFE6E6
```

## 系统监控和日志流程图

```mermaid
flowchart TD
    SystemStart[🚀 系统启动] --> InitLogger[初始化Loguru日志]
    InitLogger --> ConfigLog[配置日志级别和输出]
    ConfigLog --> StartMonitoring[开始监控]

    %% 日志收集点
    RAGProcess[RAG处理过程] --> LogInfo[信息日志]
    RAGProcess --> LogWarning[警告日志]
    RAGProcess --> LogError[错误日志]
    RAGProcess --> LogDebug[调试日志]

    %% 性能监控
    StartMonitoring --> MonitorPerformance[性能监控]
    MonitorPerformance --> TrackResponseTime[响应时间追踪]
    MonitorPerformance --> TrackMemoryUsage[内存使用监控]
    MonitorPerformance --> TrackAPIUsage[API使用统计]

    %% 日志输出
    LogInfo --> FileOutput[📁 文件输出]
    LogWarning --> FileOutput
    LogError --> FileOutput
    LogError --> ConsoleOutput[🖥️ 控制台输出]
    LogDebug --> ConsoleOutput

    FileOutput --> LogRotation[日志轮转]
    LogRotation --> ArchiveLogs[归档历史日志]

    %% 异常追踪
    TrackResponseTime --> PerformanceAlerts{性能告警}
    TrackMemoryUsage --> PerformanceAlerts
    PerformanceAlerts -->|超阈值| AlertLog[告警日志]
    PerformanceAlerts -->|正常| ContinueMonitoring[继续监控]

    AlertLog --> FileOutput
    ContinueMonitoring --> MonitorPerformance

    style SystemStart fill:#90EE90
    style LogError fill:#FFB6C1
    style AlertLog fill:#FF6B6B
    style FileOutput fill:#87CEEB
```

---

## 系统特性说明

### 1. 模块化设计

- **知识库模块**: 支持本地JSON文件存储，具备数据验证和错误恢复
- **检索模块**: 混合检索策略，结合关键词和语义检索
- **生成模块**: 支持LLM和模拟生成的双重策略
- **配置模块**: 集中式配置管理，支持环境变量

### 2. 错误处理机制

- **分层错误处理**: 在数据、模型、API、向量存储各层实现错误捕获
- **自动恢复**: 支持数据损坏修复、网络重试、索引重建
- **降级策略**: LLM不可用时自动切换到模拟生成

### 3. 数据兼容性

- **多格式支持**: 兼容数组和对象格式的JSON数据
- **版本兼容**: 支持数据结构的向前兼容
- **动态类型处理**: 使用Pydantic进行数据验证和转换

### 4. 性能优化

- **并行检索**: 关键词和语义检索并行执行
- **缓存机制**: 向量索引缓存，减少重复计算
- **懒加载**: 按需加载数据和模型

### 5. 可观测性

- **详细日志**: 使用Loguru记录系统运行状态
- **性能监控**: 追踪响应时间、内存使用、API调用
- **错误追踪**: 完整的错误栈追踪和恢复路径记录
