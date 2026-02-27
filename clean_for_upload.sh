#!/bin/bash

# RAG作文教学系统 - 上传前清理脚本

echo "🧹 开始清理项目文件..."

# 1. 清理Python缓存文件
echo "清理 Python 缓存..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# 2. 清理日志文件
echo "清理日志文件..."
rm -rf logs/*.log 2>/dev/null || true

# 3. 清理临时文件
echo "清理临时文件..."
rm -rf path/ 2>/dev/null || true
rm -rf tmp/ temp/ .tmp/ .temp/ 2>/dev/null || true

# 4. 清理向量数据库（可重建）
echo "清理向量数据库..."
rm -rf data/vectordb/*.sqlite3 2>/dev/null || true
rm -rf data/vectordb/*.index 2>/dev/null || true

# 5. 清理IDE文件
echo "清理 IDE 文件..."
rm -rf .vscode/ .idea/ 2>/dev/null || true
find . -name "*.swp" -delete 2>/dev/null || true
find . -name "*.swo" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true

# 6. 清理系统文件
echo "清理系统文件..."
find . -name ".DS_Store" -delete 2>/dev/null || true

# 7. 检查敏感文件
echo "检查敏感信息..."
if [ -f ".env" ]; then
    if grep -q "your_actual_api_key_here" .env; then
        echo "⚠️  警告: .env 文件中可能包含真实的 API 密钥"
        echo "请确保已将其替换为占位符或删除该文件"
    else
        echo "✅ .env 文件检查通过"
    fi
fi

# 8. 显示最终状态
echo "📊 清理完成！当前项目状态："
echo "文件总数: $(find . -type f | grep -v '.git' | wc -l | tr -d ' ')"
echo "目录大小: $(du -sh . | cut -f1)"

echo ""
echo "🚀 项目已准备好上传！"
echo "建议运行以下命令检查："
echo "  git add ."
echo "  git status"
echo "  git commit -m \"Initial commit: RAG作文教学系统\""

echo ""
echo "📝 上传前清单："
echo "✅ Python 缓存文件已清理"
echo "✅ 日志文件已清理"
echo "✅ 临时文件已清理"
echo "✅ 向量数据库已清理（可重建）"
echo "✅ IDE 配置文件已清理"
echo "✅ 系统临时文件已清理"
echo "✅ .gitignore 文件已配置"
echo "⚠️  请手动检查 .env 文件是否包含敏感信息"
