from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import os
import json

from app.core.controller import Controller
from app.core.data_models import UserRequest

app = FastAPI(
    title="ARQV30-AI Data Stage API",
    description="API para orquestrar missões de pesquisa de mercado autônomas.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

controller = Controller()

@app.post("/start-research", status_code=202)
async def start_research(request: UserRequest, background_tasks: BackgroundTasks):
    """
    Inicia uma nova missão de pesquisa de mercado em background.
    Retorna imediatamente o session_id para acompanhamento.
    """
    try:
        print(f"[API] Recebida requisição de pesquisa: {request.topic}")
        session_id = await controller.start_mission(request.dict())
        print(f"[API] Missão iniciada com sucesso: {session_id}")
        return {"message": "Missão de pesquisa iniciada.", "session_id": session_id, "status": "processing"}
    except Exception as e:
        print(f"[API] Erro ao iniciar missão: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar missão: {str(e)}")

@app.get("/health")
async def health_check():
    """Endpoint para verificar se a API está funcionando."""
    return {"status": "ok", "message": "ARQV30-AI API está funcionando"}

@app.get("/research-status/{session_id}")
async def get_research_status(session_id: str):
    """
    Verifica o status de uma missão de pesquisa.
    """
    print(f"[API] Verificando status da sessão: {session_id}")
    session_dir = os.path.join("sessions", session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")

    try:
        # Encontra o último arquivo de estado salvo
        files = sorted([f for f in os.listdir(session_dir) if f.endswith(".json")])
        if not files:
            return {"session_id": session_id, "status": "iniciando", "last_step": "N/A"}

        last_file = files[-1]
        with open(os.path.join(session_dir, last_file), 'r', encoding='utf-8') as f:
            state = json.load(f)

        return {
            "session_id": session_id,
            "status": "concluído" if "final_state" in last_file else "em_progresso",
            "last_step": last_file.replace('.json', ''),
            "data_summary": {
                "urls_found": len(state.get("search_results", [])),
                "contents_extracted": len(state.get("extracted_data", [])),
                "screenshots_captured": len(state.get("screenshot_results", []))
            }
        }
    except Exception as e:
        print(f"[API] Erro ao ler estado da sessão: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao ler o estado da sessão: {e}")

@app.get("/research-results/{session_id}")
async def get_research_results(session_id: str):
    """
    Retorna os resultados completos de uma missão de pesquisa.
    """
    session_dir = os.path.join("sessions", session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")

    try:
        files = sorted([f for f in os.listdir(session_dir) if f.endswith(".json")])
        if not files:
            raise HTTPException(status_code=404, detail="Nenhum resultado encontrado.")

        last_file = files[-1]
        with open(os.path.join(session_dir, last_file), 'r', encoding='utf-8') as f:
            final_state = json.load(f)

        return final_state
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar resultados: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)