from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

load_dotenv()

def main():
    print("Hello from langchain-learn! ")
    information = """Elon Musk is a prominent technology entrepreneur, investor, and business magnate, widely recognized as one of the wealthiest and most influential figures in the world. He is the driving force behind several major companies aiming to revolutionize transportation, space exploration, and technology.
Key Ventures and Roles:
Tesla, Inc.: As CEO and Product Architect, Musk helped popularize electric vehicles (EVs) globally. Tesla is also a major manufacturer of solar panels and battery energy storage systems.
SpaceX (Space Exploration Technologies Corp.): As Founder, CEO, and Chief Engineer, he focuses on reducing space transportation costs and enabling the colonization of Mars. SpaceX is notable for its reusable rockets and the Starlink satellite internet constellation.
X (formerly Twitter): Musk acquired the social media platform in 2022, serving as its owner and CTO, with stated goals of promoting free speech and developing a comprehensive "everything app."
Neuralink: Co-founder of a neurotechnology company developing implantable brain-machine interfaces to connect humans with computers.
The Boring Company: Founder of an infrastructure and tunnel construction company designed to solve urban traffic congestion.
Born in South Africa in 1971, Musk later moved to Canada and then the United States. He made his early fortune as a co-founder of Zip2 and X.com, the latter of which merged to become PayPal before being sold to eBay. Musk is known for his highly ambitious goals, unconventional management style, and significant, often controversial, impact across multiple global industries.
    """

    summary_template = """
    given the inforamtion {information} about a person I want you to create:
    1. A short summary
    2. two intersting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template =summary_template
    )

    llm = ChatOllama(temperature=0, model="gpt-oss:20b")
    chain = summary_prompt_template | llm

    response = chain.invoke(input={"information": information})
    print(response.content)

if __name__ == "__main__":
    main()