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

