from langchain_core.tools import tool
from langchain_ollama import ChatOllama

@tool
def search(query: str) -> str:
    """
    Tool that researches over internet
    Args:
        query (str): The query to search for 
    """
    print(f"\n[Hệ thống Python] Đang thực thi hàm search với từ khóa: '{query}'")
    return "Tokyo weather is sunny"

def main():
    print("1. Đang khởi tạo model...")
    llm = ChatOllama(temperature=0, model="gpt-oss:20b")

    # Gắn tool trực tiếp vào LLM (Cách hiện đại)
    llm_with_tools = llm.bind_tools([search])

    print("2. Đang hỏi LLM về thời tiết Tokyo...")
    # Lệnh invoke này LLM sẽ không trả lời ngay, mà sẽ trả về Yêu cầu gọi Tool
    ai_msg = llm_with_tools.invoke("What is Tokyo the weather like today?")

    # Kiểm tra xem LLM có muốn gọi tool không
    if ai_msg.tool_calls:
        print("\n--- 3. LLM ĐÃ HIỂU VÀ YÊU CẦU DÙNG TOOL ---")
        for tool_call in ai_msg.tool_calls:
            print(f"- Tên tool LLM muốn dùng: {tool_call['name']}")
            print(f"- Tham số LLM tự tách ra: {tool_call['args']}")
            
            # Thực thi hàm Python thực tế bằng args do LLM cung cấp
            if tool_call['name'] == "search":
                result = search.invoke(tool_call['args'])
                print(f"\n--- 4. KẾT QUẢ TỪ TOOL ---")
                print(result)
    else:
        print("\n--- LLM TRẢ LỜI TRỰC TIẾP ---")
        print(ai_msg.content)

if __name__ == "__main__":
    main()