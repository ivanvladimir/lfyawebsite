from starlette_wtf import StarletteForm, CSRFProtectMiddleware, csrf_protect
import wtforms
from wtforms.validators	import DataRequired


class DateF(StarletteForm):
    date = wtforms.fields.DateField(
        "Fecha",
        [wtforms.validators.DataRequired("Ingresar el fecha")],
        format="%d/%m/%Y",
        render_kw={"class": "input", "placeholder": "22/09/2024"},
    )

class UserF(StarletteForm):
    idunam = wtforms.fields.StringField(
        "Número de cuenta",
        [wtforms.validators.DataRequired("Ingresar número de cuenta")],
        render_kw={"class": "input", "placeholder": "Número de cuenta"},
    )

    firstname = wtforms.fields.StringField(
        "Nombre",
        [wtforms.validators.DataRequired("Ingresar nombre")],
        render_kw={"class": "input", "placeholder": "Nombres"},
    )

    lastname = wtforms.fields.StringField(
        "Apellidos",
        [wtforms.validators.DataRequired("Ingresar apellidos")],
        render_kw={"class": "input", "placeholder": "Apellidos"},
    )

    email = wtforms.fields.StringField(
        "Correo",
        [wtforms.validators.DataRequired("Ingresar correo")],
        render_kw={"class": "input", "placeholder": "correo@dominio.com"},
    )


