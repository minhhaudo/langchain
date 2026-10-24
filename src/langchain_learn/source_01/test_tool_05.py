from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from typing import List
from pydantic import BaseModel, Field
from langchain.agents import create_agent
import langchain
langchain.debug = True
# Load environment variables from .env file (Cần có TAVILY_API_KEY trong file .env)
load_dotenv() 

class Source(BaseModel):
    """Schema for a source used by the agent"""
    url: str = Field(description="The URL of the source")

class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""
    answer: str = Field(description="The agent's answer to the query")
    sources: List[Source] = Field(
        default_factory=list, 
        description="A list of sources used by the agent to answer the query"
    )

def main():
    print("1. Đang khởi tạo model và Agent...")
    # Sử dụng command-r vì mô hình này tối ưu tốt cho RAG và Tool Calling
    llm = ChatOllama(temperature=0, model="qwen2.5:32b") 
    tools = [TavilySearch()]

    # Khởi tạo Agent (không dùng state_modifier vì phiên bản hiện tại không hỗ trợ)
    agent = create_agent(
        model=llm, 
        tools=tools, 
        response_format=AgentResponse
    )

    # Lời nhắc hệ thống (System Prompt) ép model phải trả về định dạng chuẩn
    system_prompt = (
       "You are an expert. You must use TavilySearch to find the weather. "
        "Then, you MUST output the result using the structured response tool. "
        "NEVER answer directly in plain text."
    )

    print("2. Đang hỏi Agent về thời tiết Tokyo...")
    
    # Truyền cả SystemMessage và HumanMessage vào list messages
    result = agent.invoke({
        "messages": [
            SystemMessage(content=system_prompt),
            HumanMessage(content="What is Tokyo the weather like today?")
        ]
    })

    print("\n--- 3. DỮ LIỆU CÓ CẤU TRÚC (STRUCTURED RESPONSE) ---")
    
    # Lấy dữ liệu đã được Pydantic ép kiểu thành object Python
    structured_data = result.get("structured_response")
    
    if structured_data:
        print(result)
        print(f"Câu trả lời tổng hợp: {structured_data.answer}\n")
        print("Các nguồn đã dùng (URLs):")
        for source in structured_data.sources:
            print(f"- {source.url}")
    else:
        print("Luồng chạy lỗi: Model vẫn trả về None cho structured_response.\n")
        print("Nội dung raw model trả về:")
        # In ra tin nhắn cuối để xem model đã trả lời gì thay vì gọi tool
        print(result["messages"][-1].content)

if __name__ == "__main__":
    main()