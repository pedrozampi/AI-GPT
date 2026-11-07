# IA-GPT | IA Generativa Aplicada à Programação (SENAI)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![SENAI](https://img.shields.io/badge/Institui%C3%A7%C3%A3o-SENAI-D0001B?style=flat-square)](https://www.sp.senai.br/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Express-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com/python/)
[![Pandas](https://img.shields.io/badge/Pandas-DataFrames-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
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

## 🧰 Bibliotecas e Frameworks Utilizados

O ecossistema dos projetos utiliza uma stack moderna focada em análise de dados, interfaces web e ciência de dados com Python:

| Biblioteca / Framework | Função Principal |
| :--- | :--- |
| **[Python 3.10+](https://www.python.org/)** | Linguagem base para desenvolvimento dos scripts, automações e lógicas de negócio. |
| **[Streamlit](https://streamlit.io/)** | Framework para construção de interfaces web, dashboards e aplicações interativas com Python puro. |
| **[Pandas](https://pandas.pydata.org/)** | Ingestão, limpeza, manipulação tabular, cruzamento de dados (`merge`/`join`) e agregação analítica. |
| **[NumPy](https://numpy.org/)** | Computação numérica vetorial, suporte a arrays multidimensionais e operações estatísticas. |
| **[Plotly Express](https://plotly.com/python/)** | Criação de gráficos interativos com suporte a zoom, tooltips dinâmicos e layout responsivo. |
| **[OpenPyXL](https://openpyxl.readthedocs.io/)** | Motor de leitura, processamento e escrita de planilhas do Microsoft Excel (`.xlsx`). |

---

## 📁 Arquitetura do Repositório (Monorepo)

O projeto adota o padrão **Monorepo**, onde todos os exercícios e projetos estão **organizados por dia de aula** dentro do diretório `projetos/`:

```text
IA-GPT/
├── base.md                  # Prompt base de referência e diretrizes operacionais de IA
├── README.md                # Apresentação do repositório, objetivos e guia de uso
├── .gitignore               # Exclusões para Python, ambientes virtuais e credenciais
└── projetos/                # Hub central dos projetos práticos
    ├── 0711/                # Pasta referente ao dia da aula (ex: 07 de Novembro - DDMMAAAA / DDMM)
    │   └── ex1/             # Exercício ou projeto específico do dia
    │       ├── app.py           # Aplicação interativa em Streamlit
    │       ├── ex1_prompt.md    # Engenharia de prompt detalhada e documentação do projeto
    │       ├── requirements.txt # Dependências específicas do exercício
    │       ├── sales_raw.csv    # Base de dados de vendas (entrada)
    │       └── customers.xlsx   # Base cadastral de clientes (entrada)
    └── <proximo_dia>/       # Próximas aulas e exercícios subsequentes...
```

---

## 🛠️ Como Adicionar um Novo Módulo ou Exercício

Para manter a padronização ao iniciar os exercícios de um novo dia de aula:

1. **Crie a pasta do dia e do exercício dentro de `projetos/`:**
   ```bash
   mkdir -p projetos/DDMM/ex1
   ```
   *(Exemplo para a aula de 07/11: `projetos/0711/ex1`)*

2. **Desenvolva a solução:**
   - Adicione seus scripts (`app.py`, módulos auxiliares, bases de dados).
   - Documente o prompt em um arquivo markdown (ex: `ex1_prompt.md`).
   - Isole e exporte os pacotes utilizados:
     ```bash
     pip freeze > projetos/DDMM/ex1/requirements.txt
     ```

3. **Registre a evolução no Git:**
   ```bash
   git add .
   git commit -m "feat(DDMM/ex1): adiciona solucao do exercicio 1"
   git push origin main
   ```

---

## 🚀 Como Executar Localmente

Cada projeto dentro das pastas diárias é autocontido. Para executar qualquer exercício:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/pedrozampi/AI-GPT.git
   cd AI-GPT
   ```

2. **Navegue até a pasta do exercício do dia desejado:**
   ```bash
   cd projetos/0711/ex1
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
- **Design & Usabilidade:** Gráficos interativos com Plotly e layout adaptável via parâmetros modernos do Streamlit (`width='stretch'`).
