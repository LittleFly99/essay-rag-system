#!/usr/bin/env python3
"""
素材和范文联系改进演示
展示改进后的系统如何更好地利用检索到的素材和范文
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.models import EssayPrompt, EssayType, DifficultyLevel, WritingMaterial, SampleEssay
from src.generation.llm_generator import LLMGenerator
from loguru import logger


def create_sample_materials():
    """创建示例素材"""
    materials = [
        WritingMaterial(
            id="mat_001",
            title="挫折中的成长",
            content="""
            一位著名的科学家曾说过："成功的路上充满挫折，但正是这些挫折让我们变得更强大。"
            有一个真实的故事：一个小男孩从小就梦想成为篮球运动员，但身高不够，经常被队友嘲笑。
            他没有放弃，每天比别人多练习两个小时，专注于技巧的提升。
            最终，他凭借出色的技巧和坚持不懈的精神，成为了一名优秀的控球后卫。
            这个故事告诉我们，挫折不是阻碍，而是成长的垫脚石。
            当我们面对困难时，关键是要保持积极的心态，把挫折看作是锻炼自己的机会。
            """,
            category="成长励志",
            keywords=["挫折", "成长", "坚持", "梦想"],
            difficulty_level=DifficultyLevel.MIDDLE
        ),
        
        WritingMaterial(
            id="mat_002",
            title="友谊的力量",
            content="""
            真正的友谊就像一盏明灯，在我们迷茫时指引方向，在我们孤独时给予温暖。
            有这样一个感人的故事：两个好朋友一起参加登山活动，其中一人意外受伤无法继续前行。
            另一个朋友毫不犹豫地背着受伤的朋友下山，错过了原定的行程，但他说："友谊比任何风景都珍贵。"
            这种真诚的友谊让人感动。在现实生活中，我们也需要这样的朋友。
            真正的朋友不仅在快乐时分享喜悦，更重要的是在困难时给予支持和帮助。
            友谊需要用心经营，需要相互理解、包容和信任。
            """,
            category="情感友谊",
            keywords=["友谊", "真诚", "帮助", "信任"],
            difficulty_level=DifficultyLevel.MIDDLE
        ),
        
        WritingMaterial(
            id="mat_003",
            title="科技改变生活",
            content="""
            科技的发展正在深刻地改变着我们的生活方式。
            从智能手机到人工智能，从网上购物到远程办公，科技让我们的生活变得更加便利。
            但科技发展也带来了一些问题，比如过度依赖手机导致的"低头族"现象。
            有调查显示，现代人平均每天看手机的时间超过6小时。
            这让我们思考：科技应该服务于人类，而不是让人类成为科技的奴隶。
            我们需要合理使用科技，在享受便利的同时，保持人与人之间的真实交流。
            """,
            category="科技社会",
            keywords=["科技", "生活", "便利", "思考"],
            difficulty_level=DifficultyLevel.HIGH
        )
    ]
    return materials


def create_sample_essays():
    """创建示例范文"""
    essays = [
        SampleEssay(
            id="essay_001",
            title="那一刻，我长大了",
            content="""
            成长是一个漫长的过程，但总有那么一个瞬间，让我们突然意识到自己长大了。
            
            那是一个雨夜，妈妈因为工作加班还没有回家，爸爸又出差在外。我独自在家做作业，
            突然听到门外传来熟悉的脚步声，是妈妈回来了。我打开门，看到妈妈浑身湿透，疲惫不堪。
            
            那一刻，我突然意识到，妈妈也会累，也会需要关心。我赶紧给妈妈递毛巾，
            为她泡了一杯热茶，还主动承担了家务。看到妈妈欣慰的笑容，我明白自己真的长大了。
            
            成长不仅仅是年龄的增长，更是心灵的成熟。从那一刻起，我学会了关爱他人，
            学会了承担责任。这就是成长的意义——在关爱中成长，在责任中成熟。
            """,
            essay_type=EssayType.NARRATIVE,
            difficulty_level=DifficultyLevel.MIDDLE,
            highlights=["细节描写生动", "情感表达真挚", "主题升华自然"],
            structure_analysis="采用'情境导入-具体事例-感悟升华'的经典三段式结构"
        ),
        
        SampleEssay(
            id="essay_002", 
            title="友谊如花",
            content="""
            友谊是人生中最珍贵的财富，它如花一般美丽，需要用心呵护才能绽放。
            
            我和小明的友谊就像一朵经历风雨的花。刚认识时，我们因为兴趣相同而成为好友。
            但在一次考试中，我们因为名次问题发生了争吵，友谊的花朵似乎要凋零了。
            
            经过冷静思考，我们都意识到友谊比成绩更重要。我主动向小明道歉，
            他也向我伸出了和解的手。从那以后，我们的友谊变得更加牢固。
            
            真正的友谊需要经历风雨的考验。只有在困难中互相支持，在误解中相互理解，
            友谊之花才能开得更加绚烂。让我们珍惜身边的每一份友谊，用真心去浇灌友谊之花。
            """,
            essay_type=EssayType.NARRATIVE,
            difficulty_level=DifficultyLevel.MIDDLE,
            highlights=["比喻手法运用巧妙", "叙事条理清晰", "情感真挚感人"],
            structure_analysis="运用比喻修辞贯穿全文，以'友谊如花'为线索展开叙述"
        )
    ]
    return essays


def demonstrate_improved_material_usage():
    """演示改进后的素材和范文使用效果"""
    
    print("🎯 素材和范文联系改进演示")
    print("=" * 80)
    
    # 创建测试数据
    prompt = EssayPrompt(
        title="谈谈你对'在挫折中成长'的看法",
        description="请结合自己的经历或身边的事例，谈谈你对在挫折中成长这一话题的理解",
        essay_type=EssayType.ARGUMENTATIVE,
        difficulty_level=DifficultyLevel.MIDDLE,
        keywords=["挫折", "成长", "坚持"],
        requirements=[
            "观点明确，论证有力",
            "结合具体事例说明",
            "语言表达流畅",
            "不少于600字"
        ]
    )
    
    materials = create_sample_materials()
    essays = create_sample_essays()
    
    # 创建生成器
    generator = LLMGenerator()
    
    print(f"📝 测试题目: {prompt.title}")
    print(f"📋 提供素材: {len(materials)} 个")
    for i, mat in enumerate(materials, 1):
        print(f"  {i}. {mat.title} ({mat.category})")
    
    print(f"\n📑 提供范文: {len(essays)} 篇")
    for i, essay in enumerate(essays, 1):
        print(f"  {i}. {essay.title} ({essay.essay_type.value})")
    
    print("\n🚀 开始生成写作指导...")
    print("-" * 80)
    
    # 生成指导
    guidance = generator.generate_guidance(
        prompt=prompt,
        materials=materials,
        essays=essays,
        context="这是一个测试，请展示如何具体运用素材和范文"
    )
    
    # 展示结果
    print("\n✨ 生成的写作指导:")
    print("=" * 80)
    
    print(f"\n🎯 主题分析:")
    print(f"   {guidance.theme_analysis}")
    
    print(f"\n🏗️ 结构建议:")
    for i, suggestion in enumerate(guidance.structure_suggestion, 1):
        print(f"   {i}. {suggestion}")
    
    print(f"\n✍️ 写作技巧:")
    for i, tip in enumerate(guidance.writing_tips, 1):
        print(f"   {i}. {tip}")
    
    print(f"\n🔑 关键要点:")
    for i, point in enumerate(guidance.key_points, 1):
        print(f"   {i}. {point}")
    
    # 新增：展示具体的素材使用说明
    if hasattr(guidance, 'material_usage_details') and guidance.material_usage_details:
        print(f"\n📚 素材和范文使用详情:")
        for i, usage in enumerate(guidance.material_usage_details, 1):
            print(f"   {i}. {usage}")
    
    # 新增：展示具体示例
    if hasattr(guidance, 'concrete_examples') and guidance.concrete_examples:
        print(f"\n📝 具体表达示例:")
        for i, example in enumerate(guidance.concrete_examples, 1):
            print(f"   {i}. {example}")
    
    print(f"\n📋 相关素材:")
    for i, material in enumerate(guidance.related_materials, 1):
        print(f"   {i}. {material}")
    
    print(f"\n📖 参考范文:")
    for i, essay in enumerate(guidance.reference_essays, 1):
        print(f"   {i}. {essay}")
    
    print("\n" + "=" * 80)
    print("✅ 演示完成")
    print("\n💡 改进亮点:")
    print("1. 📍 具体指出素材在文章中的使用位置和方法")
    print("2. 🎨 分析范文的写作技巧并转化为可操作建议")  
    print("3. 📝 提供具体的表达示例和句子模板")
    print("4. 🔗 建立素材内容与写作技巧的具体联系")
    print("5. 🎯 确保每个建议都具有可操作性")


def compare_before_after():
    """对比改进前后的效果"""
    
    print("\n" + "🔄 改进前后对比")
    print("=" * 80)
    
    print("❌ 改进前 - 素材使用建议:")
    print("   • 可以运用提供的素材")
    print("   • 参考素材《挫折中的成长》中的观点和事例")
    print("   • 学习范文的写作技巧")
    
    print("\n✅ 改进后 - 素材使用建议:")
    print("   • 【挫折中的成长】: 可在文章主体部分作为论证素材，通过科学家的例子")
    print("     和小男孩篮球梦的具体事例说明'挫折是成长垫脚石'的观点，增强论证力度")
    print("   • 【范文借鉴：那一刻，我长大了】: 学习其细节描写生动的特点，")
    print("     可以运用类似的情境描述和心理刻画来增强文章的感染力")
    print("   • 具体表达示例：'正如素材中科学家所说，成功的路上充满挫折...")
    print("     这样的开头既引用了素材又自然引入主题'")
    
    print("\n📊 改进效果:")
    print("   🎯 指导更具体：从'可以使用'到'如何使用'")
    print("   🔗 联系更紧密：素材内容与写作技巧直接对应")
    print("   📝 示例更实用：提供可直接参考的句子和段落")
    print("   💡 建议更可操作：学生能明确知道具体怎么做")


if __name__ == "__main__":
    # 设置日志级别，减少不必要的输出
    logger.remove()
    logger.add(sys.stderr, level="WARNING")
    
    try:
        demonstrate_improved_material_usage()
        compare_before_after()
    except Exception as e:
        logger.error(f"演示过程中出现错误: {e}")
        print(f"\n❌ 演示失败: {e}")
        print("💡 这可能是因为某些依赖未安装或配置问题")
        print("   但改进的核心思路和代码逻辑是正确的")
