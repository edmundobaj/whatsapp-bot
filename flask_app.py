from flask import Flask, request, session
from flask_session import Session
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/bot', methods=['POST'])
def bot():    
    incoming_msg = request.values.get('Body', '').lower()
    print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if not responded and session.get("client_id") == request.remote_addr and session.get("level") == "3" and session.get("option") == "1":
        session["level"] = "3"
        session.pop('option', None)
        mensagem = "Digite seu Nome Completo..."
        msg.body(mensagem)
        responded = True
    if not responded and '1' in incoming_msg and session.get("client_id") == request.remote_addr and session.get("level") == "2" and session.get("option") == "1":
        # Primeira Consulta
        session["level"] = "3"
        session["option"] = "1"
        mensagem = "Legal que é sua primeira consulta. Tem alguma especialidade que você quer agendar?"
        msg.body(mensagem)
        responded = True
    if not responded and '1' in incoming_msg and session.get("client_id") == request.remote_addr and session.get("level") == "1":
        # Agendamento      
        session["level"] = "2" 
        session["option"] = "1" 
        mensagem = "Selecione uma das opções abaixo: "
        mensagem += "\n\n"
        mensagem += "1 - Primeira Consulta"
        mensagem += "\n"
        mensagem += "2 - Retorno"
        mensagem += "\n"
        mensagem += "3 - Conhecer a Clínica"
        mensagem += "\n"
        mensagem += "4 - Planos e Convênios"
        mensagem += "\n"
        mensagem += "5 - Estou com dor e preciso de ajuda"
        mensagem += "\n\n"
        mensagem += "# - Voltar ao menu principal"
        msg.body(mensagem)
        responded = True    
    if not responded or '#' in incoming_msg: 
        session["level"] = "1"
        mensagem = "Selecione uma das opções abaixo: "
        mensagem += "\n\n"
        mensagem += "1 - Agendamento"
        mensagem += "\n"
        mensagem += "2 - Atendimento humano"
        msg.body(mensagem)
    
    session["client_id"] = request.remote_addr
    return str(resp)

if __name__ == '__main__':
   app.run()