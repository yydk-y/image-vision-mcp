# image-vision-mcp

MCP 服务器，为 DeepSeek 等无视觉能力的 Claude Code 模型提供图片识别能力。

通过豆包模型（火山引擎 Ark API）实现图片→文字描述转换。

## 原理

```
Claude Code (DeepSeek) → 调用 describe_image 工具 → MCP Server → 豆包视觉模型 → 返回文字描述
```

## 安装

### 1. 前置条件

- Python 3.10+
- 火山引擎 Ark API Key（开通豆包模型）

### 2. 配置 MCP

在 `C:\Users\dyfun\.claude\.mcp.json` 中添加：

```json
"image-vision": {
  "command": "D:\\PPython\\Python313\\python.exe",
  "args": ["C:\\Users\\dyfun\\image-vision-mcp\\server.py"],
  "env": {
    "VOLCENGINE_API_KEY": "your-api-key"
  }
}
```

### 3. 重启 Claude Code

MCP 服务器自动拉起。

### 4. 依赖安装

```bash
cd C:\Users\dyfun\image-vision-mcp
pip install mcp httpx
```

## 使用

Claude Code 中直接说：

- "这张图里是什么？"
- "描述一下这张图片"  
- "帮我提取这张截图里的文字"

DeepSeek 会自动调用 `describe_image` 工具，豆包模型识别后返回文字。

## 手动测试

```bash
set VOLCENGINE_API_KEY=your-key
python test_vision.py <图片路径>
```

## 文件结构

| 文件 | 说明 |
|------|------|
| `server.py` | MCP 服务器入口 |
| `vision_client.py` | 豆包 API 封装 |
| `test_vision.py` | 独立测试脚本 |
| `requirements.txt` | Python 依赖 |
