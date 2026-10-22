from langchain_ollama import ChatOllama

# Chỉ gọi model, không dùng Agent hay Tool
llm = ChatOllama(temperature=0, model="llama3.1")

print("Đang gửi yêu cầu đến Ollama...")
response = llm.invoke("Hello, who are you?")
print(response.content)