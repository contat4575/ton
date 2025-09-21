import uuid
from typing import Dict, Any

from app.agents.agent_founder import AgentFounder
from app.agents.web_sailor_v2 import WebSailorV2
from app.agents.viral_content_agent import ViralContentAgent
from app.agents.content_extractor_v2 import ContentExtractorV2
from app.agents.visual_evidence_agent import VisualEvidenceAgent
from app.utils.data_saver import DataSaver

class Controller:
    """
    O Controller é o orquestrador-chefe que gerencia o ciclo de vida
    completo de uma missão de pesquisa.
    """

    def __init__(self):
        self.agent_map = {
            "AgentFounder": AgentFounder,
            "WebSailorV2": WebSailorV2,
            "ViralContentAgent": ViralContentAgent,
            "ContentExtractorV2": ContentExtractorV2,
            "VisualEvidenceAgent": VisualEvidenceAgent,
        }
        self.data_saver = DataSaver()
        print("Controller ARQV30-AI inicializado.")

    async def start_mission(self, user_request: Dict[str, Any]) -> str:
        """
        Inicia e gerencia uma nova missão de pesquisa.

        Args:
            user_request (Dict[str, Any]): A requisição inicial do usuário.

        Returns:
            str: O ID da sessão da missão.
        """
        session_id = f"session_{uuid.uuid4().hex}"
        state = {
            "session_id": session_id,
            "user_request": user_request,
            "mission_plan": None,
            "search_results": [],
            "extracted_data": [],
            "screenshot_results": []
        }
        await self.data_saver.save_state(session_id, "00_initial_state", state)
        print(f"[{session_id}] Nova missão iniciada. Tópico: {user_request.get('topic')}")

        # Etapa 1: Fundar a Equipe com o AgentFounder
        founder = AgentFounder(session_id)
        state = await founder.execute(state)
        await self.data_saver.save_state(session_id, "01_mission_plan", state)

        # Etapa 2: Instanciar e Executar a Equipe
        mission_plan = state.get("mission_plan", {})
        team = mission_plan.get("team", [])

        if not team:
            print(f"[{session_id}] Missão encerrada: Nenhum agente foi definido pelo AgentFounder.")
            return session_id

        # Executa os agentes definidos no plano
        for i, agent_config in enumerate(team):
            agent_class_name = agent_config.get("agent_class")
            if agent_class_name in self.agent_map:
                agent_class = self.agent_map[agent_class_name]
                agent_instance = agent_class(
                    session_id=session_id,
                    role=agent_config.get("role", ""),
                    goal=agent_config.get("goal", ""),
                    tools=agent_config.get("tools", []),
                    constraints=agent_config.get("constraints", [])
                )
                print(f"[{session_id}] Executando Agente: {agent_instance.get_name()}")
                state = await agent_instance.execute(state)
                await self.data_saver.save_state(session_id, f"{i+2:02d}_{agent_instance.get_name()}_output", state)
            else:
                print(f"[{session_id}] Aviso: Agente '{agent_class_name}' definido no plano não é reconhecido.")

        print(f"[{session_id}] Missão concluída. Todos os agentes executaram suas tarefas.")
        return session_id