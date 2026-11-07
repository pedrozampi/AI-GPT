# IA-GPT - Inteligências Artificiais Generativas Aplicadas à Programação

Este repositório agrupa os projetos em Python desenvolvidos durante o curso **"Inteligências Artificiais Generativas Aplicada a Programação"** do **SENAI**, cujo objetivo é capacitar e instruir sobre como utilizar corretamente as Inteligências Artificiais no desenvolvimento de software e programação.

O repositório está organizado no formato de **Monorepo**, centralizando exercícios, aplicações e experimentos práticos com versionamento unificado.

---

## 📁 Estrutura de Pastas

```text
IA-GPT/
├── base.md                  # System prompt e especificações base para engenharia de prompt / IA
├── README.md                # Visão geral, objetivo do curso e guia do repositório
├── .gitignore               # Regras de exclusão para Python, Streamlit e ambientes virtuais
└── projetos/                # Diretório central dos projetos práticos do curso
    ├── 01-nome-do-projeto/  # Pasta individual de cada aplicação ou exercício
    │   ├── app.py           # Código da aplicação (ex: Streamlit / scripts Python)
    │   ├── requirements.txt # Dependências específicas do projeto
    │   └── README.md        # Documentação e instruções daquele projeto
    └── ...
```

---

## 🛠️ Como Adicionar um Novo Projeto

1. **Crie a pasta do projeto dentro de `projetos/`:**
   ```bash
   mkdir projetos/01-meu-projeto
   ```

2. **Desenvolva o código e defina as dependências:**
   - Adicione seus scripts (`app.py`, módulos, etc.).
   - Recomenda-se registrar as dependências em um arquivo `requirements.txt` na própria pasta do projeto:
     ```bash
     pip freeze > projetos/01-meu-projeto/requirements.txt
     ```

3. **Submeta as alterações para o repositório:**
   ```bash
   git add .
   git commit -m "feat: adiciona projeto 01-meu-projeto"
   git push origin main
   ```

---

## 🚀 Como Executar um Projeto

1. Navegue até a pasta do projeto:
   ```bash
   cd projetos/<nome-do-projeto>
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instale os pacotes necessários:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação (exemplo com Streamlit ou Python puro):
   ```bash
   streamlit run app.py
   # ou
   python main.py
   ```
