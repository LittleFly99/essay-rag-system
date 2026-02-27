"""
核心配置模块
管理系统的所有配置信息
"""
import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings(BaseSettings):
    """系统配置类"""

    # 应用基本信息
    app_name: str = Field("RAG作文教学系统", env="APP_NAME")
    version: str = Field("1.0.0", env="VERSION")

    # LLM 配置
    llm_provider: str = Field("doubao", env="LLM_PROVIDER")  # openai, doubao

    # OpenAI 配置
    openai_api_key: str = Field("", env="OPENAI_API_KEY")  # 允许为空，用于测试
    openai_base_url: str = Field("https://api.openai.com/v1", env="OPENAI_BASE_URL")

    # 火山引擎豆包 配置
    doubao_api_key: str = Field("ecaff6b2-54e0-413c-8b16-d030a781ffbf", env="DOUBAO_API_KEY")
    doubao_endpoint: str = Field("https://ark.cn-beijing.volces.com/api/v3", env="DOUBAO_ENDPOINT")  # 例如:
    doubao_model: str = Field("doubao-seed-2-0-mini-260215", env="DOUBAO_MODEL")  # 模型名称

    # 嵌入模型配置
    embedding_model: str = Field(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        env="EMBEDDING_MODEL"
    )
    embedding_device: str = Field("cpu", env="EMBEDDING_DEVICE")

    # 向量数据库配置
    vector_db_type: str = Field("chroma", env="VECTOR_DB_TYPE")
    vector_db_path: str = Field("./data/vectordb", env="VECTOR_DB_PATH")

    # 知识库配置
    knowledge_base_path: str = Field("./data/knowledge", env="KNOWLEDGE_BASE_PATH")
    sample_essays_path: str = Field("./data/essays", env="SAMPLE_ESSAYS_PATH")

    # API 服务配置
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
    debug: bool = Field(True, env="DEBUG")

    # 日志配置
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("./logs/app.log", env="LOG_FILE")

    # RAG 配置
    retrieval_top_k: int = Field(5, env="RETRIEVAL_TOP_K")
    similarity_threshold: float = Field(0.7, env="SIMILARITY_THRESHOLD")
    max_context_length: int = Field(4000, env="MAX_CONTEXT_LENGTH")

    class Config:
        env_file = ".env"
        case_sensitive = False


# 全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例"""
    return settings


def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        settings.vector_db_path,
        settings.knowledge_base_path,
        settings.sample_essays_path,
        os.path.dirname(settings.log_file),
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# 初始化目录
ensure_directories()
