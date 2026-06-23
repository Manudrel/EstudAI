# 📚 EstudAI

Sistema desenvolvido para a disciplina de **Inteligência Artificial** do **CEFET-RJ**, com o objetivo de explorar o uso de **arquiteturas agênticas (Agentic AI)** utilizando **LangChain**.

O projeto automatiza a criação de materiais de estudo a partir de múltiplas fontes de informação, realizando pesquisa, validação e geração de conteúdo educacional por meio de agentes especializados.

---

## 🎯 Objetivo

O EstudAI foi criado para demonstrar a aplicação prática de agentes de IA cooperativos na construção de conteúdo educacional.

A aplicação recebe um tema de estudo, realiza pesquisas em diferentes fontes, valida as informações encontradas e gera uma aula estruturada contendo explicações e exercícios para o aluno.

---

## 🏗️ Arquitetura do Sistema

O sistema é composto por três agentes principais:

### 🔍 Researcher Agent

Responsável por realizar a coleta de informações sobre o tema solicitado.

#### Ferramentas Utilizadas

##### 📄 PDF Tool

Permite a leitura e extração de conteúdo de arquivos PDF fornecidos pelo usuário.

##### 📚 ArXiv Tool

Realiza buscas em artigos científicos disponíveis na plataforma ArXiv.

##### 🌐 Web Search Tool

Executa pesquisas na internet para complementar as informações obtidas.

#### Responsabilidades

* Buscar informações relevantes.
* Consultar múltiplas fontes.
* Consolidar o material coletado.
* Encaminhar os resultados para validação.

---

### 📝 Reviewer Agent

Responsável por revisar e validar o conteúdo produzido pelo agente pesquisador.

#### Responsabilidades

* Verificar consistência das informações.
* Identificar possíveis erros ou incoerências.
* Melhorar clareza e qualidade do conteúdo.
* Garantir maior confiabilidade dos dados.

---

### 👨‍🏫 Professor Agent

Responsável por transformar o conteúdo validado em material didático.

#### Responsabilidades

* Elaborar explicações estruturadas.
* Organizar os tópicos da aula.
* Produzir exemplos práticos.
* Criar questões de fixação.
* Gerar conteúdo voltado ao aprendizado.

---

## 🔄 Fluxo de Funcionamento

```text
Usuário
   │
   ▼
Researcher Agent
   │
   ├── PDF Tool
   ├── ArXiv Tool
   └── Web Search Tool
   │
   ▼
Reviewer Agent
   │
   ▼
Professor Agent
   │
   ▼
Material de Estudo Gerado
```

---

## 🛠️ Tecnologias Utilizadas

### Backend

* Python
* LangChain
* LangGraph (caso utilizado)
* APIs de LLM

### Interface

* Streamlit

### Ferramentas de Pesquisa

* ArXiv API
* Busca Web
* Leitura de PDFs

---

## 📂 Estrutura do Projeto

```text
EstudAI/
│
├── agents/
│   ├── researcher.py
│   ├── reviewer.py
│   └── professor.py
│
├── tools/
│   ├── pdf_tool.py
│   ├── arxiv_tool.py
│   └── web_search_tool.py
│
├── services/
│   └── orchestrator.py
│
├── prompts/
│   ├── researcher_system.txt
│   ├── reviewer_system.txt
│   └── professor_system.txt
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 Como Executar

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/EstudAI.git

cd EstudAI
```

### 2. Criar Ambiente Virtual

```bash
python -m venv venv
```

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` contendo as chaves necessárias para os modelos e APIs utilizadas.

Exemplo:

```env
GROQ_API_KEY=xxxxxxxxxxxxxxxx
```

### 5. Executar a Aplicação

```bash
streamlit run app.py
```

---

## 📖 Exemplo de Uso

1. O usuário informa um tema de estudo.
2. O Researcher Agent realiza pesquisas em PDFs, artigos científicos e na web.
3. O Reviewer Agent valida o conteúdo encontrado.
4. O Professor Agent organiza as informações em formato de aula.
5. O sistema retorna:

   * Explicação teórica
   * Resumo dos conceitos
   * Exercícios de fixação
   * Questões para revisão

---

## 🎓 Contexto Acadêmico

Este projeto foi desenvolvido como trabalho da disciplina de **Inteligência Artificial do CEFET-RJ**, com foco no estudo de:

* Sistemas Multiagentes
* Agentic AI
* Large Language Models (LLMs)
* Engenharia de Prompts
* Orquestração de Agentes com LangChain

---

## 👨‍💻 Autor

Desenvolvido por **Emanudrel Duarte** para a disciplina de Inteligência Artificial do CEFET-RJ.
