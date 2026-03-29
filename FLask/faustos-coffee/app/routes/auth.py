from urllib.parse import urlsplit

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.forms import build_login_data_from_form, build_register_user_from_form
from app.models import Usuario


def _next_url(default_endpoint: str = "home") -> str:
    next_url = request.args.get("next") or request.form.get("next")
    if next_url and not urlsplit(next_url).netloc:
        return next_url
    return url_for(default_endpoint)


def register_auth_routes(app):
    @app.route("/registro", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("admin_productos"))

        next_url = _next_url("admin_productos")

        if request.method == "POST":
            usuario, errores = build_register_user_from_form(request.form)

            if errores:
                for error in errores:
                    flash(error, "danger")
                return render_template("register.html", next_url=next_url)

            usuario_existente = db.session.execute(
                db.select(Usuario).where(Usuario.email == usuario.email)
            ).scalar_one_or_none()

            if usuario_existente is not None:
                flash("Ya existe un usuario registrado con ese correo electronico.", "warning")
                return render_template("register.html", next_url=next_url)

            try:
                db.session.add(usuario)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash("No se pudo crear la cuenta porque el correo ya esta registrado.", "warning")
                return render_template("register.html", next_url=next_url)

            login_user(usuario)
            flash("Tu cuenta fue creada correctamente. Ya puedes usar las rutas privadas.", "success")
            return redirect(next_url)

        return render_template("register.html", next_url=next_url)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("admin_productos"))

        next_url = _next_url("admin_productos")

        if request.method == "POST":
            login_data, errores = build_login_data_from_form(request.form)

            if errores:
                for error in errores:
                    flash(error, "danger")
                return render_template("login.html", next_url=next_url)

            usuario = db.session.execute(
                db.select(Usuario).where(Usuario.email == login_data.email)
            ).scalar_one_or_none()

            if usuario is None or not usuario.check_password(login_data.password):
                flash("Correo o contrasena incorrectos.", "danger")
                return render_template("login.html", next_url=next_url)

            if not usuario.activo:
                flash("Tu cuenta esta desactivada. Contacta al administrador.", "warning")
                return render_template("login.html", next_url=next_url)

            login_user(usuario)
            flash("Sesion iniciada correctamente.", "success")
            return redirect(next_url)

        return render_template("login.html", next_url=next_url)

    @app.post("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Sesion cerrada correctamente.", "success")
        return redirect(url_for("home"))
