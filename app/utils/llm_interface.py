import os
import json
import aiohttp
from typing import Dict, Any

class LLMInterface:
    """Interface para comunicação com o LLM via OpenRouter com fallback local."""
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "qwen/qwen-2.5-72b-instruct"
        print("LLMInterface inicializada.")

    async def generate_json(self, prompt: str) -> Dict[str, Any] | None:
        """Gera uma resposta em JSON a partir de um prompt com fallback local."""
        
        # Tenta usar a API do OpenRouter primeiro
        if self.api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"}
                }

                async with aiohttp.ClientSession() as session:
                    async with session.post(f"{self.base_url}/chat/completions", headers=headers, json=data) as response:
                        if response.status == 200:
                            result = await response.json()
                            json_content = result["choices"][0]["message"]["content"]
                            return json.loads(json_content)
                        else:
                            error_text = await response.text()
                            print(f"[LLMInterface] Erro na API OpenRouter: {response.status} - {error_text}")
                            print("[LLMInterface] Usando fallback local...")
            except Exception as e:
                print(f"[LLMInterface] Erro na requisição OpenRouter: {e}")
                print("[LLMInterface] Usando fallback local...")
        else:
            print("[LLMInterface] OPENROUTER_API_KEY não configurada. Usando fallback local...")

        # Fallback: Gera um plano de missão baseado no tópico extraído do prompt
        return self._generate_fallback_plan(prompt)

    def _generate_fallback_plan(self, prompt: str) -> Dict[str, Any]:
        """Gera um plano de missão local baseado no tópico."""
        # Extrai o tópico do prompt
        topic = "pesquisa geral"
        if "'{" in prompt and "}'" in prompt:
            start = prompt.find("'{") + 2
            end = prompt.find("}'", start)
            if end > start:
                topic = prompt[start:end]
        elif "tópico: '" in prompt:
            start = prompt.find("tópico: '") + 9
            end = prompt.find("'", start)
            if end > start:
                topic = prompt[start:end]

        print(f"[LLMInterface] Gerando plano local para tópico: '{topic}'")

        # Template de plano baseado no tópico
        plan = {
            "search_queries": [
                f"análise de mercado {topic} 2025",
                f"tendências {topic} Brasil",
                f"concorrentes {topic} principais empresas",
                f"estatísticas {topic} dados mercado",
                f"oportunidades negócio {topic}"
            ],
            "extraction_tasks": [
                {
                    "url": f"https://www.google.com/search?q={topic.replace(' ', '+')}_mercado",
                    "content_type": "market_analysis"
                }
            ],
            "screenshot_targets": [
                f"https://www.google.com/search?q={topic.replace(' ', '+')}"
            ],
            "team": [
                {
                    "agent_class": "WebSailorV2",
                    "role": f"Você é um analista de mercado especializado em {topic}, focado em dados quantitativos e análise competitiva.",
                    "goal": f"Encontrar os principais players e tendências no mercado de {topic}, identificando oportunidades e ameaças.",
                    "tools": ["search_google", "search_serper"],
                    "constraints": [
                        "Focar apenas em dados do mercado brasileiro dos últimos 12 meses.",
                        "Priorizar fontes confiáveis e dados verificáveis."
                    ]
                },
                {
                    "agent_class": "ViralContentAgent",
                    "role": f"Você é um especialista em conteúdo viral e tendências digitais relacionadas a {topic}.",
                    "goal": f"Identificar conteúdos virais, discussões em redes sociais e tendências emergentes sobre {topic}.",
                    "tools": ["search_viral", "social_media_analysis"],
                    "constraints": [
                        "Focar em conteúdo com alto engajamento dos últimos 30 dias.",
                        "Analisar sentimento e percepção do público."
                    ]
                },
                {
                    "agent_class": "ContentExtractorV2",
                    "role": "Você é um arquivista digital especializado em extração e organização de conteúdo web.",
                    "goal": "Extrair e processar todo o conteúdo textual relevante das URLs encontradas pelos outros agentes.",
                    "tools": ["extract_trafilatura", "extract_bs4"],
                    "constraints": [
                        "O conteúdo extraído deve ter no mínimo 200 palavras para ser considerado válido.",
                        "Remover elementos de navegação, anúncios e conteúdo irrelevante."
                    ]
                },
                {
                    "agent_class": "VisualEvidenceAgent",
                    "role": "Você é um documentarista visual responsável por capturar evidências visuais importantes.",
                    "goal": "Capturar screenshots de alta qualidade das páginas mais relevantes encontradas durante a pesquisa.",
                    "tools": ["capture_screenshot"],
                    "constraints": [
                        "Priorizar páginas com dados estatísticos, gráficos ou informações visuais importantes.",
                        "Garantir que os screenshots sejam legíveis e informativos."
                    ]
                }
            ]
        }

        return plan