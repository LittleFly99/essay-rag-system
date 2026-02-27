"""
数据模型定义
定义系统中使用的数据结构
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class EssayType(str, Enum): #是在定义一个枚举类型（Enum），但这里有两个父类：str 和 Enum
    """作文类型枚举"""
    NARRATIVE = "narrative"        # 记叙文
    DESCRIPTIVE = "descriptive"    # 说明文
    ARGUMENTATIVE = "argumentative" # 议论文
    EXPOSITORY = "expository"      # 应用文


class DifficultyLevel(str, Enum):
    """难度等级枚举"""
    ELEMENTARY = "elementary"      # 小学
    MIDDLE = "middle"             # 初中
    HIGH = "high"                 # 高中
    ADVANCED = "advanced"         # 高级


class EssayPrompt(BaseModel):
    """作文题目模型"""
    id: Optional[str] = None
    title: str = Field(..., description="作文题目")
# Field 是一个函数，用于为模型字段添加额外的元数据（如描述、默认值、校验规则等）。
# ... 作为第一个参数，表示该字段没有默认值，必须由用户提供。
# 你可以通过关键字参数（如 description="作文题目"）为字段添加描述等信息。
    description: Optional[str] = Field(None, description="题目描述")
    essay_type: EssayType = Field(..., description="作文类型")
    difficulty_level: DifficultyLevel = Field(..., description="难度等级")
    keywords: List[str] = Field(default=[], description="关键词")
    requirements: List[str] = Field(default=[], description="写作要求")
    word_count: Optional[int] = Field(None, description="字数要求")
    time_limit: Optional[int] = Field(None, description="时间限制（分钟）")
    created_at: datetime = Field(default_factory=datetime.now)


class WritingMaterial(BaseModel):
    """写作素材模型"""
    id: Optional[str] = None
    title: str = Field(..., description="素材标题")
    content: str = Field(..., description="素材内容")
    category: str = Field(..., description="素材分类")
    keywords: List[str] = Field(default=[], description="关键词")
    source: Optional[str] = Field(None, description="来源")
    difficulty_level: DifficultyLevel = Field(..., description="适用难度")


class SampleEssay(BaseModel):
    """范文模型"""
    id: Optional[str] = None
    title: str = Field(..., description="范文标题")
    content: str = Field(..., description="范文内容")
    prompt_id: Optional[str] = Field(None, description="对应题目ID")
    essay_type: EssayType = Field(..., description="作文类型")
    difficulty_level: DifficultyLevel = Field(..., description="难度等级")
    score: Optional[int] = Field(None, description="评分")
    highlights: List[str] = Field(default=[], description="亮点分析")
    structure_analysis: Optional[str] = Field(None, description="结构分析")


class WritingGuidance(BaseModel):
    """写作指导模型"""
    theme_analysis: str = Field(..., description="主题分析")
    structure_suggestion: List[str] = Field(..., description="结构建议")
    writing_tips: List[str] = Field(..., description="写作技巧")
    key_points: List[str] = Field(..., description="要点提示")
    reference_materials: List[WritingMaterial] = Field(default=[], description="参考素材")
    sample_essays: List[SampleEssay] = Field(default=[], description="参考范文")


class RAGRequest(BaseModel):
    """RAG 请求模型"""
    prompt: EssayPrompt = Field(..., description="作文题目")
    user_requirements: Optional[str] = Field(None, description="用户特殊要求")
    context_preference: Optional[str] = Field(None, description="上下文偏好")


class RAGResponse(BaseModel):
    """RAG 响应模型"""
    guidance: WritingGuidance = Field(..., description="写作指导")
    confidence_score: float = Field(..., description="置信度分数")
    retrieval_info: Dict[str, Any] = Field(default={}, description="检索信息")
    generation_info: Dict[str, Any] = Field(default={}, description="生成信息")


class DocumentChunk(BaseModel):
    """文档块模型"""
    id: Optional[str] = None
    content: str = Field(..., description="文档内容")
    metadata: Dict[str, Any] = Field(default={}, description="元数据")
    embedding: Optional[List[float]] = Field(None, description="向量嵌入")
    source: str = Field(..., description="来源文档")
    chunk_index: int = Field(..., description="块索引")
