from flask_wtf import FlaskForm
from wtforms.fields import StringField,EmailField, SubmitField, PasswordField, SelectField,DateField,IntegerField
from wtforms.validators import InputRequired, Length,NumberRange, Regexp, DataRequired, ValidationError



class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Tên đăng nhập"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Mật khẩu"})
    SubmitFieldLogin = SubmitField("Đăng nhập")


class AdmisionStudent(FlaskForm):
    full_name = StringField("Họ và tên", validators=[InputRequired("Vui Lòng nhập họ tên học sinh"), Length(max=50)],
                            render_kw={"placeholder": "Nhập họ và tên"})
    gender = SelectField("Giới tính", choices=[('Nam', "Nam"), ('Nu', "Nữ")],
                         validators=[InputRequired()],
                         render_kw={"placeholder": "Chọn giới tính"})
    birth_date = DateField("Ngày sinh", validators=[DataRequired()],
                           render_kw={"placeholder": "Chọn ngày sinh"},format="%Y-%m-%d")
    address = StringField("Địa chỉ", validators=[InputRequired(), Length(max=255)],
                          render_kw={"placeholder": "Nhập địa chỉ"})
    phone_number = StringField("Số điện thoại",validators=[
        Regexp(regex=r'^\d{10,}$', message="Vui lòng nhập chính xác số điện thoại."),
        Length(max=10,min=10, message="Số điện thoại phải có 10 số.")
    ], render_kw={"placeholder": "Nhập số điện thoại"})
    email = EmailField("Email", validators=[InputRequired(), Length(max=100)],
                        render_kw={"placeholder": "Nhập email"})
    submit = SubmitField("Gửi")
