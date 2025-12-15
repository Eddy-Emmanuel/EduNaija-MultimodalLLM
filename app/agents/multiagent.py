import os
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from app.agents.agent_workflow import AgentWorkFlow
from app.model.schema import ResponseVerificationSchema
from app.configurations.accesskeys import accesskeys_config
from app.agents.prompts import main_agent_prompt, verify_agent_prompt

os.environ["OPENAI_API_KEY"] = accesskeys_config.OPENAI_API_KEY
os.environ["TAVILY_API_KEY"] = accesskeys_config.TAVILY_API_KEY

llm_1 = ChatOpenAI(model_name="gpt-5-mini")
llm_2 = ChatOpenAI(model_name="gpt-5-mini")

llm_1_chain = main_agent_prompt | llm_1
llm_2_chain = verify_agent_prompt | llm_2.with_structured_output(ResponseVerificationSchema)

model = init_chat_model(model="gpt-5-mini", model_provider="openai")
search_toolkit = TavilySearch(max_results=5, topic="general")
search_agent = create_agent(model, [search_toolkit])

def EduNaijaAgent(state:AgentWorkFlow):
    response = llm_1_chain.invoke({"USER_INPUT": state["query"]}).content
    verification = llm_2_chain.invoke({"USER_INPUT": state["query"], "AGENT_RESPONSE": response})
    return {
        "query": state["query"],
        "is_question_answered": verification.is_answered == 'yes',
        "final_answer": response
    }

def ResponseChecker(state:AgentWorkFlow):
    if state["is_question_answered"]:
        return "answered"
    else:
        return "not_answered"

def CheckWeb(state:AgentWorkFlow):
    search_results = search_agent.invoke({"messages": state["query"]})["messages"][1].content
    return {
        "query": state["query"],
        "is_question_answered": True,
        "final_answer": search_results
    }

agent_graph = StateGraph(AgentWorkFlow)

agent_graph.add_node("main_agent", EduNaijaAgent)

agent_graph.add_node("check_web", CheckWeb)

agent_graph.add_edge(START, "main_agent")

agent_graph.add_conditional_edges(
    "main_agent",
    ResponseChecker,
    {
        "answered": END,
        "not_answered": "check_web"
    }
)

agent_graph.add_edge("check_web", END)

compiled_agent_graph = agent_graph.compile()

# print(compiled_agent_graph.invoke({"query": "Explain the Pythagorean theorem in Igbo."}))