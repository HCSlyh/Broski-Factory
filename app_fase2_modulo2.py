from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

# -------------------------------------------------
# Configurazione del "livello" (può essere letta da env)
# -------------------------------------------------
LEVEL = int(os.getenv("APP_LEVEL", "2"))  # valore di default 2

# -------------------------------------------------
# Funzioni di supporto
# -------------------------------------------------
def _esegui_chiamata_astratta():
    """Funzione placeholder per la logica astratta."""
    pass

if LEVEL < 3:
    def _crea_nodo_A():
        """Crea il nodo di tipo A."""
        _esegui_chiamata_astratta()
        # logica di creazione nodo A (placeholder)
        return {"node": "A", "status": "created"}

    def _crea_nodo_B():
        """Crea il nodo di tipo B."""
        _esegui_chiamata_astratta()
        # logica di creazione nodo B (placeholder)
        return {"node": "B", "status": "created"}

# -------------------------------------------------
# Modello di input per l'endpoint POST
# -------------------------------------------------
class ProcessRequest(BaseModel):
    action: str  # "A" o "B"
    data: dict | None = None

# -------------------------------------------------
# Endpoint API
# -------------------------------------------------
@app.post("/api/v1/process")
async def process(request: ProcessRequest):
    """
    Endpoint che, in base al valore di `action`,
    invoca la creazione del nodo A o B (se disponibili).
    """
    if LEVEL >= 3:
        raise HTTPException(status_code=400, detail="Operazione non supportata al livello corrente.")

    if request.action.upper() == "A":
        result = _crea_nodo_A()
    elif request.action.upper() == "B":
        result = _crea_nodo_B()
    else:
        raise HTTPException(status_code=422, detail="Action must be 'A' or 'B'.")

    return {"result": result, "input": request.dict()}

# -------------------------------------------------
# Avvio del server (solo se LEVEL == 3)
# -------------------------------------------------
if LEVEL == 3:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)