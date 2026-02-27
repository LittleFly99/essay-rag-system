"""
本地文件系统知识库实现
使用本地JSON文件存储知识库数据
"""
import os
from typing import List, Dict, Any, Optional
from loguru import logger

from .base import BaseKnowledgeBase
from ..core.models import WritingMaterial, SampleEssay, EssayType, DifficultyLevel
from ..core.utils import (
    load_json_file, save_json_file, generate_id,
    extract_keywords, calculate_similarity
)


class LocalKnowledgeBase(BaseKnowledgeBase):
    """本地文件系统知识库"""

    def __init__(self, knowledge_path: str):
        self.knowledge_path = knowledge_path
        self.materials_file = os.path.join(knowledge_path, "materials.json")
        self.essays_file = os.path.join(knowledge_path, "essays.json")

        # 确保目录存在
        os.makedirs(knowledge_path, exist_ok=True)

        # 初始化数据文件
        self._init_data_files()

    def _init_data_files(self):
        """初始化数据文件"""
        if not os.path.exists(self.materials_file):
            save_json_file({"materials": []}, self.materials_file)

        if not os.path.exists(self.essays_file):
            save_json_file({"essays": []}, self.essays_file)

    def _load_materials(self) -> List[Dict[str, Any]]:
        """加载素材数据"""
        data = load_json_file(self.materials_file)
        if not data:
            return []

        # 兼容两种格式：直接数组格式和对象格式
        if isinstance(data, list):
            # 直接是数组格式
            return data
        elif isinstance(data, dict):
            # 对象格式，包含 materials 键
            return data.get("materials", [])
        else:
            return []

    def _save_materials(self, materials: List[Dict[str, Any]]) -> bool:
        """保存素材数据"""
        return save_json_file({"materials": materials}, self.materials_file)

    def _load_essays(self) -> List[Dict[str, Any]]:
        """加载范文数据"""
        data = load_json_file(self.essays_file)
        if not data:
            return []

        # 兼容两种格式：直接数组格式和对象格式
        if isinstance(data, list):
            # 直接是数组格式
            return data
        elif isinstance(data, dict):
            # 对象格式，包含 essays 键
            return data.get("essays", [])
        else:
            return []

    def _save_essays(self, essays: List[Dict[str, Any]]) -> bool:
        """保存范文数据"""
        return save_json_file({"essays": essays}, self.essays_file)

    def add_material(self, material: WritingMaterial) -> bool:
        """添加写作素材"""
        try:
            materials = self._load_materials()

            # 生成ID如果没有
            if not material.id:
                material.id = generate_id(f"{material.title}_{material.content[:100]}")

            # 检查是否已存在
            if any(m.get("id") == material.id for m in materials):
                logger.warning(f"素材已存在: {material.id}")
                return False

            # 添加到列表
            material_dict = material.model_dump()
            materials.append(material_dict)

            return self._save_materials(materials)
        except Exception as e:
            logger.error(f"添加素材失败: {e}")
            return False

    def add_essay(self, essay: SampleEssay) -> bool:
        """添加范文"""
        try:
            essays = self._load_essays()

            # 生成ID如果没有
            if not essay.id:
                essay.id = generate_id(f"{essay.title}_{essay.content[:100]}")

            # 检查是否已存在
            if any(e.get("id") == essay.id for e in essays):
                logger.warning(f"范文已存在: {essay.id}")
                return False

            # 添加到列表
            essay_dict = essay.dict()
            essays.append(essay_dict)

            return self._save_essays(essays)
        except Exception as e:
            logger.error(f"添加范文失败: {e}")
            return False

    def search_materials(self, query: str, top_k: int = 5) -> List[WritingMaterial]:
        """搜索写作素材"""
        try:
            materials = self._load_materials()
            scored_materials = []

            # 提取查询关键词
            query_keywords = extract_keywords(query)

            for material_dict in materials:
                # 计算相似度分数
                title_score = calculate_similarity(query, material_dict.get("title", ""))
                content_score = calculate_similarity(query, material_dict.get("content", ""))

                # 关键词匹配分数
                material_keywords = material_dict.get("keywords", [])
                keyword_score = len(set(query_keywords) & set(material_keywords)) / max(len(query_keywords), 1)

                # 综合分数
                total_score = title_score * 0.4 + content_score * 0.4 + keyword_score * 0.2

                if total_score > 0.1:  # 过滤掉分数太低的结果
                    scored_materials.append((total_score, material_dict))

            # 按分数排序并返回top_k
            scored_materials.sort(key=lambda x: x[0], reverse=True)
            top_materials = scored_materials[:top_k]

            # 转换为WritingMaterial对象
            result = []
            for score, material_dict in top_materials:
                try:
                    material = WritingMaterial(**material_dict) #这里的 **material_dict 语法叫做“字典解包”，它的作用是把字典里的每个 key-value 对，作为关键字参数传递给 WritingMaterial 的构造函数。
                    result.append(material)#dict 不是直接“取 value”，而是把 key-value 对映射到参数名和值。
                except Exception as e:
                    logger.error(f"解析素材失败: {e}")
                    continue

            return result
        except Exception as e:
            logger.error(f"搜索素材失败: {e}")
            return []

    def search_essays(self, query: str, top_k: int = 3) -> List[SampleEssay]:
        """搜索范文"""
        try:
            essays = self._load_essays()
            scored_essays = []

            # 提取查询关键词
            query_keywords = extract_keywords(query)

            for essay_dict in essays:
                # 计算相似度分数
                title_score = calculate_similarity(query, essay_dict.get("title", ""))
                content_score = calculate_similarity(query, essay_dict.get("content", ""))

                # 综合分数
                total_score = title_score * 0.5 + content_score * 0.5

                if total_score > 0.1:
                    scored_essays.append((total_score, essay_dict))

            # 按分数排序并返回top_k
            scored_essays.sort(key=lambda x: x[0], reverse=True)
            top_essays = scored_essays[:top_k]

            # 转换为SampleEssay对象
            result = []
            for score, essay_dict in top_essays:
                try:
                    essay = SampleEssay(**essay_dict)
                    result.append(essay)
                except Exception as e:
                    logger.error(f"解析范文失败: {e}")
                    continue

            return result
        except Exception as e:
            logger.error(f"搜索范文失败: {e}")
            return []

    def get_material_by_id(self, material_id: str) -> Optional[WritingMaterial]:
        """根据ID获取素材"""
        try:
            materials = self._load_materials()
            for material_dict in materials:
                if material_dict.get("id") == material_id:
                    return WritingMaterial(**material_dict)
            return None
        except Exception as e:
            logger.error(f"获取素材失败: {e}")
            return None

    def get_essay_by_id(self, essay_id: str) -> Optional[SampleEssay]:
        """根据ID获取范文"""
        try:
            essays = self._load_essays()
            for essay_dict in essays:
                if essay_dict.get("id") == essay_id:
                    return SampleEssay(**essay_dict)
            return None
        except Exception as e:
            logger.error(f"获取范文失败: {e}")
            return None

    def list_materials(self, category: Optional[str] = None) -> List[WritingMaterial]:
        """列出所有素材"""
        try:
            materials = self._load_materials()
            result = []

            for material_dict in materials:
                if category is None or material_dict.get("category") == category:
                    try:
                        material = WritingMaterial(**material_dict)
                        result.append(material)
                    except Exception as e:
                        logger.error(f"解析素材失败: {e}")
                        continue

            return result
        except Exception as e:
            logger.error(f"列出素材失败: {e}")
            return []

    def list_essays(self, essay_type: Optional[str] = None) -> List[SampleEssay]:
        """列出所有范文"""
        try:
            essays = self._load_essays()
            result = []

            for essay_dict in essays:
                if essay_type is None or essay_dict.get("essay_type") == essay_type:
                    try:
                        essay = SampleEssay(**essay_dict)
                        result.append(essay)
                    except Exception as e:
                        logger.error(f"解析范文失败: {e}")
                        continue

            return result
        except Exception as e:
            logger.error(f"列出范文失败: {e}")
            return []

    def delete_material(self, material_id: str) -> bool:
        """删除素材"""
        try:
            materials = self._load_materials()
            original_length = len(materials)
            materials = [m for m in materials if m.get("id") != material_id]

            if len(materials) < original_length:
                return self._save_materials(materials)
            return False
        except Exception as e:
            logger.error(f"删除素材失败: {e}")
            return False

    def delete_essay(self, essay_id: str) -> bool:
        """删除范文"""
        try:
            essays = self._load_essays()
            original_length = len(essays)
            essays = [e for e in essays if e.get("id") != essay_id]

            if len(essays) < original_length:
                return self._save_essays(essays)
            return False
        except Exception as e:
            logger.error(f"删除范文失败: {e}")
            return False

    def update_material(self, material: WritingMaterial) -> bool:
        """更新素材"""
        try:
            materials = self._load_materials()

            for i, m in enumerate(materials):
                if m.get("id") == material.id:
                    materials[i] = material.dict()
                    return self._save_materials(materials)

            return False
        except Exception as e:
            logger.error(f"更新素材失败: {e}")
            return False

    def update_essay(self, essay: SampleEssay) -> bool:
        """更新范文"""
        try:
            essays = self._load_essays()

            for i, e in enumerate(essays):
                if e.get("id") == essay.id:
                    essays[i] = essay.dict()
                    return self._save_essays(essays)

            return False
        except Exception as e:
            logger.error(f"更新范文失败: {e}")
            return False
