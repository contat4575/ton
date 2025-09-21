import json
from typing import Dict, Any

from .base_agent import BaseAgent
from app.core.data_models import ResearchPlan
from app.utils.llm_interface import LLMInterface
from app.core.prompts import AGENT_FOUNDER_PROMPT
from pydantic import ValidationError

class AgentFounder(BaseAgent):
    """
    O cérebro estratégico da operação.

    Este meta-agente utiliza um LLM para analisar a requisição do usuário
    e criar uma equipe de agentes especializados, definindo suas personas,
    objetivos e ferramentas para a missão de pesquisa.
    """

    def __init__(self, session_id: str):
        # A constituição do AgentFounder é pré-definida.
        super().__init__(
            session_id=session_id,
            role="Meta-Agente Estratégico",
            goal="Criar um plano de missão detalhado e uma equipe de agentes de IA para executá-lo.",
            tools=["llm_call"],
            constraints=["O plano deve ser gerado em formato JSON válido e seguir o schema definido."]
        )
        self.llm = LLMInterface()

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera o plano de missão.

        Args:
            state (Dict[str, Any]): O estado inicial, contendo a 'user_request'.

        Returns:
            Dict[str, Any]: O estado atualizado com o 'mission_plan'.
        """
        self.log("Missão recebida. Fundando a equipe de agentes...")
        user_request = state.get("user_request", {})
        topic = user_request.get("topic")

        if not topic:
            self.log("Erro: Tópico da pesquisa não encontrado na requisição.")
            raise ValueError("O tópico da pesquisa é obrigatório.")

        # Formata o prompt com o tópico da requisição
        formatted_prompt = AGENT_FOUNDER_PROMPT.format(topic=topic)

        # Chama o LLM para gerar o plano de missão
        self.log(f"Consultando LLM para criar plano para o tópico: '{topic}'")
        raw_plan = await self.llm.generate_json(formatted_prompt)

        if not raw_plan:
            self.log("Erro: LLM não retornou um plano de missão válido.")
            raise ValueError("Falha ao gerar o plano de missão.")

        # Valida o plano com Pydantic
        try:
            mission_plan = ResearchPlan(**raw_plan)
            state["mission_plan"] = mission_plan.dict()
            self.log(f"Plano de missão validado. {len(mission_plan.team)} agentes designados.")
        except ValidationError as e:
            self.log(f"Erro de validação do plano gerado pela IA: {e}")
            raise ValueError(f"O plano de missão gerado pela IA é inválido: {e}")

        return state