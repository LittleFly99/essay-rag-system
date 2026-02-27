"""
测试用例
"""
import sys
import os
import pytest

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.models import EssayPrompt, EssayType, DifficultyLevel, WritingMaterial
from src.core.utils import clean_text, extract_keywords, calculate_similarity
from src.knowledge.local_kb import LocalKnowledgeBase
from src.rag_system import RAGSystem


class TestCoreModels:
    """核心模型测试"""

    def test_essay_prompt_creation(self):
        """测试作文题目创建"""
        prompt = EssayPrompt(
            title="我的老师",
            description="写一篇记叙文",
            essay_type=EssayType.NARRATIVE,
            difficulty_level=DifficultyLevel.MIDDLE
        )

        assert prompt.title == "我的老师"
        assert prompt.essay_type == EssayType.NARRATIVE
        assert prompt.difficulty_level == DifficultyLevel.MIDDLE

    def test_writing_material_creation(self):
        """测试写作素材创建"""
        material = WritingMaterial(
            title="坚持的故事",
            content="这是一个关于坚持的故事...",
            category="励志故事",
            difficulty_level=DifficultyLevel.MIDDLE
        )

        assert material.title == "坚持的故事"
        assert material.category == "励志故事"


class TestCoreUtils:
    """核心工具测试"""

    def test_clean_text(self):
        """测试文本清理"""
        dirty_text = "  这是一个    测试文本  \n\n  "
        cleaned = clean_text(dirty_text)
        assert cleaned == "这是一个 测试文本"

    def test_extract_keywords(self):
        """测试关键词提取"""
        text = "这是一个关于坚持不懈的故事，讲述了成功的重要性"
        keywords = extract_keywords(text, top_k=3)
        assert len(keywords) <= 3

    def test_calculate_similarity(self):
        """测试相似度计算"""
        text1 = "这是第一个文本"
        text2 = "这是第二个文本"
        text3 = "完全不同的内容"

        sim1 = calculate_similarity(text1, text2)
        sim2 = calculate_similarity(text1, text3)

        # text1 和 text2 应该比 text1 和 text3 更相似
        assert sim1 > sim2


class TestKnowledgeBase:
    """知识库测试"""

    def setup_method(self):
        """测试前设置"""
        self.kb = LocalKnowledgeBase("./test_data/knowledge")

    def test_add_material(self):
        """测试添加素材"""
        material = WritingMaterial(
            title="测试素材",
            content="这是一个测试素材",
            category="测试分类",
            difficulty_level=DifficultyLevel.MIDDLE
        )

        success = self.kb.add_material(material)
        assert success

    def test_search_materials(self):
        """测试搜索素材"""
        # 先添加一个素材
        material = WritingMaterial(
            title="坚持测试",
            content="关于坚持的测试内容",
            category="测试",
            difficulty_level=DifficultyLevel.MIDDLE
        )
        self.kb.add_material(material)

        # 搜索
        results = self.kb.search_materials("坚持")
        assert len(results) > 0


class TestRAGSystem:
    """RAG系统测试"""

    def setup_method(self):
        """测试前设置"""
        self.rag_system = RAGSystem()

    def test_system_initialization(self):
        """测试系统初始化"""
        success = self.rag_system.initialize()
        assert success
        assert self.rag_system.is_initialized

    def test_process_request(self):
        """测试处理请求"""
        from src.core.models import RAGRequest

        # 初始化系统
        self.rag_system.initialize()

        # 创建请求
        prompt = EssayPrompt(
            title="测试题目",
            essay_type=EssayType.NARRATIVE,
            difficulty_level=DifficultyLevel.MIDDLE
        )

        request = RAGRequest(prompt=prompt)

        # 处理请求
        response = self.rag_system.process_request(request)

        assert response is not None
        assert response.guidance is not None
        assert response.confidence_score >= 0.0

    def test_add_material(self):
        """测试添加素材"""
        self.rag_system.initialize()

        success = self.rag_system.add_material(
            title="测试素材",
            content="这是测试内容",
            category="测试"
        )

        assert success

    def test_search_functionality(self):
        """测试搜索功能"""
        self.rag_system.initialize()

        # 添加测试数据
        self.rag_system.add_material(
            title="友谊测试",
            content="关于友谊的测试内容",
            category="测试"
        )

        # 搜索
        materials = self.rag_system.search_materials("友谊")
        assert len(materials) > 0


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
