import os
from app.agents.rag import rag_tool
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from app.configurations.accesskeys import accesskeys_config
from langchain_community.utilities import GoogleSerperAPIWrapper
from app.agents.prompts import main_agent_prompt, quiz_prompt, explanation_prompt

os.environ["OPENAI_API_KEY"] = accesskeys_config.OPENAI_API_KEY
os.environ["SERPER_API_KEY"] = accesskeys_config.SERPAPI_API_KEY

model = ChatOpenAI(model="gpt-5", temperature=0)
serp_search = GoogleSerperAPIWrapper()
custom_serp_tool = Tool(
    name="web_search",
    description="Search the web for information",
    func=serp_search.run,
)

explanation_agent = create_agent(model=model, tools=[custom_serp_tool], system_prompt=explanation_prompt)
quiz_agent = create_agent(model=model, tools=[], system_prompt=quiz_prompt)

sub_agent_tools = [
    Tool(name="explain_concept", description="Explain a concept with cultural context", func=lambda q: explanation_agent.invoke({"messages": [{"role": "user", "content": q}]})),
    Tool(name="generate_quiz", description="Generate a quiz based on topic", func=lambda q: quiz_agent.invoke({"messages": [{"role": "user", "content": q}]})),
]

agent = create_agent(model=model, 
                     tools=[custom_serp_tool, rag_tool] + sub_agent_tools, 
                     system_prompt=main_agent_prompt)

# print(agent.invoke(
#     {"messages": [{"role": "user", "content": "whats the current time is lagos?"}]}
# ))
