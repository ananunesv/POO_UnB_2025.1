#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Visual - GUI do Sistema
=================================

Interface gráfica moderna e elegante usando Tkinter
VERSÃO FINAL CORRIGIDA - Todos os bugs resolvidos

Desenvolvido por: Ana Luisa
Matéria: Orientação a Objetos - UnB 2025.1
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional
import traceback
import sys
from ..models.enums import CategoriaAtividade, SituacaoTarefa


class InterfaceVisual:
    """Interface gráfica principal do sistema com design moderno."""
    
    def __init__(self, root: tk.Tk, gerenciador):
        """
        Inicializa a interface.
        
        Args:
            root: Janela principal do Tkinter
            gerenciador: GerenciadorTarefas
        """
        self.root = root
        self.gerenciador = gerenciador
        
        # Configurar captura de erros
        self._configurar_captura_erros()
        
        # Cores do tema moderno
        self.cores = {
            'primaria': '#2c3e50',      # Azul escuro
            'secundaria': '#3498db',    # Azul claro
            'sucesso': '#27ae60',       # Verde
            'aviso': '#f39c12',         # Laranja
            'perigo': '#e74c3c',        # Vermelho
            'fundo': '#ecf0f1',         # Cinza claro
            'branco': '#ffffff',
            'texto': '#2c3e50'
        }
        
        # Configurar janela principal
        self._configurar_janela()
        
        # Criar interface
        self._criar_interface()
        self._atualizar_dados()
        
        print("✅ Interface inicializada com sucesso!")
    
    def _configurar_captura_erros(self):
        """Configura captura e exibição de erros."""
        def mostrar_erro(tipo, valor, tb):
            erro_msg = f"ERRO: {tipo.__name__}: {valor}\n\n"
            erro_msg += "Traceback:\n"
            erro_msg += ''.join(traceback.format_tb(tb))
            
            print("=" * 60)
            print("❌ ERRO CAPTURADO:")
            print(erro_msg)
            print("=" * 60)
            
            # Mostrar na interface também
            try:
                messagebox.showerror("Erro do Sistema", 
                                   f"Um erro ocorreu:\n{tipo.__name__}: {valor}\n\nVerifique o terminal para detalhes.")
            except:
                pass
        
        sys.excepthook = mostrar_erro
    
    def _configurar_janela(self):
        """Configura a janela principal com estilo moderno."""
        self.root.title("🏡 Sistema de Tarefas Domésticas - Ana Luisa | POO UnB 2025.1")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.cores['fundo'])
        self.root.minsize(1200, 800)
        
        # Centralizar janela na tela
        try:
            self.root.update_idletasks()
            x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
            y = (self.root.winfo_screenheight() // 2) - (900 // 2)
            self.root.geometry(f"1400x900+{x}+{y}")
        except Exception as e:
            print(f"⚠️ Aviso ao centralizar janela: {e}")
        
        # Configurar estilo ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar estilos personalizados
        self._configurar_estilos()
    
    def _configurar_estilos(self):
        """Configura estilos personalizados para os widgets."""
        try:
            # Estilo para Notebook (abas)
            self.style.configure('Custom.TNotebook', 
                               background=self.cores['fundo'],
                               borderwidth=0,
                               tabmargins=[2, 5, 2, 0])
            
            self.style.configure('Custom.TNotebook.Tab',
                               background=self.cores['branco'],
                               foreground=self.cores['texto'],
                               padding=[15, 8],
                               font=('Arial', 11, 'bold'))
            
            self.style.map('Custom.TNotebook.Tab',
                          background=[('selected', self.cores['primaria'])],
                          foreground=[('selected', self.cores['branco'])])
            
            # Estilo para Treeview
            self.style.configure('Custom.Treeview',
                               background=self.cores['branco'],
                               foreground=self.cores['texto'],
                               fieldbackground=self.cores['branco'],
                               font=('Arial', 10),
                               rowheight=25)
            
            self.style.configure('Custom.Treeview.Heading',
                               background=self.cores['primaria'],
                               foreground=self.cores['branco'],
                               font=('Arial', 11, 'bold'),
                               relief='flat')
            
            self.style.map('Custom.Treeview',
                          background=[('selected', self.cores['secundaria'])])
            
        except Exception as e:
            print(f"⚠️ Erro ao configurar estilos: {e}")
    
    def _criar_interface(self):
        """Cria os elementos da interface."""
        try:
            # Header elegante
            self._criar_header()
            
            # Container principal
            main_container = tk.Frame(self.root, bg=self.cores['fundo'])
            main_container.pack(fill='both', expand=True, padx=15, pady=10)
            
            # Notebook para abas
            self.notebook = ttk.Notebook(main_container, style='Custom.TNotebook')
            self.notebook.pack(fill='both', expand=True, pady=5)
            
            # Criar abas
            self._criar_aba_dashboard()
            self._criar_aba_tarefas()
            self._criar_aba_moradores()
            self._criar_aba_relatorios()
            
            # Footer
            self._criar_footer()
            
            print("✅ Interface criada com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao criar interface: {e}")
            traceback.print_exc()
    
    def _criar_header(self):
        """Cria header elegante."""
        header = tk.Frame(self.root, bg=self.cores['primaria'], height=90)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título principal
        titulo_frame = tk.Frame(header, bg=self.cores['primaria'])
        titulo_frame.pack(expand=True)
        
        titulo = tk.Label(titulo_frame, 
                         text="🏡 Sistema de Tarefas Domésticas",
                         font=('Arial', 24, 'bold'),
                         bg=self.cores['primaria'],
                         fg=self.cores['branco'])
        titulo.pack(pady=(15, 5))
        
        subtitulo = tk.Label(titulo_frame,
                           text="Organize suas tarefas domésticas de forma inteligente",
                           font=('Arial', 12),
                           bg=self.cores['primaria'],
                           fg=self.cores['branco'])
        subtitulo.pack(pady=(0, 5))
        
        # Créditos
        creditos = tk.Label(titulo_frame,
                          text="📚 Desenvolvido por Ana Luisa | Orientação a Objetos - UnB 2025.1",
                          font=('Arial', 10),
                          bg=self.cores['primaria'],
                          fg=self.cores['branco'])
        creditos.pack()
    
    def _criar_footer(self):
        """Cria footer informativo."""
        footer = tk.Frame(self.root, bg=self.cores['primaria'], height=35)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        footer_text = tk.Label(footer,
                              text="💻 Desenvolvido por ANA LUISA com Python e POO | 📊 Dados salvos automaticamente | 🎓 UnB 2025.1",
                              font=('Arial', 9),
                              bg=self.cores['primaria'],
                              fg=self.cores['branco'])
        footer_text.pack(pady=8)
    
    def _criar_aba_dashboard(self):
        """Cria aba dashboard com resumo."""
        frame_dash = ttk.Frame(self.notebook)
        self.notebook.add(frame_dash, text="📊 Dashboard")
        
        # Toolbar do dashboard
        toolbar_dash = tk.Frame(frame_dash, bg=self.cores['branco'], height=60, relief='solid', borderwidth=1)
        toolbar_dash.pack(fill='x', padx=10, pady=10)
        toolbar_dash.pack_propagate(False)
        
        btn_atualizar_dash = self._criar_botao_moderno(toolbar_dash, "🔄 Atualizar Dashboard", self._atualizar_dashboard_completo,
                                                     self.cores['secundaria'])
        btn_atualizar_dash.pack(side='left', padx=8, pady=10)
        
        # Texto informativo
        info_label = tk.Label(toolbar_dash, text="Clique em 'Atualizar Dashboard' para ver as mudanças mais recentes",
                             font=('Arial', 10), bg=self.cores['branco'], fg=self.cores['texto'])
        info_label.pack(side='left', padx=15, pady=10)
        
        # Container para cards com padding
        self.cards_container = tk.Frame(frame_dash, bg=self.cores['fundo'])
        self.cards_container.pack(fill='x', padx=20, pady=10)
        
        # Cards de estatísticas
        self._criar_cards_estatisticas(self.cards_container)
        
        # Área de atividades recentes
        self._criar_area_atividades_recentes(frame_dash)
    
    def _criar_cards_estatisticas(self, parent):
        """Cria cards de estatísticas."""
        try:
            resumo = self.gerenciador.obter_resumo_sistema()
            
            cards_data = [
                ("👥", "Moradores", resumo['total_moradores'], self.cores['primaria']),
                ("📋", "Tarefas Total", resumo['total_atividades'], self.cores['secundaria']),
                ("⏳", "Pendentes", resumo['atividades_pendentes'], self.cores['aviso']),
                ("✅", "Finalizadas", resumo['atividades_finalizadas'], self.cores['sucesso'])
            ]
            
            for i, (emoji, titulo, valor, cor) in enumerate(cards_data):
                card = self._criar_card(parent, emoji, titulo, valor, cor)
                card.grid(row=0, column=i, padx=15, pady=10, sticky='ew')
            
            # Configurar colunas para serem responsivas
            for i in range(4):
                parent.grid_columnconfigure(i, weight=1)
                
        except Exception as e:
            print(f"❌ Erro ao criar cards: {e}")
    
    def _criar_card(self, parent, emoji, titulo, valor, cor):
        """Cria um card individual."""
        card_frame = tk.Frame(parent, bg=self.cores['branco'], relief='solid', 
                             borderwidth=2, padx=10, pady=10)
        card_frame.configure(highlightbackground=cor, highlightcolor=cor, highlightthickness=2)
        
        # Emoji
        emoji_label = tk.Label(card_frame, text=emoji, font=('Arial', 28), 
                              bg=self.cores['branco'], fg=cor)
        emoji_label.pack(pady=(10, 5))
        
        # Valor
        valor_label = tk.Label(card_frame, text=str(valor), font=('Arial', 22, 'bold'),
                              bg=self.cores['branco'], fg=cor)
        valor_label.pack()
        
        # Título
        titulo_label = tk.Label(card_frame, text=titulo, font=('Arial', 13, 'bold'),
                               bg=self.cores['branco'], fg=self.cores['texto'])
        titulo_label.pack(pady=(5, 10))
        
        return card_frame
    
    def _criar_area_atividades_recentes(self, parent):
        """Cria área de atividades recentes."""
        frame = tk.LabelFrame(parent, text="📈 Atividades Recentes", 
                             font=('Arial', 14, 'bold'),
                             bg=self.cores['fundo'], fg=self.cores['texto'],
                             relief='solid', borderwidth=1)
        frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Lista simplificada de atividades recentes
        self.lista_recentes = tk.Listbox(frame, font=('Arial', 11),
                                        bg=self.cores['branco'],
                                        selectbackground=self.cores['secundaria'],
                                        relief='flat', borderwidth=0)
        
        # Scrollbar para lista recentes
        scrollbar_recentes = ttk.Scrollbar(frame, orient='vertical', command=self.lista_recentes.yview)
        self.lista_recentes.configure(yscrollcommand=scrollbar_recentes.set)
        
        self.lista_recentes.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar_recentes.pack(side='right', fill='y', pady=10)
    
    def _criar_aba_tarefas(self):
        """Cria aba de tarefas melhorada."""
        frame_tarefas = ttk.Frame(self.notebook)
        self.notebook.add(frame_tarefas, text="📋 Atividade")
        
        # Toolbar superior elegante
        toolbar = tk.Frame(frame_tarefas, bg=self.cores['branco'], height=70, relief='solid', borderwidth=1)
        toolbar.pack(fill='x', padx=10, pady=10)
        toolbar.pack_propagate(False)
        
        # Botões com estilo moderno
        btn_nova = self._criar_botao_moderno(toolbar, "➕ Nova Atividade", self._nova_tarefa, 
                                           self.cores['sucesso'])
        btn_nova.pack(side='left', padx=8, pady=15)
        
        btn_finalizar = self._criar_botao_moderno(toolbar, "✅ Finalizar", self._finalizar_tarefa_selecionada,
                                                self.cores['primaria'])
        btn_finalizar.pack(side='left', padx=8, pady=15)
        
        btn_cancelar = self._criar_botao_moderno(toolbar, "❌ Cancelar", self._cancelar_tarefa_selecionada,
                                               self.cores['perigo'])
        btn_cancelar.pack(side='left', padx=8, pady=15)
        
        btn_excluir = self._criar_botao_moderno(toolbar, "🗑️ Excluir", self._excluir_tarefa_selecionada,
                                              '#795548')
        btn_excluir.pack(side='left', padx=8, pady=15)
        
        btn_atualizar = self._criar_botao_moderno(toolbar, "🔄 Atualizar", self._atualizar_lista_tarefas,
                                                self.cores['aviso'])
        btn_atualizar.pack(side='left', padx=8, pady=15)
        
        # Container para lista
        lista_container = tk.Frame(frame_tarefas, bg=self.cores['fundo'], relief='solid', borderwidth=1)
        lista_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Lista de tarefas melhorada
        colunas = ('ID', 'Categoria', 'Nome da Tarefa', 'Status', 'Responsável', 'Pontos')
        self.tree_tarefas = ttk.Treeview(lista_container, columns=colunas, show='headings',
                                        style='Custom.Treeview', height=15)
        
        # Configurar colunas
        larguras = [120, 150, 350, 120, 180, 80]
        for i, (col, largura) in enumerate(zip(colunas, larguras)):
            self.tree_tarefas.heading(col, text=col)
            anchor = 'w' if col == 'Nome da Tarefa' else 'center'
            self.tree_tarefas.column(col, width=largura, anchor=anchor, minwidth=80)
        
        # Scrollbars
        scrollbar_v = ttk.Scrollbar(lista_container, orient='vertical', command=self.tree_tarefas.yview)
        scrollbar_h = ttk.Scrollbar(lista_container, orient='horizontal', command=self.tree_tarefas.xview)
        self.tree_tarefas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # Grid layout
        self.tree_tarefas.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        scrollbar_v.grid(row=0, column=1, sticky='ns', pady=5)
        scrollbar_h.grid(row=1, column=0, sticky='ew', padx=5)
        
        lista_container.grid_rowconfigure(0, weight=1)
        lista_container.grid_columnconfigure(0, weight=1)
    
    def _criar_aba_moradores(self):
        """Cria aba de moradores melhorada."""
        frame_moradores = ttk.Frame(self.notebook)
        self.notebook.add(frame_moradores, text="👥 Moradores")
        
        # Toolbar
        toolbar_mor = tk.Frame(frame_moradores, bg=self.cores['branco'], height=70, relief='solid', borderwidth=1)
        toolbar_mor.pack(fill='x', padx=10, pady=10)
        toolbar_mor.pack_propagate(False)
        
        btn_novo_morador = self._criar_botao_moderno(toolbar_mor, "➕ Novo Morador", self._novo_morador,
                                                   self.cores['sucesso'])
        btn_novo_morador.pack(side='left', padx=8, pady=15)
        
        btn_editar_morador = self._criar_botao_moderno(toolbar_mor, "✏️ Editar", self._editar_morador_selecionado,
                                                     self.cores['secundaria'])
        btn_editar_morador.pack(side='left', padx=8, pady=15)
        
        btn_excluir_morador = self._criar_botao_moderno(toolbar_mor, "🗑️ Excluir", self._excluir_morador_selecionado,
                                                      self.cores['perigo'])
        btn_excluir_morador.pack(side='left', padx=8, pady=15)
        
        btn_atualizar_mor = self._criar_botao_moderno(toolbar_mor, "🔄 Atualizar", self._atualizar_lista_moradores,
                                                    self.cores['aviso'])
        btn_atualizar_mor.pack(side='left', padx=8, pady=15)
        
        # Lista de moradores
        lista_container_mor = tk.Frame(frame_moradores, bg=self.cores['fundo'], relief='solid', borderwidth=1)
        lista_container_mor.pack(fill='both', expand=True, padx=10, pady=5)
        
        colunas_mor = ('Nome', 'Pontos', 'Tarefas Realizadas', 'Nível', 'Status')
        self.tree_moradores = ttk.Treeview(lista_container_mor, columns=colunas_mor, 
                                          show='headings', style='Custom.Treeview', height=15)
        
        larguras_mor = [250, 120, 180, 200, 150]
        for col, largura in zip(colunas_mor, larguras_mor):
            self.tree_moradores.heading(col, text=col)
            self.tree_moradores.column(col, width=largura, anchor='center', minwidth=100)
        
        scrollbar_mor_v = ttk.Scrollbar(lista_container_mor, orient='vertical', command=self.tree_moradores.yview)
        self.tree_moradores.configure(yscrollcommand=scrollbar_mor_v.set)
        
        self.tree_moradores.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        scrollbar_mor_v.grid(row=0, column=1, sticky='ns', pady=5)
        
        lista_container_mor.grid_rowconfigure(0, weight=1)
        lista_container_mor.grid_columnconfigure(0, weight=1)
    
    def _criar_aba_relatorios(self):
        """Cria aba de relatórios melhorada."""
        frame_relatorios = ttk.Frame(self.notebook)
        self.notebook.add(frame_relatorios, text="📊 Relatórios")
        
        # Toolbar de relatórios
        toolbar_rel = tk.Frame(frame_relatorios, bg=self.cores['branco'], height=70, relief='solid', borderwidth=1)
        toolbar_rel.pack(fill='x', padx=10, pady=10)
        toolbar_rel.pack_propagate(False)
        
        btn_ranking = self._criar_botao_moderno(toolbar_rel, "🏆 Ranking", self._gerar_ranking, '#9C27B0')
        btn_ranking.pack(side='left', padx=8, pady=15)
        
        btn_categoria = self._criar_botao_moderno(toolbar_rel, "📊 Por Categoria", self._gerar_estatisticas_categoria, '#3F51B5')
        btn_categoria.pack(side='left', padx=8, pady=15)
        
        btn_performance = self._criar_botao_moderno(toolbar_rel, "📈 Performance", self._gerar_relatorio_performance, '#FF5722')
        btn_performance.pack(side='left', padx=8, pady=15)
        
        # Área de texto para relatórios
        texto_container = tk.Frame(frame_relatorios, bg=self.cores['fundo'], relief='solid', borderwidth=1)
        texto_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.texto_relatorio = tk.Text(texto_container, wrap='word', font=('Courier', 11),
                                      bg=self.cores['branco'], fg=self.cores['texto'],
                                      relief='flat', borderwidth=0)
        
        scrollbar_rel_v = ttk.Scrollbar(texto_container, orient='vertical', command=self.texto_relatorio.yview)
        scrollbar_rel_h = ttk.Scrollbar(texto_container, orient='horizontal', command=self.texto_relatorio.xview)
        self.texto_relatorio.configure(yscrollcommand=scrollbar_rel_v.set, xscrollcommand=scrollbar_rel_h.set)
        
        self.texto_relatorio.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        scrollbar_rel_v.grid(row=0, column=1, sticky='ns', pady=5)
        scrollbar_rel_h.grid(row=1, column=0, sticky='ew', padx=5)
        
        texto_container.grid_rowconfigure(0, weight=1)
        texto_container.grid_columnconfigure(0, weight=1)
    
    def _criar_botao_moderno(self, parent, texto, comando, cor):
        """Cria botão com estilo moderno."""
        botao = tk.Button(parent, text=texto, command=comando,
                         bg=cor, fg=self.cores['branco'],
                         font=('Arial', 11, 'bold'),
                         relief='flat', borderwidth=0,
                         padx=20, pady=10,
                         cursor='hand2')
        
        # Efeitos hover
        def on_enter(e):
            botao.configure(bg=self._escurecer_cor(cor))
        
        def on_leave(e):
            botao.configure(bg=cor)
        
        botao.bind("<Enter>", on_enter)
        botao.bind("<Leave>", on_leave)
        
        return botao
    
    def _escurecer_cor(self, cor):
        """Escurece uma cor hexadecimal."""
        try:
            cor = cor.lstrip('#')
            rgb = tuple(int(cor[i:i+2], 16) for i in (0, 2, 4))
            rgb_escuro = tuple(max(0, c - 30) for c in rgb)
            return f"#{rgb_escuro[0]:02x}{rgb_escuro[1]:02x}{rgb_escuro[2]:02x}"
        except:
            return cor
    
    def _nova_tarefa(self):
        """Abre diálogo para criar nova tarefa."""
        try:
            print("🔄 Abrindo diálogo para nova tarefa...")
            dialog = NovaAtividadeDialog(self.root, self.gerenciador)
            self.root.wait_window(dialog.dialog)
            
            if dialog.resultado:
                print(f"✅ Tarefa criada: {dialog.resultado.nome_tarefa}")
                self._atualizar_dados()
                self.gerenciador.salvar_dados()
                messagebox.showinfo("Sucesso!", f"Tarefa '{dialog.resultado.nome_tarefa}' criada com sucesso! 🎉")
                
        except Exception as e:
            print(f"❌ Erro ao criar nova tarefa: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao criar tarefa: {str(e)}")
    
    def _novo_morador(self):
        """Abre diálogo para novo morador."""
        try:
            print("🔄 Abrindo diálogo para novo morador...")
            nome = simpledialog.askstring("Novo Morador", 
                                         "Digite o nome do morador:",
                                         parent=self.root)
            
            if nome and nome.strip():
                if self.gerenciador.adicionar_morador(nome.strip()):
                    print(f"✅ Morador adicionado: {nome}")
                    messagebox.showinfo("Sucesso!", f"Morador '{nome}' adicionado com sucesso! 👥")
                    self._atualizar_dados()
                    self.gerenciador.salvar_dados()
                else:
                    print(f"❌ Falha ao adicionar morador: {nome}")
                    messagebox.showerror("Erro", "Não foi possível adicionar o morador.\nVerifique se o nome já não existe.")
                    
        except Exception as e:
            print(f"❌ Erro ao adicionar morador: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao adicionar morador: {str(e)}")
    
    def _finalizar_tarefa_selecionada(self):
        """Finaliza tarefa selecionada."""
        try:
            selecao = self.tree_tarefas.selection()
            if not selecao:
                messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para finalizar.")
                return
            
            item = self.tree_tarefas.item(selecao[0])
            valores = item['values']
            tarefa_id_curto = valores[0]
            nome_tarefa = valores[2]
            
            print(f"🔄 Tentando finalizar tarefa: {tarefa_id_curto} - {nome_tarefa}")
            
            # Buscar a atividade completa pelo ID
            atividade_encontrada = None
            for atividade in self.gerenciador.atividades:
                if atividade.id_atividade.startswith(tarefa_id_curto.replace("...", "")):
                    atividade_encontrada = atividade
                    break
            
            if not atividade_encontrada:
                print(f"❌ Atividade não encontrada para ID: {tarefa_id_curto}")
                messagebox.showerror("Erro", "Tarefa não encontrada no sistema.")
                return
            
            # Verificar se já está finalizada
            if atividade_encontrada.esta_finalizada:
                messagebox.showwarning("Aviso", "Esta tarefa já foi finalizada!")
                return
            
            # Confirmar ação
            resposta = messagebox.askyesno("Confirmar", 
                                          f"Deseja finalizar a tarefa:\n'{nome_tarefa}'?",
                                          icon='question')
            
            if resposta:
                sucesso = self.gerenciador.finalizar_atividade(atividade_encontrada.id_atividade)
                if sucesso:
                    print(f"✅ Tarefa finalizada com sucesso: {nome_tarefa}")
                    messagebox.showinfo("Sucesso!", f"Tarefa '{nome_tarefa}' finalizada! ✅\nPontos adicionados ao responsável!")
                    self._atualizar_dados()
                    self.gerenciador.salvar_dados()
                else:
                    print(f"❌ Falha ao finalizar tarefa: {nome_tarefa}")
                    messagebox.showerror("Erro", "Não foi possível finalizar a tarefa.\nVerifique se ela ainda está pendente.")
                    
        except Exception as e:
            print(f"❌ Erro ao finalizar tarefa: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao finalizar tarefa: {str(e)}")
    
    def _cancelar_tarefa_selecionada(self):
        """Cancela tarefa selecionada."""
        try:
            selecao = self.tree_tarefas.selection()
            if not selecao:
                messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para cancelar.")
                return
            
            item = self.tree_tarefas.item(selecao[0])
            valores = item['values']
            tarefa_id_curto = valores[0]
            nome_tarefa = valores[2]
            
            print(f"🔄 Tentando cancelar tarefa: {tarefa_id_curto} - {nome_tarefa}")
            
            # Buscar a atividade completa pelo ID
            atividade_encontrada = None
            for atividade in self.gerenciador.atividades:
                if atividade.id_atividade.startswith(tarefa_id_curto.replace("...", "")):
                    atividade_encontrada = atividade
                    break
            
            if not atividade_encontrada:
                print(f"❌ Atividade não encontrada para ID: {tarefa_id_curto}")
                messagebox.showerror("Erro", "Tarefa não encontrada no sistema.")
                return
            
            # Verificar se já está cancelada
            if atividade_encontrada.esta_cancelada:
                messagebox.showwarning("Aviso", "Esta tarefa já foi cancelada!")
                return
            
            # Verificar se não está pendente
            if not atividade_encontrada.esta_pendente:
                messagebox.showwarning("Aviso", "Só é possível cancelar tarefas pendentes!")
                return
            
            # Confirmar ação
            resposta = messagebox.askyesno("Confirmar Cancelamento", 
                                          f"Deseja cancelar a tarefa:\n'{nome_tarefa}'?",
                                          icon='warning')
            
            if resposta:
                sucesso = self.gerenciador.cancelar_atividade(atividade_encontrada.id_atividade)
                if sucesso:
                    print(f"✅ Tarefa cancelada com sucesso: {nome_tarefa}")
                    messagebox.showinfo("Tarefa Cancelada", f"Tarefa '{nome_tarefa}' foi cancelada. ❌")
                    self._atualizar_dados()
                    self.gerenciador.salvar_dados()
                else:
                    print(f"❌ Falha ao cancelar tarefa: {nome_tarefa}")
                    messagebox.showerror("Erro", "Não foi possível cancelar a tarefa.")
                    
        except Exception as e:
            print(f"❌ Erro ao cancelar tarefa: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao cancelar tarefa: {str(e)}")
    
    def _atualizar_dados(self):
        """Atualiza todos os dados da interface."""
        try:
            print("🔄 Atualizando dados da interface...")
            self._atualizar_lista_tarefas()
            self._atualizar_lista_moradores()
            self._atualizar_atividades_recentes()
            # Remover auto-atualização de cards do dashboard
            print("✅ Dados atualizados com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar dados: {e}")
            traceback.print_exc()
    
    def _atualizar_dashboard_completo(self):
        """Atualiza completamente o dashboard."""
        try:
            print("🔄 Atualizando dashboard completo...")
            
            # Limpar cards existentes
            for widget in self.cards_container.winfo_children():
                widget.destroy()
            
            # Recriar cards com dados atualizados
            self._criar_cards_estatisticas(self.cards_container)
            
            # Atualizar atividades recentes
            self._atualizar_atividades_recentes()
            
            print("✅ Dashboard atualizado com sucesso!")
            messagebox.showinfo("Dashboard Atualizado", "Dashboard atualizado com os dados mais recentes! 📊")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar dashboard: {e}")
            traceback.print_exc()
    
    def _excluir_tarefa_selecionada(self):
        """Exclui tarefa selecionada permanentemente."""
        try:
            selecao = self.tree_tarefas.selection()
            if not selecao:
                messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para excluir.")
                return
            
            item = self.tree_tarefas.item(selecao[0])
            valores = item['values']
            tarefa_id_curto = valores[0]
            nome_tarefa = valores[2]
            
            print(f"🔄 Tentando excluir tarefa: {tarefa_id_curto} - {nome_tarefa}")
            
            # Buscar a atividade completa pelo ID
            atividade_encontrada = None
            for atividade in self.gerenciador.atividades:
                if atividade.id_atividade.startswith(tarefa_id_curto.replace("...", "")):
                    atividade_encontrada = atividade
                    break
            
            if not atividade_encontrada:
                print(f"❌ Atividade não encontrada para ID: {tarefa_id_curto}")
                messagebox.showerror("Erro", "Tarefa não encontrada no sistema.")
                return
            
            # Confirmar exclusão
            resposta = messagebox.askyesno("Confirmar Exclusão", 
                                          f"⚠️ ATENÇÃO: Esta ação é irreversível!\n\n"
                                          f"Deseja excluir permanentemente a tarefa:\n'{nome_tarefa}'?\n\n"
                                          f"Esta tarefa será completamente removida do sistema.",
                                          icon='warning')
            
            if resposta:
                # Remover da lista de atividades
                self.gerenciador._lista_atividades.remove(atividade_encontrada)
                
                print(f"✅ Tarefa excluída com sucesso: {nome_tarefa}")
                messagebox.showinfo("Tarefa Excluída", f"Tarefa '{nome_tarefa}' foi excluída permanentemente. 🗑️")
                self._atualizar_dados()
                self.gerenciador.salvar_dados()
                
        except Exception as e:
            print(f"❌ Erro ao excluir tarefa: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao excluir tarefa: {str(e)}")
    
    def _editar_morador_selecionado(self):
        """Edita o morador selecionado."""
        try:
            selecao = self.tree_moradores.selection()
            if not selecao:
                messagebox.showwarning("Aviso", "Por favor, selecione um morador para editar.")
                return
            
            item = self.tree_moradores.item(selecao[0])
            nome_morador = item['values'][0].replace("🥇 ", "").replace("🥈 ", "").replace("🥉 ", "")
            
            print(f"🔄 Editando morador: {nome_morador}")
            
            # Buscar morador
            morador_encontrado = None
            for morador in self.gerenciador.obter_moradores():
                if morador.nome == nome_morador:
                    morador_encontrado = morador
                    break
            
            if not morador_encontrado:
                messagebox.showerror("Erro", "Morador não encontrado no sistema.")
                return
            
            # Abrir diálogo de edição
            dialog = EditarMoradorDialog(self.root, morador_encontrado)
            self.root.wait_window(dialog.dialog)
            
            if dialog.resultado:
                print(f"✅ Morador editado: {morador_encontrado.nome}")
                self._atualizar_dados()
                self.gerenciador.salvar_dados()
                messagebox.showinfo("Sucesso!", f"Morador '{morador_encontrado.nome}' editado com sucesso! ✏️")
                
        except Exception as e:
            print(f"❌ Erro ao editar morador: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao editar morador: {str(e)}")
    
    def _excluir_morador_selecionado(self):
        """Exclui o morador selecionado."""
        try:
            selecao = self.tree_moradores.selection()
            if not selecao:
                messagebox.showwarning("Aviso", "Por favor, selecione um morador para excluir.")
                return
            
            item = self.tree_moradores.item(selecao[0])
            nome_morador = item['values'][0].replace("🥇 ", "").replace("🥈 ", "").replace("🥉 ", "")
            
            print(f"🔄 Tentando excluir morador: {nome_morador}")
            
            # Buscar morador
            morador_encontrado = None
            for morador in self.gerenciador.obter_moradores():
                if morador.nome == nome_morador:
                    morador_encontrado = morador
                    break
            
            if not morador_encontrado:
                messagebox.showerror("Erro", "Morador não encontrado no sistema.")
                return
            
            # Verificar se tem tarefas atribuídas
            tarefas_atribuidas = [a for a in self.gerenciador.atividades if a.responsavel_id == morador_encontrado.id]
            
            mensagem_confirmacao = f"⚠️ ATENÇÃO: Esta ação é irreversível!\n\n"
            mensagem_confirmacao += f"Deseja excluir permanentemente o morador:\n'{nome_morador}'?\n\n"
            
            if tarefas_atribuidas:
                mensagem_confirmacao += f"⚠️ Este morador tem {len(tarefas_atribuidas)} tarefa(s) atribuída(s).\n"
                mensagem_confirmacao += "As tarefas ficarão sem responsável.\n\n"
            
            mensagem_confirmacao += "Este morador será completamente removido do sistema."
            
            # Confirmar exclusão
            resposta = messagebox.askyesno("Confirmar Exclusão", mensagem_confirmacao, icon='warning')
            
            if resposta:
                # Remover atribuições das tarefas
                for atividade in tarefas_atribuidas:
                    atividade.responsavel_id = None
                
                # Remover morador
                sucesso = self.gerenciador.remover_morador(morador_encontrado.id)
                
                if sucesso:
                    print(f"✅ Morador excluído com sucesso: {nome_morador}")
                    messagebox.showinfo("Morador Excluído", f"Morador '{nome_morador}' foi excluído permanentemente. 🗑️")
                    self._atualizar_dados()
                    self.gerenciador.salvar_dados()
                else:
                    messagebox.showerror("Erro", "Não foi possível excluir o morador.")
                
        except Exception as e:
            print(f"❌ Erro ao excluir morador: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao excluir morador: {str(e)}")
    
    def _atualizar_atividades_recentes(self):
        """Atualiza lista de atividades recentes."""
        try:
            if hasattr(self, 'lista_recentes'):
                self.lista_recentes.delete(0, tk.END)
                
                atividades = self.gerenciador.atividades[-10:]  # Últimas 10
                if not atividades:
                    self.lista_recentes.insert(tk.END, "📝 Nenhuma atividade cadastrada ainda")
                else:
                    for atividade in reversed(atividades):
                        status_emoji = "✅" if atividade.esta_finalizada else "⏳" if atividade.esta_pendente else "❌"
                        texto = f"{status_emoji} {atividade.nome_tarefa} ({atividade.categoria.value})"
                        self.lista_recentes.insert(tk.END, texto)
                        
        except Exception as e:
            print(f"❌ Erro ao atualizar atividades recentes: {e}")
    
    def _atualizar_lista_tarefas(self):
        """Atualiza lista de tarefas."""
        try:
            # Limpar lista
            for item in self.tree_tarefas.get_children():
                self.tree_tarefas.delete(item)
            
            print(f"📋 Carregando {len(self.gerenciador.atividades)} atividades...")
            
            for atividade in self.gerenciador.atividades:
                responsavel = "Não atribuído"
                if atividade.responsavel_id:
                    morador = self.gerenciador.obter_morador_por_id(atividade.responsavel_id)
                    if morador:
                        responsavel = morador.nome
                
                # Cores por status
                tags = []
                if atividade.esta_finalizada:
                    tags = ['finalizada']
                elif atividade.esta_cancelada:
                    tags = ['cancelada']
                else:
                    tags = ['pendente']
                
                # ID mais curto para exibição
                id_display = atividade.id_atividade[:8] + "..."
                
                self.tree_tarefas.insert('', 'end', values=(
                    id_display,
                    atividade.categoria.value,
                    atividade.nome_tarefa,
                    atividade.situacao.value,
                    responsavel,
                    atividade.pontos_tarefa
                ), tags=tags)
            
            # Configurar cores das tags
            self.tree_tarefas.tag_configure('finalizada', background='#d5f5d5', foreground='#2e7d32')
            self.tree_tarefas.tag_configure('cancelada', background='#f5d5d5', foreground='#c62828')
            self.tree_tarefas.tag_configure('pendente', background='#fff3cd', foreground='#f57c00')
            
            print(f"✅ Lista de tarefas atualizada com {len(self.gerenciador.atividades)} itens")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar lista de tarefas: {e}")
            traceback.print_exc()
    
    def _atualizar_lista_moradores(self):
        """Atualiza lista de moradores."""
        try:
            # Limpar lista
            for item in self.tree_moradores.get_children():
                self.tree_moradores.delete(item)
            
            moradores = self.gerenciador.obter_moradores()
            moradores_ordenados = sorted(moradores, key=lambda m: m.pontos_realizadas, reverse=True)
            
            print(f"👥 Carregando {len(moradores_ordenados)} moradores...")
            
            for i, morador in enumerate(moradores_ordenados):
                status = "🟢 Disponível" if morador.disponivel else "🔴 Indisponível"
                
                # Emoji de posição
                posicao_emoji = ""
                if i == 0 and morador.pontos_realizadas > 0:
                    posicao_emoji = "🥇 "
                elif i == 1 and morador.pontos_realizadas > 0:
                    posicao_emoji = "🥈 "
                elif i == 2 and morador.pontos_realizadas > 0:
                    posicao_emoji = "🥉 "
                
                self.tree_moradores.insert('', 'end', values=(
                    posicao_emoji + morador.nome,
                    morador.pontos_realizadas,
                    morador.total_tarefas_realizadas,
                    morador.nivel_performance,
                    status
                ))
            
            print(f"✅ Lista de moradores atualizada com {len(moradores_ordenados)} itens")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar lista de moradores: {e}")
            traceback.print_exc()
    
    def _gerar_ranking(self):
        """Gera relatório de ranking."""
        try:
            print("🔄 Gerando relatório de ranking...")
            ranking = self.gerenciador.ranking_melhores_moradores()
            
            texto = "🏆 RANKING DOS MORADORES\n"
            texto += "=" * 60 + "\n\n"
            
            if not ranking:
                texto += "😔 Nenhum morador cadastrado ainda.\n"
                texto += "Adicione moradores na aba 'Moradores'!\n"
            else:
                for item in ranking:
                    texto += f"{item['emoji']} {item['nome']}\n"
                    texto += f"   🏆 Pontos: {item['pontos']}\n"
                    texto += f"   📋 Tarefas realizadas: {item['tarefas']}\n"
                    texto += f"   ⭐ Nível: {item['nivel']}\n"
                    texto += "-" * 40 + "\n\n"
            
            self.texto_relatorio.delete(1.0, tk.END)
            self.texto_relatorio.insert(1.0, texto)
            print("✅ Relatório de ranking gerado")
            
        except Exception as e:
            print(f"❌ Erro ao gerar ranking: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao gerar ranking: {str(e)}")
    
    def _gerar_estatisticas_categoria(self):
        """Gera estatísticas por categoria."""
        try:
            print("🔄 Gerando estatísticas por categoria...")
            stats = self.gerenciador.estatisticas_por_categoria()
            
            if 'erro' in stats:
                texto = "❌ ESTATÍSTICAS POR CATEGORIA\n"
                texto += "=" * 60 + "\n\n"
                texto += "😔 Nenhuma atividade encontrada.\n"
                texto += "Crie algumas tarefas na aba 'Tarefas'!\n"
            else:
                texto = "📊 ESTATÍSTICAS POR CATEGORIA\n"
                texto += "=" * 60 + "\n\n"
                
                for categoria, dados in stats['categorias'].items():
                    texto += f"📂 {categoria}\n"
                    texto += f"   📊 Total de atividades: {dados['total_atividades']}\n"
                    texto += f"   ✅ Finalizadas: {dados['finalizadas']}\n"
                    texto += f"   ⏳ Pendentes: {dados['pendentes']}\n"
                    texto += f"   ❌ Canceladas: {dados['canceladas']}\n"
                    texto += f"   📈 Taxa de conclusão: {dados['porcentagem_conclusao']}%\n"
                    texto += f"   🏆 Pontos total: {dados['pontos_total']}\n"
                    texto += f"   ⭐ Pontos médio: {dados['pontos_medio']}\n"
                    texto += "-" * 40 + "\n\n"
            
            self.texto_relatorio.delete(1.0, tk.END)
            self.texto_relatorio.insert(1.0, texto)
            print("✅ Estatísticas por categoria geradas")
            
        except Exception as e:
            print(f"❌ Erro ao gerar estatísticas: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao gerar estatísticas: {str(e)}")
    
    def _gerar_relatorio_performance(self):
        """Gera relatório de performance detalhado."""
        try:
            print("🔄 Gerando relatório de performance...")
            relatorio = self.gerenciador.relatorio_performance_moradores()
            
            if 'erro' in relatorio:
                texto = "❌ RELATÓRIO DE PERFORMANCE\n"
                texto += "=" * 60 + "\n\n"
                texto += "😔 Nenhum morador cadastrado ainda.\n"
            else:
                texto = "📈 RELATÓRIO DE PERFORMANCE DETALHADO\n"
                texto += "=" * 60 + "\n"
                texto += f"📅 Gerado em: {relatorio['data_geracao']}\n"
                texto += f"👥 Total de moradores: {relatorio['total_moradores']}\n\n"
                
                stats_gerais = relatorio['estatisticas_gerais']
                texto += "📊 ESTATÍSTICAS GERAIS:\n"
                texto += f"   🏆 Total de pontos na casa: {stats_gerais['total_pontos']}\n"
                texto += f"   📋 Total de tarefas realizadas: {stats_gerais['total_tarefas']}\n"
                texto += f"   📈 Média de pontos por morador: {stats_gerais['media_pontos']}\n"
                texto += f"   🟢 Moradores disponíveis: {stats_gerais['moradores_disponiveis']}\n\n"
                
                texto += "👤 DETALHES POR MORADOR:\n"
                texto += "=" * 60 + "\n"
                
                for dados in relatorio['moradores']:
                    texto += f"\n🏠 {dados['nome']}\n"
                    texto += f"   🏆 Pontos: {dados['pontos_total']}\n"
                    texto += f"   📋 Tarefas realizadas: {dados['tarefas_realizadas']}\n"
                    texto += f"   ⭐ Nível: {dados['nivel_performance']}\n"
                    texto += f"   📅 Cadastrado há: {dados['tempo_cadastrado']}\n"
                    texto += f"   🎯 Status: {'🟢 Disponível' if dados['disponivel'] else '🔴 Indisponível'}\n"
                    
                    if dados['categorias_favoritas']:
                        texto += f"   ❤️ Categorias favoritas: {', '.join(dados['categorias_favoritas'])}\n"
                    
                    texto += "-" * 40 + "\n"
            
            self.texto_relatorio.delete(1.0, tk.END)
            self.texto_relatorio.insert(1.0, texto)
            print("✅ Relatório de performance gerado")
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório de performance: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")


class NovaAtividadeDialog:
    """Diálogo moderno para criar nova atividade."""
    
    def __init__(self, parent, gerenciador):
        self.resultado = None
        self.gerenciador = gerenciador
        
        print("🔄 Iniciando NovaAtividadeDialog...")
        
        # Cores do tema
        self.cores = {
            'primaria': '#2c3e50',
            'secundaria': '#3498db',
            'sucesso': '#27ae60',
            'perigo': '#e74c3c',
            'fundo': '#ecf0f1',
            'branco': '#ffffff',
            'texto': '#2c3e50'
        }
        
        try:
            # Criar janela modal
            self.dialog = tk.Toplevel(parent)
            self.dialog.title("✨ Nova Atividade Doméstica")
            self.dialog.geometry("520x650")
            self.dialog.configure(bg=self.cores['fundo'])
            self.dialog.transient(parent)
            self.dialog.grab_set()
            self.dialog.resizable(False, False)
            
            # Centralizar diálogo
            self.dialog.update_idletasks()
            x = parent.winfo_x() + (parent.winfo_width() // 2) - (520 // 2)
            y = parent.winfo_y() + (parent.winfo_height() // 2) - (650 // 2)
            self.dialog.geometry(f"520x650+{x}+{y}")
            
            self._criar_interface()
            
            # Focar no primeiro campo
            self.combo_categoria.focus_set()
            
            print("✅ NovaAtividadeDialog criado com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao criar NovaAtividadeDialog: {e}")
            traceback.print_exc()
    
    def _criar_interface(self):
        """Cria interface do diálogo."""
        try:
            # Header
            header = tk.Frame(self.dialog, bg=self.cores['primaria'], height=90)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            titulo = tk.Label(header, text="✨ Nova Atividade Doméstica",
                             font=('Arial', 18, 'bold'),
                             bg=self.cores['primaria'], fg=self.cores['branco'])
            titulo.pack(pady=(25, 5))
            
            subtitulo = tk.Label(header, text="Preencha os dados da nova tarefa",
                               font=('Arial', 11),
                               bg=self.cores['primaria'], fg=self.cores['branco'])
            subtitulo.pack()
            
            # Container principal
            main_frame = tk.Frame(self.dialog, bg=self.cores['branco'], relief='solid', borderwidth=1)
            main_frame.pack(fill='both', expand=True, padx=15, pady=15)
            
            # Categoria
            self._criar_campo_label(main_frame, "📂 Categoria:", 0)
            categorias = [cat.value for cat in CategoriaAtividade]
            self.combo_categoria = ttk.Combobox(main_frame, values=categorias, 
                                               font=('Arial', 12), width=45,
                                               state='readonly')
            self.combo_categoria.grid(row=1, column=0, columnspan=2, pady=(5, 20), padx=15, sticky='ew')
            
            # Nome da Tarefa
            self._criar_campo_label(main_frame, "📝 Nome da Tarefa:", 2)
            self.entry_nome = tk.Entry(main_frame, font=('Arial', 12), width=48,
                                      relief='solid', borderwidth=1)
            self.entry_nome.grid(row=3, column=0, columnspan=2, pady=(5, 20), padx=15, sticky='ew')
            
            # Descrição
            self._criar_campo_label(main_frame, "📄 Descrição (opcional):", 4)
            desc_frame = tk.Frame(main_frame, bg=self.cores['branco'])
            desc_frame.grid(row=5, column=0, columnspan=2, pady=(5, 20), padx=15, sticky='ew')
            
            self.text_descricao = tk.Text(desc_frame, height=4, width=45, font=('Arial', 11),
                                         relief='solid', borderwidth=1, wrap='word')
            scrollbar_desc = ttk.Scrollbar(desc_frame, orient='vertical', command=self.text_descricao.yview)
            self.text_descricao.configure(yscrollcommand=scrollbar_desc.set)
            
            self.text_descricao.pack(side='left', fill='both', expand=True)
            scrollbar_desc.pack(side='right', fill='y')
            
            # Responsável
            self._criar_campo_label(main_frame, "👤 Responsável:", 6)
            moradores = ["🎯 Atribuir depois"] + [f"👤 {m.nome}" for m in self.gerenciador.obter_moradores()]
            self.combo_responsavel = ttk.Combobox(main_frame, values=moradores,
                                                 font=('Arial', 12), width=45,
                                                 state='readonly')
            self.combo_responsavel.set("🎯 Atribuir depois")
            self.combo_responsavel.grid(row=7, column=0, columnspan=2, pady=(5, 30), padx=15, sticky='ew')
            
            # Botões
            self._criar_botoes(main_frame)
            
            # Configurar responsividade
            main_frame.grid_columnconfigure(0, weight=1)
            main_frame.grid_columnconfigure(1, weight=1)
            
        except Exception as e:
            print(f"❌ Erro ao criar interface do diálogo: {e}")
            traceback.print_exc()
    
    def _criar_campo_label(self, parent, texto, row):
        """Cria label para campo."""
        label = tk.Label(parent, text=texto, font=('Arial', 12, 'bold'),
                        bg=self.cores['branco'], fg=self.cores['texto'])
        label.grid(row=row, column=0, columnspan=2, sticky='w', padx=15, pady=(10, 0))
    
    def _criar_botoes(self, parent):
        """Cria botões do diálogo."""
        botoes_frame = tk.Frame(parent, bg=self.cores['branco'])
        botoes_frame.grid(row=8, column=0, columnspan=2, pady=25)
        
        # Botão Criar
        btn_criar = tk.Button(botoes_frame, text="✨ Criar Atividade", 
                             command=self._criar_atividade,
                             bg=self.cores['sucesso'], fg=self.cores['branco'],
                             font=('Arial', 12, 'bold'),
                             relief='flat', borderwidth=0,
                             padx=25, pady=12, cursor='hand2')
        btn_criar.pack(side='left', padx=10)
        
        # Botão Cancelar
        btn_cancelar = tk.Button(botoes_frame, text="❌ Cancelar",
                                command=self.dialog.destroy,
                                bg=self.cores['perigo'], fg=self.cores['branco'],
                                font=('Arial', 12, 'bold'),
                                relief='flat', borderwidth=0,
                                padx=25, pady=12, cursor='hand2')
        btn_cancelar.pack(side='left', padx=10)
        
        # Efeitos hover nos botões
        self._adicionar_hover_efeito(btn_criar, self.cores['sucesso'])
        self._adicionar_hover_efeito(btn_cancelar, self.cores['perigo'])
        
        # Bind Enter para criar
        self.dialog.bind('<Return>', lambda e: self._criar_atividade())
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
    
    def _adicionar_hover_efeito(self, botao, cor_original):
        """Adiciona efeito hover ao botão."""
        try:
            cor_hover = self._escurecer_cor(cor_original)
            
            def on_enter(e):
                botao.configure(bg=cor_hover)
            
            def on_leave(e):
                botao.configure(bg=cor_original)
            
            botao.bind("<Enter>", on_enter)
            botao.bind("<Leave>", on_leave)
        except:
            pass
    
    def _escurecer_cor(self, cor):
        """Escurece uma cor hexadecimal."""
        try:
            cor = cor.lstrip('#')
            rgb = tuple(int(cor[i:i+2], 16) for i in (0, 2, 4))
            rgb_escuro = tuple(max(0, c - 30) for c in rgb)
            return f"#{rgb_escuro[0]:02x}{rgb_escuro[1]:02x}{rgb_escuro[2]:02x}"
        except:
            return cor
    
    def _criar_atividade(self):
        """Cria a atividade com validação."""
        try:
            print("🔄 Tentando criar atividade...")
            
            categoria_nome = self.combo_categoria.get()
            nome = self.entry_nome.get().strip()
            descricao = self.text_descricao.get(1.0, tk.END).strip()
            responsavel_text = self.combo_responsavel.get()
            
            # Validações
            if not categoria_nome:
                messagebox.showerror("Erro", "Por favor, selecione uma categoria!", parent=self.dialog)
                self.combo_categoria.focus_set()
                return
            
            if not nome:
                messagebox.showerror("Erro", "Por favor, digite o nome da tarefa!", parent=self.dialog)
                self.entry_nome.focus_set()
                return
            
            if len(nome) < 3:
                messagebox.showerror("Erro", "O nome da tarefa deve ter pelo menos 3 caracteres!", parent=self.dialog)
                self.entry_nome.focus_set()
                return
            
            # Obter categoria
            categoria = None
            for cat in CategoriaAtividade:
                if cat.value == categoria_nome:
                    categoria = cat
                    break
            
            if not categoria:
                messagebox.showerror("Erro", "Categoria inválida!", parent=self.dialog)
                return
            
            # Obter responsável
            responsavel_id = None
            if responsavel_text and not responsavel_text.startswith("🎯"):
                nome_responsavel = responsavel_text.replace("👤 ", "")
                for morador in self.gerenciador.obter_moradores():
                    if morador.nome == nome_responsavel:
                        responsavel_id = morador.id
                        break
            
            # Criar atividade
            atividade = self.gerenciador.criar_nova_atividade(categoria, nome, descricao, responsavel_id)
            
            if atividade:
                print(f"✅ Atividade criada com sucesso: {nome}")
                self.resultado = atividade
                self.dialog.destroy()
            else:
                print(f"❌ Falha ao criar atividade: {nome}")
                messagebox.showerror("Erro", "Não foi possível criar a atividade.\nTente novamente.", parent=self.dialog)
                
        except Exception as e:
            print(f"❌ Erro ao criar atividade: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao criar atividade:\n{str(e)}", parent=self.dialog)


class EditarMoradorDialog:
    """Diálogo para editar dados do morador."""
    
    def __init__(self, parent, morador):
        self.resultado = False
        self.morador = morador
        
        print(f"🔄 Iniciando EditarMoradorDialog para: {morador.nome}")
        
        # Cores do tema
        self.cores = {
            'primaria': '#2c3e50',
            'secundaria': '#3498db',
            'sucesso': '#27ae60',
            'perigo': '#e74c3c',
            'fundo': '#ecf0f1',
            'branco': '#ffffff',
            'texto': '#2c3e50'
        }
        
        try:
            # Criar janela modal
            self.dialog = tk.Toplevel(parent)
            self.dialog.title("✏️ Editar Morador")
            self.dialog.geometry("450x400")
            self.dialog.configure(bg=self.cores['fundo'])
            self.dialog.transient(parent)
            self.dialog.grab_set()
            self.dialog.resizable(False, False)
            
            # Centralizar diálogo
            self.dialog.update_idletasks()
            x = parent.winfo_x() + (parent.winfo_width() // 2) - (450 // 2)
            y = parent.winfo_y() + (parent.winfo_height() // 2) - (400 // 2)
            self.dialog.geometry(f"450x400+{x}+{y}")
            
            self._criar_interface()
            
            # Focar no campo nome
            self.entry_nome.focus_set()
            self.entry_nome.select_range(0, tk.END)
            
            print("✅ EditarMoradorDialog criado com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao criar EditarMoradorDialog: {e}")
            traceback.print_exc()
    
    def _criar_interface(self):
        """Cria interface do diálogo de edição."""
        try:
            # Header
            header = tk.Frame(self.dialog, bg=self.cores['primaria'], height=80)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            titulo = tk.Label(header, text="✏️ Editar Dados do Morador",
                             font=('Arial', 16, 'bold'),
                             bg=self.cores['primaria'], fg=self.cores['branco'])
            titulo.pack(pady=(20, 5))
            
            subtitulo = tk.Label(header, text=f"Editando: {self.morador.nome}",
                               font=('Arial', 11),
                               bg=self.cores['primaria'], fg=self.cores['branco'])
            subtitulo.pack()
            
            # Container principal
            main_frame = tk.Frame(self.dialog, bg=self.cores['branco'], relief='solid', borderwidth=1)
            main_frame.pack(fill='both', expand=True, padx=15, pady=15)
            
            # Nome
            self._criar_campo_label(main_frame, "👤 Nome:", 0)
            self.entry_nome = tk.Entry(main_frame, font=('Arial', 12), width=35,
                                      relief='solid', borderwidth=1)
            self.entry_nome.insert(0, self.morador.nome)
            self.entry_nome.grid(row=1, column=0, columnspan=2, pady=(5, 15), padx=15, sticky='ew')
            
            # Disponibilidade
            self._criar_campo_label(main_frame, "🎯 Disponibilidade:", 2)
            self.var_disponibilidade = tk.BooleanVar(value=self.morador.disponivel)
            
            frame_disponibilidade = tk.Frame(main_frame, bg=self.cores['branco'])
            frame_disponibilidade.grid(row=3, column=0, columnspan=2, pady=(5, 15), padx=15, sticky='w')
            
            radio_disponivel = tk.Radiobutton(frame_disponibilidade, text="🟢 Disponível", 
                                            variable=self.var_disponibilidade, value=True,
                                            font=('Arial', 11), bg=self.cores['branco'])
            radio_disponivel.pack(side='left', padx=(0, 20))
            
            radio_indisponivel = tk.Radiobutton(frame_disponibilidade, text="🔴 Indisponível", 
                                              variable=self.var_disponibilidade, value=False,
                                              font=('Arial', 11), bg=self.cores['branco'])
            radio_indisponivel.pack(side='left')
            
            # Informações do morador (somente leitura)
            self._criar_campo_label(main_frame, "📊 Informações Atuais:", 4)
            
            info_frame = tk.Frame(main_frame, bg='#f8f9fa', relief='solid', borderwidth=1)
            info_frame.grid(row=5, column=0, columnspan=2, pady=(5, 20), padx=15, sticky='ew')
            
            info_text = f"""🏆 Pontos: {self.morador.pontos_realizadas}
📋 Tarefas realizadas: {self.morador.total_tarefas_realizadas}
⭐ Nível: {self.morador.nivel_performance}
📅 Cadastrado há: {self.morador.tempo_cadastrado()}"""
            
            info_label = tk.Label(info_frame, text=info_text, font=('Arial', 10),
                                bg='#f8f9fa', fg=self.cores['texto'], justify='left')
            info_label.pack(padx=15, pady=10)
            
            # Botões
            self._criar_botoes(main_frame)
            
            # Configurar responsividade
            main_frame.grid_columnconfigure(0, weight=1)
            main_frame.grid_columnconfigure(1, weight=1)
            
        except Exception as e:
            print(f"❌ Erro ao criar interface de edição: {e}")
            traceback.print_exc()
    
    def _criar_campo_label(self, parent, texto, row):
        """Cria label para campo."""
        label = tk.Label(parent, text=texto, font=('Arial', 12, 'bold'),
                        bg=self.cores['branco'], fg=self.cores['texto'])
        label.grid(row=row, column=0, columnspan=2, sticky='w', padx=15, pady=(10, 0))
    
    def _criar_botoes(self, parent):
        """Cria botões do diálogo."""
        botoes_frame = tk.Frame(parent, bg=self.cores['branco'])
        botoes_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Botão Salvar
        btn_salvar = tk.Button(botoes_frame, text="💾 Salvar Alterações", 
                             command=self._salvar_alteracoes,
                             bg=self.cores['sucesso'], fg=self.cores['branco'],
                             font=('Arial', 12, 'bold'),
                             relief='flat', borderwidth=0,
                             padx=20, pady=10, cursor='hand2')
        btn_salvar.pack(side='left', padx=8)
        
        # Botão Cancelar
        btn_cancelar = tk.Button(botoes_frame, text="❌ Cancelar",
                                command=self.dialog.destroy,
                                bg=self.cores['perigo'], fg=self.cores['branco'],
                                font=('Arial', 12, 'bold'),
                                relief='flat', borderwidth=0,
                                padx=20, pady=10, cursor='hand2')
        btn_cancelar.pack(side='left', padx=8)
        
        # Bind Enter para salvar
        self.dialog.bind('<Return>', lambda e: self._salvar_alteracoes())
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
    
    def _salvar_alteracoes(self):
        """Salva as alterações do morador."""
        try:
            novo_nome = self.entry_nome.get().strip()
            nova_disponibilidade = self.var_disponibilidade.get()
            
            # Validar nome
            if not novo_nome:
                messagebox.showerror("Erro", "O nome não pode estar vazio!", parent=self.dialog)
                self.entry_nome.focus_set()
                return
            
            if len(novo_nome) < 2:
                messagebox.showerror("Erro", "O nome deve ter pelo menos 2 caracteres!", parent=self.dialog)
                self.entry_nome.focus_set()
                return
            
            # Aplicar alterações
            self.morador.nome = novo_nome
            self.morador.disponivel = nova_disponibilidade
            
            print(f"✅ Morador editado: {novo_nome}, Disponível: {nova_disponibilidade}")
            
            self.resultado = True
            self.dialog.destroy()
            
        except Exception as e:
            print(f"❌ Erro ao salvar alterações: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao salvar alterações:\n{str(e)}", parent=self.dialog)