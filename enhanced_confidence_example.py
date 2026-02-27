#!/usr/bin/env python3
"""
置信度计算改进示例
演示更加智能的置信度计算方法
"""

import math
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class ConfidenceLevel(Enum):
    """置信度等级"""
    VERY_HIGH = "very_high"    # 0.9-1.0
    HIGH = "high"              # 0.8-0.9
    MEDIUM = "medium"          # 0.6-0.8
    LOW = "low"                # 0.4-0.6
    VERY_LOW = "very_low"      # 0.0-0.4


@dataclass
class ConfidenceMetrics:
    """置信度计算指标"""
    retrieval_quality: float   # 检索质量 0-1
    semantic_relevance: float  # 语义相关性 0-1
    content_completeness: float # 内容完整性 0-1
    user_context_match: float  # 用户需求匹配度 0-1

    def overall_score(self, weights: Dict[str, float] = None) -> float:
        """计算综合置信度分数"""
        if weights is None:
            weights = {
                'retrieval_quality': 0.3,
                'semantic_relevance': 0.3,
                'content_completeness': 0.2,
                'user_context_match': 0.2
            }

        score = (
            self.retrieval_quality * weights['retrieval_quality'] +
            self.semantic_relevance * weights['semantic_relevance'] +
            self.content_completeness * weights['content_completeness'] +
            self.user_context_match * weights['user_context_match']
        )

        return min(max(score, 0.0), 1.0)


