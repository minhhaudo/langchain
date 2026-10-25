from dotenv import load_dotenv
load_dotenv() 

from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langsmith import traceable
import time


MAX_ITERACTIONS = 10
MODEL = "qwen2.5:32b"

@tool
def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog."""
    print(f"   >>Executing get_product_price(product: '{product}')")
    prices = {"laptop": 1299.99, "smartphone": 799.99, "headphones": 199.99}
    return prices.get(product, 0.0)

@tool
def apply_discount(price: float, discount_tier: str) -> float:
    """Apply a discount tier to a price and return the final price. 
    Available tiers: bronze, silver, gold."""
    print(f"   >>Executing apply_discount(price: {price}, discount_tier: {discount_tier})")
    discount_percentage = {"bronze": 5, "silver": 10, "gold": 23}
    discount = discount_percentage.get(discount_tier, 0)
    return round(price*(1-discount/100), 2)

    
#--- Agent Loop ----

@traceable(name="Langchain Agent Loop")
def run_agent(question: str):
    tools = [get_product_price, apply_discount]
    tools_dict = {t.name: t for t in tools}

    #llm = init_chat_model(f"ollama:{MODEL}", temperature=0)
    #llm_with_tools = llm.bind_tools(tools)


    print(f"Question: {question}")
    print("=" * 60)
