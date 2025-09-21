import os
from typing import Dict, List

class APIRotator:
    """Gerencia e rotaciona chaves de API para diferentes serviços."""
    def __init__(self):
        self.keys: Dict[str, List[str]] = {
            "serper": [key for key in [os.getenv("SERPER_API_KEY"), os.getenv("SERPER_API_KEY_1")] if key],
            # Adicionar outras APIs aqui...
        }
        self.indices: Dict[str, int] = {service: 0 for service in self.keys}
        print("APIRotator inicializado.")

    def get_key(self, service: str) -> str | None:
        """Obtém a próxima chave de API disponível para um serviço."""
        if service not in self.keys or not self.keys[service]:
            return None
        
        key_list = self.keys[service]
        current_index = self.indices[service]
        key = key_list[current_index]
        
        # Rotaciona para a próxima chave
        self.indices[service] = (current_index + 1) % len(key_list)
        
        return key