#!/usr/bin/env python3
"""
修复materials.json中重复的ID问题
"""
import json
import uuid
from collections import defaultdict

def generate_unique_id():
    """生成12位的唯一ID"""
    return str(uuid.uuid4()).replace('-', '')[:12]

def fix_duplicate_ids(file_path):
    """修复JSON文件中的重复ID"""

    # 读取原始文件
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 统计ID使用情况
    id_counts = defaultdict(int)
    for material in data['materials']:
        id_counts[material['id']] += 1

    # 找出重复的ID
    duplicate_ids = {id_val: count for id_val, count in id_counts.items() if count > 1}

    print(f"发现 {len(duplicate_ids)} 个重复的ID:")
    for id_val, count in duplicate_ids.items():
        print(f"  - {id_val}: 出现 {count} 次")

    # 为重复的ID创建新的唯一ID
    used_ids = set()
    for material in data['materials']:
        used_ids.add(material['id'])

    # 修复重复ID
    fixed_count = 0
    for material in data['materials']:
        old_id = material['id']
        if old_id in duplicate_ids and duplicate_ids[old_id] > 1:
            # 生成新的唯一ID
            new_id = generate_unique_id()
            while new_id in used_ids:
                new_id = generate_unique_id()

            print(f"修复: {old_id} -> {new_id} (标题: {material['title']})")
            material['id'] = new_id
            used_ids.add(new_id)
            duplicate_ids[old_id] -= 1
            fixed_count += 1

    print(f"\n总共修复了 {fixed_count} 个重复ID")

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"已保存修复后的文件: {file_path}")

    # 验证修复结果
    verify_no_duplicates(file_path)

def verify_no_duplicates(file_path):
    """验证没有重复ID"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    ids = [material['id'] for material in data['materials']]
    unique_ids = set(ids)

    if len(ids) == len(unique_ids):
        print("✅ 验证通过：没有重复ID")
    else:
        print(f"❌ 验证失败：仍有 {len(ids) - len(unique_ids)} 个重复ID")

        # 找出仍然重复的ID
        id_counts = defaultdict(int)
        for id_val in ids:
            id_counts[id_val] += 1

        still_duplicate = {id_val: count for id_val, count in id_counts.items() if count > 1}
        for id_val, count in still_duplicate.items():
            print(f"  - {id_val}: 仍重复 {count} 次")

if __name__ == "__main__":
    file_path = "/Users/admin/Desktop/Work/ggame/article-rag/data/knowledge/materials.json"
    fix_duplicate_ids(file_path)
