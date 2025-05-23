#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mixin GerarRelatorios
====================

Implementa o MIXIN que adiciona funcionalidades de relatórios a outras classes.
Demonstra como reutilizar código através de mixins em POO.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from collections import defaultdict, Counter


class GerarRelatorios:
    """
    Mixin que adiciona capacidades de geração de relatórios.
    
    Este mixin demonstra o conceito de MIXIN em POO - uma classe que adiciona
    funcionalidades específicas a outras classes sem ser uma classe base.
    
    Pode ser "mixado" com qualquer classe que tenha acesso a:
    - self._residencia (instância de Residencia)
    - self._lista_atividades (lista de AtividadeDomestica)
    
    As funcionalidades incluem:
    - Relatórios de performance dos moradores
    - Ranking de pontuação
    - Estatísticas por categoria
    - Histórico de tarefas por período
    """
    
    def relatorio_performance_moradores(self) -> Dict[str, Any]:
        """
        Gera relatório completo de performance dos moradores.
        
        Returns:
            Dict: Relatório com estatísticas detalhadas de cada morador
        """
        if not hasattr(self, '_residencia'):
            raise AttributeError("Mixin requer atributo '_residencia'")
        
        moradores = self._residencia.listar_moradores()
        if not moradores:
            return {'erro': 'Nenhum morador cadastrado'}
        
        relatorio = {
            'data_geracao': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'total_moradores': len(moradores),
            'moradores': [],
            'estatisticas_gerais': self._residencia.obter_estatisticas_gerais()
        }
        
        for morador in moradores:
            desempenho = morador.calcular_desempenho()
            tarefas_mes = self._obter_tarefas_morador_mes(morador.id)
            
            dados_morador = {
                'nome': morador.nome,
                'id': morador.id,
                'pontos_total': morador.pontos_realizadas,
                'tarefas_realizadas': morador.total_tarefas_realizadas,
                'nivel_performance': morador.nivel_performance,
                'disponivel': morador.disponivel,
                'tempo_cadastrado': morador.tempo_cadastrado(),
                'desempenho': desempenho,
                'tarefas_este_mes': len(tarefas_mes),
                'categorias_favoritas': self._obter_categorias_favoritas_morador(morador.id)
            }
            relatorio['moradores'].append(dados_morador)
        
        # Ordenar por pontos (maior primeiro)
        relatorio['moradores'].sort(key=lambda x: x['pontos_total'], reverse=True)
        
        return relatorio
    
    def ranking_melhores_moradores(self, limite: int = 10) -> List[Dict[str, Any]]:
        """
        Gera ranking dos melhores moradores por pontuação.
        
        Args:
            limite (int): Número máximo de moradores no ranking
            
        Returns:
            List[Dict]: Lista ordenada com ranking dos moradores
        """
        if not hasattr(self, '_residencia'):
            raise AttributeError("Mixin requer atributo '_residencia'")
        
        ranking = self._residencia.obter_ranking_moradores()
        return ranking[:limite]
    
    def estatisticas_por_categoria(self) -> Dict[str, Any]:
        """
        Gera estatísticas das atividades agrupadas por categoria.
        
        Returns:
            Dict: Estatísticas por categoria de atividade
        """
        if not hasattr(self, '_lista_atividades'):
            raise AttributeError("Mixin requer atributo '_lista_atividades'")
        
        atividades = self._lista_atividades
        if not atividades:
            return {'erro': 'Nenhuma atividade cadastrada'}
        
        # Agrupar por categoria
        por_categoria = defaultdict(lambda: {
            'total': 0,
            'finalizadas': 0,
            'pendentes': 0,
            'canceladas': 0,
            'pontos_total': 0,
            'atividades': []
        })
        
        for atividade in atividades:
            categoria = atividade.categoria.value
            por_categoria[categoria]['total'] += 1
            por_categoria[categoria]['pontos_total'] += atividade.pontos_tarefa
            por_categoria[categoria]['atividades'].append(atividade.nome_tarefa)
            
            if atividade.esta_finalizada:
                por_categoria[categoria]['finalizadas'] += 1
            elif atividade.esta_pendente:
                por_categoria[categoria]['pendentes'] += 1
            elif atividade.esta_cancelada:
                por_categoria[categoria]['canceladas'] += 1
        
        # Calcular percentuais e médias
        estatisticas = {
            'data_geracao': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'total_atividades': len(atividades),
            'categorias': {}
        }
        
        for categoria, dados in por_categoria.items():
            total = dados['total']
            porcentagem_conclusao = (dados['finalizadas'] / total * 100) if total > 0 else 0
            pontos_medio = dados['pontos_total'] / total if total > 0 else 0
            
            estatisticas['categorias'][categoria] = {
                'total_atividades': total,
                'finalizadas': dados['finalizadas'],
                'pendentes': dados['pendentes'],
                'canceladas': dados['canceladas'],
                'porcentagem_conclusao': round(porcentagem_conclusao, 1),
                'pontos_total': dados['pontos_total'],
                'pontos_medio': round(pontos_medio, 1),
                'atividades_exemplo': dados['atividades'][:5]  # Primeiras 5 como exemplo
            }
        
        return estatisticas
    
    def historico_tarefas_mes(self, mes: int = None, ano: int = None) -> Dict[str, Any]:
        """
        Gera histórico de tarefas para um mês específico.
        
        Args:
            mes (int): Mês (1-12). Se None, usa mês atual
            ano (int): Ano. Se None, usa ano atual
            
        Returns:
            Dict: Histórico detalhado do mês
        """
        if not hasattr(self, '_lista_atividades'):
            raise AttributeError("Mixin requer atributo '_lista_atividades'")
        
        agora = datetime.now()
        mes = mes or agora.month
        ano = ano or agora.year
        
        # Filtrar atividades do mês
        atividades_mes = []
        for atividade in self._lista_atividades:
            data_atividade = atividade.data_criacao
            if data_atividade.month == mes and data_atividade.year == ano:
                atividades_mes.append(atividade)
        
        if not atividades_mes:
            return {
                'mes': mes,
                'ano': ano,
                'total_atividades': 0,
                'erro': f'Nenhuma atividade encontrada para {mes:02d}/{ano}'
            }
        
        # Agrupar por semanas
        semanas = defaultdict(list)
        for atividade in atividades_mes:
            semana = self._obter_semana_do_mes(atividade.data_criacao)
            semanas[semana].append(atividade)
        
        # Estatísticas gerais do mês
        finalizadas = len([a for a in atividades_mes if a.esta_finalizada])
        pendentes = len([a for a in atividades_mes if a.esta_pendente])
        canceladas = len([a for a in atividades_mes if a.esta_cancelada])
        pontos_total = sum(a.pontos_tarefa for a in atividades_mes if a.esta_finalizada)
        
        relatorio = {
            'mes': mes,
            'ano': ano,
            'nome_mes': self._obter_nome_mes(mes),
            'data_geracao': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'total_atividades': len(atividades_mes),
            'finalizadas': finalizadas,
            'pendentes': pendentes,
            'canceladas': canceladas,
            'pontos_total_mes': pontos_total,
            'taxa_conclusao': round(finalizadas / len(atividades_mes) * 100, 1),
            'semanas': {},
            'top_moradores': self._obter_top_moradores_mes(atividades_mes),
            'categorias_mais_ativas': self._obter_categorias_mais_ativas_mes(atividades_mes)
        }
        
        # Detalhes por semana
        for semana, atividades_semana in semanas.items():
            relatorio['semanas'][f'Semana {semana}'] = {
                'total': len(atividades_semana),
                'finalizadas': len([a for a in atividades_semana if a.esta_finalizada]),
                'atividades': [a.nome_tarefa for a in atividades_semana]
            }
        
        return relatorio
    
    def relatorio_produtividade_diaria(self, dias: int = 7) -> Dict[str, Any]:
        """
        Gera relatório de produtividade dos últimos dias.
        
        Args:
            dias (int): Número de dias para analisar
            
        Returns:
            Dict: Relatório de produtividade diária
        """
        if not hasattr(self, '_lista_atividades'):
            raise AttributeError("Mixin requer atributo '_lista_atividades'")
        
        data_limite = datetime.now() - timedelta(days=dias)
        
        # Filtrar atividades recentes
        atividades_recentes = [
            a for a in self._lista_atividades 
            if a.data_criacao >= data_limite
        ]
        
        # Agrupar por dia
        por_dia = defaultdict(lambda: {'criadas': 0, 'finalizadas': 0, 'pontos': 0})
        
        for atividade in atividades_recentes:
            data_str = atividade.data_criacao.strftime("%d/%m")
            por_dia[data_str]['criadas'] += 1
            
            if atividade.esta_finalizada:
                por_dia[data_str]['finalizadas'] += 1
                por_dia[data_str]['pontos'] += atividade.pontos_tarefa
        
        return {
            'periodo': f"Últimos {dias} dias",
            'data_geracao': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'produtividade_diaria': dict(por_dia),
            'total_atividades_periodo': len(atividades_recentes),
            'media_diaria': round(len(atividades_recentes) / dias, 1)
        }
    
    def _obter_tarefas_morador_mes(self, morador_id: str) -> List:
        """Obtém tarefas de um morador no mês atual."""
        if not hasattr(self, '_lista_atividades'):
            return []
        
        agora = datetime.now()
        return [
            a for a in self._lista_atividades 
            if (a.responsavel_id == morador_id and 
                a.data_criacao.month == agora.month and 
                a.data_criacao.year == agora.year)
        ]
    
    def _obter_categorias_favoritas_morador(self, morador_id: str) -> List[str]:
        """Obtém categorias favoritas de um morador."""
        if not hasattr(self, '_lista_atividades'):
            return []
        
        atividades_morador = [
            a for a in self._lista_atividades 
            if a.responsavel_id == morador_id and a.esta_finalizada
        ]
        
        if not atividades_morador:
            return []
        
        categorias = [a.categoria.value for a in atividades_morador]
        contador = Counter(categorias)
        return [cat for cat, _ in contador.most_common(3)]
    
    def _obter_semana_do_mes(self, data: datetime) -> int:
        """Obtém o número da semana no mês."""
        return (data.day - 1) // 7 + 1
    
    def _obter_top_moradores_mes(self, atividades_mes: List) -> List[Dict[str, Any]]:
        """Obtém top moradores do mês."""
        if not hasattr(self, '_residencia'):
            return []
        
        # Contar atividades finalizadas por morador
        contador_moradores = defaultdict(int)
        for atividade in atividades_mes:
            if atividade.esta_finalizada and atividade.responsavel_id:
                contador_moradores[atividade.responsavel_id] += 1
        
        # Obter nomes dos moradores
        top_moradores = []
        for morador_id, count in contador_moradores.most_common(5):
            morador = self._residencia.obter_morador_por_id(morador_id)
            if morador:
                top_moradores.append({
                    'nome': morador.nome,
                    'tarefas_finalizadas': count
                })
        
        return top_moradores
    
    def _obter_categorias_mais_ativas_mes(self, atividades_mes: List) -> List[Dict[str, Any]]:
        """Obtém categorias mais ativas do mês."""
        contador_categorias = Counter([a.categoria.value for a in atividades_mes])
        
        return [
            {'categoria': cat, 'quantidade': count}
            for cat, count in contador_categorias.most_common(5)
        ]