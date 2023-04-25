from langchain.chat_models import ChatOpenAI
import os

from llm.qa_chain import qa_chain
from llm.sql_chain import db_chain
from langchain.agents import Tool, AgentExecutor, ConversationalAgent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

llm = ChatOpenAI(temperature=0)

tools = [
    Tool(
        name="Product descriptions and store information",
        func=qa_chain.run,
        description="Useful when the user asks for the brand, history, policies, shipping policies, return policies, collections, product suggestions or descriptions"
    ),
    Tool(
        name="Product specific information",
        func=db_chain.run,
        description="Useful when the user asks about price, color, size, availability."
    ),
]

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",  # important to align with agent prompt (below)
    k=5,
    return_messages=True
)

store_agent = ConversationalAgent.from_llm_and_tools(
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=1,
    early_stopping_method="generate",
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=store_agent,
    tools=tools,
    memory=memory,
    verbose=True,
)


