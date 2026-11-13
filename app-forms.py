import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


class SistemaCadastroClientes:

    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Clientes")
        self.root.geometry("460x260")
        self.root.resizable(False, False)

        # Inicializa o banco de dados e cria a tabela
        self.criar_banco()

        # Configura os elementos da interface gráfica
        self.criar_interface()

    def criar_banco(self):
        """Cria a conexão com o SQLite e a tabela de clientes, se não existir."""
        conexao = sqlite3.connect("clientes.db")
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        """)
        conexao.commit()
        conexao.close()

    def criar_interface(self):
        """Constrói os rótulos, campos de entrada e botões do formulário."""
        frame_principal = tk.Frame(self.root, padx=20, pady=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Campo: Nome
        tk.Label(frame_principal, text="Nome Completo:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.entry_nome = tk.Entry(frame_principal, width=36, font=("Arial", 10))
        self.entry_nome.grid(row=0, column=1, pady=5, padx=(10, 0))

        # Campo: E-mail
        tk.Label(frame_principal, text="E-mail:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.entry_email = tk.Entry(
            frame_principal, width=36, font=("Arial", 10)
        )
        self.entry_email.grid(row=1, column=1, pady=5, padx=(10, 0))

        # Campo: Telefone
        tk.Label(frame_principal, text="Telefone:", font=("Arial", 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.entry_telefone = tk.Entry(
            frame_principal, width=36, font=("Arial", 10)
        )
        self.entry_telefone.grid(row=2, column=1, pady=5, padx=(10, 0))

        # Frame para os botões
        frame_botoes = tk.Frame(frame_principal)
        frame_botoes.grid(row=3, column=0, columnspan=2, pady=25)

        # Botão Salvar
        btn_salvar = tk.Button(
            frame_botoes,
            text="Salvar",
            width=12,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.salvar_cliente,
        )
        btn_salvar.pack(side=tk.LEFT, padx=5)

        # Botão Limpar
        btn_limpar = tk.Button(
            frame_botoes,
            text="Limpar",
            width=12,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.limpar_formulario,
        )
        btn_limpar.pack(side=tk.LEFT, padx=5)

        # Botão Visualizar Clientes (Novo requisito)
        btn_visualizar = tk.Button(
            frame_botoes,
            text="Visualizar Clientes",
            width=16,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.visualizar_clientes,
        )
        btn_visualizar.pack(side=tk.LEFT, padx=5)

    def salvar_cliente(self):
        """Valida os campos e insere os dados no banco de dados SQLite."""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()

        # Validação de preenchimento obrigatório
        if not nome or not email or not telefone:
            messagebox.showwarning(
                "Campos Obrigatórios",
                "Por favor, preencha todos os campos (Nome, E-mail e Telefone).",
            )
            return

        try:
            conexao = sqlite3.connect("clientes.db")
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                (nome, email, telefone),
            )
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.limpar_formulario()

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro no Banco de Dados", f"Não foi possível salvar: {erro}"
            )

    def limpar_formulario(self):
        """Limpa todos os campos de entrada e retorna o foco ao primeiro campo."""
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_nome.focus_set()

    def visualizar_clientes(self):
        """Abre uma nova janela exibindo todos os clientes cadastrados no banco."""
        try:
            conexao = sqlite3.connect("clientes.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes")
            registros = cursor.fetchall()
            conexao.close()
        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro no Banco de Dados", f"Não foi possível carregar os dados: {erro}"
            )
            return

        # Cria a nova janela secundária (Toplevel)
        janela_lista = tk.Toplevel(self.root)
        janela_lista.title("Clientes Cadastrados")
        janela_lista.geometry("620x350")

        frame_tabela = tk.Frame(janela_lista, padx=15, pady=15)
        frame_tabela.pack(fill=tk.BOTH, expand=True)

        # Configuração da tabela (Treeview)
        colunas = ("id", "nome", "email", "telefone")
        tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        tabela.heading("id", text="ID")
        tabela.heading("nome", text="Nome Completo")
        tabela.heading("email", text="E-mail")
        tabela.heading("telefone", text="Telefone")

        tabela.column("id", width=50, anchor=tk.CENTER)
        tabela.column("nome", width=200, anchor=tk.W)
        tabela.column("email", width=200, anchor=tk.W)
        tabela.column("telefone", width=120, anchor=tk.CENTER)

        # Barra de rolagem vertical
        scrollbar = ttk.Scrollbar(
            frame_tabela, orient=tk.VERTICAL, command=tabela.yview
        )
        tabela.configure(yscrollcommand=scrollbar.set)

        tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Preenche a tabela com os registros do SQLite
        for cliente in registros:
            tabela.insert("", tk.END, values=cliente)


if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaCadastroClientes(janela)
    janela.mainloop()
