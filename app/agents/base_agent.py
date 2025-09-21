from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """
    Classe base abstrata para todos os Agentes de IA do sistema ARQV30.

    Cada agente representa uma entidade autônoma com uma função específica
    dentro de uma missão de pesquisa. Eles operam sobre um estado compartilhado,
    modificando-o sequencialmente para atingir o objetivo da missão.
    """
    def __init__(self, session_id: str, role: str, goal: str, tools: list, constraints: list):
        """
        Inicializa o agente com sua 'constituição' definida pelo AgentFounder.

        Args:
            session_id (str): O ID único da missão atual.
            role (str): A persona que o agente deve assumir.
            goal (str): O objetivo mensurável que o agente deve alcançar.
            tools (list): A lista de ferramentas que o agente está autorizado a usar.
            constraints (list): As limitações e regras que o agente deve seguir.
        """
        self.session_id = session_id
        self.role = role
        self.goal = goal
        self.tools = tools
        self.constraints = constraints
        self.memory = set()  # Memória interna para evitar trabalho duplicado

    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a tarefa principal do agente.

        Recebe o estado atual da missão, realiza sua tarefa e retorna o estado
        modificado para o próximo agente na cadeia.

        Args:
            state (Dict[str, Any]): O dicionário de estado atual da missão.

        Returns:
            Dict[str, Any]: O dicionário de estado atualizado.
        """
        pass

    def get_name(self) -> str:
        """Retorna o nome da classe do agente."""
        return self.__class__.__name__

    def log(self, message: str):
        """Helper para logging padronizado dos agentes."""
        print(f"[{self.get_name()}][{self.session_id}]: {message}")