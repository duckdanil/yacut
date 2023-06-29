from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import StringField
from wtforms.validators import (
    DataRequired, Length, Regexp, Optional, ValidationError
)


def validate_url_with_prefix(form, field):
    if field.data and not field.data.startswith('http://') and not field.data.startswith('https://'):
        field.data = 'http://' + field.data


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Адрес URL',
        description='https://example.com',
        validators=[
            DataRequired(message='Обязательное поле.'),
            Length(max=2048, message='Превышена максимальная длина URL-адреса (2048 символов).'),
            validate_url_with_prefix
        ]
    )
    custom_id = StringField(
        'Короткая ссылка',
        description='Длина не более 16 символов, латинские буквы и цифры',
        validators=[
            Length(max=16, message='Длина поля не должна превышать 16 символов.'),
            Regexp(r"^[a-zA-Z0-9]*$", message='Идентификатор может состоять только из латинских букв и цифр.'),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
