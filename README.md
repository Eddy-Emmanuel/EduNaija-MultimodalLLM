# EduNaijaAgent: A Multi-Agent System for Nigerian Educational Assistance

## Abstract

This paper presents EduNaijaAgent, a multi-agent AI system designed to provide educational assistance tailored to the Nigerian curriculum and linguistic diversity. The system leverages large language models (LLMs) and web search capabilities to answer educational queries in multiple languages, including English, Nigerian Pidgin, Yorùbá, Igbo, and Hausa. Implemented using LangGraph for workflow orchestration, the system consists of a main reasoning agent, a verification agent, and a web search agent. The architecture ensures accurate, culturally relevant responses while maintaining academic integrity. Preliminary design analysis suggests potential for improving educational access in multilingual contexts.

## Introduction

Education in Nigeria faces challenges such as limited access to quality resources, linguistic diversity, and alignment with national curricula like WAEC, NECO, and JAMB. With over 250 ethnic groups and multiple languages, educational AI systems must accommodate this diversity to be effective. EduNaijaAgent addresses this by creating a multi-agent system that detects input language, responds accordingly, and provides step-by-step explanations for academic problems.

The system is built on LangChain and LangGraph, utilizing OpenAI's GPT models and Tavily for web search. It emphasizes learner-friendly teaching, using local examples and discouraging exam cheating.

## Related Work

Multi-agent systems in education have been explored for personalized learning (e.g., ITS systems). Works like those using LLMs for tutoring (e.g., GPT-based assistants) focus on English, but few address multilingual, culturally specific contexts. In Africa, AI education tools are emerging, but EduNaijaAgent uniquely combines language detection, verification, and web augmentation for Nigerian education.

## Methodology

### System Architecture

EduNaijaAgent uses a state graph with three nodes:

1. **Main Agent**: Processes user queries, generates responses in the detected language.
2. **Verifier Agent**: Checks if the response fully answers the query.
3. **Web Search Agent**: If verification fails, performs web search for additional information.

The workflow starts at the main agent, conditionally routes to web search if needed, and ends with a final answer.

### Agents and Prompts

- **Main Agent Prompt**: Instructs the LLM to respond in the input language, align with Nigerian curriculum, use local examples.
- **Verifier Prompt**: Binary check (yes/no) on whether the question is answered.
- **Search Integration**: Uses TavilySearch for general topics, limited to 5 results.

### Technologies

- **LLMs**: GPT-4o-mini (referred to as "gpt-5-mini" in code, likely a placeholder).
- **Framework**: LangGraph for state management, LangChain for chains.
- **Search**: Tavily API.
- **Schema**: Pydantic for structured outputs.

## Implementation

The code is structured in Python modules:

- `multiagent.py`: Defines the graph, agents, and compilation.
- `agent_workflow.py`: TypedDict for state.
- `prompts.py`: ChatPromptTemplates for agents.
- `accesskeys.py`: Configuration for API keys.
- `schema.py`: Response verification schema.

The system is invoked via `compiled_agent_graph.invoke({"query": user_input})`.

## Evaluation

As a prototype, evaluation is design-based. The system aims for:

- Accuracy: Verified responses.
- Cultural Relevance: Nigerian examples.
- Language Support: Automatic detection and response.
- Integrity: No exam cheating assistance.

Future work includes user testing, performance metrics, and expansion to more subjects.

## Conclusion

EduNaijaAgent demonstrates the potential of multi-agent AI for localized education. By integrating language diversity and verification, it provides a foundation for scalable educational tools in Nigeria. Ongoing development will focus on multimodal inputs and broader curriculum coverage.

## References

1. LangChain Documentation. https://python.langchain.com/
2. LangGraph Documentation. https://langchain-ai.github.io/langgraph/
3. Nigerian Education Curriculum. https://www.waec.org/
4. Tavily Search API. https://tavily.com/

(Note: This is a preliminary write-up based on the project code. Expand with empirical data for a full research paper.)