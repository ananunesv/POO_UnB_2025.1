#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe Residencia
=================

Implementa a classe Residencia que demonstra COMPOSIÇÃO FORTE com Morador.
Esta é a entidade principal que agrega moradores da casa.
"""

from datetime import datetime
from typing import List, Optional
import uuid
from .morador import Morador


class Residencia:
    """
    Classe que representa uma residência no sistema.
    
    Esta classe demonstra COMPOSIÇÃO FORTE com Morador - quando a residência
    é destruída, os moradores também são removidos do contexto.
    
    Demonstra os conceitos de:
    - COMPOSIÇÃO: Relação forte com Morador (todo-parte)
    - ENCAPSULAMENTO: Controle de acesso aos moradores
    - AGREGAÇÃO: Gerencia coleção de moradores
    
    Attributes:
        _id (str): Identificador único da residência
        _nome_casa (str): Nome/apelido da casa
        _moradores (List[Morador]): Lista de moradores da casa
        _data_criacao (datetime): Data de criação da residência
    """
    
    def __init__(self, nome_casa: str):
        """
        Inicializa uma nova residência.
        
        Args:
            nome_casa (str): Nome ou apelido da casa
            
        Raises:
            ValueError: Se o nome da casa for inválido
        """
        self._validar_nome_casa(nome_casa)
        
        self._id = self._gerar_id()
        self._nome_casa = nome_casa.strip()
        self._moradores = []  # Composição: lista de moradores pertence à residência
        self._data_criacao = datetime.now()
    
    @property
    def id(self) -> str:
        """Retorna o ID único da residência."""
        return self._id
    
    @property
    def nome_casa(self) -> str:
        """Retorna o nome da casa."""
        return self._nome_casa
    
    @nome_casa.setter
    def nome_casa(self, novo_nome: str):
        """
        Define um novo nome para a casa.
        
        Args:
            novo_nome (str): Novo nome da casa
            
        Raises:
            ValueError: Se o nome for inválido
        """
        self._validar_nome_casa(novo_nome)
        self._nome_casa = novo_nome.strip()
    
    @property
    def data_criacao(self) -> datetime:
        """Retorna a data de criação da residência."""
        return self._data_criacao
    
    @property
    def total_moradores(self) -> int:
        """Retorna o total de moradores na casa."""
        return len(self._moradores)
    
    @property
    def moradores_disponiveis(self) -> List[Morador]:
        """Retorna lista de moradores disponíveis para tarefas."""
        return [morador for morador in self._moradores if morador.disponivel]
    
    @property
    def moradores_indisponiveis(self) -> List[Morador]:
        """Retorna lista de moradores indisponíveis."""
        return [morador for morador in self._moradores if not morador.disponivel]
    
    def adicionar_morador(self, morador: Morador) -> bool:
        """
        Adiciona um morador à residência.
        
        Demonstra COMPOSIÇÃO - o morador passa a fazer parte da residência.
        
        Args:
            morador (Morador): Morador a ser adicionado
            
        Returns:
            bool: True se adicionado com sucesso, False caso contrário
            
        Raises:
            ValueError: Se o parâmetro for inválido
        """
        if not isinstance(morador, Morador):
            raise ValueError("Deve ser uma instância de Morador")
        
        # Verificar se o morador já existe (por ID)
        if self.obter_morador_por_id(morador.id):
            return False  # Morador já existe
        
        # Verificar se já existe morador com o mesmo nome
        if self.obter_morador_por_nome(morador.nome):
            return False  # Já existe morador com este nome
        
        self._moradores.append(morador)
        return True
    
    def remover_morador(self, morador_id: str) -> bool:
        """
        Remove um morador da residência.
        
        Args:
            morador_id (str): ID do morador a ser removido
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        morador = self.obter_morador_por_id(morador_id)
        if morador:
            self._moradores.remove(morador)
            return True
        return False
    
    def obter_morador_por_id(self, morador_id: str) -> Optional[Morador]:
        """
        Obtém um morador pelo ID.
        
        Args:
            morador_id (str): ID do morador
            
        Returns:
            Optional[Morador]: Morador encontrado ou None
        """
        for morador in self._moradores:
            if morador.id == morador_id:
                return morador
        return None
    
    def obter_morador_por_nome(self, nome: str) -> Optional[Morador]:
        """
        Obtém um morador pelo nome.
        
        Args:
            nome (str): Nome do morador
            
        Returns:
            Optional[Morador]: Morador encontrado ou None
        """
        nome_limpo = nome.strip().lower()
        for morador in self._moradores:
            if morador.nome.lower() == nome_limpo:
                return morador
        return None
    
    def listar_moradores(self) -> List[Morador]:
        """
        Retorna uma cópia da lista de moradores.
        
        Returns:
            List[Morador]: Lista com todos os moradores
        """
        return self._moradores.copy()
    
    def listar_moradores_ordenados_por_pontos(self, decrescente: bool = True) -> List[Morador]:
        """
        Retorna moradores ordenados por pontuação.
        
        Args:
            decrescente (bool): Se True, ordena do maior para o menor
            
        Returns:
            List[Morador]: Lista ordenada de moradores
        """
        return sorted(self._moradores, 
                     key=lambda m: m.pontos_realizadas, 
                     reverse=decrescente)
    
    def obter_ranking_moradores(self) -> List[dict]:
        """
        Obtém ranking dos moradores com posição.
        
        Returns:
            List[dict]: Lista com ranking dos moradores
        """
        moradores_ordenados = self.listar_moradores_ordenados_por_pontos()
        ranking = []
        
        for posicao, morador in enumerate(moradores_ordenados, 1):
            emoji_posicao = self._obter_emoji_posicao(posicao)
            ranking.append({
                'posicao': posicao,
                'emoji': emoji_posicao,
                'morador': morador,
                'nome': morador.nome,
                'pontos': morador.pontos_realizadas,
                'tarefas': morador.total_tarefas_realizadas,
                'nivel': morador.nivel_performance
            })
        
        return ranking
    
    def obter_estatisticas_gerais(self) -> dict:
        """
        Obtém estatísticas gerais da residência.
        
        Returns:
            dict: Estatísticas da residência
        """
        if not self._moradores:
            return {
                'total_moradores': 0,
                'total_pontos': 0,
                'media_pontos': 0,
                'total_tarefas': 0,
                'moradores_ativos': 0,
                'moradores_disponiveis': 0
            }
        
        total_pontos = sum(m.pontos_realizadas for m in self._moradores)
        total_tarefas = sum(m.total_tarefas_realizadas for m in self._moradores)
        moradores_ativos = len([m for m in self._moradores if m.pontos_realizadas > 0])
        moradores_disponiveis = len(self.moradores_disponiveis)
        
        return {
            'total_moradores': self.total_moradores,
            'total_pontos': total_pontos,
            'media_pontos': round(total_pontos / self.total_moradores, 1),
            'total_tarefas': total_tarefas,
            'moradores_ativos': moradores_ativos,
            'moradores_disponiveis': moradores_disponiveis,
            'moradores_indisponiveis': self.total_moradores - moradores_disponiveis
        }
    
    def resetar_pontos_todos_moradores(self):
        """
        Reseta os pontos de todos os moradores (início de novo período).
        """
        for morador in self._moradores:
            morador.resetar_pontos()
    
    def definir_disponibilidade_todos(self, disponivel: bool):
        """
        Define a disponibilidade de todos os moradores.
        
        Args:
            disponivel (bool): Nova disponibilidade para todos
        """
        for morador in self._moradores:
            morador.disponivel = disponivel
    
    def _validar_nome_casa(self, nome: str):
        """
        Valida o nome da casa.
        
        Args:
            nome (str): Nome a ser validado
            
        Raises:
            ValueError: Se o nome for inválido
        """
        if not nome or not isinstance(nome, str):
            raise ValueError("Nome da casa deve ser uma string não vazia")
        
        nome_limpo = nome.strip()
        if len(nome_limpo) < 2:
            raise ValueError("Nome da casa deve ter pelo menos 2 caracteres")
        
        if len(nome_limpo) > 50:
            raise ValueError("Nome da casa deve ter no máximo 50 caracteres")
    
    def _gerar_id(self) -> str:
        """
        Gera um ID único para a residência.
        
        Returns:
            str: ID único no formato 'casa_xxxxxxxx'
        """
        return f"casa_{uuid.uuid4().hex[:8]}"
    
    def _obter_emoji_posicao(self, posicao: int) -> str:
        """
        Obtém emoji correspondente à posição no ranking.
        
        Args:
            posicao (int): Posição no ranking
            
        Returns:
            str: Emoji correspondente
        """
        emojis = {
            1: "🥇",  # Ouro
            2: "🥈",  # Prata
            3: "🥉",  # Bronze
        }
        return emojis.get(posicao, f"{posicao}º")
    
    def to_dict(self) -> dict:
        """
        Converte a residência para dicionário (para serialização JSON).
        
        Returns:
            dict: Dados da residência em formato dicionário
        """
        return {
            'id': self._id,
            'nome_casa': self._nome_casa,
            'data_criacao': self._data_criacao.isoformat(),
            'moradores': [morador.to_dict() for morador in self._moradores]
        }
    
    @classmethod
    def from_dict(cls, dados: dict):
        """
        Cria uma instância de Residencia a partir de um dicionário.
        
        Args:
            dados (dict): Dicionário com dados da residência
            
        Returns:
            Residencia: Nova instância da residência
        """
        residencia = cls(dados['nome_casa'])
        
        # Restaurar ID original
        residencia._id = dados['id']
        
        # Restaurar data de criação
        residencia._data_criacao = datetime.fromisoformat(dados['data_criacao'])
        
        # Restaurar moradores
        for dados_morador in dados.get('moradores', []):
            morador = Morador.from_dict(dados_morador)
            residencia._moradores.append(morador)
        
        return residencia
    
    def __str__(self) -> str:
        """
        Representação string da residência.
        
        Returns:
            str: Nome da casa com total de moradores
        """
        return f"{self._nome_casa} ({self.total_moradores} moradores)"
    
    def __repr__(self) -> str:
        """
        Representação técnica da residência.
        
        Returns:
            str: Representação técnica detalhada
        """
        return (f"Residencia(id='{self._id}', nome='{self._nome_casa}', "
                f"moradores={self.total_moradores})")
    
    def __len__(self) -> int:
        """
        Retorna o número de moradores na residência.
        
        Returns:
            int: Número de moradores
        """
        return len(self._moradores)
    
    def __contains__(self, item) -> bool:
        """
        Verifica se um morador está na residência.
        
        Args:
            item: Morador ou ID do morador
            
        Returns:
            bool: True se o morador estiver na residência
        """
        if isinstance(item, Morador):
            return item in self._moradores
        elif isinstance(item, str):
            return self.obter_morador_por_id(item) is not None
        return False
    
    def __iter__(self):
        """
        Permite iteração sobre os moradores.
        
        Returns:
            Iterator: Iterador dos moradores
        """
        return iter(self._moradores)