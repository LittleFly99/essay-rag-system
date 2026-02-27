"""
知识库基础类
定义知识库的通用接口
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..core.models import WritingMaterial, SampleEssay, DocumentChunk


# (Abstract Base Classes，抽象基类）模块中的一个类。它用于定义抽象基类
class BaseKnowledgeBase(ABC):
    """知识库基础抽象类"""

    @abstractmethod
    def add_material(self, material: WritingMaterial) -> bool:
        """添加写作素材"""
        pass

    @abstractmethod
    def add_essay(self, essay: SampleEssay) -> bool:
        """添加范文"""
        pass

    @abstractmethod
    def search_materials(self, query: str, top_k: int = 5) -> List[WritingMaterial]:
        """搜索写作素材"""
        pass

    @abstractmethod
    def search_essays(self, query: str, top_k: int = 3) -> List[SampleEssay]:
        """搜索范文"""
        pass

    @abstractmethod
    def get_material_by_id(self, material_id: str) -> Optional[WritingMaterial]:
        """根据ID获取素材"""
        pass

    @abstractmethod
    def get_essay_by_id(self, essay_id: str) -> Optional[SampleEssay]:
        """根据ID获取范文"""
        pass

    @abstractmethod
    def list_materials(self, category: Optional[str] = None) -> List[WritingMaterial]:
        """列出所有素材"""
        pass

    @abstractmethod
    def list_essays(self, essay_type: Optional[str] = None) -> List[SampleEssay]:
        """列出所有范文"""
        pass

    @abstractmethod
    def delete_material(self, material_id: str) -> bool:
        """删除素材"""
        pass

    @abstractmethod
    def delete_essay(self, essay_id: str) -> bool:
        """删除范文"""
        pass

    @abstractmethod
    def update_material(self, material: WritingMaterial) -> bool:
        """更新素材"""
        pass

    @abstractmethod
    def update_essay(self, essay: SampleEssay) -> bool:
        """更新范文"""
        pass
