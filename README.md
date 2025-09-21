# ARQV30-AI Data Stage

Sistema Multi-Agente de Pesquisa de Mercado Autônoma

## 🚀 Instalação Rápida

### Windows
```bash
# Execute o instalador automático
install.bat
```

### Linux/Mac
```bash
# Instalar dependências Python
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Instalar dependências Node.js
npm install

# Configurar variáveis de ambiente
cp .env.example .env
```

## 🔧 Configuração

### Variáveis de Ambiente (Opcionais)

O sistema funciona **sem configuração de APIs externas**, usando fallbacks locais:

```env
# OpenRouter API (Opcional - para IA avançada)
OPENROUTER_API_KEY=your_key_here

# Serper API (Opcional - para buscas web)
SERPER_API_KEY=your_key_here
```

### Como Obter as Chaves (Opcional)

1. **OpenRouter**: Acesse [openrouter.ai](https://openrouter.ai) e crie uma conta
2. **Serper**: Acesse [serper.dev](https://serper.dev) e obtenha sua chave gratuita

## 🎯 Como Usar

### Iniciar o Sistema
```bash
# Windows
run.bat

# Linux/Mac
# Terminal 1 - Backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
npm run dev
```

### Acessar a Interface
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

### Exemplo de Pesquisa
1. Digite um tópico: "mercado de café especial no Brasil"
2. Clique em "Iniciar Missão de Pesquisa"
3. Acompanhe o progresso dos agentes
4. Visualize os resultados organizados

## 🤖 Agentes Disponíveis

- **AgentFounder**: Cria o plano de missão e define a equipe
- **WebSailorV2**: Realiza buscas web especializadas
- **ViralContentAgent**: Encontra conteúdo viral e tendências
- **ContentExtractorV2**: Extrai e processa conteúdo das URLs
- **VisualEvidenceAgent**: Captura screenshots como evidência

## 📊 Funcionalidades

- ✅ **Funciona offline** (sem APIs externas)
- ✅ **Pesquisa multi-fonte** (web, redes sociais, etc.)
- ✅ **Extração inteligente** de conteúdo
- ✅ **Captura de screenshots** automática
- ✅ **Interface web moderna** com acompanhamento em tempo real
- ✅ **Resultados organizados** por categorias
- ✅ **Exportação de dados** em JSON

## 🛠️ Arquitetura

```
ARQV30-AI/
├── app/                    # Backend Python (FastAPI)
│   ├── agents/            # Agentes de IA especializados
│   ├── core/              # Controlador e modelos
│   ├── tools/             # Ferramentas de busca e extração
│   └── utils/             # Utilitários e interfaces
├── src/                   # Frontend React + TypeScript
├── sessions/              # Dados das missões executadas
└── requirements.txt       # Dependências Python
```

## 🔍 Troubleshooting

### Erro de Créditos OpenRouter
- **Solução**: O sistema funciona sem a API, usando fallback local
- **Opcional**: Configure OPENROUTER_API_KEY para IA avançada

### Erro de Selenium/Screenshots
```bash
# Instalar ChromeDriver automaticamente
pip install webdriver-manager
```

### Porta em Uso
```bash
# Verificar processos na porta 8000
netstat -ano | findstr :8000
# Matar processo se necessário
taskkill /PID <PID> /F
```

## 📈 Roadmap

- [ ] Integração com mais APIs de busca
- [ ] Análise de sentimento avançada
- [ ] Exportação para PDF/Excel
- [ ] Dashboard de analytics
- [ ] API de webhooks
- [ ] Integração com bancos de dados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🆘 Suporte

- **Issues**: Abra uma issue no GitHub
- **Documentação**: Acesse http://localhost:8000/docs
- **Logs**: Verifique o console durante a execução