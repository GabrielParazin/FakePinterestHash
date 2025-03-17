#wtf formulario
#flask form estrutura da classe e o wtforms sao os cam,pos
#data required - usuario tem que preencher o campo

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")

    def validate_email(self, emailv):
        usuario = Usuario.query.filter_by(email=emailv.data).first()
        if not usuario:
            raise ValidationError("Usuário já existe, crie uma conta")

class FormCriarConta(FlaskForm):
    username = StringField("Nome de usuario", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(3,15)])
    confirmacao_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Criar conta")


    def validate_email(self, emailv):
        usuario = Usuario.query.filter_by(email=emailv.data).first()
        if usuario:
            raise ValidationError("E-mail já existe")


class FormFoto(FlaskForm):
    foto = FileField(validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")