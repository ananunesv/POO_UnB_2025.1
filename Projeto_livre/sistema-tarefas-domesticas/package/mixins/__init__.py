#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mixins do Sistema
================

Classes mixin que adicionam funcionalidades específicas:
- GerarRelatorios (funcionalidades de relatórios e estatísticas)

Os mixins demonstram como reutilizar código em POO através de herança múltipla.
"""

# Importar mixins
from .gerar_relatorios import GerarRelatorios

# Definir exportações
__all__ = [
    'GerarRelatorios'
]