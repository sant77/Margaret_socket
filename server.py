#Librerias
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from assistenPython import AssistenPython
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

#chabot y asistente
#________________________________________________
#Clase chatbot, parametro es el nombre del bot
chat = ChatBot('Margaret')
#Entrenamiento del bot
trainer = ChatterBotCorpusTrainer(chat)
#Con que se va a entrenar el bot
trainer.train('chatterbot.corpus.spanish.greetings')
#Invoca la clase asistente de python
asistente  = AssistenPython('Margaret')


#Inicializacion del servidor
#________________________________________________
#Objeto flask
app = Flask(__name__)
#Inicializacion de socket
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
print('Servidor iniciado')
#Servidor
#________________________________________________
#Ruta del servidor
@app.route('/')
def index():
	return 'hello'

#Escucha el mensaje del cliente 
@socketio.on('message')
def handelMessage(msg):
	print('Message:'+ msg)
	if 'fecha' in msg:
		response = asistente.getDate()
		print('Respuesta:'+response)
		emit('message', {'name': 'Margaret','message':str(response)})
	else:
		peticion = msg
		respuesta = chat.get_response(peticion)
		print('Respuesta:'+ str(respuesta))
		emit('message', {'name': 'Margaret','message':str(respuesta)})
	
#Escucha cuando el cliente se conecta y envia un mensaje	
@socketio.on('connect')
def test_connect():

	print('Cliente conectado')
	emit('message', {'data': 'Connected'})

#Cuando se desconecta envian un mensaje 
@socketio.on('disconnect')
def test_disconnect():
    print('Cliente desconectado')

if __name__ == '__main__':
	socketio.run(app)

