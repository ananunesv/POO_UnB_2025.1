#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enumerações do Sistema de Tarefas Domésticas
============================================

Define as enumerações utilizadas no sistema para categorias de atividades
e situações das tarefas.
"""

from enum import Enum


class CategoriaAtividade(Enum):
    """
    Enumeração que define as categorias possíveis para as atividades domésticas.
    
    Cada categoria representa um tipo específico de tarefa da casa:
    - COZINHA: Tarefas relacionadas à cozinha (lavar louça, limpar fogão, etc.)
    - LIMPEZA: Tarefas de limpeza geral (varrer, passar pano, aspirar, etc.)
    - JARDIM: Cuidados com plantas e área externa (regar, podar, varrer quintal)
    - ROUPAS: Cuidados com vestuário (lavar, passar, dobrar, guardar)
    - MANUTENCAO: Pequenos reparos e manutenção da casa
    """
    
    COZINHA = "🍽️ Cozinha"
    LIMPEZA = "🧹 Limpeza"
    JARDIM = "🌱 Jardim"
    ROUPAS = "🧺 Roupas"
    MANUTENCAO = "🔧 Manutenção"
    
    def __str__(self):
        """Retorna representação string da categoria."""
        return self.value
    
    @classmethod
    def obter_categorias(cls):
        """
        Retorna lista com todas as categorias disponíveis.
        
        Returns:
            list: Lista de strings com nomes das categorias
        """
        return [categoria.value for categoria in cls]
    
    @classmethod
    def obter_por_nome(cls, nome):
        """
        Obtém categoria pelo nome.
        
        Args:
            nome (str): Nome da categoria
            
        Returns:
            CategoriaAtividade: Categoria correspondente ou None
        """
        for categoria in cls:
            if categoria.value == nome or categoria.name == nome:
                return categoria
        return None


class SituacaoTarefa(Enum):
    """
    Enumeração que define as situações possíveis para uma tarefa.
    
    Estados do ciclo de vida de uma tarefa:
    - PENDENTE: Tarefa criada mas ainda não realizada
    - FINALIZADA: Tarefa completada com sucesso
    - CANCELADA: Tarefa cancelada (não será realizada)
    """
    
    PENDENTE = "⏳ Pendente"
    FINALIZADA = "✅ Finalizada"
    CANCELADA = "❌ Cancelada"
    
    def __str__(self):
        """Retorna representação string da situação."""
        return self.value
    
    @classmethod
    def obter_situacoes(cls):
        """
        Retorna lista com todas as situações disponíveis.
        
        Returns:
            list: Lista de strings com nomes das situações
        """
        return [situacao.value for situacao in cls]
    
    @classmethod
    def obter_por_nome(cls, nome):
        """
        Obtém situação pelo nome.
        
        Args:
            nome (str): Nome da situação
            
        Returns:
            SituacaoTarefa: Situação correspondente ou None
        """
        for situacao in cls:
            if situacao.value == nome or situacao.name == nome:
                return situacao
        return None
    
    def cor_interface(self):
        """
        Retorna cor apropriada para exibição na interface.
        
        Returns:
            str: Código da cor em hexadecimal
        """
        cores = {
            self.PENDENTE: "#FFA726",    # Laranja
            self.FINALIZADA: "#66BB6A",  # Verde
            self.CANCELADA: "#EF5350"    # Vermelho
        }
        return cores.get(self, "#757575")  # Cinza padrão


# Constantes auxiliares para facilitar o uso
TODAS_CATEGORIAS = CategoriaAtividade.obter_categorias()
TODAS_SITUACOES = SituacaoTarefa.obter_situacoes()

# Mapeamento de emojis por categoria (para interface)
EMOJIS_CATEGORIA = {
    CategoriaAtividade.COZINHA: "🍽️",
    CategoriaAtividade.LIMPEZA: "🧹",
    CategoriaAtividade.JARDIM: "🌱",
    CategoriaAtividade.ROUPAS: "🧺",
    CategoriaAtividade.MANUTENCAO: "🔧"
}

# Mapeamento de emojis por situação (para interface)
EMOJIS_SITUACAO = {
    SituacaoTarefa.PENDENTE: "⏳",
    SituacaoTarefa.FINALIZADA: "✅", 
    SituacaoTarefa.CANCELADA: "❌"
}


def obter_emoji_categoria(categoria):
    """
    Obtém emoji correspondente à categoria.
    
    Args:
        categoria (CategoriaAtividade): Categoria da atividade
        
    Returns:
        str: Emoji correspondente
    """
    return EMOJIS_CATEGORIA.get(categoria, "📝")


def obter_emoji_situacao(situacao):
    """
    Obtém emoji correspondente à situação.
    
    Args:
        situacao (SituacaoTarefa): Situação da tarefa
        
    Returns:
        str: Emoji correspondente
    """
    return EMOJIS_SITUACAO.get(situacao, "📋")