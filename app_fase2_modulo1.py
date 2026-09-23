from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Livello corrente dell'applicazione
LEVEL = 2  # Cambia questo valore a 3 per avviare il server

def _esegui_chiamata_astratta():
    """Funzione placeholder per una chiamata astratta."""
    pass

# Definizioni disponibili solo se il livello è inferiore a 3
if LEVEL < 3:
    def _crea_nodo_A():
        """Crea il nodo A."""
        _esegui_chiamata_astratta()
        return {"node": "A", "status": "created"}

    def _crea_nodo_B():
        """Crea il nodo B."""
        _esegui_chiamata_astratta()
        return {"node": "B", "status": "created"}

class ProcessRequest(BaseModel):
    data: dict

@app.post("/api/v1/process")
def process(request: ProcessRequest):
    """
    Endpoint POST che, se il livello è < 3, crea i nodi A e B.
    """
    if LEVEL < 3:
        result_a = _crea_nodo_A()
        result_b = _crea_nodo_B()
        return {
            "level": LEVEL,
            "input": request.data,
            "result_A": result_a,
            "result_B": result_b,
        }
    else:
        raise HTTPException(status_code=400, detail="Operazione non consentita al livello corrente.")

# Avvio del server solo quando il livello è esattamente 3
if __name__ == "__main__" and LEVEL == 3:
    uvicorn.run(app, host="0.0.0.0", port=8000)