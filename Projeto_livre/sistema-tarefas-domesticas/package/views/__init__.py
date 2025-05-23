#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Views do Sistema
===============

Interfaces visuais do sistema:
- InterfaceVisual (GUI principal usando Tkinter)

As views implementam a camada de apresentação do padrão MVC.
"""

# Importar views
from .interface_visual import InterfaceVisual

# Definir exportações
__all__ = [
    'InterfaceVisual'
]