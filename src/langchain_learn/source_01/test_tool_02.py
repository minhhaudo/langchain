from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from tavily import TavilyClient

load_dotenv()  # Load environment variables from .env file

tavily_client = TavilyClient()

@tool
def search(query: str) -> str:
    """
    Tool that researches over internet
    Args:
        query (str): The query to search for 
    """
    print(f"\n[Hệ thống Python] Đang thực thi hàm search với từ khóa: '{query}'")
    return tavily_client.search(query=query)

def main():
    print("1. Đang khởi tạo model và Agent...")
    llm = ChatOllama(temperature=0, model="gpt-oss:20b")
    tools = [search]

    # Khởi tạo Agent để tự động hóa luồng suy nghĩ và gọi tool
    agent = create_react_agent(llm, tools)

    print("2. Đang hỏi Agent về thời tiết Tokyo...")
    
    # Gửi yêu cầu qua agent.invoke
    result = agent.invoke({
        "messages": [HumanMessage(content="What is Tokyo the weather like today?")]
    })

    print("\n--- 3. KẾT QUẢ CUỐI CÙNG TỪ AGENT ---")
    # Lấy tin nhắn cuối cùng trong danh sách (câu trả lời tổng hợp từ LLM)
    print(result["messages"][-1].content)

if __name__ == "__main__":
    main()