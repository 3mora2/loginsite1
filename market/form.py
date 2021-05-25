from wtforms import SubmitField, StringField, PasswordField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired(),
                                       Length(max=64)])

    password = PasswordField(label='Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self._errors = dict()

    @property
    def new_errors(self):
        self._errors.update(self.errors)
        return self._errors

    @new_errors.setter
    def new_errors(self, error):
        self._errors.update(error)


class RegistrationForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired(),
                                       Length(max=64)])

    email = StringField(label='Email',
                        validators=[DataRequired(),
                                    Email(),
                                    Length(max=120)])

    password = PasswordField(label='Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Password should be at least %(min)d characters long')])

    confirm = PasswordField(label='Confirm Password',
                            validators=[DataRequired(message='*Required'),
                                        EqualTo('password', message='Both password fields must be equal!')])
    accept_tos = BooleanField('I accept the TOS', [DataRequired()])
    submit = SubmitField('Create Account')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self._errors = dict()

    @property
    def new_errors(self):
        self._errors.update(self.errors)
        return self._errors

    @new_errors.setter
    def new_errors(self, error):
        self._errors.update(error)
