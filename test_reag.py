#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from reag.client import ReagClient, Document

load_dotenv()
async def main():
      # 使用 OpenAI 模型
    async with ReagClient(
        model="openai/gpt-4o-mini",  # 添加 openai/ 前缀
        system="You are a helpful AI assistant.",
        batch_size=1
    ) as client:
        docs = [
            Document(
                name="Superagent",
                content="Superagent is a workspace for AI-agents that learn, perform work, and collaborate.",
                metadata={
                    "url": "https://superagent.sh",
                    "source": "web",
                },
            ),
        ]
        response = await client.query("What is Superagent?", documents=docs)
        print("Response:", response)

if __name__ == "__main__":
    asyncio.run(main())