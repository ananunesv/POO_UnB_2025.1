#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controladores do Sistema
=======================

Classes controladoras que gerenciam a lógica de negócio:
- GerenciadorTarefas (controladora principal + mixin)
- ArmazenamentoDados (persistência em JSON)
"""

# Importar classes controladoras
from .gerenciador_tarefas import GerenciadorTarefas
from .armazenamento_dados import ArmazenamentoDados

# Definir exportações
__all__ = [
    'GerenciadorTarefas',
    'ArmazenamentoDados'
]