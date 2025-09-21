import React, { useState, useEffect } from 'react';
import { Search, Activity, Users, Database, Camera, Zap, Clock, CheckCircle, AlertCircle, Eye } from 'lucide-react';

interface MissionStatus {
  session_id: string;
  status: 'iniciando' | 'em_progresso' | 'concluído' | 'erro';
  last_step: string;
  data_summary?: {
    urls_found: number;
    contents_extracted: number;
    screenshots_captured: number;
  };
}

interface MissionResults {
  session_id: string;
  user_request: {
    topic: string;
  };
  mission_plan?: {
    search_queries: string[];
    team: any[];
  };
  search_results?: any[];
  extracted_data?: any[];
  screenshot_results?: any[];
}

const AgentCard = ({ agent, isActive, isCompleted }: { agent: any; isActive: boolean; isCompleted: boolean }) => {
  const getAgentIcon = (agentClass: string) => {
    switch (agentClass) {
      case 'WebSailorV2': return <Search className="w-6 h-6" />;
      case 'ViralContentAgent': return <Zap className="w-6 h-6" />;
      case 'ContentExtractorV2': return <Database className="w-6 h-6" />;
      case 'VisualEvidenceAgent': return <Camera className="w-6 h-6" />;
      default: return <Users className="w-6 h-6" />;
    }
  };

  const getStatusColor = () => {
    if (isCompleted) return 'from-green-500 to-emerald-600';
    if (isActive) return 'from-blue-500 to-cyan-600';
    return 'from-gray-400 to-gray-500';
  };

  return (
    <div className={`p-4 rounded-xl border-2 transition-all duration-500 ${
      isActive ? 'border-blue-400 shadow-lg shadow-blue-500/20' : 
      isCompleted ? 'border-green-400 shadow-lg shadow-green-500/20' :
      'border-gray-600'
    }`}>
      <div className="flex items-start gap-3">
        <div className={`p-3 rounded-lg bg-gradient-to-r ${getStatusColor()}`}>
          {getAgentIcon(agent.agent_class)}
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-white mb-1">{agent.agent_class}</h3>
          <p className="text-gray-300 text-sm mb-2">{agent.role}</p>
          <p className="text-gray-400 text-xs">{agent.goal}</p>
          <div className="flex items-center mt-2">
            {isCompleted && <CheckCircle className="w-4 h-4 text-green-400 mr-2" />}
            {isActive && <Activity className="w-4 h-4 text-blue-400 mr-2 animate-pulse" />}
            <span className={`text-xs ${
              isCompleted ? 'text-green-400' : 
              isActive ? 'text-blue-400' : 
              'text-gray-500'
            }`}>
              {isCompleted ? 'Concluído' : isActive ? 'Em execução' : 'Aguardando'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

const ResultsSection = ({ results }: { results: MissionResults }) => {
  const [activeTab, setActiveTab] = useState('overview');

  const tabs = [
    { id: 'overview', label: 'Visão Geral', icon: <Activity className="w-4 h-4" /> },
    { id: 'searches', label: 'Buscas', icon: <Search className="w-4 h-4" /> },
    { id: 'content', label: 'Conteúdo', icon: <Database className="w-4 h-4" /> },
    { id: 'screenshots', label: 'Screenshots', icon: <Camera className="w-4 h-4" /> },
  ];

  return (
    <div className="space-y-6">
      <div className="flex space-x-1 bg-gray-800 rounded-lg p-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
              activeTab === tab.id
                ? 'bg-blue-600 text-white shadow-lg'
                : 'text-gray-400 hover:text-white hover:bg-gray-700'
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      <div className="bg-gray-800 rounded-xl p-6">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gradient-to-r from-blue-600 to-cyan-600 p-4 rounded-lg text-white">
                <div className="flex items-center gap-3">
                  <Search className="w-8 h-8" />
                  <div>
                    <p className="text-sm opacity-90">URLs Encontradas</p>
                    <p className="text-2xl font-bold">{results.search_results?.length || 0}</p>
                  </div>
                </div>
              </div>
              <div className="bg-gradient-to-r from-green-600 to-emerald-600 p-4 rounded-lg text-white">
                <div className="flex items-center gap-3">
                  <Database className="w-8 h-8" />
                  <div>
                    <p className="text-sm opacity-90">Conteúdos Extraídos</p>
                    <p className="text-2xl font-bold">{results.extracted_data?.length || 0}</p>
                  </div>
                </div>
              </div>
              <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-4 rounded-lg text-white">
                <div className="flex items-center gap-3">
                  <Camera className="w-8 h-8" />
                  <div>
                    <p className="text-sm opacity-90">Screenshots</p>
                    <p className="text-2xl font-bold">{results.screenshot_results?.length || 0}</p>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-white mb-3">Consultas de Busca</h3>
              <div className="grid grid-cols-1 gap-2">
                {results.mission_plan?.search_queries?.map((query, index) => (
                  <div key={index} className="bg-gray-700 p-3 rounded-lg">
                    <p className="text-gray-300">{query}</p>
                  </div>
                )) || []}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'searches' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Resultados de Busca</h3>
            <div className="grid grid-cols-1 gap-4">
              {results.search_results?.map((result, index) => (
                <div key={index} className="bg-gray-700 p-4 rounded-lg">
                  <h4 className="font-semibold text-white mb-2">{result.title}</h4>
                  <a 
                    href={result.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 text-sm break-all"
                  >
                    {result.url}
                  </a>
                  <p className="text-gray-300 text-sm mt-2">{result.snippet}</p>
                </div>
              )) || []}
            </div>
          </div>
        )}

        {activeTab === 'content' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Conteúdo Extraído</h3>
            <div className="grid grid-cols-1 gap-4">
              {results.extracted_data?.map((content, index) => (
                <div key={index} className="bg-gray-700 p-4 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Eye className="w-4 h-4 text-green-400" />
                    <span className="text-sm text-green-400">{content.method}</span>
                  </div>
                  <a 
                    href={content.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 text-sm break-all block mb-2"
                  >
                    {content.url}
                  </a>
                  <div className="bg-gray-800 p-3 rounded max-h-48 overflow-y-auto">
                    <p className="text-gray-300 text-sm">{content.content?.substring(0, 500)}...</p>
                  </div>
                </div>
              )) || []}
            </div>
          </div>
        )}

        {activeTab === 'screenshots' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Screenshots Capturados</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {results.screenshot_results?.map((screenshot, index) => (
                <div key={index} className="bg-gray-700 p-4 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Camera className="w-4 h-4 text-blue-400" />
                    <span className="text-sm text-green-400">Capturado</span>
                  </div>
                  <a 
                    href={screenshot.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 text-sm break-all block mb-2"
                  >
                    {screenshot.url}
                  </a>
                  <p className="text-gray-400 text-xs">Arquivo: {screenshot.filepath}</p>
                </div>
              )) || []}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

function App() {
  const [topic, setTopic] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [missionStatus, setMissionStatus] = useState<MissionStatus | null>(null);
  const [missionResults, setMissionResults] = useState<MissionResults | null>(null);
  const [error, setError] = useState<string | null>(null);

  const startMission = async () => {
    if (!topic.trim()) return;

    setIsLoading(true);
    setError(null);
    setMissionResults(null);

    try {
      // Primeiro, testa se o backend está respondendo
      console.log('Testando conexão com o backend...');
      const healthResponse = await fetch('/api/health');
      if (!healthResponse.ok) {
        throw new Error('Backend não está respondendo');
      }
      console.log('Backend está ativo, iniciando missão...');

      const response = await fetch('/api/start-research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic: topic.trim() }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Erro na resposta:', errorText);
        throw new Error(`Falha ao iniciar a missão: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log('Missão iniciada:', data);
      setMissionStatus({
        session_id: data.session_id,
        status: 'iniciando',
        last_step: 'Inicializando...'
      });
    } catch (err) {
      console.error('Erro completo:', err);
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!missionStatus?.session_id) return;

    const pollStatus = async () => {
      try {
        console.log(`Verificando status da sessão: ${missionStatus.session_id}`);
        const response = await fetch(`/api/research-status/${missionStatus.session_id}`);
        if (response.ok) {
          const status = await response.json();
          console.log('Status atualizado:', status);
          setMissionStatus(status);

          if (status.status === 'concluído') {
            // Buscar resultados completos
            const resultsResponse = await fetch(`/api/research-results/${missionStatus.session_id}`);
            if (resultsResponse.ok) {
              const results = await resultsResponse.json();
              setMissionResults(results);
            }
            setIsLoading(false);
          }
        } else {
          console.error('Erro ao verificar status:', response.status);
        }
      } catch (err) {
        console.error('Erro ao verificar status:', err);
      }
    };

    const interval = setInterval(pollStatus, 3000);
    return () => clearInterval(interval);
  }, [missionStatus?.session_id]);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-900 via-purple-900 to-indigo-900 py-8">
        <div className="container mx-auto px-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              ARQV30-AI Data Stage
            </h1>
            <p className="text-blue-200 text-lg">Sistema Multi-Agente de Pesquisa de Mercado Autônoma</p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-8">
        {/* Mission Control Panel */}
        <div className="bg-gray-800 rounded-2xl p-8 mb-8 shadow-2xl">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
            <Zap className="w-7 h-7 text-yellow-400" />
            Centro de Controle de Missões
          </h2>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-3">
                Tópico de Pesquisa
              </label>
              <div className="space-y-4">
                <textarea
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="Digite o tópico que você quer pesquisar (ex: mercado de café especial no Brasil, tendências de moda 2025, análise competitiva de startups fintech...)"
                  className="w-full p-4 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  rows={4}
                  disabled={isLoading}
                />
                <button
                  onClick={startMission}
                  disabled={isLoading || !topic.trim()}
                  className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all duration-200 ${
                    isLoading || !topic.trim()
                      ? 'bg-gray-600 cursor-not-allowed'
                      : 'bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 shadow-lg hover:shadow-xl'
                  }`}
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center gap-2">
                      <Activity className="w-5 h-5 animate-spin" />
                      Processando Missão...
                    </div>
                  ) : (
                    <div className="flex items-center justify-center gap-2">
                      <Search className="w-5 h-5" />
                      Iniciar Missão de Pesquisa
                    </div>
                  )}
                </button>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold flex items-center gap-2">
                <Activity className="w-5 h-5 text-blue-400" />
                Status da Missão
              </h3>
              
              {missionStatus ? (
                <div className="bg-gray-700 p-4 rounded-lg">
                  <div className="flex items-center gap-3 mb-3">
                    <div className={`w-3 h-3 rounded-full ${
                      missionStatus.status === 'concluído' ? 'bg-green-400' :
                      missionStatus.status === 'em_progresso' ? 'bg-blue-400 animate-pulse' :
                      missionStatus.status === 'erro' ? 'bg-red-400' :
                      'bg-yellow-400'
                    }`}></div>
                    <span className="text-white font-medium">
                      Sessão: {missionStatus.session_id.substring(0, 12)}...
                    </span>
                  </div>
                  
                  <div className="text-sm text-gray-300 space-y-1">
                    <p><strong>Status:</strong> {missionStatus.status}</p>
                    <p><strong>Última Etapa:</strong> {missionStatus.last_step}</p>
                    {missionStatus.data_summary && (
                      <div className="mt-3 pt-3 border-t border-gray-600">
                        <p>URLs: {missionStatus.data_summary.urls_found} | 
                           Conteúdos: {missionStatus.data_summary.contents_extracted} | 
                           Screenshots: {missionStatus.data_summary.screenshots_captured}</p>
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div className="bg-gray-700 p-4 rounded-lg text-gray-400 text-center">
                  Aguardando início da missão...
                </div>
              )}

              {error && (
                <div className="bg-red-900/50 border border-red-600 p-4 rounded-lg">
                  <div className="flex items-center gap-2">
                    <AlertCircle className="w-5 h-5 text-red-400" />
                    <span className="text-red-400 font-medium">Erro</span>
                  </div>
                  <p className="text-red-300 text-sm mt-1">{error}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Agent Team Status */}
        {missionResults?.mission_plan?.team && (
          <div className="bg-gray-800 rounded-2xl p-8 mb-8 shadow-2xl">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <Users className="w-7 h-7 text-green-400" />
              Equipe de Agentes
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {missionResults.mission_plan.team.map((agent, index) => (
                <AgentCard
                  key={index}
                  agent={agent}
                  isActive={false}
                  isCompleted={missionStatus?.status === 'concluído'}
                />
              ))}
            </div>
          </div>
        )}

        {/* Results */}
        {missionResults && missionStatus?.status === 'concluído' && (
          <div className="bg-gray-800 rounded-2xl p-8 shadow-2xl">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <Database className="w-7 h-7 text-purple-400" />
              Resultados da Missão
            </h2>
            <ResultsSection results={missionResults} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;