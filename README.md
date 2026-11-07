# IA-GPT - Repositório Principal com Submódulos

Este repositório está configurado para suportar **Git Submodules** (Submódulos do GitHub).

---

## 📁 Estrutura do Projeto

```text
IA-GPT/
├── .git/                 # Repositório Git principal
├── .gitmodules           # Arquivo gerado automaticamente ao adicionar submódulos
├── .gitignore            # Regras de exclusão para Python e ambiente local
├── base.md               # Prompt base / especificações do projeto
├── submodules/           # Diretório reservado para submódulos externos
│   └── .gitkeep
└── README.md             # Instruções de uso e comandos
```

---

## 🚀 Como Utilizar Submódulos

### 1. Clonar este repositório com todos os submódulos
Para clonar o projeto principal já trazendo todos os submódulos inicializados:
```bash
git clone --recurse-submodules <URL_DO_REPOSITORIO>
```

Se o repositório já foi clonado sem a flag:
```bash
git submodule update --init --recursive
```

---

### 2. Adicionar um novo submódulo
Para adicionar um repositório como submódulo dentro da pasta `submodules/`:
```bash
git submodule add <URL_DO_SUBMODULO> submodules/<nome-do-modulo>
```

Após executar, o Git criará automaticamente o arquivo `.gitmodules` e registrará o ponteiro para o commit do submódulo. Em seguida, comite a alteração:
```bash
git add .gitmodules submodules/<nome-do-modulo>
git commit -m "Adiciona submódulo <nome-do-modulo>"
```

---

### 3. Atualizar os submódulos
Para atualizar todos os submódulos para os commits mais recentes das suas respectivas branches remotas:
```bash
git submodule update --remote --merge
```

---

### 4. Remover um submódulo (se necessário)
Caso queira remover um submódulo:
```bash
# 1. Desinicializar
git submodule deinit -f submodules/<nome-do-modulo>

# 2. Remover do índice e do disco
git rm -f submodules/<nome-do-modulo>

# 3. Limpar histórico interno do Git
rm -rf .git/modules/submodules/<nome-do-modulo>

# 4. Comitar a remoção
git commit -m "Remove submódulo <nome-do-modulo>"
```
