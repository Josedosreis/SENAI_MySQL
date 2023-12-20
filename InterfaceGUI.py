import PySimpleGUI as sg
import mysql.connector
from mysql.connector import Error

class TabelaEstudantesApp:
    def __init__(self):
        # Definir o layout da interface gráfica
        layout = [
            [sg.Text("SENAI - LISTA DE CHAMADA", font=("Helvetica", 16))],
            [sg.Text("Matrícula", size=(15, 1)), sg.Text("Nome", size=(30, 1))],
            [sg.Listbox(values=[], size=(50, 10), key="-LISTA-")],
            [sg.Button("Atualizar Lista", key="-ATUALIZAR-")],
            [sg.Text("Nova Matrícula:"), sg.InputText(key='nova_matricula')],
            [sg.Text("Novo Nome:"), sg.InputText(key='novo_nome')],
            [sg.Button("Inserir Novo Estudante", key='-INSERIR-')]
        ]

        # Criar a janela
        self.window = sg.Window("Lista de Estudantes", layout, finalize=True)

        # Conectar ao banco de dados
        self.conexao = self.conectar()
        self.atualizar_lista()

    def conectar(self):
        try:
            dbconfig = {
                'host': '127.0.0.1',
                'user': 'Python',
                'password': 'Python21',
                'database': 'escola',
            }

            con = mysql.connector.connect(**dbconfig)
            return con
        except(Exception, Error) as error:
            print('Não conectou! ' + str(error))

    def atualizar_lista(self):
        # Estabelecer a conexão
        cursor = self.conexao.cursor()

        query = '''SELECT * FROM estudante;'''

        try:
            cursor.execute(query)
            resultados = [f"{campo[0]:<15} {campo[1]:<30}" for campo in cursor.fetchall()]
            self.window["-LISTA-"].update(values=resultados)

        except(Exception, Error) as error:
            print('Conectou mas não funcionou! ' + str(error))
        finally:
            if self.conexao is not None:
                cursor.close()

    def inserir_novo_estudante(self, matricula, nome):
        cursor = self.conexao.cursor()
        query = '''INSERT INTO estudante(matricula, nome) VALUES(%s, %s);'''

        try:
            cursor.execute(query, (matricula, nome))
            self.conexao.commit()
            sg.popup('Estudante inserido com sucesso!')
            self.atualizar_lista()

        except(Exception, Error) as error:
            sg.popup_error(f'Erro ao inserir estudante: {str(error)}')
        finally:
            cursor.close()

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == "-ATUALIZAR-":
                self.atualizar_lista()
            elif event == '-INSERIR-':
                nova_matricula = values['nova_matricula']
                novo_nome = values['novo_nome']
                self.inserir_novo_estudante(nova_matricula, novo_nome)

        self.window.close()

# Criar e iniciar a aplicação
app = TabelaEstudantesApp()
app.run()
