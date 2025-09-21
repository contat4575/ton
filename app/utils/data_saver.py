import os
import json
from typing import Dict, Any

class DataSaver:
    """Salva o estado da missão em arquivos JSON."""
    def __init__(self):
        self.base_dir = "sessions"
        os.makedirs(self.base_dir, exist_ok=True)
        print("DataSaver inicializado.")

    async def save_state(self, session_id: str, step_name: str, state: Dict[str, Any]):
        """Salva o estado atual da missão."""
        session_dir = os.path.join(self.base_dir, session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        filepath = os.path.join(session_dir, f"{step_name}.json")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                # Usar default=str para lidar com objetos não serializáveis como Pydantic models
                json.dump(state, f, ensure_ascii=False, indent=2, default=str)
            print(f"[DataSaver] Estado salvo em: {filepath}")
        except Exception as e:
            print(f"[DataSaver] Erro ao salvar estado: {e}")