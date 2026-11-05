import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import REFUND_AGENT_SYSTEM_PROMPT
from tools.transaction_tools import get_transaction_details, get_refund_policy, calculate_elapsed_time, process_refund

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") 
# MODEL = "gemini-3.6-flash"
MODEL = "gemini-3.5-flash-lite"

llm = ChatGoogleGenerativeAI(
    model=MODEL,
    api_key=api_key,
    temperature=0
)

toosl=[
    get_transaction_details,
    get_refund_policy,
    calculate_elapsed_time,
    process_refund
]

agent = create_agent(
    model=llm,
    system_prompt=REFUND_AGENT_SYSTEM_PROMPT,
    tools= toosl
    )


if __name__ == "__main__":
    transaction_id = "txn_101"  
    # response = agent.invoke({"role": "user", "messages": f"Please check the refund eligibility for transaction ID: {transaction_id}"})

    user_query = f"Please check the refund eligibility for transaction ID: {transaction_id}"

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_query}
        ]
    })
    print("**********Response**********")
    # print(response["messages"][-1].content)
    message = response["messages"][-1].content
    if isinstance(message, list):
        output_text = "".join(
            block.get("text", "") 
            for block in message 
            if isinstance(block, dict)
        )
        print(output_text)
    else:
        print(message)