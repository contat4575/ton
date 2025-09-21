import asyncio
from typing import Dict, Any, List

from .base_agent import BaseAgent
from app.tools import search_tools

class WebSailorV2(BaseAgent):
    """
    O agente de busca principal, responsável por navegar na web.

    Utiliza um arsenal de ferramentas de busca para encontrar informações
    relevantes, seguindo as diretrizes de seu objetivo e persona.
    """

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa as buscas na web definidas no plano.

        Args:
            state (Dict[str, Any]): O estado atual, contendo o 'mission_plan'.

        Returns:
            Dict[str, Any]: O estado atualizado com os 'search_results'.
        """
        self.log(f"Iniciando missão: {self.goal}")

        mission_plan = state.get("mission_plan", {})
        queries = mission_plan.get("search_queries", [])

        if not queries:
            self.log("Nenhuma query de busca definida no plano. Missão de busca encerrada.")
            state["search_results"] = []
            return state

        tasks = []
        for query in queries:
            # Seleciona a ferramenta de busca apropriada (aqui simplificado, poderia ser mais inteligente)
            if "social" in query.lower() or "instagram" in query.lower():
                tasks.append(search_tools.search_viral_content(query))
            else:
                # Usa uma ferramenta de busca genérica com rotação
                tasks.append(search_tools.search_web_robust(query))

        self.log(f"Executando {len(tasks)} tarefas de busca em paralelo...")
        results_list = await asyncio.gather(*tasks, return_exceptions=True)

        # Consolida e limpa os resultados
        all_results: List[Dict[str, Any]] = []
        for result in results_list:
            if isinstance(result, Exception):
                self.log(f"Erro em uma tarefa de busca: {result}")
            elif result:
                all_results.extend(result)

        # Remove duplicatas baseadas na URL
        unique_urls = set()
        unique_results = []
        for item in all_results:
            url = item.get("url")
            if url and url not in unique_urls:
                unique_urls.add(url)
                unique_results.append(item)

        state["search_results"] = unique_results
        self.log(f"Busca concluída. {len(unique_results)} URLs únicas encontradas.")

        return state