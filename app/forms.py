from flask_wtf import FlaskForm
from wtforms import PasswordField 

class AdminLogin(FlaskForm):
    password = PasswordField(label="Password",
            
            render_kw={'placeholder':'password'})
