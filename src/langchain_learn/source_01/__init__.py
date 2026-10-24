from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama

load_dotenv()


def main() -> None:
    print("Hello from langchain-learn!")
    print(os.environ.get("OPENAI_API_KEY"))


if __name__ == "__main__":
    main()
