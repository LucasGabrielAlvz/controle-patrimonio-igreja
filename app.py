"""
Sistema de Controle de Patrimônio Institucional
Interface desktop feita com Tkinter, conectada a um banco MySQL.

Como executar:
    1. pip install -r requirements.txt
    2. Rode o schema.sql no seu MySQL (mysql -u root -p < schema.sql)
    3. Edite db.py com o usuário/senha do seu MySQL
    4. python app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

import db


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Controle de Patrimônio Institucional")
        self.geometry("820x520")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.aba_departamentos = AbaDepartamentos(notebook)
        self.aba_itens = AbaItens(notebook)
        self.aba_movimentacao = AbaMovimentacao(notebook)
        self.aba_relatorio = AbaRelatorio(notebook)

        notebook.add(self.aba_departamentos, text="Departamentos")
        notebook.add(self.aba_itens, text="Itens")
        notebook.add(self.aba_movimentacao, text="Movimentação")
        notebook.add(self.aba_relatorio, text="Relatório")

        # Atualiza combos dependentes quando o usuário troca de aba
        notebook.bind("<<NotebookTabChanged>>", lambda e: self.atualizar_tudo())

    def atualizar_tudo(self):
        self.aba_itens.atualizar_departamentos()
        self.aba_itens.atualizar_lista()
        self.aba_movimentacao.atualizar_listas()
        self.aba_relatorio.atualizar()


class AbaDepartamentos(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Novo departamento/setor:").pack(anchor="w", padx=10, pady=(10, 0))
        linha = ttk.Frame(self)
        linha.pack(fill="x", padx=10, pady=5)
        self.entry_nome = ttk.Entry(linha)
        self.entry_nome.pack(side="left", fill="x", expand=True)
        ttk.Button(linha, text="Adicionar", command=self.adicionar).pack(side="left", padx=5)

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        self.atualizar_lista()

    def adicionar(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Informe o nome do departamento.")
            return
        try:
            db.adicionar_departamento(nome)
            self.entry_nome.delete(0, tk.END)
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        try:
            for _id, nome in db.listar_departamentos():
                self.lista.insert(tk.END, nome)
        except Exception as e:
            messagebox.showerror("Erro de conexão", str(e))


class AbaItens(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        form = ttk.LabelFrame(self, text="Cadastrar novo item")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.entry_nome = ttk.Entry(form, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=3)

        ttk.Label(form, text="Categoria:").grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.entry_categoria = ttk.Entry(form, width=20)
        self.entry_categoria.grid(row=0, column=3, padx=5, pady=3)

        ttk.Label(form, text="Valor (R$):").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.entry_valor = ttk.Entry(form, width=15)
        self.entry_valor.grid(row=1, column=1, sticky="w", padx=5, pady=3)

        ttk.Label(form, text="Departamento:").grid(row=1, column=2, sticky="w", padx=5, pady=3)
        self.combo_departamento = ttk.Combobox(form, state="readonly", width=20)
        self.combo_departamento.grid(row=1, column=3, padx=5, pady=3)

        ttk.Button(form, text="Cadastrar item", command=self.cadastrar).grid(
            row=2, column=0, columnspan=4, pady=8
        )

        colunas = ("nome", "categoria", "valor", "departamento", "status")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings")
        for col, titulo in zip(colunas, ["Nome", "Categoria", "Valor", "Departamento", "Status"]):
            self.tabela.heading(col, text=titulo)
        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

        self._departamentos_map = {}
        self.atualizar_departamentos()
        self.atualizar_lista()

    def atualizar_departamentos(self):
        try:
            deps = db.listar_departamentos()
        except Exception:
            deps = []
        self._departamentos_map = {nome: _id for _id, nome in deps}
        self.combo_departamento["values"] = list(self._departamentos_map.keys())

    def cadastrar(self):
        nome = self.entry_nome.get().strip()
        categoria = self.entry_categoria.get().strip()
        valor = self.entry_valor.get().strip()
        dep_nome = self.combo_departamento.get()

        if not nome or not dep_nome:
            messagebox.showwarning("Aviso", "Preencha ao menos o nome e o departamento.")
            return

        dep_id = self._departamentos_map.get(dep_nome)
        try:
            db.adicionar_item(
                nome, categoria, float(valor) if valor else None,
                date.today().isoformat(), dep_id,
            )
            self.entry_nome.delete(0, tk.END)
            self.entry_categoria.delete(0, tk.END)
            self.entry_valor.delete(0, tk.END)
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_lista(self):
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)
        try:
            for _id, nome, categoria, valor, dep_nome, status in db.listar_itens():
                self.tabela.insert(
                    "", tk.END,
                    values=(nome, categoria or "-", valor or "-", dep_nome or "-", status),
                )
        except Exception as e:
            messagebox.showerror("Erro de conexão", str(e))


class AbaMovimentacao(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        retirar = ttk.LabelFrame(self, text="Registrar retirada de item")
        retirar.pack(fill="x", padx=10, pady=10)

        ttk.Label(retirar, text="Item disponível:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_item = ttk.Combobox(retirar, state="readonly", width=30)
        self.combo_item.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(retirar, text="Responsável:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_responsavel = ttk.Entry(retirar, width=25)
        self.entry_responsavel.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(retirar, text="Registrar retirada", command=self.retirar).grid(
            row=0, column=4, padx=8
        )

        devolver = ttk.LabelFrame(self, text="Itens em uso (clique e depois em Devolver)")
        devolver.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ("item", "responsavel", "data_retirada")
        self.tabela = ttk.Treeview(devolver, columns=colunas, show="headings")
        for col, titulo in zip(colunas, ["Item", "Responsável", "Retirado em"]):
            self.tabela.heading(col, text=titulo)
        self.tabela.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Button(devolver, text="Registrar devolução", command=self.devolver).pack(pady=5)

        self._itens_map = {}
        self._mov_map = {}
        self.atualizar_listas()

    def atualizar_listas(self):
        try:
            disponiveis = db.listar_itens_disponiveis()
        except Exception:
            disponiveis = []
        self._itens_map = {nome: _id for _id, nome in disponiveis}
        self.combo_item["values"] = list(self._itens_map.keys())

        for linha in self.tabela.get_children():
            self.tabela.delete(linha)
        try:
            em_uso = db.listar_itens_em_uso()
        except Exception:
            em_uso = []
        self._mov_map = {}
        for mov_id, nome_item, responsavel, data_retirada in em_uso:
            iid = self.tabela.insert("", tk.END, values=(nome_item, responsavel, data_retirada))
            self._mov_map[iid] = mov_id

    def retirar(self):
        nome_item = self.combo_item.get()
        responsavel = self.entry_responsavel.get().strip()
        if not nome_item or not responsavel:
            messagebox.showwarning("Aviso", "Selecione o item e informe o responsável.")
            return
        item_id = self._itens_map.get(nome_item)
        try:
            db.registrar_retirada(item_id, responsavel)
            self.entry_responsavel.delete(0, tk.END)
            self.atualizar_listas()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def devolver(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item na lista de itens em uso.")
            return
        iid = selecionado[0]
        mov_id = self._mov_map.get(iid)
        # Recupera o item_id a partir do nome mostrado na tabela (busca simples)
        nome_item = self.tabela.item(iid, "values")[0]
        try:
            # Busca o id do item pelo nome (suficiente para este MVP)
            itens = db.listar_itens()
            item_id = next((i[0] for i in itens if i[1] == nome_item), None)
            db.registrar_devolucao(mov_id, item_id)
            self.atualizar_listas()
        except Exception as e:
            messagebox.showerror("Erro", str(e))


class AbaRelatorio(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Button(self, text="Atualizar relatório", command=self.atualizar).pack(pady=10)

        colunas = ("departamento", "total", "em_uso")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings")
        for col, titulo in zip(colunas, ["Departamento", "Total de itens", "Itens em uso"]):
            self.tabela.heading(col, text=titulo)
        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)
        self.atualizar()

    def atualizar(self):
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)
        try:
            for nome, total, em_uso in db.relatorio_por_departamento():
                self.tabela.insert("", tk.END, values=(nome, total, em_uso or 0))
        except Exception as e:
            messagebox.showerror("Erro de conexão", str(e))


if __name__ == "__main__":
    App().mainloop()
