#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Controle de Tarefas Domésticas
=========================================

Pacote principal do sistema que implementa conceitos de POO:
- Herança, Polimorfismo, Mixin, Composição, Associação, Encapsulamento

Autor: Projeto Acadêmico POO
Versão: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Projeto Acadêmico POO"
__description__ = "Sistema de controle de tarefas domésticas com POO"

# Importações principais para facilitar uso do pacote
from .models import *
from .controllers import *
from .mixins import *
from .views import *

__all__ = [
    # Models
    'Pessoa', 'Morador', 'AtividadeDomestica', 'Residencia',
    'CategoriaAtividade', 'SituacaoTarefa',
    
    # Controllers  
    'GerenciadorTarefas', 'ArmazenamentoDados',
    
    # Mixins
    'GerarRelatorios',
    
    # Views
    'InterfaceVisual'
]