#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe AtividadeDomestica
========================

Implementa a classe principal que representa uma atividade/tarefa doméstica.
Demonstra ASSOCIAÇÃO com Morador e uso de enumerações.
"""

from datetime import datetime
import uuid
from .enums import CategoriaAtividade, SituacaoTarefa


class AtividadeDomestica:
    """
    Classe que representa uma atividade doméstica no sistema.
    
    Esta classe é o core do negócio, representando as tarefas que precisam
    ser realizadas na casa. Demonstra os conceitos de:
    - ENCAPSULAMENTO: Atributos privados com controle de acesso
    - ASSOCIAÇÃO: Relacionamento com Morador (responsável)
    - USO DE ENUMS: Categoria e situação da tarefa
    
    Attributes:
        _id_atividade (str): Identificador único da atividade
        _categoria (CategoriaAtividade): Categoria da atividade
        _nome_tarefa (str): Nome/título da tarefa
        _descricao (str): Descrição detalhada da tarefa
        _situacao (SituacaoTarefa): Situação atual da tarefa
        _data_criacao (datetime): Data e hora de criação
        _data_finalizacao (datetime): Data e hora de finalização (se aplicável)
        _responsavel_id (str): ID do morador responsável
        _pontos_tarefa (int): Pontos que a tarefa vale
    """
    
    def __init__(self, categoria: CategoriaAtividade, nome_tarefa: str, 
                 descricao: str = "", responsavel_id: str = None):
        """
        Inicializa uma nova atividade doméstica.
        
        Args:
            categoria (CategoriaAtividade): Categoria da atividade
            nome_tarefa (str): Nome da tarefa
            descricao (str): Descrição detalhada (opcional)
            responsavel_id (str): ID do responsável (opcional)
            
        Raises:
            ValueError: Se os parâmetros forem inválidos
        """
        self._validar_parametros(categoria, nome_tarefa)
        
        self._id_atividade = self._gerar_id()
        self._categoria = categoria
        self._nome_tarefa = nome_tarefa.strip()
        self._descricao = descricao.strip() if descricao else ""
        self._situacao = SituacaoTarefa.PENDENTE
        self._data_criacao = datetime.now()
        self._data_finalizacao = None
        self._responsavel_id = responsavel_id
        self._pontos_tarefa = self._calcular_pontos_por_categoria()
    
    @property
    def id_atividade(self) -> str:
        """Retorna o ID único da atividade."""
        return self._id_atividade
    
    @property
    def categoria(self) -> CategoriaAtividade:
        """Retorna a categoria da atividade."""
        return self._categoria
    
    @property
    def nome_tarefa(self) -> str:
        """Retorna o nome da tarefa."""
        return self._nome_tarefa
    
    @nome_tarefa.setter
    def nome_tarefa(self, novo_nome: str):
        """
        Define um novo nome para a tarefa.
        
        Args:
            novo_nome (str): Novo nome da tarefa
            
        Raises:
            ValueError: Se o nome for inválido
        """
        if not novo_nome or not isinstance(novo_nome, str):
            raise ValueError("Nome da tarefa deve ser uma string não vazia")
        
        nome_limpo = novo_nome.strip()
        if len(nome_limpo) < 3:
            raise ValueError("Nome da tarefa deve ter pelo menos 3 caracteres")
        
        self._nome_tarefa = nome_limpo
    
    @property
    def descricao(self) -> str:
        """Retorna a descrição da atividade."""
        return self._descricao
    
    @descricao.setter
    def descricao(self, nova_descricao: str):
        """
        Define uma nova descrição para a atividade.
        
        Args:
            nova_descricao (str): Nova descrição
        """
        self._descricao = nova_descricao.strip() if nova_descricao else ""
    
    @property
    def situacao(self) -> SituacaoTarefa:
        """Retorna a situação atual da tarefa."""
        return self._situacao
    
    @property
    def data_criacao(self) -> datetime:
        """Retorna a data de criação da atividade."""
        return self._data_criacao
    
    @property
    def data_finalizacao(self) -> datetime:
        """Retorna a data de finalização (None se não finalizada)."""
        return self._data_finalizacao
    
    @property
    def responsavel_id(self) -> str:
        """Retorna o ID do responsável pela tarefa."""
        return self._responsavel_id
    
    @responsavel_id.setter
    def responsavel_id(self, novo_responsavel_id: str):
        """
        Define um novo responsável para a tarefa.
        
        Args:
            novo_responsavel_id (str): ID do novo responsável
        """
        self._responsavel_id = novo_responsavel_id
    
    @property
    def pontos_tarefa(self) -> int:
        """Retorna os pontos que a tarefa vale."""
        return self._pontos_tarefa
    
    @property
    def esta_pendente(self) -> bool:
        """Verifica se a tarefa está pendente."""
        return self._situacao == SituacaoTarefa.PENDENTE
    
    @property
    def esta_finalizada(self) -> bool:
        """Verifica se a tarefa está finalizada."""
        return self._situacao == SituacaoTarefa.FINALIZADA
    
    @property
    def esta_cancelada(self) -> bool:
        """Verifica se a tarefa está cancelada."""
        return self._situacao == SituacaoTarefa.CANCELADA
    
    def marcar_finalizada(self) -> bool:
        """
        Marca a tarefa como finalizada.
        
        Returns:
            bool: True se foi possível finalizar, False caso contrário
        """
        if self._situacao == SituacaoTarefa.PENDENTE:
            self._situacao = SituacaoTarefa.FINALIZADA
            self._data_finalizacao = datetime.now()
            return True
        return False
    
    def marcar_cancelada(self) -> bool:
        """
        Marca a tarefa como cancelada.
        
        Returns:
            bool: True se foi possível cancelar, False caso contrário
        """
        if self._situacao == SituacaoTarefa.PENDENTE:
            self._situacao = SituacaoTarefa.CANCELADA
            self._data_finalizacao = datetime.now()
            return True
        return False
    
    def reabrir_tarefa(self) -> bool:
        """
        Reabre uma tarefa finalizada ou cancelada, voltando para pendente.
        
        Returns:
            bool: True se foi possível reabrir, False caso contrário
        """
        if self._situacao in [SituacaoTarefa.FINALIZADA, SituacaoTarefa.CANCELADA]:
            self._situacao = SituacaoTarefa.PENDENTE
            self._data_finalizacao = None
            return True
        return False
    
    def obter_detalhes(self) -> dict:
        """
        Obtém detalhes completos da atividade.
        
        Returns:
            dict: Dicionário com todos os detalhes da atividade
        """
        tempo_criacao = datetime.now() - self._data_criacao
        
        detalhes = {
            'id': self._id_atividade,
            'categoria': self._categoria.value,
            'nome': self._nome_tarefa,
            'descricao': self._descricao,
            'situacao': self._situacao.value,
            'pontos': self._pontos_tarefa,
            'responsavel_id': self._responsavel_id,
            'data_criacao': self._data_criacao.strftime("%d/%m/%Y %H:%M"),
            'tempo_desde_criacao': self._formatar_tempo_decorrido(tempo_criacao),
            'finalizada': self.esta_finalizada,
            'cancelada': self.esta_cancelada,
            'pendente': self.esta_pendente
        }
        
        if self._data_finalizacao:
            detalhes['data_finalizacao'] = self._data_finalizacao.strftime("%d/%m/%Y %H:%M")
            tempo_realizacao = self._data_finalizacao - self._data_criacao
            detalhes['tempo_realizacao'] = self._formatar_tempo_decorrido(tempo_realizacao)
        
        return detalhes
    
    def _validar_parametros(self, categoria, nome_tarefa):
        """
        Valida os parâmetros da atividade.
        
        Args:
            categoria: Categoria da atividade
            nome_tarefa: Nome da tarefa
            
        Raises:
            ValueError: Se algum parâmetro for inválido
        """
        if not isinstance(categoria, CategoriaAtividade):
            raise ValueError("Categoria deve ser uma instância de CategoriaAtividade")
        
        if not nome_tarefa or not isinstance(nome_tarefa, str):
            raise ValueError("Nome da tarefa deve ser uma string não vazia")
        
        if len(nome_tarefa.strip()) < 3:
            raise ValueError("Nome da tarefa deve ter pelo menos 3 caracteres")
    
    def _gerar_id(self) -> str:
        """
        Gera um ID único para a atividade.
        
        Returns:
            str: ID único no formato 'ativ_xxxxxxxx'
        """
        return f"ativ_{uuid.uuid4().hex[:8]}"
    
    def _calcular_pontos_por_categoria(self) -> int:
        """
        Calcula pontos baseado na categoria da atividade.
        
        Returns:
            int: Pontos que a atividade vale
        """
        pontos_categoria = {
            CategoriaAtividade.COZINHA: 15,      # Tarefas de cozinha valem mais
            CategoriaAtividade.LIMPEZA: 10,      # Limpeza padrão
            CategoriaAtividade.JARDIM: 12,       # Jardim vale um pouco mais
            CategoriaAtividade.ROUPAS: 8,        # Roupas valor médio
            CategoriaAtividade.MANUTENCAO: 20    # Manutenção vale mais
        }
        return pontos_categoria.get(self._categoria, 10)
    
    def _formatar_tempo_decorrido(self, tempo_delta) -> str:
        """
        Formata um tempo decorrido em string legível.
        
        Args:
            tempo_delta: Diferença de tempo (timedelta)
            
        Returns:
            str: Tempo formatado
        """
        if tempo_delta.days > 0:
            return f"{tempo_delta.days} dia(s)"
        elif tempo_delta.seconds > 3600:
            horas = tempo_delta.seconds // 3600
            return f"{horas} hora(s)"
        elif tempo_delta.seconds > 60:
            minutos = tempo_delta.seconds // 60
            return f"{minutos} minuto(s)"
        else:
            return "Poucos segundos"
    
    def to_dict(self) -> dict:
        """
        Converte a atividade para dicionário (para serialização JSON).
        
        Returns:
            dict: Dados da atividade em formato dicionário
        """
        return {
            'id_atividade': self._id_atividade,
            'categoria': self._categoria.name,  # Salva o nome do enum
            'nome_tarefa': self._nome_tarefa,
            'descricao': self._descricao,
            'situacao': self._situacao.name,    # Salva o nome do enum
            'data_criacao': self._data_criacao.isoformat(),
            'data_finalizacao': (self._data_finalizacao.isoformat() 
                               if self._data_finalizacao else None),
            'responsavel_id': self._responsavel_id,
            'pontos_tarefa': self._pontos_tarefa
        }
    
    @classmethod
    def from_dict(cls, dados: dict):
        """
        Cria uma instância de AtividadeDomestica a partir de um dicionário.
        
        Args:
            dados (dict): Dicionário com dados da atividade
            
        Returns:
            AtividadeDomestica: Nova instância da atividade
        """
        # Obter enums pelos nomes
        categoria = CategoriaAtividade[dados['categoria']]
        
        # Criar atividade
        atividade = cls(
            categoria=categoria,
            nome_tarefa=dados['nome_tarefa'],
            descricao=dados.get('descricao', ''),
            responsavel_id=dados.get('responsavel_id')
        )
        
        # Restaurar ID original
        atividade._id_atividade = dados['id_atividade']
        
        # Restaurar situação
        atividade._situacao = SituacaoTarefa[dados['situacao']]
        
        # Restaurar datas
        atividade._data_criacao = datetime.fromisoformat(dados['data_criacao'])
        if dados.get('data_finalizacao'):
            atividade._data_finalizacao = datetime.fromisoformat(dados['data_finalizacao'])
        
        # Restaurar pontos (pode ter sido customizado)
        atividade._pontos_tarefa = dados.get('pontos_tarefa', 
                                           atividade._calcular_pontos_por_categoria())
        
        return atividade
    
    def __str__(self) -> str:
        """
        Representação string da atividade.
        
        Returns:
            str: Nome da tarefa com situação
        """
        emoji_situacao = {
            SituacaoTarefa.PENDENTE: "⏳",
            SituacaoTarefa.FINALIZADA: "✅",
            SituacaoTarefa.CANCELADA: "❌"
        }
        emoji = emoji_situacao.get(self._situacao, "📋")
        return f"{emoji} {self._nome_tarefa}"
    
    def __repr__(self) -> str:
        """
        Representação técnica da atividade.
        
        Returns:
            str: Representação técnica detalhada
        """
        return (f"AtividadeDomestica(id='{self._id_atividade}', "
                f"nome='{self._nome_tarefa}', situacao='{self._situacao.name}')")
    
    def __eq__(self, other) -> bool:
        """
        Compara duas atividades pela igualdade.
        
        Args:
            other: Outra atividade para comparação
            
        Returns:
            bool: True se forem a mesma atividade (mesmo ID)
        """
        if not isinstance(other, AtividadeDomestica):
            return False
        return self._id_atividade == other._id_atividade
    
    def __hash__(self) -> int:
        """
        Retorna hash da atividade (baseado no ID).
        
        Returns:
            int: Hash da atividade
        """
        return hash(self._id_atividade)