#!/usr/bin/env python3
"""
置信度实际应用示例
演示如何在教学和学习中使用置信度信息
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ConfidenceExample:
    """置信度使用示例"""
    topic: str
    confidence_score: float
    user_message: str
    teacher_guidance: str
    student_action: str


def generate_confidence_examples() -> List[ConfidenceExample]:
    """生成不同置信度水平的应用示例"""

    examples = [
        # 高置信度示例
        ConfidenceExample(
            topic="以'友谊'为主题写一篇记叙文",
            confidence_score=0.92,
            user_message="🎉 系统非常确信能为您提供高质量的写作指导（置信度：92%）",
            teacher_guidance="可以直接使用系统建议作为教学参考，指导学生按照提供的结构和技巧进行写作。",
            student_action="认真学习系统提供的写作技巧，按照结构建议组织文章，参考推荐的素材和范文。"
        ),

        # 中等置信度示例
        ConfidenceExample(
            topic="谈谈对网络游戏的看法",
            confidence_score=0.65,
            user_message="📝 系统能提供基础指导，但建议您补充更多个人思考（置信度：65%）",
            teacher_guidance="系统建议可作为起点，但需要老师补充最新的网络游戏案例和更深入的分析框架。",
            student_action="参考系统的基本框架，但要自己搜集更多资料，形成独立的观点和论据。"
        ),

        # 低置信度示例
        ConfidenceExample(
            topic="元宇宙技术对未来教育的影响",
            confidence_score=0.28,
            user_message="⚠️ 系统对此话题把握有限，建议寻求老师帮助或查阅专业资料（置信度：28%）",
            teacher_guidance="系统缺乏相关知识，老师需要提供专门的资料和指导，或者调整为学生更熟悉的话题。",
            student_action="这个话题超出系统能力范围，需要主动查找专业资料、新闻报道，或请教老师。"
        )
    ]

    return examples


def demonstrate_confidence_decision_tree():
    """演示基于置信度的决策流程"""

    print("=" * 60)
    print("🌳 基于置信度的决策流程")
    print("=" * 60)

    decision_tree = """
    输入题目 → 系统处理 → 计算置信度
                    ↓
              置信度 ≥ 0.8？
                    ↓
                ┌─── 是 ──→ 直接使用建议
                │            ├─ 学生：按建议写作
                │            └─ 老师：作为教学参考
                ↓
                否
                ↓
           置信度 ≥ 0.4？
                ↓
            ┌─── 是 ──→ 谨慎使用建议
            │            ├─ 学生：参考+补充
            │            └─ 老师：基础框架+自己补充
            ↓
            否
            ↓
        置信度 < 0.4 ──→ 寻求其他帮助
                       ├─ 学生：请教老师或查资料
                       └─ 老师：提供专门指导
    """

    print(decision_tree)


def explain_confidence_components():
    """解释置信度各组成部分的含义"""

    print("\n" + "=" * 60)
    print("🔍 置信度组成部分详解")
    print("=" * 60)

    components = {
        "检索质量 (40%)": {
            "含义": "衡量系统能否找到相关的素材和范文",
            "影响因素": [
                "知识库中相关内容的数量",
                "检索算法的准确性",
                "题目与已有内容的匹配度"
            ],
            "改进方法": [
                "扩充知识库内容",
                "优化检索算法",
                "提高内容标注质量"
            ]
        },

        "内容生成质量 (60%)": {
            "含义": "衡量生成的写作指导是否全面、具体、有用",
            "影响因素": [
                "大语言模型的能力",
                "prompt设计的质量",
                "输入信息的充分性"
            ],
            "改进方法": [
                "升级或微调语言模型",
                "优化prompt模板",
                "增加上下文信息"
            ]
        }
    }

    for component, details in components.items():
        print(f"\n📊 {component}")
        print(f"   含义: {details['含义']}")
        print("   影响因素:")
        for factor in details['影响因素']:
            print(f"     • {factor}")
        print("   改进方法:")
        for method in details['改进方法']:
            print(f"     • {method}")


def show_confidence_improvement_tips():
    """展示提升置信度的技巧"""

    print("\n" + "=" * 60)
    print("💡 提升置信度的实用技巧")
    print("=" * 60)

    tips = {
        "对于用户": [
            "清晰描述写作要求和背景信息",
            "提供具体的题目和文体要求",
            "说明目标读者和写作目的",
            "给出字数、时间等限制条件",
            "反馈使用体验帮助系统改进"
        ],

        "对于开发者": [
            "定期更新和扩充知识库内容",
            "优化检索算法提高准确率",
            "改进生成模板确保内容完整性",
            "基于用户反馈调整置信度权重",
            "监控系统表现识别薄弱环节"
        ],

        "对于教师": [
            "了解置信度含义正确解读结果",
            "高置信度时放心使用系统建议",
            "低置信度时提供额外指导",
            "收集学生反馈优化系统使用",
            "结合教学经验完善系统建议"
        ]
    }

    for role, tip_list in tips.items():
        print(f"\n👥 {role}:")
        for tip in tip_list:
            print(f"   ✓ {tip}")


def calculate_confidence_impact():
    """计算置信度对学习效果的影响"""

    print("\n" + "=" * 60)
    print("📈 置信度对学习效果的影响分析")
    print("=" * 60)

    # 模拟数据：不同置信度水平的学习效果
    impact_data = [
        {
            "confidence_range": "0.8-1.0 (高)",
            "user_satisfaction": "90%",
            "learning_efficiency": "高",
            "skill_improvement": "显著",
            "recommendation": "继续保持，可作为标准流程"
        },
        {
            "confidence_range": "0.6-0.8 (中高)",
            "user_satisfaction": "75%",
            "learning_efficiency": "中高",
            "skill_improvement": "良好",
            "recommendation": "适当优化，提升到高置信度"
        },
        {
            "confidence_range": "0.4-0.6 (中等)",
            "user_satisfaction": "60%",
            "learning_efficiency": "中等",
            "skill_improvement": "一般",
            "recommendation": "需要人工干预和补充指导"
        },
        {
            "confidence_range": "0.0-0.4 (低)",
            "user_satisfaction": "35%",
            "learning_efficiency": "低",
            "skill_improvement": "有限",
            "recommendation": "建议使用其他教学方法"
        }
    ]

    print(f"{'置信度范围':<15} {'用户满意度':<10} {'学习效率':<10} {'技能提升':<10} {'建议'}")
    print("-" * 80)

    for data in impact_data:
        print(f"{data['confidence_range']:<15} {data['user_satisfaction']:<10} "
              f"{data['learning_efficiency']:<10} {data['skill_improvement']:<10} {data['recommendation']}")


def main():
    """主函数：演示置信度的实际应用"""

    print("🎯 RAG系统置信度实际应用指南")
    print("="*60)

    # 1. 展示不同置信度水平的处理方式
    print("\n📋 不同置信度水平的应用示例:")
    examples = generate_confidence_examples()

    for i, example in enumerate(examples, 1):
        print(f"\n{i}. 题目: {example.topic}")
        print(f"   置信度: {example.confidence_score:.2f}")
        print(f"   系统消息: {example.user_message}")
        print(f"   教师指导: {example.teacher_guidance}")
        print(f"   学生行动: {example.student_action}")

    # 2. 决策流程
    demonstrate_confidence_decision_tree()

    # 3. 组成部分解释
    explain_confidence_components()

    # 4. 改进技巧
    show_confidence_improvement_tips()

    # 5. 影响分析
    calculate_confidence_impact()

    print(f"\n{'='*60}")
    print("✅ 置信度应用指南演示完成")
    print("📝 关键要点:")
    print("   • 置信度是系统自信心的量化指标")
    print("   • 不同置信度水平需要不同的使用策略")
    print("   • 置信度可以指导教学决策和学习方法")
    print("   • 持续优化置信度计算有助于提升教学效果")
    print("="*60)


if __name__ == "__main__":
    main()
