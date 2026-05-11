"""MCP server exposing image description tool."""
import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from vision_client import VisionClient

server = Server("image-vision-mcp")
vision = VisionClient()


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="describe_image",
            description="Describe an image using Doubao Vision API. Use this to understand images, screenshots, charts, or documents. Returns a text description of the image content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Absolute path to the image file (.png, .jpg, .webp, .gif, .bmp)",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Optional custom prompt for image description. Default describes image in detail.",
                    },
                },
                "required": ["image_path"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "describe_image":
        image_path = arguments["image_path"]
        prompt = arguments.get(
            "prompt",
            "请详细描述这张图片的内容。如果是图表，请描述其中的数据、标签和趋势。如果是文档截图，请提取其中的文字内容。",
        )
        try:
            description = await vision.describe(image_path, prompt)
            return [TextContent(type="text", text=description)]
        except FileNotFoundError as e:
            return [TextContent(type="text", text=f"Error: {e}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error calling Vision API: {e}")]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
