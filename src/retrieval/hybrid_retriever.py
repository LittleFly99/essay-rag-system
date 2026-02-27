"""
混合检索器
结合关键词检索和向量检索
"""
from typing import List, Dict, Any, Tuple, Optional
from loguru import logger

from ..core.models import EssayPrompt, WritingMaterial, SampleEssay, DocumentChunk
from ..core.utils import extract_keywords, calculate_similarity
from ..knowledge.base import BaseKnowledgeBase
from .vector_store import VectorStore


class HybridRetriever:
    """混合检索器"""

    def __init__(self, knowledge_base: BaseKnowledgeBase, vector_store: VectorStore):
        self.knowledge_base = knowledge_base
        self.vector_store = vector_store

        # 检索权重配置
        self.keyword_weight = 0.3
        self.semantic_weight = 0.7
        self.material_weight = 0.6
        self.essay_weight = 0.4

    def retrieve_for_prompt(self, prompt: EssayPrompt, top_k: int = 10) -> Dict[str, Any]:
        """为作文题目检索相关内容"""
        try:
            logger.info("🔍 开始混合检索 (关键词 + 语义检索)")

            # 构建查询文本
            query_text = self._build_query_text(prompt)
            logger.info(f"🔎 构建的查询文本: {query_text}")

            # 关键词检索
            logger.info("📝 执行关键词检索...")
            keyword_results = self._keyword_retrieval(query_text, prompt)
            logger.info(f"📝 关键词检索结果: {len(keyword_results)} 项")

            # 向量检索
            logger.info("🧠 执行语义检索...")
            semantic_results = self._semantic_retrieval(query_text, top_k)
            logger.info(f"🧠 语义检索结果: {len(semantic_results)} 项")

            # 合并和重排序结果
            logger.info("🔄 合并和重排序检索结果...")
            combined_results = self._combine_results(
                keyword_results, semantic_results, top_k
            )
            logger.info(f"🔄 合并后结果: {len(combined_results)} 项")

            # 分离素材和范文
            materials, essays = self._separate_content_types(combined_results)

            # 截取结果并添加分数
            final_materials = materials[:max(1, int(top_k * self.material_weight))]
            final_essays = essays[:max(1, int(top_k * self.essay_weight))]

            # 记录详细的检索结果
            logger.info("📊 最终检索结果详情:")
            logger.info(f"  - 素材: {len(final_materials)} 个")
            if final_materials:
                for i, (material, score) in enumerate(final_materials[:3], 1):
                    logger.info(f"    {i}. 【{material.category}】{material.title} (得分: {score:.3f})")
                    # 为素材添加分数属性以便后续使用
                    material.score = score

            logger.info(f"  - 范文: {len(final_essays)} 篇")
            if final_essays:
                for i, (essay, score) in enumerate(final_essays[:3], 1):
                    logger.info(f"    {i}. 【{essay.essay_type}】{essay.title} (得分: {score:.3f})")
                    # 为范文添加分数属性以便后续使用
                    essay.score = score

            # 提取内容对象（不包含分数）
            materials_only = [item[0] for item in final_materials]
            essays_only = [item[0] for item in final_essays]

            return {
                "materials": materials_only,
                "essays": essays_only,
                "query_text": query_text,
                "keyword_results_count": len(keyword_results),
                "semantic_results_count": len(semantic_results),
                "total_results": len(combined_results)
            }
        except Exception as e:
            logger.error(f"❌ 检索失败: {e}")
            return {
                "materials": [],
                "essays": [],
                "query_text": "",
                "keyword_results_count": 0,
                "semantic_results_count": 0,
                "total_results": 0
            }

    def _build_query_text(self, prompt: EssayPrompt) -> str:
        """构建查询文本"""
        query_parts = [prompt.title]

        if prompt.description:
            query_parts.append(prompt.description)

        if prompt.keywords:
            query_parts.extend(prompt.keywords)

        if prompt.requirements:
            query_parts.extend(prompt.requirements)

        return " ".join(query_parts)

    def _keyword_retrieval(self, query: str, prompt: EssayPrompt) -> List[Tuple[Any, float, str]]:
        """关键词检索"""
        try:
            results = []

            # 搜索素材
            materials = self.knowledge_base.search_materials(query, top_k=10)
            for material in materials:
                # 计算匹配度
                score = self._calculate_keyword_score(query, material, prompt)
                results.append((material, score, "material"))

            # 搜索范文
            essays = self.knowledge_base.search_essays(query, top_k=5)
            for essay in essays:
                # 计算匹配度
                score = self._calculate_keyword_score(query, essay, prompt)
                results.append((essay, score, "essay"))

            return results
        except Exception as e:
            logger.error(f"关键词检索失败: {e}")
            return []

    def _semantic_retrieval(self, query: str, top_k: int) -> List[Tuple[DocumentChunk, float, str]]:
        """向量检索"""
        try:
            # 执行向量搜索
            results = self.vector_store.search(query, top_k=top_k)

            # 转换结果格式
            semantic_results = []
            for chunk, score in results:
                content_type = chunk.metadata.get("content_type", "unknown")
                semantic_results.append((chunk, score, content_type))

            return semantic_results
        except Exception as e:
            logger.error(f"语义检索失败: {e}")
            return []

    def _calculate_keyword_score(self, query: str, content: Any, prompt: EssayPrompt) -> float:
        """计算关键词匹配分数"""
        try:
            # 基础文本相似度
            if hasattr(content, 'title') and hasattr(content, 'content'):
                title_score = calculate_similarity(query, content.title)
                content_score = calculate_similarity(query, content.content)
                base_score = title_score * 0.4 + content_score * 0.6
            else:
                base_score = 0.0

            # 类型匹配加分
            type_bonus = 0.0
            if hasattr(content, 'essay_type') and content.essay_type == prompt.essay_type:
                type_bonus = 0.2

            # 难度匹配加分
            difficulty_bonus = 0.0
            if hasattr(content, 'difficulty_level') and content.difficulty_level == prompt.difficulty_level:
                difficulty_bonus = 0.1

            return min(1.0, base_score + type_bonus + difficulty_bonus)
        except Exception as e:
            logger.error(f"计算关键词分数失败: {e}")
            return 0.0

    def _combine_results(self, keyword_results: List[Tuple], semantic_results: List[Tuple], top_k: int) -> List[Tuple[Any, float, str]]:
        """合并和重排序结果"""
        try:
            combined = {}

            # 处理关键词结果
            for content, score, content_type in keyword_results:
                content_id = getattr(content, 'id', id(content))
                if content_id not in combined:
                    combined[content_id] = {
                        'content': content,
                        'content_type': content_type,
                        'keyword_score': score,
                        'semantic_score': 0.0
                    }
                else:
                    combined[content_id]['keyword_score'] = max(
                        combined[content_id]['keyword_score'], score
                    )

            # 处理语义结果
            for chunk, score, content_type in semantic_results:
                # 对于向量检索结果，我们需要重建原始内容
                # 这里简化处理，直接使用chunk作为内容
                content_id = chunk.id
                if content_id not in combined:
                    combined[content_id] = {
                        'content': chunk,
                        'content_type': content_type,
                        'keyword_score': 0.0,
                        'semantic_score': score
                    }
                else:
                    combined[content_id]['semantic_score'] = max(
                        combined[content_id]['semantic_score'], score
                    )

            # 计算综合分数并排序
            final_results = []
            for content_id, data in combined.items():
                final_score = (
                    data['keyword_score'] * self.keyword_weight +
                    data['semantic_score'] * self.semantic_weight
                )
                final_results.append((data['content'], final_score, data['content_type']))

            # 按分数排序
            final_results.sort(key=lambda x: x[1], reverse=True)

            return final_results[:top_k]
        except Exception as e:
            logger.error(f"合并结果失败: {e}")
            return []

    def _separate_content_types(self, results: List[Tuple[Any, float, str]]) -> Tuple[List[Any], List[Any]]:
        """分离不同类型的内容"""
        materials = []
        essays = []

        for content, score, content_type in results:
            if isinstance(content, WritingMaterial):
                materials.append(content)
            elif isinstance(content, SampleEssay):
                essays.append(content)
            elif isinstance(content, DocumentChunk):
                # 根据元数据判断类型
                chunk_type = content.metadata.get("content_type", "material")
                if chunk_type == "essay":
                    # 重建 SampleEssay 对象（简化处理）
                    essay = SampleEssay(
                        id=content.id,
                        title=content.metadata.get("title", "未知标题"),
                        content=content.content,
                        essay_type=content.metadata.get("essay_type", "narrative"),
                        difficulty_level=content.metadata.get("difficulty_level", "middle")
                    )
                    essays.append(essay)
                else:
                    # 重建 WritingMaterial 对象（简化处理）
                    material = WritingMaterial(
                        id=content.id,
                        title=content.metadata.get("title", "未知标题"),
                        content=content.content,
                        category=content.metadata.get("category", "未知分类"),
                        difficulty_level=content.metadata.get("difficulty_level", "middle")
                    )
                    materials.append(material)

        return materials, essays

    def index_knowledge_base(self) -> bool:
        """将知识库内容索引到向量数据库"""
        try:
            chunks = []

            # 索引素材
            materials = self.knowledge_base.list_materials()
            for material in materials:
                chunk = DocumentChunk(
                    id=f"material_{material.id}",
                    content=f"{material.title}\n\n{material.content}",
                    metadata={
                        "content_type": "material",
                        "title": material.title,
                        "category": material.category,
                        "difficulty_level": material.difficulty_level.value,
                        "keywords": material.keywords
                    },
                    source=f"material_{material.id}",
                    chunk_index=0
                )
                chunks.append(chunk)

            # 索引范文
            essays = self.knowledge_base.list_essays()
            for essay in essays:
                chunk = DocumentChunk(
                    id=f"essay_{essay.id}",
                    content=f"{essay.title}\n\n{essay.content}",
                    metadata={
                        "content_type": "essay",
                        "title": essay.title,
                        "essay_type": essay.essay_type.value,
                        "difficulty_level": essay.difficulty_level.value,
                        "score": essay.score
                    },
                    source=f"essay_{essay.id}",
                    chunk_index=0
                )
                chunks.append(chunk)

            # 添加到向量数据库
            success = self.vector_store.add_documents(chunks)

            if success:
                logger.info(f"成功索引 {len(chunks)} 个文档到向量数据库")

            return success
        except Exception as e:
            logger.error(f"索引知识库失败: {e}")
            return False