class EnhancedConfidenceCalculator:
    """增强版置信度计算器"""

    def __init__(self):
        self.user_feedback_history = []  # 用户反馈历史
        self.model_performance_cache = {}  # 模型性能缓存

    def calculate_retrieval_quality(self, retrieval_results: Dict) -> float:
        """计算检索质量分数"""
        materials = retrieval_results.get('materials', [])
        essays = retrieval_results.get('essays', [])

        # 基础数量分数
        material_score = min(len(materials) / 3, 1.0) * 0.5
        essay_score = min(len(essays) / 2, 1.0) * 0.5

        # 检索相关性分数（如果有分数信息）
        relevance_scores = []
        for material in materials:
            if hasattr(material, 'score'):
                relevance_scores.append(material.score)

        for essay in essays:
            if hasattr(essay, 'score'):
                relevance_scores.append(essay.score)

        # 平均相关性分数
        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.5

        # 综合评分：数量分数 + 相关性分数
        quality_score = (material_score + essay_score) * 0.6 + avg_relevance * 0.4

        return min(quality_score, 1.0)

    def calculate_semantic_relevance(self, query: str, generated_content: str) -> float:
        """计算语义相关性（简化版本，实际可用更复杂的NLP模型）"""
        # 这里是简化实现，实际应用中可以使用句向量相似度
        query_words = set(query.lower().split())
        content_words = set(generated_content.lower().split())

        if not query_words:
            return 0.5

        # 计算词汇重叠度
        overlap = len(query_words.intersection(content_words))
        relevance = overlap / len(query_words)

        # 应用sigmoid函数进行平滑
        return 1 / (1 + math.exp(-5 * (relevance - 0.5)))

    def calculate_content_completeness(self, guidance) -> float:
        """计算内容完整性"""
        scores = []

        # 主题分析完整性
        if hasattr(guidance, 'theme_analysis') and guidance.theme_analysis:
            analysis_score = min(len(guidance.theme_analysis) / 100, 1.0)
            scores.append(analysis_score)

        # 结构建议完整性
        if hasattr(guidance, 'structure_suggestion') and guidance.structure_suggestion:
            structure_score = min(len(guidance.structure_suggestion) / 3, 1.0)
            scores.append(structure_score)

        # 写作技巧完整性
        if hasattr(guidance, 'writing_tips') and guidance.writing_tips:
            tips_score = min(len(guidance.writing_tips) / 4, 1.0)
            scores.append(tips_score)

        # 关键要点完整性
        if hasattr(guidance, 'key_points') and guidance.key_points:
            points_score = min(len(guidance.key_points) / 4, 1.0)
            scores.append(points_score)

        return sum(scores) / len(scores) if scores else 0.0

    def calculate_user_context_match(self, prompt, user_requirements: str, guidance) -> float:
        """计算用户需求匹配度"""
        match_score = 0.5  # 基础分数

        # 检查是否满足作文类型要求
        if hasattr(prompt, 'essay_type') and hasattr(guidance, 'theme_analysis'):
            if prompt.essay_type.value in guidance.theme_analysis.lower():
                match_score += 0.1

        # 检查是否满足难度等级要求
        if hasattr(prompt, 'difficulty_level') and hasattr(guidance, 'writing_tips'):
            difficulty_keywords = {
                'elementary': ['简单', '基础', '小学'],
                'middle': ['适中', '初中', '中等'],
                'high': ['高级', '高中', '复杂']
            }

            level = prompt.difficulty_level.value
            keywords = difficulty_keywords.get(level, [])

            for keyword in keywords:
                if any(keyword in tip for tip in guidance.writing_tips):
                    match_score += 0.1
                    break

        # 检查用户特殊要求
        if user_requirements:
            req_words = set(user_requirements.lower().split())
            guidance_text = ' '.join([
                guidance.theme_analysis or '',
                ' '.join(guidance.structure_suggestion or []),
                ' '.join(guidance.writing_tips or [])
            ]).lower()

            matched_reqs = sum(1 for word in req_words if word in guidance_text)
            if req_words:
                match_score += 0.3 * (matched_reqs / len(req_words))

        return min(match_score, 1.0)

    def calculate_enhanced_confidence(
        self,
        prompt,
        retrieval_results: Dict,
        guidance,
        user_requirements: str = ""
    ) -> Tuple[float, ConfidenceLevel, Dict[str, float]]:
        """计算增强版置信度"""

        # 计算各项指标
        retrieval_quality = self.calculate_retrieval_quality(retrieval_results)

        # 构建查询文本
        query_text = f"{prompt.title} {prompt.description or ''} {' '.join(prompt.keywords or [])}"
        guidance_text = f"{guidance.theme_analysis or ''} {' '.join(guidance.structure_suggestion or [])}"
        semantic_relevance = self.calculate_semantic_relevance(query_text, guidance_text)

        content_completeness = self.calculate_content_completeness(guidance)
        user_context_match = self.calculate_user_context_match(prompt, user_requirements, guidance)

        # 创建指标对象
        metrics = ConfidenceMetrics(
            retrieval_quality=retrieval_quality,
            semantic_relevance=semantic_relevance,
            content_completeness=content_completeness,
            user_context_match=user_context_match
        )

        # 根据场景动态调整权重
        weights = self._get_dynamic_weights(prompt)

        # 计算最终分数
        final_score = metrics.overall_score(weights)

        # 确定置信度等级
        confidence_level = self._get_confidence_level(final_score)

        # 返回详细信息
        details = {
            'retrieval_quality': retrieval_quality,
            'semantic_relevance': semantic_relevance,
            'content_completeness': content_completeness,
            'user_context_match': user_context_match,
            'weights_used': weights
        }

        return final_score, confidence_level, details

    def _get_dynamic_weights(self, prompt) -> Dict[str, float]:
        """根据场景动态调整权重"""
        # 默认权重
        weights = {
            'retrieval_quality': 0.3,
            'semantic_relevance': 0.3,
            'content_completeness': 0.2,
            'user_context_match': 0.2
        }

        # 根据作文类型调整权重
        if hasattr(prompt, 'essay_type'):
            if prompt.essay_type.value == 'argumentative':
                # 议论文更依赖检索质量
                weights['retrieval_quality'] = 0.4
                weights['semantic_relevance'] = 0.25
                weights['content_completeness'] = 0.2
                weights['user_context_match'] = 0.15
            elif prompt.essay_type.value == 'narrative':
                # 记叙文更注重内容完整性
                weights['retrieval_quality'] = 0.2
                weights['semantic_relevance'] = 0.25
                weights['content_completeness'] = 0.35
                weights['user_context_match'] = 0.2

        # 根据难度等级调整
        if hasattr(prompt, 'difficulty_level'):
            if prompt.difficulty_level.value == 'elementary':
                # 小学阶段更注重用户需求匹配
                weights['user_context_match'] += 0.1
                weights['semantic_relevance'] -= 0.05
                weights['content_completeness'] -= 0.05

        return weights

    def _get_confidence_level(self, score: float) -> ConfidenceLevel:
        """根据分数确定置信度等级"""
        if score >= 0.9:
            return ConfidenceLevel.VERY_HIGH
        elif score >= 0.8:
            return ConfidenceLevel.HIGH
        elif score >= 0.6:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.4:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW

    def get_confidence_message(self, level: ConfidenceLevel, score: float) -> str:
        """根据置信度等级生成用户友好的消息"""
        messages = {
            ConfidenceLevel.VERY_HIGH: f"🌟 系统生成了高质量的写作指导（置信度：{score:.1%}），建议直接使用",
            ConfidenceLevel.HIGH: f"✅ 系统生成了优质的写作建议（置信度：{score:.1%}），质量有保障",
            ConfidenceLevel.MEDIUM: f"📝 系统生成了不错的写作指导（置信度：{score:.1%}），建议结合其他资料参考",
            ConfidenceLevel.LOW: f"⚠️ 当前指导质量一般（置信度：{score:.1%}），建议补充更多信息或重新描述需求",
            ConfidenceLevel.VERY_LOW: f"🔄 当前指导质量有限（置信度：{score:.1%}），建议重新尝试或寻求其他帮助"
        }

        return messages.get(level, f"置信度：{score:.1%}")


