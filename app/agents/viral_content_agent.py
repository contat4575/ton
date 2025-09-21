from typing import Dict, Any

from .base_agent import BaseAgent
from app.tools import search_tools

class ViralContentAgent(BaseAgent):
    """
    Agente especializado em encontrar e analisar conteúdo viral.

    Focado em redes sociais, utiliza ferramentas específicas para identificar
    posts com alto engajamento.
    """

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa buscas focadas em conteúdo viral.

        Args:
            state (Dict[str, Any]): O estado atual da missão.

        Returns:
            Dict[str, Any]: O estado atualizado com 'viral_content_results'.
        """
        self.log(f"Iniciando busca por conteúdo viral: {self.goal}")

        topic = state.get("user_request", {}).get("topic", "")
        if not topic:
            self.log("Tópico não encontrado para a busca viral.")
            return state

        # A lógica de busca viral já está encapsulada na ferramenta
        viral_results = await search_tools.search_viral_content(topic)

        if "viral_content_results" not in state:
            state["viral_content_results"] = []

        state["viral_content_results"].extend(viral_results)
        self.log(f"Busca por conteúdo viral concluída. {len(viral_results)} itens encontrados.")

        return state