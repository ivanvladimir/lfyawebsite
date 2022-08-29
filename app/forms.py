from flask_wtf import FlaskForm
import wtforms


class AdminLogin(FlaskForm):
    password = wtforms.fields.PasswordField(
        "Password",
        [wtforms.validators.DataRequired("Ingresar el password")],
        render_kw={"class": "input", "placeholder": "password"},
    )


class DateF(FlaskForm):
    date = wtforms.fields.DateField(
        "Fecha",
        [wtforms.validators.DataRequired("Ingresar el fecha")],
        format="%d/%m/%Y",
        render_kw={"class": "input", "placeholder": "22/09/2024"},
    )


class MailTo(FlaskForm):
    to = wtforms.fields.EmailField(
        "A:",
        [
            wtforms.validators.DataRequired("Ingresar a quien va dirigido"),
            wtforms.validators.Email("Ingresar un correo válido"),
        ],
        render_kw={"class": "input", "placeholder": "email"},
    )
    subject = wtforms.fields.StringField(
        "Tema:",
        [wtforms.validators.DataRequired("Ingresar el tema")],
        render_kw={"class": "input", "placeholder": "tema"},
    )
    msg = wtforms.fields.TextAreaField(
        "Mensaje",
        [wtforms.validators.DataRequired("Ingresar el mensaje a enviar")],
        render_kw={
            "class": "textarea",
            "id": "msg1",
            "placeholder": "escribe el mensaje",
            "rows": 10,
        },
    )
