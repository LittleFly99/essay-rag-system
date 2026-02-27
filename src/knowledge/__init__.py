"""
知识库管理模块
"""
from .base import BaseKnowledgeBase
from .local_kb import LocalKnowledgeBase
from .loader import KnowledgeLoader

__all__ = [
    'BaseKnowledgeBase',
    'LocalKnowledgeBase',
    'KnowledgeLoader'
]
