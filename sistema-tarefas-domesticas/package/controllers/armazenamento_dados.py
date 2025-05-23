#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe ArmazenamentoDados
========================

Implementa a persistência de dados em JSON.
Demonstra SERIALIZAÇÃO de objetos em POO.
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, Any, Optional


class ArmazenamentoDados:
    """
    Classe responsável pela persistência dos dados do sistema.
    
    Implementa serialização e deserialização de objetos para/do formato JSON,
    demonstrando como manter dados entre execuções do programa.
    
    Funcionalidades:
    - Salvar dados em JSON
    - Carregar dados do JSON
    - Fazer backup automático
    - Validar integridade dos dados
    """
    
    def __init__(self, arquivo_json: str):
        """
        Inicializa o sistema de armazenamento.
        
        Args:
            arquivo_json (str): Caminho para o arquivo JSON
        """
        self._arquivo_json = arquivo_json
        self._arquivo_backup = f"{arquivo_json}.backup"
        self._criar_diretorios()
    
    def salvar_em_json(self, dados: Dict[str, Any]) -> bool:
        """
        Salva dados no arquivo JSON.
        
        Args:
            dados (Dict): Dados para salvar
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            # Fazer backup antes de salvar
            self.fazer_backup()
            
            # Adicionar metadados
            dados_completos = {
                'metadata': {
                    'versao': '1.0',
                    'data_salvamento': datetime.now().isoformat(),
                    'sistema': 'Tarefas Domésticas'
                },
                'dados': dados
            }
            
            # Salvar com encoding UTF-8
            with open(self._arquivo_json, 'w', encoding='utf-8') as arquivo:
                json.dump(dados_completos, arquivo, 
                         indent=2, ensure_ascii=False, default=str)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar dados: {e}")
            return False
    
    def carregar_do_json(self) -> Optional[Dict[str, Any]]:
        """
        Carrega dados do arquivo JSON.
        
        Returns:
            Optional[Dict]: Dados carregados ou None se erro
        """
        try:
            if not os.path.exists(self._arquivo_json):
                print("📝 Arquivo de dados não existe. Iniciando novo...")
                return None
            
            with open(self._arquivo_json, 'r', encoding='utf-8') as arquivo:
                dados_completos = json.load(arquivo)
            
            # Verificar estrutura
            if 'dados' in dados_completos:
                return dados_completos['dados']
            else:
                # Formato antigo, retornar diretamente
                return dados_completos
                
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar JSON: {e}")
            return self._tentar_restaurar_backup()
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return None
    
    def fazer_backup(self) -> bool:
        """
        Faz backup do arquivo atual.
        
        Returns:
            bool: True se backup foi criado
        """
        try:
            if os.path.exists(self._arquivo_json):
                shutil.copy2(self._arquivo_json, self._arquivo_backup)
                return True
            return False
        except Exception as e:
            print(f"⚠️ Erro ao fazer backup: {e}")
            return False
    
    def validar_integridade(self) -> bool:
        """
        Valida integridade dos dados salvos.
        
        Returns:
            bool: True se dados estão íntegros
        """
        try:
            dados = self.carregar_do_json()
            if dados is None:
                return False
            
            # Verificações básicas de integridade
            campos_obrigatorios = ['residencia', 'atividades']
            for campo in campos_obrigatorios:
                if campo not in dados:
                    print(f"⚠️ Campo obrigatório missing: {campo}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na validação: {e}")
            return False
    
    def _criar_diretorios(self):
        """Cria diretórios necessários se não existirem."""
        diretorio = os.path.dirname(self._arquivo_json)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
    
    def _tentar_restaurar_backup(self) -> Optional[Dict[str, Any]]:
        """Tenta restaurar dados do backup."""
        try:
            if os.path.exists(self._arquivo_backup):
                print("🔄 Tentando restaurar backup...")
                shutil.copy2(self._arquivo_backup, self._arquivo_json)
                return self.carregar_do_json()
        except:
            pass
        return None