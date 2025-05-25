# Sistema de Controle de Tarefas Domésticas

**Universidade de Brasília - UnB**  
**Disciplina:** Programação Orientada a Objetos  
**Desenvolvido por:** Ana Luisa  

## 📋 Visão Geral

Sistema desktop para gerenciar tarefas domésticas entre moradores de uma residência. O projeto demonstra a aplicação prática dos conceitos fundamentais de POO através de um problema real: organizar quem faz o quê em casa e reconhecer quem mais contribui.

### O que o sistema faz:
- Cadastra moradores e tarefas domésticas
- Atribui responsáveis e acompanha conclusões
- Calcula pontos por tarefa realizada
- Gera ranking e relatórios de desempenho
- Salva tudo automaticamente em arquivo JSON

## 🎯 Conceitos de POO Aplicados

O projeto implementa todos os pilares da orientação a objetos:

1. **Herança**: `Pessoa` (abstrata) → `Morador`
2. **Polimorfismo**: Método `obter_informacoes()` com comportamentos diferentes
3. **Encapsulamento**: Atributos privados (`_nome`) com getters/setters
4. **Abstração**: Classe abstrata `Pessoa` define contrato
5. **Composição**: `Residencia` contém lista de `Moradores`
6. **Mixin**: `GerarRelatorios` adiciona funcionalidades extras

## 📖 Casos de Uso

### UC01 - Gerenciar Moradores

**Descrição:** Permite cadastrar, editar e excluir moradores da casa.

**Fluxo Principal:**
1. Usuário acessa aba "Moradores"
2. Sistema mostra lista com ranking, pontos e status
3. Usuário escolhe ação:
   - **Novo**: Informa nome (2-50 caracteres, só letras)
   - **Editar**: Altera nome ou disponibilidade
   - **Excluir**: Remove após confirmação
4. Sistema valida, executa e salva automaticamente

**Validações:**
- Nome único por residência
- Apenas letras e espaços permitidos
- Ao excluir, tarefas pendentes ficam sem responsável

---

### UC02 - Criar e Gerenciar Tarefas

**Descrição:** Controla o ciclo completo das tarefas domésticas.

**Fluxo Principal:**
1. Usuário clica em "Nova Atividade"
2. Sistema abre formulário com:
   - **Categoria** (define pontos):
     - 🍽️ Cozinha: 15 pontos
     - 🧹 Limpeza: 10 pontos  
     - 🌱 Jardim: 12 pontos
     - 🧺 Roupas: 8 pontos
     - 🔧 Manutenção: 20 pontos
   - **Nome da tarefa** (mínimo 3 caracteres)
   - **Descrição** (opcional)
   - **Responsável** (opcional)
3. Sistema cria com status "Pendente"
4. Usuário gerencia tarefas:
   - **Finalizar**: Adiciona pontos ao responsável
   - **Cancelar**: Não gera pontos
   - **Excluir**: Remove permanentemente

**Estados das Tarefas:**
- ⏳ Pendente (amarelo)
- ✅ Finalizada (verde)  
- ❌ Cancelada (vermelho)

---

### UC03 - Visualizar Dashboard

**Descrição:** Tela inicial com resumo do sistema.

**O que mostra:**
- Cards com estatísticas:
  - Total de moradores
  - Total de tarefas
  - Tarefas pendentes
  - Tarefas finalizadas
- Lista das 10 atividades mais recentes
- Botão para atualizar dados

---

### UC04 - Gerar Relatórios

**Descrição:** Três tipos de análises disponíveis.

**Tipos de Relatório:**

1. **🏆 Ranking**: 
   - Lista ordenada por pontos
   - Medalhas para top 3
   - Mostra nível e total de tarefas

2. **📊 Por Categoria**:
   - Total de tarefas por tipo
   - Taxa de conclusão
   - Pontuação média

3. **📈 Performance Individual**:
   - Análise detalhada por morador
   - Tempo de cadastro
   - Categorias favoritas

---

### UC05 - Persistência Automática

**Descrição:** Sistema salva dados automaticamente.

**Como funciona:**
1. Ao iniciar, carrega dados do JSON
2. A cada mudança, cria backup e salva
3. Se houver erro, restaura do backup
4. Estrutura JSON preserva todos os objetos

**Formato dos dados:**
```json
{
  "metadata": {
    "versao": "1.0",
    "data_salvamento": "2025-05-23T12:08:28",
    "sistema": "Tarefas Domésticas"
  },
  "dados": {
    "residencia": { ... },
    "atividades": [ ... ]
  }
}
```

## 🏗️ Arquitetura MVC

O projeto segue o padrão Model-View-Controller:

```
VIEW (interface_visual.py)
    ↓
CONTROLLER (gerenciador_tarefas.py + mixin)
    ↓
MODEL (pessoa, morador, atividade, residencia)
    ↓
PERSISTÊNCIA (armazenamento_dados.py → JSON)
```

### Estrutura de Pastas:
```
sistema-tarefas-domesticas/
├── main.py                 # Ponto de entrada
├── package/
│   ├── models/            # Classes do domínio
│   ├── controllers/       # Lógica de negócio
│   ├── mixins/           # Funcionalidades extras
│   └── views/            # Interface gráfica
└── dados/                # Arquivos JSON
```

## 💻 Como Executar

**Requisitos:** Python 3.8+ (Tkinter já vem incluído)

```bash
# Clone ou baixe o projeto
cd sistema-tarefas-domesticas

# Execute
python main.py
```

## 🎨 Interface do Sistema

A interface foi desenvolvida com Tkinter e possui:

- **Design moderno** com tema de cores consistente
- **4 abas principais**: Dashboard, Atividades, Moradores, Relatórios
- **Diálogos modais** para formulários
- **Feedback visual** com cores e emojis
- **Mensagens de confirmação** para ações críticas

## 📊 Regras de Negócio Principais

1. **Pontuação**: Só é atribuída quando tarefa é finalizada
2. **Nomes únicos**: Não permite moradores com mesmo nome
3. **Status imutável**: Tarefa finalizada não pode ser reaberta
4. **Ranking**: Considera apenas moradores com pontos > 0
5. **Níveis de performance**:
   - 🆕 Novato: 0-4 pontos
   - 🌱 Iniciante: 5-19 pontos
   - 📈 Intermediário: 20-49 pontos
   - ⭐ Avançado: 50-99 pontos
   - 🏆 Expert: 100+ pontos

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Tkinter**: Interface gráfica nativa
- **JSON**: Persistência de dados
- **UUID**: Geração de IDs únicos
- **Datetime**: Controle de datas
- **Enum**: Categorias e estados

## 📝 Considerações Finais

Este projeto demonstra como aplicar POO em um sistema real e funcional. Cada conceito foi implementado com propósito claro:

- **Herança** facilita extensão (podemos criar outros tipos de pessoa)
- **Encapsulamento** protege dados críticos (pontos, IDs)
- **Composição** modela relação natural (casa tem moradores)
- **Mixin** evita repetição de código (relatórios)

O sistema está pronto para uso e pode ser facilmente estendido com novas funcionalidades mantendo os princípios SOLID.

---
**Universidade de Brasília**  
**Projeto POO - 2025/1**
