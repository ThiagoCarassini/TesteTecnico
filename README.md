# Teste Técnico – Desenvolvedor Python Full Stack (Scraping + LLM Agent)

## Descrição

Este projeto foi desenvolvido como parte de um desafio técnico para a vaga de Desenvolvedor Python Full Stack. O objetivo é possibilitar a consulta de dados de advogados(as) diretamente do site oficial da OAB (CNA – Cadastro Nacional dos Advogados) e permitir que um agente de IA responda perguntas sobre esses dados automaticamente.

## Tecnologias Utilizadas

- Python 3.9+
- FastAPI
- LangChain
- OpenAI API
- Web Scraping com `requests` e `BeautifulSoup`
- Docker & Docker Compose
- Ambiente virtual com `venv`

## Estrutura do Projeto

```
TesteTecnico/
├── agent/
│   └── main.py                # Agente LLM com LangChain e OpenAI
├── scraper/
│   └── main.py                # Web scraper do site da OAB (CNA)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── venv/                      # Ambiente virtual Python
└── README.md
```

## Instalação e Execução com Docker

### Pré-requisitos

- Docker
- Docker Compose

### Clone o repositório

```bash
git clone https://github.com/ThiagoCarassini/TesteTecnico.git
cd TesteTecnico
```

### Adicione sua chave da OpenAI como variável de ambiente

Crie um arquivo `.env` na raiz do projeto com o conteúdo:

```env
OPENAI_API_KEY=sua_chave_aqui
```

### Execute a aplicação com Docker Compose

```bash
docker-compose up --build
```

## Instalação e Execução com Ambiente Virtual (venv)

Como alternativa ao Docker, você pode rodar o projeto localmente com `venv`:

```bash
# Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Exporte sua chave da OpenAI
export OPENAI_API_KEY=sua_chave_aqui  # Linux/macOS
set OPENAI_API_KEY=sua_chave_aqui     # Windows

# Execute os serviços manualmente
uvicorn scraper.main:app --port 8000
uvicorn agent.main:app --port 8001
```

## Funcionalidade da API (scraper)

### Endpoint: `/fetch_oab`

**Requisição:**

```json
POST /fetch_oab
{
  "name": "FULANO DE TAL",
  "uf": "SP"
}
```

**Resposta esperada:**

```json
{
  "oab": "123456",
  "nome": "FULANO DE TAL",
  "uf": "SP",
  "categoria": "Advogado",
  "data_inscricao": "01/01/2000",
  "situacao": "Ativo"
}
```

## Como funciona o Agente LLM (LangChain)

O agente é capaz de receber uma pergunta em linguagem natural, como:

> "Qual a situação de FULANO DE TAL em SP?"

Ele:

1. Detecta que precisa consultar o serviço `/fetch_oab`;
2. Envia a requisição para o scraper com base nos parâmetros extraídos da pergunta;
3. Gera uma resposta em português natural utilizando a API da OpenAI.

## Exemplos de uso via `curl`

### Consulta direta ao endpoint

```bash
curl -X POST http://localhost:8000/fetch_oab \
-H "Content-Type: application/json" \
-d '{"name": "JOAO", "uf": "MS"}'
```

### Interação com o agente

```bash
curl -X POST http://localhost:8001/ask \
-H "Content-Type: application/json" \
-d '{"question": "Qual a situação do advogado JOAO em MS?"}'
```

## Limitação Atual

A aplicação está estruturada corretamente e os serviços (scraper e agente) funcionam isoladamente. No entanto, durante os testes, foi identificado um problema na comunicação entre o agente LLM e o endpoint `/fetch_oab`, resultando em erros `404 Not Found` mesmo com a API online.

Além disso, as respostas do agente retornam:

```text
Resposta do agente LLM: Nenhum resultado encontrado para os critérios informados.
```

### Suspeita técnica

Esse problema pode estar relacionado a algum tipo de proteção contra scraping ou ataques DoS no site da OAB (https://cna.oab.org.br/), como:

- Rate limiting;
- Verificações de header;
- Cookies de sessão;
- Mudanças dinâmicas de HTML que afetam o scraper.

Por limitação de tempo para debugging profundo, essa questão ainda não foi totalmente resolvida.

### Capturas de Tela

#### Erro 404 nas chamadas ao endpoint `/fetch_oab`

![Erro 404](docs/img/fetch_oab_404.png)

#### Agente não encontra dados, mesmo com entrada válida

![Resposta vazia](docs/img/agente_resposta_vazia.png)

## Execução Local com venv (utilizada durante o desenvolvimento)

Durante o desenvolvimento do projeto, utilizei um ambiente virtual Python com `venv` para rodar os serviços localmente.

O ambiente foi criado com o seguinte comando:

```bash
python3 -m venv venv
```

Após a ativação do ambiente virtual, instalei as dependências com:

```bash
pip install -r requirements.txt
```

Os serviços foram então executados diretamente via Uvicorn:

```bash
uvicorn scraper.main:app --port 8000
uvicorn agent.main:app --port 8001
```

Apesar de o projeto contar com os arquivos `Dockerfile` e `docker-compose.yml`, a execução com Docker não foi usada diretamente no desenvolvimento, mas esses arquivos foram incluídos para atender aos requisitos do desafio técnico.

## Autor

Thiago Alves  
[github.com/ThiagoCarassini](https://github.com/ThiagoCarassini)
