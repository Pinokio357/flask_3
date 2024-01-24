from flask import Flask, render_template, redirect, url_for
from models import db, User
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm
from hashlib import sha256


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = b"0c850454104030e18a0da242805ed2c1d36927fa479300c90520640d730c2b3d"
csrf = CSRFProtect(app)
db.init_app(app)


@app.route("/", methods=["get", "post"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = sha256(form.password.data.encode(encoding="utf-8")).hexdigest()
        user = User(name=name, surname=surname, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("register"))
    return render_template("reg.html", form=form)

@app.cli.command("init-db")
def init_db():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
