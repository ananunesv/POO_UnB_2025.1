#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Controle de Tarefas Domésticas
==========================================

Sistema desktop para gerenciar tarefas domésticas entre moradores,
desenvolvido aplicando conceitos de Programação Orientada a Objetos.

Autor: Projeto Acadêmico POO
Data: 2025
Versão: 1.0
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from package.controllers.gerenciador_tarefas import GerenciadorTarefas
    from package.views.interface_visual import InterfaceVisual
    from package.controllers.armazenamento_dados import ArmazenamentoDados
    from package.models.residencia import Residencia
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("📁 Verifique se a estrutura de pastas está correta!")
    sys.exit(1)


def criar_estrutura_diretorios():
    """Cria estrutura de diretórios necessária para o projeto."""
    diretorios = [
        'dados',
        'assets',
        'assets/icones'
    ]
    
    for diretorio in diretorios:
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
            print(f"📁 Criado diretório: {diretorio}")


def verificar_dependencias():
    """Verifica se todas as dependências estão disponíveis."""
    dependencias = ['tkinter', 'json', 'datetime', 'enum']
    faltando = []
    
    for dep in dependencias:
        try:
            __import__(dep)
        except ImportError:
            faltando.append(dep)
    
    if faltando:
        print(f"❌ Dependências faltando: {', '.join(faltando)}")
        return False
    
    print("✅ Todas as dependências verificadas!")
    return True


def inicializar_sistema():
    """Inicializa o sistema de tarefas domésticas."""
    print("🏡 Inicializando Sistema de Tarefas Domésticas...")
    
    # Verificar dependências
    if not verificar_dependencias():
        return None
    
    # Criar estrutura de diretórios
    criar_estrutura_diretorios()
    
    # Inicializar componentes do sistema
    try:
        # Criar residência padrão
        residencia = Residencia("Casa Principal")
        
        # Inicializar armazenamento
        armazenamento = ArmazenamentoDados("dados/sistema_tarefas.json")
        
        # Inicializar gerenciador principal
        gerenciador = GerenciadorTarefas(residencia, armazenamento)
        
        # Tentar carregar dados existentes
        if gerenciador.carregar_dados():
            print("📂 Dados carregados com sucesso!")
        else:
            print("📝 Iniciando com dados em branco...")
        
        print("✅ Sistema inicializado com sucesso!")
        return gerenciador
        
    except Exception as e:
        print(f"❌ Erro ao inicializar sistema: {e}")
        return None


def main():
    """Função principal do sistema."""
    print("=" * 60)
    print("🏡 SISTEMA DE CONTROLE DE TAREFAS DOMÉSTICAS")
    print("=" * 60)
    print("📚 Projeto Acadêmico - Programação Orientada a Objetos")
    print("🎯 Aplicando: Herança, Polimorfismo, Mixin, Composição")
    print("-" * 60)
    
    # Inicializar sistema
    gerenciador = inicializar_sistema()
    
    if gerenciador is None:
        print("❌ Falha na inicialização do sistema!")
        input("Pressione Enter para sair...")
        return
    
    try:
        # Criar janela principal
        root = tk.Tk()
        root.title("🏡 Sistema de Tarefas Domésticas")
        
        # Configurar ícone da janela (se disponível)
        try:
            root.iconbitmap("assets/icones/casa.ico")
        except:
            pass  # Continuar sem ícone se não encontrar
        
        # Configurar tamanho mínimo da janela
        root.minsize(1000, 700)
        
        # Centralizar janela na tela
        root.geometry("1200x800")
        
        # Configurar fechamento da aplicação
        def on_closing():
            if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
                print("💾 Salvando dados finais...")
                gerenciador.salvar_dados()
                print("👋 Sistema encerrado!")
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Inicializar interface visual
        interface = InterfaceVisual(root, gerenciador)
        
        print("🖥️ Interface gráfica carregada!")
        print("🚀 Sistema pronto para uso!")
        print("-" * 60)
        
        # Iniciar loop principal da interface
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erro na interface gráfica: {e}")
        messagebox.showerror("Erro", f"Erro crítico na interface:\n{e}")
    
    finally:
        # Salvar dados ao encerrar
        if gerenciador:
            gerenciador.salvar_dados()
        print("📊 Dados salvos com segurança!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrompido pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
        input("Pressione Enter para sair...")
    finally:
        print("🔚 Fim da execução!")