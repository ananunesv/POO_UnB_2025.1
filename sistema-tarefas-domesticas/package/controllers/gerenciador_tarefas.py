#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe GerenciadorTarefas
========================

Controller principal que usa MIXIN e coordena todo o sistema.
"""

from typing import List, Optional, Dict, Any
from ..models.residencia import Residencia
from ..models.morador import Morador
from ..models.atividade_domestica import AtividadeDomestica
from ..models.enums import CategoriaAtividade, SituacaoTarefa
from ..mixins.gerar_relatorios import GerarRelatorios
from .armazenamento_dados import ArmazenamentoDados


class GerenciadorTarefas(GerarRelatorios):
    """
    Classe controladora principal que gerencia todo o sistema.
    
    Demonstra:
    - MIXIN: Herda funcionalidades de GerarRelatorios
    - COMPOSIÇÃO: Tem uma Residencia e ArmazenamentoDados
    - CONTROLLER: Coordena todas as operações do sistema
    """
    
    def __init__(self, residencia: Residencia, armazenamento: ArmazenamentoDados):
        """
        Inicializa o gerenciador.
        
        Args:
            residencia (Residencia): Residência a ser gerenciada
            armazenamento (ArmazenamentoDados): Sistema de persistência
        """
        self._residencia = residencia
        self._lista_atividades = []
        self._armazenamento = armazenamento
    
    @property
    def residencia(self) -> Residencia:
        """Retorna a residência."""
        return self._residencia
    
    @property
    def atividades(self) -> List[AtividadeDomestica]:
        """Retorna lista de atividades."""
        return self._lista_atividades.copy()
    
    # === GERENCIAMENTO DE MORADORES ===
    
    def adicionar_morador(self, nome: str) -> bool:
        """Adiciona novo morador."""
        try:
            morador = Morador(nome)
            return self._residencia.adicionar_morador(morador)
        except Exception as e:
            print(f"❌ Erro ao adicionar morador: {e}")
            return False
    
    def obter_moradores(self) -> List[Morador]:
        """Retorna lista de moradores."""
        return self._residencia.listar_moradores()
    
    def obter_morador_por_id(self, morador_id: str) -> Optional[Morador]:
        """Obtém morador por ID."""
        return self._residencia.obter_morador_por_id(morador_id)
    
    def remover_morador(self, morador_id: str) -> bool:
        """Remove um morador da residência."""
        return self._residencia.remover_morador(morador_id)
    
    # === GERENCIAMENTO DE ATIVIDADES ===
    
    def criar_nova_atividade(self, categoria: CategoriaAtividade, 
                           nome: str, descricao: str = "", 
                           responsavel_id: str = None) -> Optional[AtividadeDomestica]:
        """Cria nova atividade."""
        try:
            atividade = AtividadeDomestica(categoria, nome, descricao, responsavel_id)
            self._lista_atividades.append(atividade)
            return atividade
        except Exception as e:
            print(f"❌ Erro ao criar atividade: {e}")
            return None
    
    def atribuir_responsavel(self, atividade_id: str, morador_id: str) -> bool:
        """Atribui responsável a uma atividade."""
        atividade = self.obter_atividade_por_id(atividade_id)
        morador = self.obter_morador_por_id(morador_id)
        
        if atividade and morador:
            atividade.responsavel_id = morador_id
            return True
        return False
    
    def finalizar_atividade(self, atividade_id: str) -> bool:
        """Finaliza uma atividade e adiciona pontos ao responsável."""
        atividade = self.obter_atividade_por_id(atividade_id)
        
        if not atividade or not atividade.esta_pendente:
            return False
        
        if atividade.marcar_finalizada():
            # Adicionar pontos ao responsável
            if atividade.responsavel_id:
                morador = self.obter_morador_por_id(atividade.responsavel_id)
                if morador:
                    morador.finalizar_tarefa(atividade_id, atividade.pontos_tarefa)
            return True
        return False
    
    def cancelar_atividade(self, atividade_id: str) -> bool:
        """Cancela uma atividade."""
        atividade = self.obter_atividade_por_id(atividade_id)
        return atividade.marcar_cancelada() if atividade else False
    
    def excluir_atividade(self, atividade_id: str) -> bool:
        """Exclui uma atividade permanentemente."""
        atividade = self.obter_atividade_por_id(atividade_id)
        if atividade:
            self._lista_atividades.remove(atividade)
            return True
        return False
    
    def obter_atividade_por_id(self, atividade_id: str) -> Optional[AtividadeDomestica]:
        """Obtém atividade por ID."""
        for atividade in self._lista_atividades:
            if atividade.id_atividade == atividade_id:
                return atividade
        return None
    
    def listar_atividades_por_categoria(self, categoria: CategoriaAtividade = None) -> List[AtividadeDomestica]:
        """Lista atividades filtradas por categoria."""
        if categoria is None:
            return self._lista_atividades.copy()
        
        return [a for a in self._lista_atividades if a.categoria == categoria]
    
    def listar_atividades_por_situacao(self, situacao: SituacaoTarefa) -> List[AtividadeDomestica]:
        """Lista atividades por situação."""
        return [a for a in self._lista_atividades if a.situacao == situacao]
    
    def obter_atividades_pendentes(self) -> List[AtividadeDomestica]:
        """Retorna atividades pendentes."""
        return self.listar_atividades_por_situacao(SituacaoTarefa.PENDENTE)
    
    # === PERSISTÊNCIA ===
    
    def salvar_dados(self) -> bool:
        """Salva todos os dados do sistema."""
        try:
            dados = {
                'residencia': self._residencia.to_dict(),
                'atividades': [a.to_dict() for a in self._lista_atividades]
            }
            return self._armazenamento.salvar_em_json(dados)
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return False
    
    def carregar_dados(self) -> bool:
        """Carrega dados salvos."""
        try:
            dados = self._armazenamento.carregar_do_json()
            if not dados:
                return False
            
            # Carregar residência
            if 'residencia' in dados:
                self._residencia = Residencia.from_dict(dados['residencia'])
            
            # Carregar atividades
            if 'atividades' in dados:
                self._lista_atividades = []
                for dados_atividade in dados['atividades']:
                    atividade = AtividadeDomestica.from_dict(dados_atividade)
                    self._lista_atividades.append(atividade)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar: {e}")
            return False
    
    # === ESTATÍSTICAS RÁPIDAS ===
    
    def obter_resumo_sistema(self) -> Dict[str, Any]:
        """Obtém resumo geral do sistema."""
        return {
            'total_moradores': self._residencia.total_moradores,
            'total_atividades': len(self._lista_atividades),
            'atividades_pendentes': len(self.obter_atividades_pendentes()),
            'atividades_finalizadas': len(self.listar_atividades_por_situacao(SituacaoTarefa.FINALIZADA)),
            'moradores_disponiveis': len(self._residencia.moradores_disponiveis)
        }