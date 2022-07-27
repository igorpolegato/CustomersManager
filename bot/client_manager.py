from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

from data import *
from excel_extractor import data as dt

from time import sleep
from datetime import datetime, timedelta

app = Client(bot_name,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token)


with app:
    pass

monitoring = False
removidos = []

@app.on_message(filters.private & filters.command("start"))
def start(bot, mensagem):
    user_id = mensagem.chat.id
    if permitido(user_id):
        app.send_message(user_id, "Olá, sejá bem vindo!")
        helpC(bot, mensagem)
    
    else:
        app.send_message(user_id, "Sinto muito, mas você não possui permissão para utilizar este bot!")

@app.on_message(filters.private & filters.command("help"))
def helpC(bot, mensagem):
    user_id = mensagem.chat.id
    
    if permitido(user_id):
        btns = [
            [InlineKeyboardButton("Iniciar/Parar Monitoramento", callback_data="help_mon")],
            [InlineKeyboardButton("Verificar datas", callback_data="help_vd")]
        ]

        markup = InlineKeyboardMarkup(btns)

        app.send_message(user_id, "Esses são minhas funções!\n\nSelecione o que deseja fazer", reply_markup=markup)
    
    else:
        app.send_message(user_id, "Sinto muito, mas você não possui permissão para utilizar este bot!")

@app.on_message(filters.private & filters.command("verificar"))
def verificar(bot, mensagem):
    user_id = mensagem.chat.id
    
    if permitido(user_id):
        dados ={}
        users = dt(name="confirmação chat vip", coluna="ID")
        nomes = dt(name="confirmação chat vip", coluna="Usuario")
        dates = dt(name="confirmação chat vip", coluna="Data")


        for i in range(len(users)):
            dados[users[i]] = [nomes[i], dates[i].date()]
        
        for k, v in dados.items():
            nome, date = v

            if date < datetime.now().date():
                if k not in removidos:
                    app.ban_chat_member(gp_id, k, datetime.now() + timedelta(seconds=10))

                    for u in pmu:

                        app.send_message(u, f"O usuário {nome} foi removido do canal!")
                        print(f"O usuário {nome} foi removido do canal!\n")

                    removidos.append(k)


    else:
        app.send_message(user_id, "Sinto muito, mas você não possui permissão para utilizar este bot!")

@app.on_message(filters.private & filters.command("monitorar"))
def atualizar(bot, mensagem):
    global monitoring
    user_id = mensagem.chat.id

    if permitido(user_id):

        if monitoring:
            app.send_message(user_id, "O monitoramento foi pausado!")
            monitoring = False

        else:
            app.send_message(user_id, "O monitoramento foi iniciado!")
            monitoring = True
            monitorar()

    else:
        app.send_message(user_id, "Sinto muito, mas você não possui permissão para utilizar este bot!")

def monitorar():
    while monitoring:
        dados = {}
        try:
            users = dt(name="confirmação chat vip", coluna="ID")
            nomes = dt(name="confirmação chat vip", coluna="Usuario")
            status = dt(name="confirmação chat vip", coluna="Status")

            for i in range(len(users)):
                dados[users[i]] = [nomes[i], status[i]]

            for k, v in dados.items():
                nome, lib = v
                if k in removidos and lib == "liberado":
                    removidos.remove(k)
                
                if lib == "bloqueado" and k not in removidos:
                    try:
                        app.ban_chat_member(gp_id, k, datetime.now() + timedelta(seconds=10))
                        removidos.append(k)
                        for u in pmu:
                            app.send_message(u, f"O usuário {nome} foi removido do canal!")
                            print(f"O usuário {nome} foi removido do canal!\n")
                    except Exception:
                        pass
        
        except Exception:
            print("Nenhum arquivo localizado!")
        sleep(1)

def permitido(user_id):
    return user_id in pmu

@app.on_callback_query(filters.regex("^help_mon"))
def callMonitorar(bot, call):
    data = call.message

    atualizar(bot, data)

@app.on_callback_query(filters.regex("^help_vd"))
def callVerificar(bot, call):
    data = call.message

    verificar(bot, data)

if __name__ == "__main__":
    print("+---------------------+\n"
          "| ManagerBot Iniciado |\n"
          "+---------------------+\n")
    app.run()
