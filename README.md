# IA-GPT - Repositório de Projetos (Monorepo)

Este repositório está organizado como um **Monorepo** para centralizar todos os projetos, exercícios e aplicações desenvolvidas durante o curso, mantendo um único versionamento e uma única origem remota no GitHub.

---

## 📁 Estrutura de Pastas

```text
IA-GPT/
├── base.md                  # System prompt e especificações base para IA
├── README.md                # Visão geral e guia do repositório
├── .gitignore               # Regras de exclusão (ambientes virtuais, caches, etc.)
└── projetos/                # Diretório central de todos os projetos do curso
    ├── 01-nome-do-projeto/  # Exemplo de pasta de projeto individual
    │   ├── app.py           # Aplicação principal (ex: Streamlit)
    │   ├── requirements.txt # Dependências específicas do projeto
    │   └── README.md        # Documentação e instruções de execução daquele projeto
    └── ...
```

---

## 🛠️ Como Adicionar um Novo Projeto

1. **Crie uma nova pasta dentro de `projetos/`:**
   ```bash
   mkdir projetos/01-meu-primeiro-projeto
   ```

2. **Desenvolva seu código e defina as dependências:**
   - Adicione seus arquivos (`app.py`, módulos, etc.).
   - Recomenda-se salvar as dependências em um `requirements.txt` na própria pasta do projeto:
     ```bash
     pip freeze > projetos/01-meu-primeiro-projeto/requirements.txt
     ```

3. **Submeta as alterações para o GitHub:**
   ```bash
   git add .
   git commit -m "feat: adiciona projeto 01-meu-primeiro-projeto"
   git push origin main
   ```

---

## 🚀 Como Executar um Projeto

Navegue até a pasta do projeto desejado:
```bash
cd projetos/<nome-do-projeto>
```

Crie e ative o ambiente virtual (opcional, mas recomendado):
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Instale os pacotes necessários
pip install -r requirements.txt
```

Inicie a aplicação (por exemplo, Streamlit):
```bash
streamlit run app.py
```
