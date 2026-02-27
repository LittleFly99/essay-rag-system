#!/usr/bin/env python3
"""
简化的RAG系统测试 - 测试核心组件
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python    try:
        import json
        from src.core.models import EssayPrompt, EssayType, DifficultyLevel

        # 创建对象
        prompt = EssayPrompt(
            title="春天的故事",
            essay_type=EssayType.DESCRIPTIVE,
            difficulty_level=DifficultyLevel.MIDDLE,
            keywords=["春天", "生机", "美丽"]
        )root = Path(__file__).parent
sys.path.append(str(project_root))

def test_core_models():
    """测试核心数据模型"""
    print("🔧 测试核心数据模型...")

    try:
        from src.core.models import EssayPrompt, EssayType, DifficultyLevel

        # 测试作文题目创建
        prompt = EssayPrompt(
            title="我的梦想",
            description="写一篇关于梦想的作文",
            essay_type=EssayType.NARRATIVE,
            difficulty_level=DifficultyLevel.MIDDLE,
            keywords=["梦想", "未来", "目标"]
        )

        print(f"✅ 作文题目创建成功: {prompt.title}")
        print(f"   类型: {prompt.essay_type}")
        print(f"   难度: {prompt.difficulty_level}")
        print(f"   关键词: {prompt.keywords}")

        return True

    except Exception as e:
        print(f"❌ 模型测试失败: {e}")
        return False

def test_config():
    """测试配置系统"""
    print("\n⚙️ 测试配置系统...")

    try:
        from src.core.config import Settings

        # 创建配置实例
        settings = Settings()

        print(f"✅ 配置加载成功:")
        print(f"   应用名称: {settings.app_name}")
        print(f"   调试模式: {settings.debug}")
        print(f"   知识库路径: {settings.knowledge_base_path}")

        return True

    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_data_creation():
    """测试数据模型创建"""
    print("\n📝 测试完整数据模型...")

    try:
        from src.core.models import (
            EssayPrompt, WritingMaterial, SampleEssay,
            EssayType, DifficultyLevel
        )

        # 创建作文题目
        prompt = EssayPrompt(
            title="友谊的力量",
            description="通过一个具体的事例，描述友谊给你带来的力量",
            essay_type=EssayType.NARRATIVE,
            difficulty_level=DifficultyLevel.MIDDLE,
            keywords=["友谊", "帮助", "感动"]
        )

        # 创建写作素材
        material = WritingMaterial(
            title="友谊名言",
            content="真正的友谊是人生最宝贵的财富",
            category="名言警句",
            keywords=["友谊", "财富", "珍贵"],
            difficulty_level=DifficultyLevel.MIDDLE
        )

        # 创建范文示例
        example = SampleEssay(
            title="我的好朋友小明",
            content="小明是我最好的朋友，他总是在我需要帮助的时候出现...",
            essay_type=EssayType.NARRATIVE,
            difficulty_level=DifficultyLevel.MIDDLE,
            score=92,
            highlights=["人物描写生动", "情节感人", "主题突出"],
            keywords=["友谊", "帮助", "感恩"]
        )

        print("✅ 数据模型创建成功:")
        print(f"   题目: {prompt.title}")
        print(f"   素材: {material.title}")
        print(f"   范文: {example.title} (评分: {example.score})")

        return True

    except Exception as e:
        print(f"❌ 数据创建失败: {e}")
        return False

def test_json_serialization():
    """测试JSON序列化"""
    print("\n💾 测试数据序列化...")

    try:
        import json
        from src.core.models import EssayPrompt, EssayType

        # 创建对象
        prompt = EssayPrompt(
            title="春天的故事",
            essay_type=EssayType.DESCRIPTIVE,
            difficulty_level=DifficultyLevel.MIDDLE,
            keywords=["春天", "生机", "美丽"]
        )

        # 序列化为JSON
        json_data = prompt.model_dump()
        json_str = json.dumps(json_data, ensure_ascii=False, indent=2)

        print("✅ JSON序列化成功:")
        print(json_str[:200] + "..." if len(json_str) > 200 else json_str)

        # 反序列化
        loaded_data = json.loads(json_str)
        restored_prompt = EssayPrompt(**loaded_data)

        print(f"✅ JSON反序列化成功: {restored_prompt.title}")

        return True

    except Exception as e:
        print(f"❌ 序列化测试失败: {e}")
        return False

def create_sample_knowledge():
    """创建示例知识库数据"""
    print("\n📚 创建示例知识库...")

    try:
        import json
        from src.core.models import WritingMaterial, EssayExample

        # 确保数据目录存在
        data_dir = project_root / "data" / "knowledge"
        data_dir.mkdir(parents=True, exist_ok=True)

        # 创建素材数据
        materials = [
            {
                "id": "material_friendship_001",
                "title": "友谊如阳光",
                "content": "真挚的友谊如同温暖的阳光，能照亮我们内心最黑暗的角落，给我们前进的勇气和力量。",
                "category": "情感表达",
                "keywords": ["友谊", "阳光", "温暖", "勇气"],
                "usage_scenario": ["开头", "结尾"],
                "difficulty": 3
            },
            {
                "id": "material_dream_001",
                "title": "追梦的路上",
                "content": "每个人心中都有一个梦想，它像夜空中最亮的星，指引着我们前进的方向。",
                "category": "励志成长",
                "keywords": ["梦想", "星星", "方向", "追求"],
                "usage_scenario": ["开头", "过渡"],
                "difficulty": 2
            },
            {
                "id": "material_family_001",
                "title": "母爱的伟大",
                "content": "母爱是世界上最纯真、最无私的爱，它不求回报，只求我们健康快乐地成长。",
                "category": "亲情家庭",
                "keywords": ["母爱", "无私", "纯真", "成长"],
                "usage_scenario": ["情感表达", "结尾"],
                "difficulty": 2
            }
        ]

        # 保存素材数据
        with open(data_dir / "materials.json", "w", encoding="utf-8") as f:
            json.dump(materials, f, ensure_ascii=False, indent=2)

        # 创建范文数据
        examples = [
            {
                "id": "example_friendship_001",
                "title": "我的好朋友",
                "content": "我有一个好朋友叫小华，她是一个既聪明又善良的女孩...",
                "essay_type": "narrative",
                "score": 90,
                "highlights": ["人物形象鲜明", "语言生动自然", "情感真挚"],
                "structure": {
                    "开头": "简介人物，点明主题",
                    "中间": "通过具体事例展现友谊",
                    "结尾": "总结感悟，升华主题"
                },
                "keywords": ["友谊", "同学", "帮助", "感动"]
            },
            {
                "id": "example_dream_001",
                "title": "我的科学家梦想",
                "content": "从小我就梦想成为一名科学家，为人类的进步贡献自己的力量...",
                "essay_type": "narrative",
                "score": 88,
                "highlights": ["立意高远", "条理清晰", "语言流畅"],
                "structure": {
                    "开头": "点明梦想，引起兴趣",
                    "中间": "叙述梦想的由来和努力",
                    "结尾": "表达决心，展望未来"
                },
                "keywords": ["梦想", "科学家", "努力", "未来"]
            }
        ]

        # 保存范文数据
        with open(data_dir / "examples.json", "w", encoding="utf-8") as f:
            json.dump(examples, f, ensure_ascii=False, indent=2)

        print("✅ 示例知识库创建成功:")
        print(f"   素材数量: {len(materials)}")
        print(f"   范文数量: {len(examples)}")
        print(f"   保存路径: {data_dir}")

        return True

    except Exception as e:
        print(f"❌ 知识库创建失败: {e}")
        return False

def demo_usage():
    """演示基础使用方法"""
    print("\n🎮 演示基础使用...")

    try:
        from src.core.models import EssayPrompt, EssayType

        # 模拟用户输入
        user_topic = "写一篇关于母爱的作文"

        # 解析为数据模型
        prompt = EssayPrompt(
            title="母爱",
            content=user_topic,
            essay_type=EssayType.NARRATIVE,
            keywords=["母爱", "亲情", "感恩"],
            difficulty=3
        )

        print("✅ 用户请求处理:")
        print(f"   原始输入: {user_topic}")
        print(f"   解析结果: {prompt.title} ({prompt.essay_type})")
        print(f"   关键词: {prompt.keywords}")

        # 模拟系统响应
        response_data = {
            "prompt": prompt.model_dump(),
            "status": "success",
            "message": "题目解析成功，可以开始检索相关素材"
        }

        print("✅ 系统响应:")
        print(f"   状态: {response_data['status']}")
        print(f"   消息: {response_data['message']}")

        return True

    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def main():
    """主函数"""
    print("🎯 RAG作文教学系统 - 核心组件测试")
    print("=" * 50)

    # 执行测试
    tests = [
        ("核心模型测试", test_core_models),
        ("配置系统测试", test_config),
        ("数据创建测试", test_data_creation),
        ("序列化测试", test_json_serialization),
        ("知识库创建", create_sample_knowledge),
        ("基础使用演示", demo_usage)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 执行异常: {e}")
            results.append((test_name, False))

    # 汇总结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")

    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1

    print(f"\n通过率: {passed}/{len(results)} ({passed/len(results)*100:.1f}%)")

    if passed == len(results):
        print("\n🎉 太棒了！核心组件全部正常！")
        print("✨ 系统基础架构运行良好")
        print("📚 你现在可以开始学习各个模块的代码了")

        print("\n📖 推荐学习路径:")
        print("1. 📁 查看 data/knowledge/ 目录下的示例数据")
        print("2. 📝 研究 src/core/models.py 中的数据模型定义")
        print("3. ⚙️ 了解 src/core/config.py 中的配置管理")
        print("4. 🔧 逐步学习其他模块的实现")

    elif passed >= len(results) * 0.7:
        print("\n✨ 很好！大部分功能正常")
        print("💡 少数问题不影响核心功能学习")

    else:
        print("\n🔧 需要解决一些基础问题")
        print("💡 建议检查 Python 环境和依赖包")

    return passed == len(results)

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 准备就绪！开始你的RAG系统学习之旅吧！")
    else:
        print("\n🔧 请解决上述问题后重新测试")