# 使用示例
def demonstrate_enhanced_confidence():
    """演示增强版置信度计算"""
    calculator = EnhancedConfidenceCalculator()

    # 模拟数据
    class MockPrompt:
        def __init__(self):
            self.title = "我的家乡"
            self.description = "描写家乡的美丽风景"
            self.essay_type = type('EssayType', (), {'value': 'descriptive'})()
            self.difficulty_level = type('DifficultyLevel', (), {'value': 'elementary'})()
            self.keywords = ['家乡', '风景', '美丽']

    class MockGuidance:
        def __init__(self):
            self.theme_analysis = "这是一篇描写家乡风景的小学作文，重点在于通过具体的景物描写展现家乡的美丽特色，表达对家乡的喜爱之情。"
            self.structure_suggestion = [
                "开头：点明家乡位置，表达喜爱",
                "主体：分段描写不同景物",
                "结尾：总结升华，抒发情感"
            ]
            self.writing_tips = [
                "使用感官描写",
                "运用修辞手法",
                "融入真情实感",
                "语言简洁生动"
            ]
            self.key_points = [
                "选择具体景物",
                "注意描写顺序",
                "表达真实情感",
                "控制文章篇幅"
            ]

    prompt = MockPrompt()
    guidance = MockGuidance()
    retrieval_results = {
        'materials': [type('Material', (), {'score': 0.8})()] * 2,
        'essays': [type('Essay', (), {'score': 0.9})()] * 1
    }

    # 计算置信度
    score, level, details = calculator.calculate_enhanced_confidence(
        prompt, retrieval_results, guidance, "重点指导景物描写技巧"
    )

    print(f"=== 增强版置信度计算结果 ===")
    print(f"最终得分: {score:.3f}")
    print(f"置信度等级: {level.value}")
    print(f"用户消息: {calculator.get_confidence_message(level, score)}")
    print(f"\n详细分解:")
    for metric, value in details.items():
        if metric != 'weights_used':
            print(f"  {metric}: {value:.3f}")

    print(f"\n使用的权重:")
    for weight_name, weight_value in details['weights_used'].items():
        print(f"  {weight_name}: {weight_value:.3f}")


if __name__ == "__main__":
    demonstrate_enhanced_confidence()
