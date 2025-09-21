import asyncio
from typing import Dict, Any, List

from .base_agent import BaseAgent
from app.tools import extraction_tools

class ContentExtractorV2(BaseAgent):
    """
    Agente responsável por processar URLs e extrair conteúdo limpo.
    """
    MAX_CONCURRENT_EXTRACTIONS = 10

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai conteúdo das URLs coletadas pelos agentes de busca.

        Args:
            state (Dict[str, Any]): O estado atual com 'search_results'.

        Returns:
            Dict[str, Any]: O estado atualizado com 'extracted_data'.
        """
        self.log(f"Iniciando extração de conteúdo: {self.goal}")
        search_results = state.get("search_results", [])
        urls_to_extract = [item.get("url") for item in search_results if item.get("url")]

        if not urls_to_extract:
            self.log("Nenhuma URL para extrair.")
            state["extracted_data"] = []
            return state

        tasks = []
        semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_EXTRACTIONS)

        async def extract_with_semaphore(url):
            async with semaphore:
                return await extraction_tools.extract_content_robust(url)

        for url in urls_to_extract:
            if url not in self.memory:
                tasks.append(extract_with_semaphore(url))
                self.memory.add(url)

        self.log(f"Extraindo conteúdo de {len(tasks)} URLs...")
        extracted_results = await asyncio.gather(*tasks, return_exceptions=True)

        final_data = []
        for result in extracted_results:
            if isinstance(result, Exception):
                self.log(f"Erro na extração: {result}")
            elif result:
                final_data.append(result)

        state["extracted_data"] = final_data
        self.log(f"Extração concluída. {len(final_data)} conteúdos extraídos com sucesso.")

        return state