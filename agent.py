# main.py file

"""
Telegram bot (using pyTelegramBotAPI / telebot) that answers messages
with the agent wired up to every MCP server registered in mcp_config.py.
"""
import asyncio
import os

import telebot
from dotenv import load_dotenv

from mcp_config import get_mcp_client
from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from langchain_core.chec

load_dotenv()

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
bot = telebot.TeleBot(BOT_TOKEN)

async def ask_agent(query: str) -> str:
    client = get_mcp_client()
    tools = await client.get_tools()

    agent = create_agent(
        model="gpt-4o-mini",
        tools=tools,
        system_prompt="You are a helpful assistant.",
    )
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"][-1].content


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, "typing")
    try:
        reply = asyncio.run(ask_agent(message.text))
    except Exception as e:
        reply = f"Something went wrong: {e}"
    bot.send_message(message.chat.id, reply)


if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
