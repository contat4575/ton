import asyncio
from typing import Dict, Any

from .base_agent import BaseAgent
from app.tools import screenshot_tool

class VisualEvidenceAgent(BaseAgent):
    """
    O "fotógrafo" da missão, responsável por capturar screenshots
    como prova visual irrefutável.
    """
    MAX_CONCURRENT_SCREENSHOTS = 3  # Limita para não sobrecarregar o sistema

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Captura screenshots das URLs alvo.

        Args:
            state (Dict[str, Any]): O estado com 'mission_plan' e 'search_results'.

        Returns:
            Dict[str, Any]: O estado atualizado com 'screenshot_results'.
        """
        self.log(f"Iniciando captura de evidências visuais: {self.goal}")
        mission_plan = state.get("mission_plan", {})
        targets = mission_plan.get("screenshot_targets", [])

        if not targets:
            self.log("Nenhum alvo para screenshot definido no plano.")
            state["screenshot_results"] = []
            return state

        tasks = []
        semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_SCREENSHOTS)

        async def capture_with_semaphore(url):
            async with semaphore:
                return await screenshot_tool.capture_screenshot(url, self.session_id)

        for url in targets:
            tasks.append(capture_with_semaphore(url))

        self.log(f"Capturando {len(tasks)} screenshots...")
        results = await asyncio.gather(*tasks, return_exceptions=True)

        final_results = []
        for result in results:
            if isinstance(result, Exception):
                self.log(f"Erro na captura de screenshot: {result}")
            elif result and result.get("success"):
                final_results.append(result)

        state["screenshot_results"] = final_results
        self.log(f"Captura de evidências concluída. {len(final_results)} screenshots salvos.")

        return state