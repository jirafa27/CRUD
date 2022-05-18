from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms import validators


class CreateTaskForm(FlaskForm):
    text = TextAreaField('Text of the task', validators=[validators.DataRequired(), validators.Length(min=2, max=250)])
    submit = SubmitField('Save')


class UpdateTaskForm(FlaskForm):
    text = TextAreaField('Text of the task', validators=[validators.DataRequired(), validators.Length(min=2, max=250)])
    created = SelectField('Select task, which you want to change')
    submit = SubmitField('Save')


class DeleteTaskForm(FlaskForm):
    created = SelectField('Select task, which you want to delete', render_kw={'onchange':'func()'})
    submit = SubmitField('Delete')
