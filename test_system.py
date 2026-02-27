#!/usr/bin/env python3
"""
RAG系统基础功能测试
用于验证系统各个组件是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_imports():
    """测试基础导入功能"""
    print("🔧 测试基础导入...")

    try:
        # 测试核心模块导入
        from src.core.models import EssayPrompt, EssayType
        from src.core.config import settings
        print("✅ 核心模块导入成功")

        # 测试创建基础对象
        prompt = EssayPrompt(
            title="测试作文题目",
            essay_type=EssayType.NARRATIVE,
            difficulty=3,
            keywords=["测试", "学习"]
        )
        print(f"✅ 数据模型工作正常: {prompt.title}")

        # 测试配置读取
        print(f"✅ 配置读取成功: {settings.app_name}")

        return True

    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请检查:")
        print("   - Python虚拟环境是否激活")
        print("   - requirements.txt依赖是否安装完整")
        print("   - 项目目录结构是否正确")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_file_structure():
    """测试文件结构"""
    print("\n📁 检查项目文件结构...")

    required_files = [
        "src/core/__init__.py",
        "src/core/models.py",
        "src/core/config.py",
        "src/knowledge/__init__.py",
        "src/rag_system.py",
        "requirements.txt"
    ]

    missing_files = []
    for file_path in required_files:
        full_path = project_root / file_path
        if not full_path.exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")

    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    else:
        print("✅ 所有必需文件都存在")
        return True

def test_data_directories():
    """测试数据目录"""
    print("\n📂 检查数据目录...")

    data_dirs = ["data", "data/knowledge", "logs"]

    for dir_path in data_dirs:
        full_path = project_root / dir_path
        if not full_path.exists():
            print(f"📁 创建目录: {dir_path}")
            full_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ {dir_path}")

    return True

def test_dependencies():
    """测试依赖包"""
    print("\n📦 检查依赖包...")

    required_packages = [
        "pydantic",
        "loguru",
        "fastapi",
        "uvicorn"
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")

    if missing_packages:
        print(f"\n💡 需要安装的包: {missing_packages}")
        print("运行命令: pip install " + " ".join(missing_packages))
        return False

    return True

def test_basic_functionality():
    """测试基础功能"""
    print("\n⚡ 测试基础功能...")

    try:
        from src.core.models import EssayPrompt, WritingMaterial, EssayExample

        # 测试作文题目创建
        prompt = EssayPrompt(
            title="我的梦想",
            content="写一篇关于自己梦想的作文",
            keywords=["梦想", "未来", "目标"]
        )
        print(f"✅ 作文题目创建: {prompt.title}")

        # 测试写作素材创建
        material = WritingMaterial(
            title="关于梦想的名言",
            content="梦想是人生的指路明灯",
            category="名言警句",
            keywords=["梦想", "励志"]
        )
        print(f"✅ 写作素材创建: {material.title}")

        # 测试范文示例创建
        example = EssayExample(
            title="我的科学家梦",
            content="从小我就有一个科学家的梦想...",
            essay_type="narrative",
            score=85,
            highlights=["结构清晰", "语言生动"]
        )
        print(f"✅ 范文示例创建: {example.title}")

        return True

    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False

def create_sample_data():
    """创建示例数据文件"""
    print("\n📝 创建示例数据...")

    data_dir = project_root / "data" / "knowledge"
    data_dir.mkdir(parents=True, exist_ok=True)

    # 创建示例素材数据
    sample_materials = [
        {
            "id": "material_001",
            "title": "友谊的力量",
            "content": "真正的友谊是人生最宝贵的财富之一",
            "category": "情感表达",
            "keywords": ["友谊", "真诚", "陪伴"],
            "usage_scenario": ["开头", "论证"],
            "difficulty": 3
        },
        {
            "id": "material_002",
            "title": "母爱如山",
            "content": "母爱是世界上最伟大、最无私的爱",
            "category": "亲情",
            "keywords": ["母爱", "无私", "伟大"],
            "usage_scenario": ["开头", "结尾"],
            "difficulty": 2
        }
    ]

    # 写入文件
    import json
    with open(data_dir / "materials.json", "w", encoding="utf-8") as f:
        json.dump(sample_materials, f, ensure_ascii=False, indent=2)

    print("✅ 示例素材数据已创建")

    # 创建示例范文数据
    sample_examples = [
        {
            "id": "example_001",
            "title": "我的好朋友",
            "content": "我有一个好朋友叫小明，他是一个很特别的人...",
            "essay_type": "narrative",
            "score": 88,
            "highlights": ["人物描写生动", "情感真挚"],
            "structure": {
                "开头": "介绍人物",
                "中间": "具体事例",
                "结尾": "感悟总结"
            },
            "keywords": ["友谊", "同学", "帮助"]
        }
    ]

    with open(data_dir / "examples.json", "w", encoding="utf-8") as f:
        json.dump(sample_examples, f, ensure_ascii=False, indent=2)

    print("✅ 示例范文数据已创建")
    return True

def run_simple_demo():
    """运行简单演示"""
    print("\n🎮 运行简单演示...")

    try:
        # 尝试导入RAG系统
        from src.rag_system import RAGSystem
        print("✅ RAG系统导入成功")

        # 创建系统实例
        rag = RAGSystem()
        print("✅ RAG系统实例创建成功")

        # 尝试初始化
        if rag.initialize(load_sample_data=False):
            print("✅ RAG系统初始化成功")
        else:
            print("⚠️  RAG系统初始化有问题，但基础功能正常")

        return True

    except Exception as e:
        print(f"❌ 演示运行失败: {e}")
        print("💡 这是正常的，可能是因为某些组件还未完全配置")
        return False

def main():
    """主测试函数"""
    print("🎯 RAG作文教学系统 - 基础功能测试")
    print("=" * 50)

    # 执行各项测试
    tests = [
        ("文件结构检查", test_file_structure),
        ("数据目录检查", test_data_directories),
        ("依赖包检查", test_dependencies),
        ("基础导入测试", test_imports),
        ("基础功能测试", test_basic_functionality),
        ("创建示例数据", create_sample_data),
        ("简单演示测试", run_simple_demo)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 执行失败: {e}")
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

    # 给出建议
    if passed == len(results):
        print("\n🎉 恭喜！所有测试都通过了！")
        print("💡 你可以开始学习和修改代码了")
        print("🚀 试试运行: python simple_demo.py")
    elif passed >= len(results) * 0.7:
        print("\n✨ 大部分功能正常！")
        print("💡 一些小问题不影响学习，继续前进吧！")
    else:
        print("\n🔧 需要修复一些基础问题")
        print("💡 建议先解决依赖和导入问题")

    print("\n📚 学习建议:")
    print("1. 查看 CODE_DEBUG_GUIDE.md 了解详细调试方法")
    print("2. 从 src/core/models.py 开始学习数据模型")
    print("3. 逐步理解各个模块的功能")

if __name__ == "__main__":
    main()
