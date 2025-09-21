import os
import json
import aiohttp
from typing import Dict, Any

# Esta classe deve ser robusta, usando o OpenRouter para acessar
# modelos como Tongyi/Qwen ou Claude 3.5 Sonnet.

class LLMInterface:
    """Interface para comunicação com o LLM via OpenRouter."""
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        # Corrigido: Removido o espaço em branco no final da URL
        self.base_url = "https://openrouter.ai/api/v1"
        # Atualizado: Usando um modelo Qwen mais recente/disponível
        # Verifique em https://openrouter.ai/models o nome exato
        self.model = "qwen/qwen-2.5-72b-instruct" # Exemplo, confirme no site
        print("LLMInterface inicializada.")

    async def generate_json(self, prompt: str) -> Dict[str, Any] | None:
        """Gera uma resposta em JSON a partir de um prompt."""
        if not self.api_key:
            print("[LLMInterface] Erro: OPENROUTER_API_KEY não configurada.")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }

        try:
            async with aiohttp.ClientSession() as session:
                # Corrigido: A URL agora será montada corretamente
                async with session.post(f"{self.base_url}/chat/completions", headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        json_content = result["choices"][0]["message"]["content"]
                        return json.loads(json_content)
                    else:
                        error_text = await response.text()
                        print(f"[LLMInterface] Erro na API: {response.status} - {error_text}")
                        return None
        except Exception as e:
            print(f"[LLMInterface] Erro na requisição: {e}")
            return None