#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe Abstrata Pessoa
======================

Define a classe base abstrata para representar pessoas no sistema.
Demonstra o conceito de HERANÇA e POLIMORFISMO em POO.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import uuid


class Pessoa(ABC):
    """
    Classe abstrata que define a estrutura básica para pessoas no sistema.
    
    Esta classe implementa os conceitos de:
    - ENCAPSULAMENTO: Atributos privados com getters/setters
    - ABSTRAÇÃO: Classe abstrata com método abstrato
    - POLIMORFISMO: Método obter_informacoes() implementado diferentemente nas filhas
    
    Attributes:
        _nome (str): Nome da pessoa
        _data_cadastro (datetime): Data e hora do cadastro
        _id (str): Identificador único da pessoa
    """
    
    def __init__(self, nome: str):
        """
        Inicializa uma nova pessoa.
        
        Args:
            nome (str): Nome da pessoa
            
        Raises:
            ValueError: Se o nome estiver vazio ou inválido
        """
        self._validar_nome(nome)
        self._id = self._gerar_id()
        self._nome = nome.strip().title()
        self._data_cadastro = datetime.now()
    
    @property
    def id(self) -> str:
        """Retorna o ID único da pessoa."""
        return self._id
    
    @property
    def nome(self) -> str:
        """Retorna o nome da pessoa."""
        return self._nome
    
    @nome.setter
    def nome(self, novo_nome: str):
        """
        Define um novo nome para a pessoa.
        
        Args:
            novo_nome (str): Novo nome para a pessoa
            
        Raises:
            ValueError: Se o nome for inválido
        """
        self._validar_nome(novo_nome)
        self._nome = novo_nome.strip().title()
    
    @property
    def data_cadastro(self) -> datetime:
        """Retorna a data de cadastro da pessoa."""
        return self._data_cadastro
    
    def _validar_nome(self, nome: str):
        """
        Valida se o nome informado é válido.
        
        Args:
            nome (str): Nome a ser validado
            
        Raises:
            ValueError: Se o nome for inválido
        """
        if not nome or not isinstance(nome, str):
            raise ValueError("Nome deve ser uma string não vazia")
        
        nome_limpo = nome.strip()
        if len(nome_limpo) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        
        if len(nome_limpo) > 50:
            raise ValueError("Nome deve ter no máximo 50 caracteres")
        
        # Verificar se contém apenas letras e espaços
        if not all(c.isalpha() or c.isspace() for c in nome_limpo):
            raise ValueError("Nome deve conter apenas letras e espaços")
    
    def _gerar_id(self) -> str:
        """
        Gera um ID único para a pessoa.
        
        Returns:
            str: ID único no formato 'pessoa_xxxxxxxx'
        """
        return f"pessoa_{uuid.uuid4().hex[:8]}"
    
    @abstractmethod
    def obter_informacoes(self) -> str:
        """
        Método abstrato que deve ser implementado pelas classes filhas.
        
        Este método demonstra POLIMORFISMO - cada classe filha implementará
        de forma diferente, retornando informações específicas do tipo de pessoa.
        
        Returns:
            str: Informações formatadas da pessoa
        """
        pass
    
    def tempo_cadastrado(self) -> str:
        """
        Calcula há quanto tempo a pessoa está cadastrada.
        
        Returns:
            str: Tempo formatado (ex: "5 dias", "2 horas")
        """
        agora = datetime.now()
        diferenca = agora - self._data_cadastro
        
        if diferenca.days > 0:
            return f"{diferenca.days} dia(s)"
        elif diferenca.seconds > 3600:
            horas = diferenca.seconds // 3600
            return f"{horas} hora(s)"
        elif diferenca.seconds > 60:
            minutos = diferenca.seconds // 60
            return f"{minutos} minuto(s)"
        else:
            return "Poucos segundos"
    
    def to_dict(self) -> dict:
        """
        Converte a pessoa para dicionário (para serialização JSON).
        
        Returns:
            dict: Dados da pessoa em formato dicionário
        """
        return {
            'id': self._id,
            'nome': self._nome,
            'data_cadastro': self._data_cadastro.isoformat(),
            'tipo': self.__class__.__name__
        }
    
    @classmethod
    def from_dict(cls, dados: dict):
        """
        Cria uma instância de Pessoa a partir de um dicionário.
        
        Este método é usado na deserialização dos dados JSON.
        
        Args:
            dados (dict): Dicionário com dados da pessoa
            
        Returns:
            Pessoa: Instância da pessoa (classe específica)
            
        Note:
            Este método deve ser sobrescrito nas classes filhas para
            criar instâncias do tipo correto.
        """
        # Este método será sobrescrito nas classes filhas
        raise NotImplementedError("Método deve ser implementado nas classes filhas")
    
    def __str__(self) -> str:
        """
        Representação string da pessoa.
        
        Returns:
            str: Nome da pessoa
        """
        return self._nome
    
    def __repr__(self) -> str:
        """
        Representação técnica da pessoa.
        
        Returns:
            str: Representação técnica com classe e ID
        """
        return f"{self.__class__.__name__}(id='{self._id}', nome='{self._nome}')"
    
    def __eq__(self, other) -> bool:
        """
        Compara duas pessoas pela igualdade.
        
        Args:
            other: Outra pessoa para comparação
            
        Returns:
            bool: True se forem a mesma pessoa (mesmo ID)
        """
        if not isinstance(other, Pessoa):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        """
        Retorna hash da pessoa (baseado no ID).
        
        Returns:
            int: Hash da pessoa
        """
        return hash(self._id)