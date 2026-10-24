from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from typing import List
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage

load_dotenv()  # Load environment variables from .env file



class Source(BaseModel):
    """"Scheam for a source used by the agetn"""

    url:str = Field(description="The URL of the source")

class AgentResponse(BaseModel):
    """"Schema for agetn response with answer and sources"""

    answer:str = Field(description="The agent's answer to the query")
    sources:List[Source] = Field(default_factory=list, description="A list of sources used by the agent to answer the query")

llm = ChatOllama(temperature=0, model="llama3.1")
tools = [TavilySearch()]

    # Khởi tạo Agent để tự động hóa luồng suy nghĩ và gọi tool
agent = create_agent(model = llm, tools = tools, response_format=AgentResponse)

def main():
    #print("1. Đang khởi tạo model và Agent...")
   

    print("2. Đang hỏi Agent về thời tiết Tokyo...")
    
    # Gửi yêu cầu qua agent.invoke
    result = agent.invoke({
        "messages": [
            SystemMessage(content="You MUST use the provided structured format/tool to return your final answer. Do NOT output raw text."),
            HumanMessage(content="What is Tokyo the weather like today?")
        ]
    })

    print("\n--- 3. KẾT QUẢ CUỐI CÙNG TỪ AGENT ---")
    # Lấy tin nhắn cuối cùng trong danh sách (câu trả lời tổng hợp từ LLM)
    print(result)

if __name__ == "__main__":
    main()