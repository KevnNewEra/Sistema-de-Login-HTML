from flask import Flask, render_template, request, redirect, session
import json
import os
import hashlib

app = Flask(__name__)
app.secret_key = "chave_super_secreta"

# ======================
# FUNÇÕES
# ======================

def carregar_usuarios():
    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r") as arquivo:
            return json.load(arquivo)
    return []

def salvar_usuarios(usuarios):
    with open("usuarios.json", "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# ======================
# ROTAS
# ======================

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        senha_hash = criptografar_senha(senha)

        usuarios = carregar_usuarios()

        for u in usuarios:
            if u["usuario"] == usuario and u["senha"] == senha_hash:
                session["usuario"] = usuario
                return redirect("/dashboard")

        return "Login inválido"

    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        usuarios = carregar_usuarios()

        for u in usuarios:
            if u["usuario"] == usuario:
                return "Usuário já existe"

        novo_usuario = {
            "usuario": usuario,
            "senha": criptografar_senha(senha)
        }

        usuarios.append(novo_usuario)
        salvar_usuarios(usuarios)

        return redirect("/login")

    return render_template("cadastro.html")

@app.route("/dashboard")
def dashboard():
    if "usuario" in session:
        return render_template("dashboard.html", usuario=session["usuario"])
    return redirect("/login")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)



# isso é apenas uma base para um sistema de login simples, feito por mim