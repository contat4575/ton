from pydantic import BaseModel, Field
from typing import List, Dict, Any

class AgentConfig(BaseModel):
    """Configuração para um único agente na equipe da missão."""
    agent_class: str = Field(..., description="O nome da classe do agente a ser instanciado.")
    role: str = Field(..., description="A persona detalhada que o agente deve assumir.")
    goal: str = Field(..., description="O objetivo claro e mensurável do agente.")
    tools: List[str] = Field(..., description="A lista de ferramentas que o agente está autorizado a usar.")
    constraints: List[str] = Field(..., description="As limitações e regras que o agente deve seguir.")

class ResearchPlan(BaseModel):
    """O plano de missão completo gerado pelo AgentFounder."""
    search_queries: List[str] = Field(..., description="Lista de queries de busca altamente específicas.")
    extraction_tasks: List[Dict[str, Any]] = Field(default_factory=list, description="Tarefas de extração com URLs e tipos de conteúdo.")
    screenshot_targets: List[str] = Field(default_factory=list, description="URLs prioritárias para captura de evidência visual.")
    team: List[AgentConfig] = Field(..., description="A equipe de agentes de IA designada para a missão.")

class UserRequest(BaseModel):
    """Modelo para a requisição do usuário que inicia a pesquisa."""
    topic: str
    user_id: str | None = None