import asyncio
import os

import telebot
from dotenv import load_dotenv

from mcp_config import get_mcp_client
# from langchain.agents import create_agent
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langchain.messages import HumanMessage, SystemMessage
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend, FilesystemBackend
from langchain.tools import tool


load_dotenv()

memory = InMemorySaver()
store = InMemoryStore()

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
bot = telebot.TeleBot(BOT_TOKEN)

config = {'configurable':{'thread_id':'1'}}

backend = CompositeBackend(
    default=StateBackend(),
    routes={
        "/memories/": StoreBackend(namespace=lambda _rt: ("use_one",)),
        "/skills/": FilesystemBackend(root_dir='./skills/',virtual_mode=True)
    }
)


async def ask_agent(query: str) -> str:
    client = get_mcp_client()
    tools = await client.get_tools()

    agent = create_deep_agent(
        model="gpt-4o-mini",
        tools=tools,
        system_prompt="You are a helpful assistant.",
        skills=['/skills/'],
        backend= backend,
        checkpointer=memory,
        store=InMemoryStore()
    )
    result = await agent.ainvoke({
        "messages": HumanMessage(content=query)},config=config)
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
