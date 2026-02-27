"""
RAG 系统主类
整合检索和生成功能
"""
from typing import Dict, Any, Optional
from loguru import logger

from src.core.models import EssayPrompt, RAGRequest, RAGResponse, WritingGuidance
from src.core.config import settings
from src.knowledge import LocalKnowledgeBase, KnowledgeLoader
from src.retrieval import VectorStore, HybridRetriever
from src.generation import LLMGenerator


class RAGSystem:
    """RAG 系统主类"""

    def __init__(self):
        # 初始化组件
        self.knowledge_base = LocalKnowledgeBase(settings.knowledge_base_path)
        self.vector_store = VectorStore(settings.vector_db_path)
        self.retriever = HybridRetriever(self.knowledge_base, self.vector_store)
        self.generator = LLMGenerator()

        # 系统状态
        self.is_initialized = False

        logger.info("RAG 系统初始化完成")

    def initialize(self, load_sample_data: bool = True) -> bool:
        """初始化系统"""
        try:
            # 加载示例数据
            if load_sample_data:
                loader = KnowledgeLoader(self.knowledge_base)
                if not loader.load_sample_data():
                    logger.warning("加载示例数据失败")

            # 构建向量索引
            if not self.retriever.index_knowledge_base():
                logger.warning("构建向量索引失败")

            self.is_initialized = True
            logger.info("RAG 系统初始化成功")
            return True
        except Exception as e:
            logger.error(f"RAG 系统初始化失败: {e}")
            return False

    def process_request(self, request: RAGRequest) -> RAGResponse:
        """处理 RAG 请求"""
        try:
            logger.info("=" * 80)
            logger.info("🎯 开始处理RAG请求")

            # 记录请求信息
            prompt = request.prompt
            logger.info(f"📝 处理作文题目: {prompt.title}")
            logger.info(f"📖 题目描述: {prompt.description or '无'}")
            logger.info(f"🎯 作文类型: {prompt.essay_type}")
            logger.info(f"📊 难度等级: {prompt.difficulty_level}")
            logger.info(f"🔑 关键词: {prompt.keywords}")
            logger.info(f"👤 用户额外要求: {request.user_requirements or '无'}")

            if not self.is_initialized:
                logger.warning("⚠️ 系统未初始化，尝试自动初始化")
                self.initialize()

            # 检索相关内容
            logger.info("🔍 开始检索相关内容...")
            retrieval_results = self.retriever.retrieve_for_prompt(
                prompt,
                top_k=settings.retrieval_top_k
            )

            materials = retrieval_results.get("materials", [])
            essays = retrieval_results.get("essays", [])

            # 记录检索结果
            logger.info("📚 检索结果统计:")
            logger.info(f"  - 相关素材: {len(materials)} 个")
            logger.info(f"  - 相关范文: {len(essays)} 篇")
            logger.info(f"  - 总检索结果: {retrieval_results.get('total_results', 0)} 项")
            logger.info(f"  - 检索查询: {retrieval_results.get('query_text', '')}")

            if materials:
                logger.info("📄 检索到的素材详情:")
                for i, material in enumerate(materials[:3], 1):
                    logger.info(f"  {i}. 【{material.category}】{material.title}")
                    if hasattr(material, 'score'):
                        logger.info(f"     相似度得分: {material.score:.3f}")

            if essays:
                logger.info("📝 检索到的范文详情:")
                for i, essay in enumerate(essays[:3], 1):
                    logger.info(f"  {i}. 【{essay.essay_type}】{essay.title}")
                    if hasattr(essay, 'score'):
                        logger.info(f"     相似度得分: {essay.score:.3f}")

            # 生成写作指导
            logger.info("🤖 开始生成写作指导...")
            context = f"用户要求: {request.user_requirements}" if request.user_requirements else ""

            guidance = self.generator.generate_guidance(
                prompt=prompt,
                materials=materials,
                essays=essays,
                context=context
            )

            # 计算置信度分数
            logger.info("📊 计算置信度分数...")
            confidence_score = self._calculate_confidence_score(
                retrieval_results, guidance
            )
            logger.info(f"📊 最终置信度得分: {confidence_score:.3f}")

            # 构建响应
            response = RAGResponse(
                guidance=guidance,
                confidence_score=confidence_score,
                retrieval_info={
                    "materials_count": len(materials),
                    "essays_count": len(essays),
                    "total_results": retrieval_results.get("total_results", 0),
                    "query_text": retrieval_results.get("query_text", "")
                },
                generation_info={
                    "generator_type": "LLM" if self._is_generator_available() else "Mock",
                    "provider": self.generator.provider,
                    "model_name": self._get_current_model_name()
                }
            )

            logger.info("✅ RAG请求处理完成")
            logger.info("=" * 80)

            return response

        except Exception as e:
            logger.error(f"❌ 处理RAG请求失败: {e}")
            logger.error("=" * 80)

            # 返回错误响应
            fallback_guidance = WritingGuidance(
                theme_analysis="系统暂时无法分析题目，请稍后重试。",
                structure_suggestion=["请根据题目要求规划文章结构"],
                writing_tips=["注意语言表达的准确性"],
                key_points=["紧扣题目要求"],
                reference_materials=[],
                sample_essays=[]
            )

            return RAGResponse(
                guidance=fallback_guidance,
                confidence_score=0.0,
                retrieval_info={"error": str(e)},
                generation_info={"error": str(e)}
            )

    def _calculate_confidence_score(
        self,
        retrieval_results: Dict[str, Any],
        guidance: WritingGuidance
    ) -> float:
        """计算置信度分数"""
        try:
            score = 0.0

            # 检索结果质量 (40%)
            materials_count = len(retrieval_results.get("materials", []))
            essays_count = len(retrieval_results.get("essays", []))

            if materials_count > 0:
                score += 0.2 * min(materials_count / 3, 1.0)  # 最多3个素材

            if essays_count > 0:
                score += 0.2 * min(essays_count / 2, 1.0)    # 最多2个范文

            # 生成内容质量 (60%)
            if guidance.theme_analysis and len(guidance.theme_analysis) > 10:
                score += 0.15

            if guidance.structure_suggestion and len(guidance.structure_suggestion) >= 3:
                score += 0.15

            if guidance.writing_tips and len(guidance.writing_tips) >= 3:
                score += 0.15

            if guidance.key_points and len(guidance.key_points) >= 3:
                score += 0.15

            return min(score, 1.0)
        except Exception as e:
            logger.error(f"计算置信度失败: {e}")
            return 0.5

    def add_material(self, title: str, content: str, category: str = "用户添加") -> bool:
        """添加写作素材"""
        try:
            from ..core.models import WritingMaterial, DifficultyLevel

            material = WritingMaterial(
                title=title,
                content=content,
                category=category,
                difficulty_level=DifficultyLevel.MIDDLE
            )

            success = self.knowledge_base.add_material(material)

            if success:
                # 重建索引
                self.retriever.index_knowledge_base()
                logger.info(f"成功添加素材: {title}")

            return success
        except Exception as e:
            logger.error(f"添加素材失败: {e}")
            return False

    def add_essay(self, title: str, content: str, essay_type: str = "narrative") -> bool:
        """添加范文"""
        try:
            from ..core.models import SampleEssay, EssayType, DifficultyLevel

            essay = SampleEssay(
                title=title,
                content=content,
                essay_type=EssayType(essay_type),
                difficulty_level=DifficultyLevel.MIDDLE
            )

            success = self.knowledge_base.add_essay(essay)

            if success:
                # 重建索引
                self.retriever.index_knowledge_base()
                logger.info(f"成功添加范文: {title}")

            return success
        except Exception as e:
            logger.error(f"添加范文失败: {e}")
            return False

    def _is_generator_available(self) -> bool:
        """检查生成器是否可用"""
        if self.generator.provider == "doubao":
            return self.generator.doubao_client is not None
        elif self.generator.provider == "openai":
            return self.generator.llm is not None
        return False

    def _get_current_model_name(self) -> str:
        """获取当前使用的模型名称"""
        if self.generator.provider == "doubao":
            return getattr(settings, 'doubao_model', 'unknown')
        elif self.generator.provider == "openai":
            return "gpt-3.5-turbo"
        return "unknown"

    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        try:
            # 知识库统计
            materials = self.knowledge_base.list_materials()
            essays = self.knowledge_base.list_essays()

            # 向量数据库统计
            vector_info = self.vector_store.get_collection_info()

            return {
                "initialized": self.is_initialized,
                "knowledge_base": {
                    "materials_count": len(materials),
                    "essays_count": len(essays)
                },
                "vector_store": vector_info,
                "generator": {
                    "available": self._is_generator_available(),
                    "provider": self.generator.provider,
                    "model": self._get_current_model_name()
                }
            }
        except Exception as e:
            logger.error(f"获取系统状态失败: {e}")
            return {"error": str(e)}

    def search_materials(self, query: str, top_k: int = 5) -> list:
        """搜索写作素材"""
        try:
            return self.knowledge_base.search_materials(query, top_k)
        except Exception as e:
            logger.error(f"搜索素材失败: {e}")
            return []

    def search_essays(self, query: str, top_k: int = 3) -> list:
        """搜索范文"""
        try:
            return self.knowledge_base.search_essays(query, top_k)
        except Exception as e:
            logger.error(f"搜索范文失败: {e}")
            return []
