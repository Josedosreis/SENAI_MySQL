import PySimpleGUI as psg 
from CRUD import conectar, read, create

layout = [
    [psg.Text('Matrícula:'), psg.InputText(key='matricula')],
    [psg.Text('Nome:'), psg.InputText(key='nome')],
    [psg.Button('Inserir'), psg.Button('Atualizar'), psg.Button('Excluir'), psg.Button('Listar'), psg.Button('Sair')],
]

janela = psg.Window('PySimpleGUI + MySQL', layout)

con = conectar()

while True:
    eventos, valores = janela.read()

    if eventos == psg.WIN_CLOSED or eventos == 'Sair':
        break
    elif eventos == 'Inserir':
        create(con, [(valores['matricula'], valores['nome'])])
    elif eventos == 'Atualizar':
        # Implemente a função update
        pass
    elif eventos == 'Excluir':
        # Implemente a função delete
        pass
    elif eventos == 'Listar':
        data = read(con)
        psg.popup_scrolled(str(data), title='Lista de Estudantes')

janela.close()