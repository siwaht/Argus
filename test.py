"""
Agentic RAG
-----------
Expose retrieval as a tool; the agent decides when to call it and can
call it multiple times with refined queries. Better for multi-hop questions.
"""

from pathlib import Path
from langchain.agents import create_agent
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
from deepagents import CompiledSubAgent
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model("gpt-4o-mini")

# 1. Load the source document (plain text read, no loader abstraction needed).
source_path = Path("story.txt")
docs = [Document(page_content=source_path.read_text(encoding="utf-8"), metadata={"source": str(source_path)})]

# 2. Split into retrieval-friendly chunks.
splits = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)

# 3. Embed and index in memory.
embeddings = OpenAIEmbeddings()
vectorstore = InMemoryVectorStore.from_documents(splits, embeddings)
retriever = vectorstore.as_retriever()

# @tool(response_format="content_and_artifact")
@tool
def retrieve(query: str):
    """Retrieve top-3 relevant chunks for a query.

    Returns (text, artifact) so the agent gets both a string to read
    and the raw Document objects for downstream use.
    """
    results = retriever.invoke(query, k=3)
    text = "\n\n".join(f"Source: {d.metadata}\n{d.page_content}" for d in results)
    return text, results

agentx = create_agent(
    model,
    tools=[retrieve],
    system_prompt="""You are a retrieval specialist for the story "Lunch at the Liberty Diner".

Your job is to:
1. Use the retrieve tool to search the story document for relevant passages
2. Return accurate, complete information from the story
3. For character questions, retrieve their background, profession, and nationality
4. For plot questions, retrieve the relevant scene and events
5. Provide complete passages that answer the user's question

Always search thoroughly - you can call retrieve multiple times with different queries to get complete information.""",
)

# # Wrap it as a CompiledSubAgent
# rag_agent = CompiledSubAgent(
#     name="rag-agent",
#     description="Retrieval-augmented generation agent that searches a document vectorstore to answer questions with relevant context",
#     runnable=agentx,
# )



# stream_mode="values" yields full state per step; pretty-print latest message.
# result = agentx.invoke({'messages' : HumanMessage(content='who is the american')})
# print(result['messages'][-1].content)