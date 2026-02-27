"""
核心工具模块
提供系统通用的工具函数
"""
import os
import json
import hashlib
import jieba
from typing import List, Dict, Any, Optional
from loguru import logger


def setup_logger(log_file: str = "./logs/app.log", log_level: str = "INFO"):
    """设置日志配置"""
    logger.remove()  # 移除默认的控制台日志

    # 添加文件日志
    logger.add(
        log_file,
        rotation="1 day",
        retention="7 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}",
        encoding="utf-8"
    )

    # 添加控制台日志
    logger.add(
        lambda msg: print(msg, end=""),
        level=log_level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )


def generate_id(content: str) -> str:
    """根据内容生成唯一ID"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()[:12]


def clean_text(text: str) -> str:
    """文本清理"""
    if not text:
        return ""

    # 移除多余的空白字符
    text = ' '.join(text.split())

    # 移除特殊字符（保留中文、英文、数字、基本标点）
    import re
    text = re.sub(r'[^\w\s\u4e00-\u9fff，。！？；：""''（）【】《》\.\,\!\?\;\:\"\'\(\)\[\]<>]', '', text)

    return text.strip()


# jieba 包是一个用于中文文本分词的第三方 Python 库。它的主要作用是把连续的中文句子切分成有意义的词语（即“分词”），方便后续的文本处理、自然语言处理（NLP）等任务。

# jieba 的分词规则和原理
# 基于前缀词典实现高效词图扫描
# jieba 内部有一个大规模的中文词典，会把句子中的字符组合与词典进行匹配，构建出所有可能的分词路径（DAG）。

# 采用动态规划找出最大概率路径
# 默认模式下，jieba 会用动态规划算法（如 Viterbi 算法）找出一条概率最大的分词路径，也就是最合理的分词结果。

# 支持 HMM（隐马尔可夫模型）新词发现
# 对于词典中没有的新词，jieba 可以用 HMM 模型进行识别和切分。

# 支持多种分词模式

# 精确模式（默认）：试图将句子最精确地切开，适合文本分析。
# 全模式：把句子中所有可能的词语都扫描出来，速度快但不能解决歧义。
# 搜索引擎模式：在精确模式基础上，对长词再次切分，提高召回率，适合搜索引擎分词。

# segment_chinese_text("我爱自然语言处理")
# # 可能输出：['我', '爱', '自然语言', '处理']
def segment_chinese_text(text: str) -> List[str]:
    """中文分词"""
    return list(jieba.cut(text))


# 原理简介
# TF-IDF（Term Frequency-Inverse Document Frequency，词频-逆文档频率）是一种常用的关键词提取算法。
# TF（词频）：某个词在文本中出现的频率，出现越多，TF 越高。
# IDF（逆文档频率）：某个词在所有文档中出现的稀有程度，越稀有，IDF 越高。
# TF-IDF 的值越高，说明这个词对当前文本越重要。
# jieba.analyse.extract_tags 就是用 TF-IDF 算法来给每个词打分，分数高的就是关键词。

# topK 参数
# topK 控制返回多少个关键词。
# 比如 topK=10，就返回分数最高的前 10 个关键词。
# 你可以根据需要调整，比如只要 5 个关键词就写 topK=5。
# import jieba.analyse

# text = "人工智能正在改变世界，机器学习和深度学习是其中的重要分支。"
# keywords = jieba.analyse.extract_tags(text, topK=3)
# print(keywords)
# # 输出类似：['人工智能', '机器学习', '深度学习']
def extract_keywords(text: str, top_k: int = 10) -> List[str]:
    """提取关键词"""
    import jieba.analyse

    # 使用 TF-IDF 提取关键词
    keywords = jieba.analyse.extract_tags(text, topK=top_k, withWeight=False)
    return keywords


def calculate_similarity(text1: str, text2: str) -> float:
    """计算文本相似度（简单的词汇重叠度）"""
    if not text1 or not text2:
        return 0.0

    words1 = set(segment_chinese_text(text1))
    words2 = set(segment_chinese_text(text2))

    if not words1 or not words2:
        return 0.0

    # 计算 Jaccard 相似度
    intersection = words1 & words2
    union = words1 | words2

    return len(intersection) / len(union) if union else 0.0

# 举例说明：
# 假设 words1 = {"apple", "banana", "cherry"}，words2 = {"banana", "cherry", "date"}

# 交集：{"banana", "cherry"}，数量为 2
# 并集：{"apple", "banana", "cherry", "date"}，数量为 4
# 相似度 = 2 / 4 = 0.5
# 用途：
# Jaccard 相似度常用于文本去重、推荐系统、聚类等场景，用于衡量两个集合的相似程度。

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """文本分块"""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # 尝试在句号处断开
        if end < len(text):
            # 查找最近的句号
            last_period = text.rfind('。', start, end)
            if last_period > start:
                end = last_period + 1

        chunks.append(text[start:end])

        if end >= len(text):
            break

        start = max(start + chunk_size - overlap, end - overlap)

    return chunks


def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """加载JSON文件"""
    if not os.path.exists(file_path):
        logger.warning(f"文件不存在: {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载JSON文件失败 {file_path}: {e}")
        return None


def save_json_file(data: Dict[str, Any], file_path: str) -> bool:
    """保存JSON文件"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"保存JSON文件失败 {file_path}: {e}")
        return False


def read_text_file(file_path: str) -> Optional[str]:
    """读取文本文件"""
    if not os.path.exists(file_path):
        logger.warning(f"文件不存在: {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"读取文本文件失败 {file_path}: {e}")
        return None


def write_text_file(content: str, file_path: str) -> bool:
    """写入文本文件"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"写入文本文件失败 {file_path}: {e}")
        return False


def validate_essay_prompt(prompt_data: Dict[str, Any]) -> bool:
    """验证作文题目数据的完整性"""
    required_fields = ['title', 'essay_type', 'difficulty_level']

    for field in required_fields:
        if field not in prompt_data or not prompt_data[field]:
            logger.error(f"缺少必需字段: {field}")
            return False

    return True


def format_guidance_output(guidance: Dict[str, Any]) -> str:
    """格式化写作指导输出"""
    output = []

    if 'theme_analysis' in guidance:
        output.append(f"## 主题分析\n{guidance['theme_analysis']}\n")

    if 'structure_suggestion' in guidance and guidance['structure_suggestion']:
        output.append("## 结构建议")
        for i, suggestion in enumerate(guidance['structure_suggestion'], 1):
            output.append(f"{i}. {suggestion}")
        output.append("")

    if 'writing_tips' in guidance and guidance['writing_tips']:
        output.append("## 写作技巧")
        for tip in guidance['writing_tips']:
            output.append(f"- {tip}")
        output.append("")

    if 'key_points' in guidance and guidance['key_points']:
        output.append("## 要点提示")
        for point in guidance['key_points']:
            output.append(f"- {point}")
        output.append("")

    return '\n'.join(output)
