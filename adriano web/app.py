from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
# Clave necesaria para las sesiones seguras y mensajes flash
app.secret_key = "clave_secreta_telefonia"


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Base de datos simulada de usuarios
usuarios = {
    "Mikolas": {
        "password": "upn1234"
    }
}

# Clase requerida por Flask-Login para manejar la sesión
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)




# 1. PÁGINA PRINCIPAL (DASHBOARD)
@app.route("/")
@login_required
def inicio():
    return render_template("index.html")


# 2. INICIAR SESIÓN
@app.route("/login", methods=["GET", "POST"])
def login():
    # Si ya inició sesión previamente, lo manda al inicio directo
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        # Validación de credenciales
        if usuario in usuarios and usuarios[usuario]["password"] == password:
            user = User(usuario)
            login_user(user)
            return redirect(url_for("inicio"))
        else:
            flash("Usuario o contraseña incorrectos. Inténtalo de nuevo.")

    return render_template("login.html")


# 3. MIS SERVICIOS
@app.route("/servicios")
@login_required
def servicios():
    return render_template("servicios.html")


# 4. HISTORIAL DE FACTURAS
@app.route("/facturas")
@login_required
def facturas():
    return render_template("facturas.html")


# 5. CERRAR SESIÓN
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
