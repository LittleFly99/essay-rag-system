"""
LLM 生成器
支持多种大语言模型API：OpenAI、火山引擎豆包
"""
import os
import json
import requests
from typing import List, Dict, Any, Optional
from loguru import logger

from ..core.models import EssayPrompt, WritingMaterial, SampleEssay, WritingGuidance
from ..core.config import settings

try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("langchain 相关库未安装，OpenAI功能不可用")


class DoubaoClient:
    """火山引擎豆包API客户端"""

    def __init__(self, api_key: str, endpoint: str, model: str):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        self.model = model
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """调用豆包聊天接口"""
        try:
            url = f"{self.endpoint}/chat/completions"

            data = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 4000,
                "stream": False
            }

            response = requests.post(url, headers=self.headers, json=data, timeout=60)
            response.raise_for_status()

            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"豆包API响应格式错误: {result}")
                return ""

        except requests.exceptions.RequestException as e:
            logger.error(f"豆包API调用失败: {e}")
            return ""
        except Exception as e:
            logger.error(f"豆包API处理错误: {e}")
            return ""


class LLMGenerator:
    """LLM 生成器 - 支持多种模型"""

    def __init__(self, temperature: float = 0.7):
        self.temperature = temperature
        self.provider = settings.llm_provider
        self.llm = None
        self.doubao_client = None
        self._initialize_llm()

    def _initialize_llm(self):
        """初始化 LLM"""
        try:
            if self.provider == "doubao":
                self._initialize_doubao()
            elif self.provider == "openai":
                self._initialize_openai()
            else:
                logger.warning(f"不支持的LLM提供商: {self.provider}")
        except Exception as e:
            logger.error(f"LLM 初始化失败: {e}")

    def _initialize_doubao(self):
        """初始化火山引擎豆包"""
        if not all([settings.doubao_api_key, settings.doubao_endpoint]):
            logger.warning("豆包API配置不完整，将使用模拟生成")
            return

        try:
            self.doubao_client = DoubaoClient(
                api_key=settings.doubao_api_key,
                endpoint=settings.doubao_endpoint,
                model=settings.doubao_model
            )
            logger.info(f"豆包LLM初始化成功: {settings.doubao_model}")
        except Exception as e:
            logger.error(f"豆包LLM初始化失败: {e}")

    def _initialize_openai(self):
        """初始化OpenAI"""
        if not LANGCHAIN_AVAILABLE or not settings.openai_api_key:
            logger.warning("OpenAI配置不完整，将使用模拟生成")
            return

        try:
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=self.temperature,
                openai_api_key=settings.openai_api_key,
                openai_api_base=settings.openai_base_url
            )
            logger.info("OpenAI LLM初始化成功")
        except Exception as e:
            logger.error(f"OpenAI LLM初始化失败: {e}")

    def generate_guidance(
        self,
        prompt: EssayPrompt,
        materials: List[WritingMaterial] = None,
        essays: List[SampleEssay] = None,
        context: str = ""
    ) -> WritingGuidance:
        """生成写作指导"""
        try:
            if self.provider == "doubao" and self.doubao_client:
                return self._generate_with_doubao(prompt, materials, essays, context)
            elif self.provider == "openai" and self.llm:
                return self._generate_with_openai(prompt, materials, essays, context)
            else:
                logger.warning("LLM不可用，使用模拟生成")
                return self._generate_mock_guidance(prompt, materials, essays)
        except Exception as e:
            logger.error(f"生成指导失败: {e}")
            return self._generate_mock_guidance(prompt, materials, essays)

    def _generate_with_doubao(
        self,
        prompt: EssayPrompt,
        materials: List[WritingMaterial],
        essays: List[SampleEssay],
        context: str
    ) -> WritingGuidance:
        """使用豆包模型生成指导"""
        logger.info("=" * 80)
        logger.info("🚀 开始调用豆包LLM生成写作指导")

        # 记录输入信息
        logger.info(f"📝 作文题目: {prompt.title}")
        logger.info(f"📖 题目描述: {prompt.description or '无'}")
        logger.info(f"🎯 作文类型: {prompt.essay_type}")
        logger.info(f"📊 难度等级: {prompt.difficulty_level}")
        logger.info(f"📋 写作要求: {prompt.requirements}")
        logger.info(f"🔑 关键词: {prompt.keywords}")

        # 记录检索到的材料信息
        if materials:
            logger.info(f"📚 检索到 {len(materials)} 个相关写作素材:")
            for i, material in enumerate(materials[:3], 1):  # 只显示前3个
                logger.info(f"  {i}. 【{material.category}】{material.title}")
                logger.info(f"     内容摘要: {material.content[:]}...")
        else:
            logger.info("📚 未检索到相关写作素材")

        # 记录检索到的范文信息
        if essays:
            logger.info(f"📑 检索到 {len(essays)} 篇相关范文:")
            for i, essay in enumerate(essays[:3], 1):  # 只显示前3个
                logger.info(f"  {i}. 【{essay.essay_type}】{essay.title}")
                logger.info(f"     内容摘要: {essay.content[:]}...")
        else:
            logger.info("📑 未检索到相关范文")

        # 构建系统提示
        system_prompt = self._build_system_prompt()
        logger.info(f"🎭 系统提示长度: {len(system_prompt)} 字符")

        # 构建用户提示
        user_prompt = self._build_user_prompt(prompt, materials, essays, context)
        logger.info(f"👤 用户提示长度: {len(user_prompt)} 字符")
        logger.info(f"👤 用户提示内容预览:")
        logger.info(f"     {user_prompt[:]}...")

        # 调用豆包API
        logger.info("🔄 正在调用豆包API...")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response_text = self.doubao_client.chat_completion(messages, self.temperature)

        # 记录API响应
        if response_text:
            logger.info("✅ 豆包API调用成功")
            logger.info(f"📤 API响应长度: {len(response_text)} 字符")
            logger.info(f"📤 API响应内容预览:")
            logger.info(f"     {response_text[:]}...")
        else:
            logger.warning("⚠️ 豆包API返回空响应，使用模拟生成")
            return self._generate_mock_guidance(prompt, materials, essays)

        # 解析响应
        logger.info("🔍 开始解析LLM响应...")
        guidance = self._parse_llm_response(response_text, materials, essays)

        # 记录解析结果
        logger.info("✅ LLM响应解析完成")
        logger.info(f"🎯 主题分析长度: {len(guidance.theme_analysis)} 字符")
        logger.info(f"📝 结构建议数量: {len(guidance.structure_suggestion)} 条")
        logger.info(f"✏️ 写作技巧数量: {len(guidance.writing_tips)} 条")
        logger.info(f"🔑 关键要点数量: {len(guidance.key_points)} 条")
        logger.info("=" * 80)

        return guidance

    def _generate_with_openai(
        self,
        prompt: EssayPrompt,
        materials: List[WritingMaterial],
        essays: List[SampleEssay],
        context: str
    ) -> WritingGuidance:
        """使用 OpenAI 生成指导"""
        logger.info("=" * 80)
        logger.info("🚀 开始调用OpenAI LLM生成写作指导")

        # 记录输入信息
        logger.info(f"📝 作文题目: {prompt.title}")
        logger.info(f"📖 题目描述: {prompt.description or '无'}")
        logger.info(f"🎯 作文类型: {prompt.essay_type}")
        logger.info(f"📊 难度等级: {prompt.difficulty_level}")
        logger.info(f"📋 写作要求: {prompt.requirements}")
        logger.info(f"🔑 关键词: {prompt.keywords}")

        # 记录检索到的材料信息
        if materials:
            logger.info(f"📚 检索到 {len(materials)} 个相关写作素材:")
            for i, material in enumerate(materials[:3], 1):  # 只显示前3个
                logger.info(f"  {i}. 【{material.category}】{material.title}")
                logger.info(f"     内容摘要: {material.content[:100]}...")
        else:
            logger.info("📚 未检索到相关写作素材")

        # 记录检索到的范文信息
        if essays:
            logger.info(f"📑 检索到 {len(essays)} 篇相关范文:")
            for i, essay in enumerate(essays[:3], 1):  # 只显示前3个
                logger.info(f"  {i}. 【{essay.essay_type}】{essay.title}")
                logger.info(f"     内容摘要: {essay.content[:100]}...")
        else:
            logger.info("📑 未检索到相关范文")

        # 构建系统提示
        system_prompt = self._build_system_prompt()
        logger.info(f"🎭 系统提示长度: {len(system_prompt)} 字符")

        # 构建用户提示
        user_prompt = self._build_user_prompt(prompt, materials, essays, context)
        logger.info(f"👤 用户提示长度: {len(user_prompt)} 字符")
        logger.info(f"👤 用户提示内容预览:")
        logger.info(f"     {user_prompt[:200]}...")

        # 调用 OpenAI API
        logger.info("🔄 正在调用OpenAI API...")
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = self.llm(messages)

        # 记录API响应
        logger.info("✅ OpenAI API调用成功")
        logger.info(f"📤 API响应长度: {len(response.content)} 字符")
        logger.info(f"📤 API响应内容预览:")
        logger.info(f"     {response.content[:300]}...")

        # 解析响应
        logger.info("🔍 开始解析LLM响应...")
        guidance = self._parse_llm_response(response.content, materials, essays)

        # 记录解析结果
        logger.info("✅ LLM响应解析完成")
        logger.info(f"🎯 主题分析长度: {len(guidance.theme_analysis)} 字符")
        logger.info(f"📝 结构建议数量: {len(guidance.structure_suggestion)} 条")
        logger.info(f"✏️ 写作技巧数量: {len(guidance.writing_tips)} 条")
        logger.info(f"🔑 关键要点数量: {len(guidance.key_points)} 条")
        logger.info("=" * 80)

        return guidance

    def _build_system_prompt(self) -> str:
        """构建系统提示"""
        return """你是一位经验丰富的语文老师和写作指导专家，专门为学生提供作文写作指导。

你的任务是根据给定的作文题目，**充分利用并具体指导如何使用提供的写作素材和范文**，生成详细的写作指导。

**重要要求**：
1. **必须具体说明如何运用每个提供的素材** - 不能只是列出素材标题，要说明在文章的哪个部分、如何使用
2. **必须分析范文的优秀写法** - 指出范文的结构特点、表达技巧，并建议学生如何借鉴
3. **要建立素材与写作技巧的具体联系** - 说明某个素材适合用来论证哪个观点、表达哪种情感
4. **提供可操作的具体建议** - 避免空泛的指导，要给出学生能直接运用的方法

请按照以下JSON格式返回结果：

```json
{
  "theme_analysis": "深入分析作文题目的核心主题和写作要求，结合提供的素材分析写作方向",
  "structure_suggestions": [
    "开头：具体建议如何开头，可以运用哪个素材或借鉴哪个范文的开头方式",
    "主体：分段建议，明确指出在每段中如何运用具体素材",
    "结尾：结尾建议，说明如何升华主题"
  ],
  "writing_techniques": [
    "具体的写作技巧，结合提供的素材举例说明",
    "从范文中学到的表达方法，并说明如何运用",
    "针对题目特点的专门技巧"
  ],
  "key_points": [
    "重点内容，结合具体素材说明",
    "从范文中总结的关键要点",
    "针对题目的特殊注意事项"
  ],
  "material_usage": [
    "【素材名称】: 具体说明这个素材在文章的哪个位置、如何使用、能解决什么问题",
    "【范文借鉴】: 具体说明从范文中学到什么、如何应用到自己的写作中"
  ],
  "concrete_examples": [
    "提供具体的段落或句子示例，展示如何运用素材",
    "给出范文中值得学习的具体表达方式"
  ]
}
```

请确保你的指导：
- **素材运用具体化**：明确说明每个素材的使用方法和位置
- **范文借鉴实用化**：分析范文的优点并转化为可操作的建议
- **技巧说明详细化**：不只说"要生动"，要说"怎样生动"
- **示例说明具体化**：提供具体的表达示例
- 适合目标难度等级的学生
- 条理清晰，易于理解和执行

请严格按照上述JSON格式返回，不要添加其他内容。"""

    def _build_user_prompt(
        self,
        prompt: EssayPrompt,
        materials: List[WritingMaterial],
        essays: List[SampleEssay],
        context: str
    ) -> str:
        """构建用户提示"""
        user_prompt_parts = []

        # 添加作文题目信息
        user_prompt_parts.append("## 作文题目信息")
        user_prompt_parts.append(f"**题目**: {prompt.title}")
        if prompt.description:
            user_prompt_parts.append(f"**描述**: {prompt.description}")
        user_prompt_parts.append(f"**类型**: {prompt.essay_type.value}")
        user_prompt_parts.append(f"**难度等级**: {prompt.difficulty_level.value}")

        if prompt.keywords:
            user_prompt_parts.append(f"**关键词**: {', '.join(prompt.keywords)}")

        if prompt.requirements:
            user_prompt_parts.append("**写作要求**:")
            for req in prompt.requirements:
                user_prompt_parts.append(f"- {req}")

        if prompt.word_count:
            user_prompt_parts.append(f"**字数要求**: {prompt.word_count}字")

        # 添加相关素材
        if materials:
            user_prompt_parts.append("\n## 相关写作素材（请务必具体指导如何运用）")
            for i, material in enumerate(materials[:5], 1):  # 增加到5个素材
                user_prompt_parts.append(f"### 素材{i}: {material.title}")
                user_prompt_parts.append(f"**分类**: {material.category}")
                user_prompt_parts.append(f"**难度**: {material.difficulty_level.value if hasattr(material, 'difficulty_level') else '中等'}")
                # 提供更多内容
                content = material.content[:500] if len(material.content) > 500 else material.content
                user_prompt_parts.append(f"**内容**: {content}")
                if hasattr(material, 'themes') and material.themes:
                    user_prompt_parts.append(f"**适用主题**: {', '.join(material.themes)}")
                user_prompt_parts.append("") # 空行分隔

        # 添加范文参考
        if essays:
            user_prompt_parts.append("\n## 参考范文（请分析优点并指导如何借鉴）")
            for i, essay in enumerate(essays[:3], 1):  # 保持3篇范文
                user_prompt_parts.append(f"### 范文{i}: {essay.title}")
                user_prompt_parts.append(f"**类型**: {essay.essay_type.value}")
                user_prompt_parts.append(f"**难度**: {essay.difficulty_level.value if hasattr(essay, 'difficulty_level') else '中等'}")
                
                if hasattr(essay, 'highlights') and essay.highlights:
                    user_prompt_parts.append(f"**写作亮点**: {', '.join(essay.highlights)}")
                
                if hasattr(essay, 'structure_analysis') and essay.structure_analysis:
                    user_prompt_parts.append(f"**结构分析**: {essay.structure_analysis}")
                
                if hasattr(essay, 'language_features') and essay.language_features:
                    user_prompt_parts.append(f"**语言特色**: {', '.join(essay.language_features)}")
                
                # 提供更多范文内容
                content = essay.content[:800] if len(essay.content) > 800 else essay.content
                user_prompt_parts.append(f"**范文内容**: {content}")
                user_prompt_parts.append("") # 空行分隔

        # 添加上下文
        if context:
            user_prompt_parts.append(f"\n## 补充信息\n{context}")

        # 添加生成要求
        user_prompt_parts.append("""
## 请生成指导

请基于以上信息，为这个作文题目生成详细的写作指导。

**重要要求**：
1. **必须具体说明如何运用每个素材** - 在material_usage中，要写明"在文章的开头可以运用《素材名》中的XXX观点/事例，用来XXX"
2. **必须分析范文的借鉴价值** - 在material_usage中，要写明"可以学习《范文名》的XXX写法，比如XXX，运用到自己文章的XXX部分"  
3. **提供具体的表达示例** - 在concrete_examples中，给出具体的句子或段落示例
4. **确保指导的可操作性** - 学生看了指导后能知道具体怎么做

严格按照系统提示中的JSON格式返回结果，包含以下字段：
- theme_analysis: 主题分析（结合素材分析写作方向）
- structure_suggestions: 结构建议列表（具体说明每部分如何运用素材）
- writing_techniques: 写作技巧列表（结合素材和范文举例说明）
- key_points: 要点提示列表（结合具体素材说明）
- material_usage: 素材和范文使用建议列表（具体说明如何运用）
- concrete_examples: 具体示例列表（提供可参考的表达方式）

请确保返回的是有效的JSON格式，且每个字段都有实质性的、具体的内容。""")

        return "\n".join(user_prompt_parts)

    def _parse_llm_response(
        self,
        response: str,
        materials: List[WritingMaterial],
        essays: List[SampleEssay]
    ) -> WritingGuidance:
        """解析 LLM 响应"""
        try:
            # 尝试解析JSON格式响应
            json_data = self._extract_json_from_response(response)

            if json_data:
                # 提取素材使用建议
                material_usage = json_data.get("material_usage", [])
                concrete_examples = json_data.get("concrete_examples", [])
                
                # 合并相关信息
                related_materials = []
                reference_essays = []
                
                # 从material_usage中提取具体的材料使用信息
                for usage in material_usage:
                    if isinstance(usage, str) and usage.strip():
                        if "】" in usage:  # 格式化的素材说明
                            related_materials.append(usage)
                        else:
                            related_materials.append(usage)
                
                # 如果没有具体使用说明，则使用材料标题
                if not related_materials and materials:
                    related_materials = [f"《{mat.title}》- {mat.category}" for mat in materials]
                
                # 处理范文信息
                if essays:
                    reference_essays = [f"《{essay.title}》- {essay.essay_type.value}" for essay in essays]

                return WritingGuidance(
                    theme_analysis=json_data.get("theme_analysis", ""),
                    structure_suggestion=json_data.get("structure_suggestions", []),
                    writing_tips=json_data.get("writing_techniques", []),
                    key_points=json_data.get("key_points", []),
                    related_materials=related_materials,
                    reference_essays=reference_essays,
                    material_usage_details=material_usage,  # 新增字段：详细的素材使用说明
                    concrete_examples=concrete_examples     # 新增字段：具体示例
                )
            else:
                # 如果JSON解析失败，尝试文本解析
                return self._parse_text_response(response, materials, essays)

        except Exception as e:
            logger.error(f"解析LLM响应失败: {e}")
            return self._create_fallback_guidance(materials, essays)

    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """从响应中提取JSON数据"""
        try:
            # 尝试直接解析整个响应为JSON
            return json.loads(response.strip())
        except json.JSONDecodeError:
            pass

        try:
            # 尝试从markdown代码块中提取JSON
            import re
            json_pattern = r'```json\s*(.*?)\s*```'
            matches = re.findall(json_pattern, response, re.DOTALL)
            if matches:
                return json.loads(matches[0].strip())
        except json.JSONDecodeError:
            pass

        try:
            # 尝试查找花括号包围的内容
            start_idx = response.find('{')
            end_idx = response.rfind('}')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx+1]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        logger.warning("无法从响应中提取有效JSON")
        return None

    def _parse_text_response(
        self,
        response: str,
        materials: List[WritingMaterial],
        essays: List[SampleEssay]
    ) -> WritingGuidance:
        """解析文本格式响应（备用方案）"""
        try:
            # 简单的文本解析，实际可以更复杂
            sections = {
                "theme_analysis": "",
                "structure_suggestion": [],
                "writing_tips": [],
                "key_points": []
            }

            current_section = None
            lines = response.split('\n')

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # 识别章节
                if "主题分析" in line or "theme_analysis" in line.lower():
                    current_section = "theme_analysis"
                    continue
                elif "结构建议" in line or "structure" in line.lower():
                    current_section = "structure_suggestion"
                    continue
                elif "写作技巧" in line or "writing_tips" in line.lower():
                    current_section = "writing_tips"
                    continue
                elif "要点提示" in line or "key_points" in line.lower():
                    current_section = "key_points"
                    continue

                # 添加内容
                if current_section == "theme_analysis":
                    if sections["theme_analysis"]:
                        sections["theme_analysis"] += " " + line
                    else:
                        sections["theme_analysis"] = line
                elif current_section in ["structure_suggestion", "writing_tips", "key_points"]:
                    if line.startswith(('-', '•', '*', '1.', '2.', '3.')):
                        cleaned_line = line.lstrip('-•*0123456789. ').strip()
                        sections[current_section].append(cleaned_line)
                    elif line and not line.startswith('#'):
                        sections[current_section].append(line)

            # 如果解析失败，使用原始响应
            if not any(sections.values()):
                sections["theme_analysis"] = response

            return WritingGuidance(
                theme_analysis=sections["theme_analysis"] or "请根据题目要求进行主题分析。",
                structure_suggestion=sections["structure_suggestion"] or ["开头引入", "主体论证", "结尾总结"],
                writing_tips=sections["writing_tips"] or ["注意语言表达", "合理使用修辞", "逻辑清晰"],
                key_points=sections["key_points"] or ["紧扣主题", "内容充实", "结构完整"],
                related_materials=[mat.title for mat in materials] if materials else [],
                reference_essays=[essay.title for essay in essays] if essays else []
            )
        except Exception as e:
            logger.error(f"解析文本响应失败: {e}")
            return self._create_fallback_guidance(materials, essays)

    def _create_fallback_guidance(
        self,
        materials: List[WritingMaterial],
        essays: List[SampleEssay]
    ) -> WritingGuidance:
        """创建备用指导"""
        return WritingGuidance(
            theme_analysis="请仔细阅读题目要求，分析写作主题和目标。",
            structure_suggestion=[
                "开头：引入话题，明确观点",
                "主体：分层次展开论述",
                "结尾：总结观点，深化主题"
            ],
            writing_tips=[
                "语言表达要清晰准确",
                "逻辑结构要条理清楚",
                "内容要充实具体"
            ],
            key_points=[
                "紧扣题目要求",
                "观点明确统一",
                "论证充分有力"
            ],
            related_materials=[mat.title for mat in materials] if materials else [],
            reference_essays=[essay.title for essay in essays] if essays else []
        )

    def _generate_mock_guidance(
        self,
        prompt: Optional[EssayPrompt],
        materials: List[WritingMaterial],
        essays: List[SampleEssay]
    ) -> WritingGuidance:
        """生成模拟指导（当 LLM 不可用时使用）"""
        if not prompt:
            prompt_type = "general"
            prompt_level = "middle"
        else:
            prompt_type = prompt.essay_type.value if prompt.essay_type else "narrative"
            prompt_level = prompt.difficulty_level.value if prompt.difficulty_level else "middle"

        # 根据作文类型生成不同的指导模板
        guidance_templates = {
            "narrative": {
                "theme_analysis": "记叙文要求通过叙述事件来表达主题思想，注意情节的完整性和人物的生动性。",
                "structure_suggestion": [
                    "开头：简要交代时间、地点、人物、事件",
                    "发展：详细叙述事件的经过，突出重点",
                    "高潮：事件的关键转折点",
                    "结尾：总结事件意义，点明主题"
                ],
                "writing_tips": [
                    "运用生动的描写手法，让读者有身临其境的感觉",
                    "合理安排叙述顺序，可采用倒叙、插叙等手法",
                    "注意详略得当，重点部分要详写",
                    "融入真情实感，使文章感人"
                ],
                "key_points": [
                    "确保事件的真实性和完整性",
                    "人物形象要鲜明立体",
                    "语言要生动形象，富有表现力",
                    "主题要明确，通过事件自然体现"
                ]
            },
            "argumentative": {
                "theme_analysis": "议论文要求明确提出观点，并运用事实和道理进行论证，逻辑性要强。",
                "structure_suggestion": [
                    "引论：提出问题，明确论点",
                    "本论：分层论证，举例说明",
                    "结论：总结论证，强调观点"
                ],
                "writing_tips": [
                    "论点要明确、正确、深刻",
                    "论据要典型、充分、有说服力",
                    "论证要严密、合理、有逻辑",
                    "语言要准确、鲜明、生动"
                ],
                "key_points": [
                    "开门见山，直接提出论点",
                    "选择有代表性的事例和名言",
                    "注意正反对比论证",
                    "结尾要有力，升华主题"
                ]
            },
            "expository": {
                "theme_analysis": "说明文要求客观准确地说明事物的特征、原理或方法，语言要准确简洁。",
                "structure_suggestion": [
                    "开头：概括介绍说明对象",
                    "主体：分条目或分方面说明",
                    "结尾：总结要点，强调意义"
                ],
                "writing_tips": [
                    "运用多种说明方法，如举例、对比、分类等",
                    "语言要准确、简洁、通俗易懂",
                    "结构要清晰，层次要分明",
                    "可适当使用图表、数据等辅助说明"
                ],
                "key_points": [
                    "抓住事物的本质特征",
                    "说明要科学准确",
                    "条理清楚，逻辑性强",
                    "语言平实，通俗易懂"
                ]
            },
            "general": {
                "theme_analysis": "根据题目要求确定写作主题和表达目的，选择合适的写作方法。",
                "structure_suggestion": [
                    "开头：引入主题，概括观点",
                    "主体：分层次展开内容",
                    "结尾：总结全文，深化主题"
                ],
                "writing_tips": [
                    "仔细审题，把握写作要求",
                    "选择合适的文体和表达方式",
                    "注意语言的准确性和生动性",
                    "结构要完整，逻辑要清晰"
                ],
                "key_points": [
                    "紧扣题目，不跑题",
                    "内容要充实具体",
                    "表达要清楚流畅",
                    "书写要工整美观"
                ]
            }
        }

        # 选择合适的模板
        template = guidance_templates.get(prompt_type, guidance_templates["general"])

        # 添加素材相关建议
        material_suggestions = []
        material_usage_details = []
        if materials:
            material_suggestions.append(f"可以运用提供的{len(materials)}个相关素材")
            for i, material in enumerate(materials[:3], 1):
                # 根据素材类型给出具体使用建议
                if material.category in ["成长", "励志"]:
                    usage_detail = f"【{material.title}】：可在文章主体部分作为论证素材，通过具体事例说明{prompt_type}主题，增强文章的说服力和感染力"
                elif material.category in ["情感", "友谊", "亲情"]:
                    usage_detail = f"【{material.title}】：适合在情感表达部分引用，通过生动的情感描述引起读者共鸣，增强文章的感染力"
                elif material.category in ["科技", "社会", "环保"]:
                    usage_detail = f"【{material.title}】：可作为论据支撑观点，在分析问题时引用相关数据或事例，使论证更加有力"
                else:
                    usage_detail = f"【{material.title}】：建议在文章的{['开头引入', '主体论证', '结尾升华'][i % 3]}部分运用，结合具体内容展开论述"
                
                material_usage_details.append(usage_detail)
                material_suggestions.append(f"参考素材《{material.title}》中的观点和事例")

        # 添加范文参考建议
        essay_suggestions = []
        if essays:
            essay_suggestions.append(f"可以参考提供的{len(essays)}篇范文的结构和表达方式")
            for essay in essays[:2]:
                if hasattr(essay, 'highlights') and essay.highlights:
                    essay_suggestions.append(f"学习范文《{essay.title}》的亮点：{', '.join(essay.highlights[:2])}")
                    # 添加具体的范文使用建议
                    range_usage = f"【范文借鉴：{essay.title}】：学习其{essay.highlights[0] if essay.highlights else '表达方式'}，可以运用类似的写作手法和结构安排"
                    material_usage_details.append(range_usage)
        
        # 生成具体示例
        concrete_examples = []
        if materials:
            concrete_examples.append("开头示例：\"正如素材中提到的...\，这样的经历让我们明白...\"")
            concrete_examples.append("论证示例：\"通过具体事例我们可以看到...\，这说明了...的重要性\"")
        if essays:
            concrete_examples.append("结构借鉴：\"可以采用'总-分-总'的结构，先提出观点，再分层论证，最后总结升华\"")

        return WritingGuidance(
            theme_analysis=template["theme_analysis"],
            structure_suggestion=template["structure_suggestion"],
            writing_tips=template["writing_tips"] + material_suggestions,
            key_points=template["key_points"] + essay_suggestions,
            related_materials=[mat.title for mat in materials] if materials else [],
            reference_essays=[essay.title for essay in essays] if essays else [],
            material_usage_details=material_usage_details,
            concrete_examples=concrete_examples
        )
