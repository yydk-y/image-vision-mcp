"""Volcano Engine Doubao Vision API client."""
import base64
import os
from pathlib import Path
from typing import Optional

import httpx


class VisionClient:
    """Calls Doubao Vision API to describe images."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ["VOLCENGINE_API_KEY"]
        self.base_url = base_url or os.environ.get(
            "VOLCENGINE_BASE_URL",
            "https://ark.cn-beijing.volces.com/api/v3",
        )
        self.model = model or os.environ.get(
            "VOLCENGINE_VISION_MODEL",
            "doubao-seed-2-0-code-preview-260215",
        )

    async def describe(
        self,
        image_path: str,
        prompt: str = "请详细描述这张图片的内容。如果是图表，请描述其中的数据、标签和趋势。如果是文档截图，请提取其中的文字内容。",
    ) -> str:
        """Send image to Doubao Vision and return text description."""
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        ext = path.suffix.lower()
        media_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
        }
        media_type = media_types.get(ext)
        if not media_type:
            raise ValueError(f"Unsupported image format: {ext}")

        image_data = path.read_bytes()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        data_url = f"data:{media_type};base64,{base64_image}"

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "image_url", "image_url": {"url": data_url}},
                                {"type": "text", "text": prompt},
                            ],
                        }
                    ],
                    "max_tokens": 4096,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
