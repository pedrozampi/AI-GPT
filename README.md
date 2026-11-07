# IA-GPT | IA Generativa Aplicada à Programação (SENAI)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![SENAI](https://img.shields.io/badge/Institui%C3%A7%C3%A3o-SENAI-D0001B?style=flat-square)](https://www.sp.senai.br/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Architecture](https://img.shields.io/badge/Architecture-Monorepo-informational?style=flat-square)]()

Repositório central de projetos, experimentos práticos e soluções desenvolvidas durante a formação **"Inteligências Artificiais Generativas Aplicadas à Programação"** ofertada pelo **SENAI**.

---

## 🎯 Sobre o Curso e Repositório

O avanço das Inteligências Artificiais Generativas transformou a dinâmica do desenvolvimento de software. Este curso tem como foco capacitar desenvolvedores a utilizarem modelos de linguagem e ferramentas de IA generativa de forma estratégica, segura e eficiente no fluxo de trabalho técnico.

Mais do que apenas gerar código automaticamente, a formação ensina a atuar como um **arquiteto e avaliador crítico**: refinando contextos, estabelecendo diretrizes rigorosas, aplicando técnicas avançadas de Engenharia de Prompts e garantindo que o código gerado atenda a padrões profissionais de modularidade, desempenho e segurança.

### 🧠 Competências e Tópicos Desenvolvidos

- **Engenharia de Prompt para Código:** Elaboração de *System Prompts*, definição de personas técnicas, contexto operacional e restrições rígidas (conforme documentado em [`base.md`](./base.md)).
- **Pair Programming Assistido por IA:** Aceleração de desenvolvimento, refatoração orientada, geração de casos de teste e documentação técnica.
- **Desenvolvimento de Aplicações e Data Analytics:** Criação de dashboards interativos com **Streamlit**, análise exploratória e pipelines de manipulação de dados com **Pandas** e **NumPy**.
- **Validação e Qualidade de Código:** Inspeção contra alucinações de modelos, garantia de boas práticas (PEP 8), tratamento de exceções e otimização de performance (ex: cache e concorrência).

---

## 📁 Arquitetura do Repositório (Monorepo)

O projeto adota o padrão **Monorepo**, mantendo um ecossistema integrado para todos os módulos e projetos práticos com versionamento unificado:

```text
IA-GPT/
├── base.md                  # Prompt base de referência e diretrizes operacionais de IA
├── README.md                # Apresentação do repositório, objetivos e guia de uso
├── .gitignore               # Exclusões para Python, ambientes virtuais e credenciais
└── projetos/                # Hub de aplicações e exercícios práticos
    ├── 01-nome-do-projeto/  # Pasta individual do projeto/módulo
    │   ├── app.py           # Aplicação ou script principal
    │   ├── requirements.txt # Dependências específicas do módulo
    │   └── README.md        # Documentação e regras de negócio do projeto
    └── ...
```

---

## 🛠️ Como Adicionar um Novo Módulo ou Projeto

Para manter a organização do repositório ao iniciar um novo exercício ou projeto:

1. **Crie a pasta do módulo:**
   ```bash
   mkdir projetos/01-nome-do-projeto
   ```

2. **Desenvolva a solução:**
   - Adicione seus scripts (`app.py`, módulos auxiliares, dados de exemplo).
   - Isole e exporte os pacotes utilizados:
     ```bash
     pip freeze > projetos/01-nome-do-projeto/requirements.txt
     ```

3. **Registre a evolução no Git:**
   ```bash
   git add .
   git commit -m "feat(projeto-01): adiciona solucao com analise e streamlit"
   git push origin main
   ```

---

## 🚀 Como Executar Localmente

Cada projeto dentro de `projetos/` é autocontido. Para executar qualquer um deles:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/pedrozampi/AI-GPT.git
   cd AI-GPT
   ```

2. **Navegue até o projeto desejado:**
   ```bash
   cd projetos/<pasta-do-projeto>
   ```

3. **Configure o ambiente virtual:**
   ```bash
   # Criar ambiente virtual
   python -m venv .venv

   # Ativar ambiente (Windows)
   .venv\Scripts\activate

   # Ativar ambiente (Linux/Mac)
   source .venv/bin/activate
   ```

4. **Instale as dependências e execute:**
   ```bash
   pip install -r requirements.txt

   # Caso seja uma aplicação Streamlit:
   streamlit run app.py

   # Ou para scripts Python convencionais:
   python main.py
   ```

---

## 📜 Diretrizes de Desenvolvimento

Ao utilizar as IAs do curso para geração de novas soluções, adote como padrão o modelo especificado em [`base.md`](./base.md):
- **Modularidade & PEP 8:** Funções desacopladas e código legível.
- **Tratamento de Dados:** Validação prévia de tipos e tratamento consistente de valores ausentes/nulos.
- **Performance:** Uso de caching inteligente (`@st.cache_data`) em leituras de dados.
