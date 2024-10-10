from starlette_wtf import StarletteForm, CSRFProtectMiddleware, csrf_protect
import wtforms
from wtforms.validators	import DataRequired


class ProblemEntryF(wtforms.Form):
    section = wtforms.fields.StringField(
        "Sección",
        [wtforms.validators.DataRequired("Ingesar la sección")],
        render_kw={"class": "input", "placeholder": "Insertar la sección"},
    )
    amount = wtforms.fields.IntegerField(
        "Cantidad",
        [wtforms.validators.DataRequired("Ingesar la cantidad de ejercicios")],
        render_kw={"class": "input", "placeholder": "Insertar la cantidad"},
    )
 
class AssigmentF(StarletteForm):
    name = wtforms.fields.StringField(
        "Nombre de assingación",
        [wtforms.validators.DataRequired("Ingesar el nombre")],
        render_kw={"class": "input", "placeholder": "Insertar el nombre"},
    )
    problems = wtforms.fields.FieldList(wtforms.fields.FormField(ProblemEntryF),min_entries=1)

class PresentationF(StarletteForm):
    talks = wtforms.fields.TextAreaField(
        "Lista de presentaciones",
        [wtforms.validators.DataRequired("Ingesar la lista de presentaciones")],
        render_kw={"class": "input", "placeholder": "Lista de presentaciones", "rows": 40 },
    )

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


