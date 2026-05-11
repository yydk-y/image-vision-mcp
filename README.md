# image-vision-mcp

MCP 服务器，为无视觉能力的 Claude Code 模型（如 DeepSeek）提供图片识别能力。

通过火山引擎豆包 API 实现图片→文字描述转换。

## 原理

```
Claude Code (DeepSeek) → describe_image 工具 → MCP Server → 豆包 API → 文字描述
```

## 安装

### 1. 前置条件

- Python 3.10+
- pip install mcp httpx
- 火山引擎 Ark API Key（开通豆包模型）

```bash
git clone https://github.com/yydk-y/image-vision-mcp.git
cd image-vision-mcp
pip install -r requirements.txt
```

### 2. 配置 MCP

编辑 `~/.claude/.mcp.json`（Windows: `C:\Users\<用户名>\.claude\.mcp.json`）：

```json
{
  "mcpServers": {
    "image-vision": {
      "command": "python3",
      "args": ["/path/to/image-vision-mcp/server.py"],
      "env": {
        "VOLCENGINE_API_KEY": "your-api-key"
      }
    }
  }
}
```

**Windows 示例：**

```json
{
  "mcpServers": {
    "image-vision": {
      "command": "python",
      "args": ["C:\\Users\\<用户名>\\image-vision-mcp\\server.py"],
      "env": {
        "VOLCENGINE_API_KEY": "your-api-key"
      }
    }
  }
}
```

### 3. 重启 Claude Code

MCP 服务器自动拉起，之后可用 `describe_image` 工具。

## 使用

Claude Code 中直接：

- "这张图里是什么？"
- "描述一下这张图片"
- "帮我提取这张截图里的文字"

## 手动测试

```bash
export VOLCENGINE_API_KEY=your-key    # macOS/Linux
set VOLCENGINE_API_KEY=your-key       # Windows
python test_vision.py <图片路径>
```

## 配置项

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `VOLCENGINE_API_KEY` | 火山引擎 API Key | 必填 |
| `VOLCENGINE_BASE_URL` | API 地址 | `https://ark.cn-beijing.volces.com/api/v3` |
| `VOLCENGINE_VISION_MODEL` | 模型名 | `doubao-seed-2-0-code-preview-260215` |

## 文件结构

| 文件 | 说明 |
|------|------|
| `server.py` | MCP 服务器入口 |
| `vision_client.py` | 豆包 API 封装 |
| `test_vision.py` | 独立测试脚本 |
| `requirements.txt` | Python 依赖 |
