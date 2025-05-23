# 🏡 Sistema de Controle de Tarefas Domésticas

Um sistema desktop elegante para gerenciar tarefas domésticas, desenvolvido em Python com interface gráfica moderna.

## 📋 Definição do Problema

O sistema resolve a necessidade de organizar e distribuir tarefas domésticas entre os moradores de uma casa, permitindo:

- ✅ Cadastrar tarefas por categoria (Cozinha, Limpeza, Jardim, etc.)
- 👥 Associar responsáveis às tarefas
- 📊 Acompanhar o desempenho dos moradores
- 🏆 Ranking de quem mais contribui com as atividades
- 💾 Salvar dados em arquivo JSON

## 📖 Casos de Uso

### **UC01 - Gerenciar Moradores**
**Ator:** Usuário do Sistema  
**Descrição:** Cadastrar, listar e gerenciar moradores da casa

**Fluxo Principal:**
1. Usuário acessa a tela de moradores
2. Sistema exibe lista de moradores cadastrados
3. Usuário pode adicionar novo morador informando nome
4. Sistema salva morador e atualiza a lista
5. Sistema exibe pontuação atual de cada morador

### **UC02 - Criar Nova Tarefa**
**Ator:** Usuário do Sistema  
**Descrição:** Criar uma nova atividade doméstica

**Fluxo Principal:**
1. Usuário clica em "Nova Tarefa"
2. Sistema exibe formulário com:
   - Categoria (Cozinha, Limpeza, Jardim, Roupas, Manutenção)
   - Nome da tarefa
   - Descrição
   - Responsável
3. Usuário preenche dados e confirma
4. Sistema cria tarefa com status "PENDENTE"
5. Sistema atualiza lista de tarefas

### **UC03 - Gerenciar Status das Tarefas**
**Ator:** Usuário do Sistema  
**Descrição:** Marcar tarefas como finalizadas ou canceladas

**Fluxo Principal:**
1. Usuário visualiza lista de tarefas
2. Sistema exibe tarefas com status atual
3. Usuário seleciona tarefa e altera status
4. Para tarefas FINALIZADAS: sistema adiciona pontos ao responsável
5. Sistema atualiza dados e salva no arquivo JSON

### **UC04 - Visualizar Relatórios**
**Ator:** Usuário do Sistema  
**Descrição:** Consultar estatísticas e ranking dos moradores

**Fluxo Principal:**
1. Usuário acessa aba "Relatórios"
2. Sistema exibe:
   - Ranking dos moradores por pontos
   - Estatísticas por categoria
   - Gráfico de desempenho
   - Histórico de tarefas do mês
3. Usuário pode filtrar dados por período

### **UC05 - Persistir Dados**
**Ator:** Sistema  
**Descrição:** Salvar e carregar dados automaticamente

**Fluxo Principal:**
1. Sistema carrega dados do arquivo JSON na inicialização
2. A cada operação, sistema salva dados automaticamente
3. Sistema faz backup dos dados periodicamente
4. Em caso de erro, sistema restaura backup anterior

## 🛠️ Instalação e Execução

### **Pré-requisitos:**
- Python 3.8 ou superior
- Bibliotecas incluídas: tkinter, json, datetime, enum

### **Passo a Passo:**

1. **Clone ou baixe o projeto:**
```bash
git clone [seu-repositorio]
cd sistema-tarefas-domesticas
```

2. **Estrutura de pastas:**
```
sistema-tarefas-domesticas/
├── README.md
├── main.py
├── package/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pessoa.py
│   │   ├── morador.py
│   │   ├── atividade_domestica.py
│   │   ├── residencia.py
│   │   └── enums.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── gerenciador_tarefas.py
│   │   └── armazenamento_dados.py
│   ├── mixins/
│   │   ├── __init__.py
│   │   └── gerar_relatorios.py
│   └── views/
│       ├── __init__.py
│       └── interface_visual.py
├── dados/
│   └── sistema_tarefas.json
└── assets/
    └── icones/
```

3. **Execute o sistema:**
```bash
python main.py
```

## 🎯 Funcionalidades Implementadas

### **✅ Core do Sistema:**
- [x] Classes com todos os relacionamentos POO (Herança, Polimorfismo, Mixin, Composição, Associação)
- [x] Persistência em JSON (Serialização de objetos)
- [x] Interface gráfica elegante para desktop
- [x] Sistema completo de gerenciamento de tarefas

### **✅ Interface Visual:**
- [x] Tela principal com abas organizadas
- [x] Lista de tarefas com filtros por categoria
- [x] Formulários para criar tarefas e moradores
- [x] Dashboard com estatísticas e ranking
- [x] Design moderno e responsivo

### **✅ Funcionalidades de Negócio:**
- [x] Cadastro de moradores com sistema de pontos
- [x] Criação de tarefas por categoria
- [x] Atribuição automática e manual de responsáveis
- [x] Sistema de status (Pendente, Finalizada, Cancelada)
- [x] Relatórios de desempenho e ranking
- [x] Backup automático dos dados

## 🏗️ Arquitetura

O sistema segue o padrão **MVC** com aplicação rigorosa dos conceitos de **POO**:

### **Model (package/models/):**
- Pessoa (Classe abstrata)
- Morador (Herança + Polimorfismo)
- AtividadeDomestica (Entidade principal)
- Residencia (Composição forte)
- Enums (CategoriaAtividade, SituacaoTarefa)

### **Controller (package/controllers/):**
- GerenciadorTarefas (Classe controladora + Mixin)
- ArmazenamentoDados (Persistência JSON)

### **View (package/views/):**
- InterfaceVisual (Interface gráfica Tkinter)

### **Mixin (package/mixins/):**
- GerarRelatorios (Funcionalidades extras de relatórios)

## 📊 Banco de Dados (JSON)

O sistema utiliza serialização JSON para persistir os dados:

```json
{
  "residencia": {
    "nome_casa": "Casa da Família Silva",
    "moradores": [...]
  },
  "atividades": [
    {
      "id_atividade": "ativ_001",
      "categoria": "LIMPEZA",
      "nome_tarefa": "Varrer a sala",
      "situacao": "PENDENTE",
      "responsavel_id": "morador_001"
    }
  ]
}
```

## 🎮 Como Usar

1. **Inicie o sistema** executando `main.py`
2. **Cadastre moradores** na aba "Moradores"
3. **Crie tarefas** clicando em "Nova Tarefa"
4. **Gerencie status** das tarefas na lista principal
5. **Consulte relatórios** na aba "Relatórios"
6. **Dados são salvos automaticamente**

## 🏆 Conceitos POO Aplicados

- ✅ **Herança:** Pessoa → Morador
- ✅ **Polimorfismo:** `obter_informacoes()`
- ✅ **Mixin:** GerarRelatorios
- ✅ **Composição:** Residencia ♦ Morador
- ✅ **Associação:** AtividadeDomestica ↔ Morador
- ✅ **Encapsulamento:** Todas as classes

## 🚀 Tecnologias

- **Python 3.8+**
- **Tkinter** (Interface gráfica)
- **JSON** (Persistência de dados)
- **Datetime** (Manipulação de datas)
- **Enum** (Enumerações)

## 📝 Notas do Desenvolvedor

Este sistema foi desenvolvido como projeto acadêmico aplicando rigorosamente os conceitos de Programação Orientada a Objetos. Todas as funcionalidades são executadas localmente, sem necessidade de servidor web.

O foco foi criar uma aplicação desktop elegante, funcional e que demonstre domínio dos princípios de POO através de um caso de uso real e prático.

---
**Desenvolvido com ❤️ para organizar as tarefas de casa!** 🏡✨
