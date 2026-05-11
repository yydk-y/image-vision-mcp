"""Standalone test for VisionClient (doesn't require MCP)."""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from vision_client import VisionClient


async def main():
    if not os.environ.get("VOLCENGINE_API_KEY"):
        print("ERROR: VOLCENGINE_API_KEY not set")
        print(
            "Set it via: set VOLCENGINE_API_KEY=your-key (Windows) or export (Linux/Mac)"
        )
        sys.exit(1)

    client = VisionClient()
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not image_path:
        print("Usage: python test_vision.py <image_path> [prompt]")
        sys.exit(1)

    prompt = sys.argv[2] if len(sys.argv) > 2 else None
    print(f"Describing: {image_path}")
    result = await client.describe(image_path, prompt)
    print(f"\nDescription:\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
