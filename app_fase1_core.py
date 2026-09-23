import os
import sys
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

# Inizializzazione delle variabili d'ambiente per il Cloud
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")

app = FastAPI(
    title="Broski Factory Core Cloud",
    description="Infrastruttura Server Web FastAPI per Micro-SaaS con IA scalabile",
    version="1.0.0"
)

class PayloadSaaS(BaseModel):
    prompt: str
    client_id: str = "commercial_user"

@app.get("/")
def read_root():
    return {
        "status": "ONLINE",
        "factory_level": 1,
        "message": "Broski Factory Server Core attivo nel Cloud."
    }

@app.post("/api/v1/process", summary="Elaborazione Richiesta Commerciale IA")
def process_ai_request(payload: PayloadSaaS):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY assente.")
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Sei l'assistente IA commerciale della Broski Factory."},
                {"role": "user", "content": payload.prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        return {
            "success": True,
            "engine": "Groq Llama3 Cloud Network",
            "response": completion.choices[0].message.content.strip()
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_fase1_core:app", host="0.0.0.0", port=8000, reload=True)
