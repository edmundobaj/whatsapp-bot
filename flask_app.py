from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'citação' in incoming_msg:
        # retorne uma citação        
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'Não consegui recuperar uma citação neste momento, desculpe.'
        msg.body(quote)
        responded = True
    if 'gato' in incoming_msg or 'gata' in incoming_msg:
        # retorne uma foto de gato        
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:  
        mensagem = "Selecione uma das opções abaixo: "
        mensagem += "\n\n"
        mensagem += "1 - Agendamento"
        mensagem += "\n"
        mensagem += "2 - Quero atendimento humano"
        msg.body(mensagem)
    return str(resp)

if __name__ == '__main__':
   app.run()