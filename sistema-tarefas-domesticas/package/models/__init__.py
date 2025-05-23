#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelos do Sistema
=================

Classes de modelo que representam as entidades do domínio:
- Pessoa (classe abstrata)
- Morador (herança de Pessoa)
- AtividadeDomestica (entidade principal)
- Residencia (composição com Moradores)
- Enumerações (CategoriaAtividade, SituacaoTarefa)
"""

# Importar todas as classes do modelo
from .pessoa import Pessoa
from .morador import Morador
from .atividade_domestica import AtividadeDomestica
from .residencia import Residencia
from .enums import CategoriaAtividade, SituacaoTarefa

# Definir o que será exportado quando usar "from models import *"
__all__ = [
    'Pessoa',
    'Morador', 
    'AtividadeDomestica',
    'Residencia',
    'CategoriaAtividade',
    'SituacaoTarefa'
]