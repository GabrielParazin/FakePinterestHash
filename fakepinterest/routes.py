#render template vai procurar uma pasta  no projetos chamado templates
#sql aclhey permite mexer no bd em codigos phyton
#login_required  exigir que o cara tenha login
#validate on submit --> so roda se o usuario crlicou no botao enviar no formulario, que todos os campos forma preenchidas e todas as validaçoes foram aplicadas
#form_criarconta.username.data -->form. campo. informçao preenchida
#form_criarconta.senha.data --> armazena a senha, considerado falha
    #bcrypt.generate_password_hash(form_criarconta.senha.data) pegar o txt do usuario e trandformar em uma sequencia aleatoria, a unica forma de reverte e o
    #bcrypt.check_password_hash()
#login_user fazer login
# current_user usuario que ja está logado



from fakepinterest import app, database, bcrypt
from flask import Flask, render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormCriarConta, FormLogin, FormFoto
from fakepinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template("homepage.html", form=form_login)


@app.route('/criarconta', methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, senha=senha, email=form_criarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criarconta)


#tag diz que o usuario é uma variavel
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):     #aqui o usuario está vendo o proprio perfil dele
        form_Foto = FormFoto()
        if form_Foto.validate_on_submit():
            arquivo = form_Foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                app.config["UPLOAD_FOLDER"], nome_seguro)    #caminho do projeto / local do upload folder, é uma constante / nome _seguro
            arquivo.save(caminho)
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_Foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)              #permite que eu passe parametros para o html


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao).all() #[:100] Foto.data_criacao.desc()
    return render_template("feed.html", fotos=fotos)