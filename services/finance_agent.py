from phi.model.groq import Groq 
from phi.agent import Agent 
from phi.tools.googlesearch import GoogleSearch
from phi.tools.yfinance import YFinanceTools
import os
from dotenv import load_dotenv

load_dotenv()

MODEL="qwen/qwen3.8-27b"


web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for news, market developments, and macro context.",
    model=Groq(id=MODEL),
    tools=[GoogleSearch()],
    show_tool_calls=True,
)

finance_data_agent = Agent(
    name="Finance Data Agent",
    role="Query stock market metrics, fundamentals, and prices.",
    model=Groq(id=MODEL),
    tools=[YFinanceTools()],
    show_tool_calls=True,
    markdown=True
)

multiagent = Agent(
    name="Investment Strategy MultiAgent",
    model=Groq(id=MODEL),
    team=[web_search_agent, finance_data_agent],
    instructions=[
        "Use the Finance Data Agent for stock tickers and numerical metrics.",
        "Use the Web Search Agent for current news and qualitative context.",
        "Synthesize both outputs to form a detailed financial analysis."
    ],
    show_tool_calls=True,
    markdown=True,
)


