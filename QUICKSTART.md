# HikeButler 快速开始指南

## 5 分钟快速启动

### 1. 安装依赖

```bash
# 使用 Poetry（推荐）
poetry install

# 或使用 pip
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp env.example .env

# 编辑 .env 文件，至少配置以下必需项：
# - DEEPSEEK_API_KEY 或 OPENAI_API_KEY（LLM）
# - QWEN_API_KEY 或 OPENAI_API_KEY（Embedding）
# - LANGSMITH_API_KEY（可选，用于监控）
```

### 3. 初始化数据库（可选）

如果使用 MySQL 存储用户数据：

```bash
# 确保 MySQL 服务已启动
python scripts/init_db.py
```

### 4. 启动应用

```bash
python -m hikebutler.main
```

或：

```bash
python hikebutler/main.py
```

### 5. 访问 UI

打开浏览器访问：`http://127.0.0.1:7860`

## 最小化配置

如果只想快速测试，最小配置如下：

1. **仅配置 LLM API Key**（在 `.env` 中）：
   ```
   OPENAI_API_KEY=your_openai_key
   ```

2. **修改模型配置**（`config/models.yaml`）：
   ```yaml
   llm:
     provider: openai
     model_name: gpt-3.5-turbo
     api_key: ${OPENAI_API_KEY}
   
   embedding:
     provider: openai
     model_name: text-embedding-ada-002
     api_key: ${OPENAI_API_KEY}
   ```

3. **跳过数据库初始化**（如果不需要持久化存储）

4. **启动应用**

## 常见问题

### Q: 启动时提示缺少依赖？

A: 确保已安装所有依赖：
```bash
pip install -r requirements.txt
```

### Q: 数据库连接失败？

A: 检查 MySQL 服务是否启动，以及 `.env` 中的数据库配置是否正确。

### Q: API Key 错误？

A: 确保 `.env` 文件中的 API Key 已正确配置，并且 `config/models.yaml` 中的环境变量引用正确。

### Q: ChromaDB 初始化失败？

A: 确保有写入权限，ChromaDB 会在 `./chroma_db` 目录创建数据库文件。

## 下一步

- 查看 [README.md](README.md) 了解完整功能
- 查看 [项目规范](.cursor/rules/agent.mdc) 了解开发规范
- 开始实现具体的节点功能（目前为框架代码）

