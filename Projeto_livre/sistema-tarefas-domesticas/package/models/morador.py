#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe Morador
==============

Implementa a classe Morador que herda de Pessoa.
Demonstra HERANÇA e POLIMORFISMO em POO.
"""

from datetime import datetime
from .pessoa import Pessoa


class Morador(Pessoa):
    """
    Classe que representa um morador da casa.
    
    Herda de Pessoa e adiciona funcionalidades específicas para moradores,
    como sistema de pontuação por tarefas realizadas e controle de disponibilidade.
    
    Demonstra os conceitos de:
    - HERANÇA: Herda atributos e métodos de Pessoa
    - POLIMORFISMO: Implementa obter_informacoes() de forma específica
    - ENCAPSULAMENTO: Atributos privados com controle de acesso
    
    Attributes:
        _pontos_realizadas (int): Pontos acumulados por tarefas finalizadas
        _disponivel (bool): Se o morador está disponível para novas tarefas
        _historico_tarefas (list): Lista de IDs das tarefas realizadas
        _nivel_performance (str): Nível baseado na pontuação
    """
    
    def __init__(self, nome: str):
        """
        Inicializa um novo morador.
        
        Args:
            nome (str): Nome do morador
        """
        super().__init__(nome)
        self._pontos_realizadas = 0
        self._disponivel = True
        self._historico_tarefas = []
        self._nivel_performance = self._calcular_nivel()
    
    @property
    def pontos_realizadas(self) -> int:
        """Retorna os pontos acumulados pelo morador."""
        return self._pontos_realizadas
    
    @property
    def disponivel(self) -> bool:
        """Retorna se o morador está disponível."""
        return self._disponivel
    
    @disponivel.setter
    def disponivel(self, valor: bool):
        """
        Define a disponibilidade do morador.
        
        Args:
            valor (bool): Nova disponibilidade
        """
        if not isinstance(valor, bool):
            raise ValueError("Disponibilidade deve ser True ou False")
        self._disponivel = valor
    
    @property
    def nivel_performance(self) -> str:
        """Retorna o nível de performance atual."""
        return self._nivel_performance
    
    @property
    def total_tarefas_realizadas(self) -> int:
        """Retorna o total de tarefas realizadas."""
        return len(self._historico_tarefas)
    
    def finalizar_tarefa(self, tarefa_id: str, pontos: int = 10):
        """
        Registra a finalização de uma tarefa e adiciona pontos.
        
        Args:
            tarefa_id (str): ID da tarefa finalizada
            pontos (int): Pontos a serem adicionados (padrão: 10)
        """
        if not isinstance(pontos, int) or pontos < 0:
            raise ValueError("Pontos devem ser um número inteiro positivo")
        
        if tarefa_id not in self._historico_tarefas:
            self._historico_tarefas.append(tarefa_id)
            self._pontos_realizadas += pontos
            self._nivel_performance = self._calcular_nivel()
    
    def calcular_desempenho(self) -> dict:
        """
        Calcula estatísticas de desempenho do morador.
        
        Returns:
            dict: Dicionário com estatísticas de desempenho
        """
        tempo_cadastrado_dias = (datetime.now() - self.data_cadastro).days
        if tempo_cadastrado_dias == 0:
            tempo_cadastrado_dias = 1  # Evitar divisão por zero
        
        tarefas_por_dia = self.total_tarefas_realizadas / tempo_cadastrado_dias
        pontos_por_tarefa = (self._pontos_realizadas / self.total_tarefas_realizadas 
                           if self.total_tarefas_realizadas > 0 else 0)
        
        return {
            'total_pontos': self._pontos_realizadas,
            'total_tarefas': self.total_tarefas_realizadas,
            'tarefas_por_dia': round(tarefas_por_dia, 2),
            'pontos_por_tarefa': round(pontos_por_tarefa, 1),
            'nivel': self._nivel_performance,
            'tempo_cadastrado_dias': tempo_cadastrado_dias,
            'disponivel': self._disponivel
        }
    
    def definir_disponibilidade(self, disponivel: bool, motivo: str = ""):
        """
        Define a disponibilidade do morador com motivo opcional.
        
        Args:
            disponivel (bool): Nova disponibilidade
            motivo (str): Motivo da mudança (opcional)
        """
        self._disponivel = disponivel
        # Aqui poderíamos registrar o motivo em um log se necessário
    
    def _calcular_nivel(self) -> str:
        """
        Calcula o nível de performance baseado nos pontos.
        
        Returns:
            str: Nível de performance
        """
        if self._pontos_realizadas >= 100:
            return "🏆 Expert"
        elif self._pontos_realizadas >= 50:
            return "⭐ Avançado"
        elif self._pontos_realizadas >= 20:
            return "📈 Intermediário"
        elif self._pontos_realizadas >= 5:
            return "🌱 Iniciante"
        else:
            return "🆕 Novato"
    
    def obter_informacoes(self) -> str:
        """
        Implementação específica do método abstrato de Pessoa.
        
        Demonstra POLIMORFISMO - mesmo método, comportamento específico.
        
        Returns:
            str: Informações detalhadas do morador
        """
        status_disponibilidade = "Disponível" if self._disponivel else "Indisponível"
        
        return (f"👤 {self.nome}\n"
                f"🏆 Pontos: {self._pontos_realizadas}\n"
                f"📋 Tarefas realizadas: {self.total_tarefas_realizadas}\n"
                f"⭐ Nível: {self._nivel_performance}\n"
                f"✅ Status: {status_disponibilidade}\n"
                f"📅 Cadastrado há: {self.tempo_cadastrado()}")
    
    def resetar_pontos(self):
        """
        Reseta os pontos do morador (para início de novo período).
        Mantém o histórico de tarefas.
        """
        self._pontos_realizadas = 0
        self._nivel_performance = self._calcular_nivel()
    
    def obter_historico_resumido(self, limite: int = 5) -> list:
        """
        Obtém as últimas tarefas realizadas.
        
        Args:
            limite (int): Número máximo de tarefas a retornar
            
        Returns:
            list: Lista com os IDs das últimas tarefas
        """
        return self._historico_tarefas[-limite:] if self._historico_tarefas else []
    
    def to_dict(self) -> dict:
        """
        Converte o morador para dicionário (para serialização JSON).
        
        Returns:
            dict: Dados do morador em formato dicionário
        """
        dados_base = super().to_dict()
        dados_base.update({
            'pontos_realizadas': self._pontos_realizadas,
            'disponivel': self._disponivel,
            'historico_tarefas': self._historico_tarefas.copy(),
            'nivel_performance': self._nivel_performance
        })
        return dados_base
    
    @classmethod
    def from_dict(cls, dados: dict):
        """
        Cria uma instância de Morador a partir de um dicionário.
        
        Args:
            dados (dict): Dicionário com dados do morador
            
        Returns:
            Morador: Nova instância do morador
        """
        morador = cls(dados['nome'])
        
        # Restaurar ID original se fornecido
        if 'id' in dados:
            morador._id = dados['id']
        
        # Restaurar data de cadastro se fornecida
        if 'data_cadastro' in dados:
            morador._data_cadastro = datetime.fromisoformat(dados['data_cadastro'])
        
        # Restaurar atributos específicos do morador
        morador._pontos_realizadas = dados.get('pontos_realizadas', 0)
        morador._disponivel = dados.get('disponivel', True)
        morador._historico_tarefas = dados.get('historico_tarefas', [])
        morador._nivel_performance = dados.get('nivel_performance', morador._calcular_nivel())
        
        return morador
    
    def __str__(self) -> str:
        """
        Representação string do morador.
        
        Returns:
            str: Nome e pontos do morador
        """
        return f"{self.nome} ({self._pontos_realizadas} pts)"
    
    def __repr__(self) -> str:
        """
        Representação técnica do morador.
        
        Returns:
            str: Representação técnica detalhada
        """
        return (f"Morador(id='{self.id}', nome='{self.nome}', "
                f"pontos={self._pontos_realizadas}, disponivel={self._disponivel})")
    
    def __lt__(self, other):
        """
        Comparação para ordenação por pontos (menor que).
        
        Args:
            other (Morador): Outro morador para comparação
            
        Returns:
            bool: True se este morador tem menos pontos
        """
        if not isinstance(other, Morador):
            return NotImplemented
        return self._pontos_realizadas < other._pontos_realizadas
    
    def __gt__(self, other):
        """
        Comparação para ordenação por pontos (maior que).
        
        Args:
            other (Morador): Outro morador para comparação
            
        Returns:
            bool: True se este morador tem mais pontos
        """
        if not isinstance(other, Morador):
            return NotImplemented
        return self._pontos_realizadas > other._pontos_realizadas