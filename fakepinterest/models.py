# database.Model  permite criar classe no formato que o nosso bd/databse entende -- criando classe que o bd vai entender e permitir criar uma tabela no bd
#UserMixin diz qual a classe que vai gerenciar a estrutura de logins
#vai recebr um id e retornar quem é -- load_usuario

from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

#sao sub classes de databse.Model
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)
    # Foto.usuario no hmtl voce vê todas as fotos do usuario

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")  #texto por que é um local onde ela esta armazenada
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)