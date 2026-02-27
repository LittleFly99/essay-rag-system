#!/usr/bin/env python3
"""
当前RAG系统置信度计算演示
复现实际系统中的置信度计算逻辑
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class MockMaterial:
    """模拟素材对象"""
    title: str
    content: str
    category: str


@dataclass
class MockEssay:
    """模拟范文对象"""
    title: str
    content: str
    essay_type: str


@dataclass
class MockGuidance:
    """模拟生成的写作指导"""
    theme_analysis: str
    structure_suggestion: List[str]
    writing_tips: List[str]
    key_points: List[str]


def calculate_current_confidence(
    materials: List[MockMaterial],
    essays: List[MockEssay],
    guidance: MockGuidance
) -> float:
    """
    按照当前系统逻辑计算置信度
    完全复现 rag_system.py 中的 _calculate_confidence_score 方法
    """
    score = 0.0

    print("🧮 开始计算置信度...")
    print("-" * 50)

    # 检索结果质量 (40%)
    materials_count = len(materials)
    essays_count = len(essays)

    print(f"📚 检索质量评估 (40%):")

    # 素材得分 (20%)
    if materials_count > 0:
        material_score = 0.2 * min(materials_count / 3, 1.0)
        score += material_score
        print(f"  📄 素材得分: min({materials_count}/3, 1.0) × 0.2 = {material_score:.3f}")
    else:
        print(f"  📄 素材得分: 0个素材 → 0.000")

    # 范文得分 (20%)
    if essays_count > 0:
        essay_score = 0.2 * min(essays_count / 2, 1.0)
        score += essay_score
        print(f"  📝 范文得分: min({essays_count}/2, 1.0) × 0.2 = {essay_score:.3f}")
    else:
        print(f"  📝 范文得分: 0篇范文 → 0.000")

    print(f"  📊 检索小计: {score:.3f}")

    # 生成内容质量 (60%)
    print(f"\n🤖 生成质量评估 (60%):")

    # 主题分析 (15%)
    if guidance.theme_analysis and len(guidance.theme_analysis) > 10:
        theme_score = 0.15
        score += theme_score
        print(f"  🎯 主题分析: 长度{len(guidance.theme_analysis)} > 10 → 0.150")
    else:
        theme_length = len(guidance.theme_analysis) if guidance.theme_analysis else 0
        print(f"  🎯 主题分析: 长度{theme_length} ≤ 10 → 0.000")

    # 结构建议 (15%)
    structure_count = len(guidance.structure_suggestion) if guidance.structure_suggestion else 0
    if structure_count >= 3:
        structure_score = 0.15
        score += structure_score
        print(f"  🏗️ 结构建议: {structure_count}条 ≥ 3 → 0.150")
    else:
        print(f"  🏗️ 结构建议: {structure_count}条 < 3 → 0.000")

    # 写作技巧 (15%)
    tips_count = len(guidance.writing_tips) if guidance.writing_tips else 0
    if tips_count >= 3:
        tips_score = 0.15
        score += tips_score
        print(f"  ✍️ 写作技巧: {tips_count}条 ≥ 3 → 0.150")
    else:
        print(f"  ✍️ 写作技巧: {tips_count}条 < 3 → 0.000")

    # 关键要点 (15%)
    points_count = len(guidance.key_points) if guidance.key_points else 0
    if points_count >= 3:
        points_score = 0.15
        score += points_score
        print(f"  💡 关键要点: {points_count}条 ≥ 3 → 0.150")
    else:
        print(f"  💡 关键要点: {points_count}条 < 3 → 0.000")

    # 确保分数在合理范围
    final_score = min(score, 1.0)

    print(f"\n📊 置信度计算结果:")
    print(f"  原始总分: {score:.3f}")
    print(f"  最终得分: {final_score:.3f} (限制在1.0以内)")

    return final_score


def get_confidence_level(score: float) -> str:
    """根据分数确定置信度等级"""
    if score >= 0.8:
        return "优秀 🟢"
    elif score >= 0.6:
        return "良好 🟡"
    elif score >= 0.4:
        return "一般 🟠"
    elif score >= 0.2:
        return "较差 🔴"
    else:
        return "很差 ⚫"


def demonstrate_confidence_scenarios():
    """演示不同场景下的置信度计算"""

    scenarios = [
        {
            "name": "高质量场景",
            "description": "充足的检索结果 + 完整的生成内容",
            "materials": [
                MockMaterial("成长的烦恼", "关于青少年成长过程中遇到的困惑...", "成长"),
                MockMaterial("挫折教育", "挫折是成长路上的必修课...", "励志"),
                MockMaterial("友谊的力量", "真正的友谊能帮助人度过难关...", "情感"),
                MockMaterial("学习的乐趣", "在知识的海洋中感受快乐...", "学习")
            ],
            "essays": [
                MockEssay("那一刻我长大了", "记得那个雨夜，我独自在家...", "记叙文"),
                MockEssay("成长路上有你真好", "感谢一路相伴的老师和同学...", "记叙文")
            ],
            "guidance": MockGuidance(
                theme_analysis="成长是人生必经的过程，需要通过具体的事例来展现内心的变化和感悟，体现从幼稚到成熟的转变。",
                structure_suggestion=[
                    "开头：设置特定情境，引出成长话题",
                    "发展：叙述具体成长事件，详写心理变化过程",
                    "高潮：突出关键转折点，展现成长的关键时刻",
                    "结尾：升华主题，表达成长的意义和收获"
                ],
                writing_tips=[
                    "运用细节描写突出人物心理变化",
                    "使用对比手法展现成长前后的差异",
                    "适当运用议论抒情点明成长意义",
                    "注意情节的起伏和情感的递进"
                ],
                key_points=[
                    "选择具有转折意义的成长事件",
                    "重点描写心理变化的过程",
                    "体现成长的积极意义和启发",
                    "语言要真挚自然，贴近学生生活"
                ]
            )
        },

        {
            "name": "中等质量场景",
            "description": "部分检索结果 + 基础生成内容",
            "materials": [
                MockMaterial("网络时代", "互联网改变了我们的生活方式...", "科技")
            ],
            "essays": [],
            "guidance": MockGuidance(
                theme_analysis="网络对现代生活的影响是多方面的。",
                structure_suggestion=[
                    "开头：提出网络时代背景",
                    "主体：分析网络影响",
                    "结尾：总结观点"
                ],
                writing_tips=[
                    "举例说明",
                    "逻辑清晰"
                ],
                key_points=[
                    "网络便利性",
                    "网络问题",
                    "理性使用"
                ]
            )
        },

        {
            "name": "低质量场景",
            "description": "无检索结果 + 简单生成内容",
            "materials": [],
            "essays": [],
            "guidance": MockGuidance(
                theme_analysis="需要分析题目。",
                structure_suggestion=["开头", "中间"],
                writing_tips=["注意语言"],
                key_points=["重点突出"]
            )
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*60}")
        print(f"📝 场景 {i}: {scenario['name']}")
        print(f"📋 描述: {scenario['description']}")
        print(f"{'='*60}")

        confidence = calculate_current_confidence(
            scenario["materials"],
            scenario["essays"],
            scenario["guidance"]
        )

        level = get_confidence_level(confidence)
        print(f"\n🎯 置信度等级: {level}")
        print(f"📈 置信度分数: {confidence:.3f}")

        # 给出使用建议
        if confidence >= 0.8:
            advice = "✅ 建议直接使用系统指导，质量可靠"
        elif confidence >= 0.6:
            advice = "⚡ 可以使用但建议补充完善"
        elif confidence >= 0.4:
            advice = "⚠️ 谨慎使用，需要大量补充"
        else:
            advice = "❌ 不建议使用，需要人工指导"

        print(f"💡 使用建议: {advice}")


def main():
    """主函数"""
    print("🎯 RAG系统置信度计算演示")
    print("🔍 按照当前系统逻辑复现置信度计算过程")

    demonstrate_confidence_scenarios()

    print(f"\n{'='*60}")
    print("📊 置信度计算规则总结:")
    print("1. 检索质量 (40%):")
    print("   • 素材: min(数量/3, 1.0) × 20%")
    print("   • 范文: min(数量/2, 1.0) × 20%")
    print("2. 生成质量 (60%):")
    print("   • 主题分析: 长度>10字符 → 15%")
    print("   • 结构建议: 数量≥3条 → 15%")
    print("   • 写作技巧: 数量≥3条 → 15%")
    print("   • 关键要点: 数量≥3条 → 15%")
    print("3. 最终得分限制在 [0, 1] 区间")
    print("="*60)


if __name__ == "__main__":
    main()
