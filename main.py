import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from agent import agent

load_dotenv()

app = FastAPI(title="RefundAI Agent Service")

class RefundRequest(BaseModel):
    query: str

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "RefundAI Agent"}

@app.post("/refund")
def handle_refund(request: RefundRequest):
    try:
        response = agent.invoke({
            "messages": [
                {"role": "user", "content": request.query}
            ]
        })
        
        last_message = response["messages"][-1]
        content = last_message.content

        if isinstance(content, list):
            reply_text = "".join(
                b.get("text", "") for b in content if isinstance(b, dict)
            )
        else:
            reply_text = str(content)

        return {"status": "success", "response": reply_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))