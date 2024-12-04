from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import StringField, EmailField, SubmitField, PasswordField, SelectField, DateField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange, Regexp, DataRequired, ValidationError
from app.models import Regulation, TYPE_REGULATION


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()],
                           render_kw={"placeholder": "Tên đăng nhập"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Mật khẩu"})
    SubmitFieldLogin = SubmitField("Đăng nhập")


class AdmisionStudent(FlaskForm):
    full_name = StringField("Họ và tên", validators=[InputRequired("Vui Lòng nhập họ tên học sinh"), Length(max=50)],
                            render_kw={"placeholder": "Nhập họ và tên"})
    gender = SelectField("Giới tính", choices=[('Nam', "Nam"), ('Nữ', "Nữ")],
                         validators=[InputRequired()],
                         render_kw={"placeholder": "Chọn giới tính"})
    birth_date = DateField("Ngày sinh", validators=[DataRequired()],
                           render_kw={"placeholder": "Chọn ngày sinh"}, format="%Y-%m-%d")
    address = StringField("Địa chỉ", validators=[InputRequired(), Length(max=255)],
                          render_kw={"placeholder": "Nhập địa chỉ"})
    phone_number = StringField("Số điện thoại", validators=[
        Regexp(regex=r'^\d{10,}$', message="Vui lòng chỉ nhập số vào số điện thoại !"),
        Length(max=10, min=10)
    ], render_kw={"placeholder": "Nhập số điện thoại"})
    email = EmailField("Email", validators=[InputRequired(), Length(max=100)],
                       render_kw={"placeholder": "Nhập email"})
    # Kiểm tra email tồn tại
    submit = SubmitField( "Gửi" )


class Info_Account(FlaskForm):
    name = StringField('Họ và tên', validators=[DataRequired()], render_kw={"readonly": True} )
    email = StringField('Email', validators=[DataRequired()])
    birthday = DateField('Ngày sinh', validators=[DataRequired()], render_kw={"readonly": True}, format="%Y-%m-%d")
    gender = StringField('Giới tính',  render_kw={"disabled": True})
    phone = StringField("Số điện thoại", validators=[DataRequired(), Length(max=10)])
    address = StringField("Địa chỉ", validators=[InputRequired(), Length(max=255)])

    # Avatar không bắt buộc, chỉ yêu cầu chọn nếu muốn thay đổi
    avatar = FileField('Ảnh đại diện', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Chỉ cho phép ảnh định dạng JPG, JPEG, PNG'),

    ])

    submit = SubmitField('Tải lên')


class ChangeClass(FlaskForm):
    teacher = SelectField("Giáo viên chủ nhiệm",
                          validators=[InputRequired()])
    grade = SelectField("Khối học", choices=[("K10", "Khối 10"), ("K11", "Khối 11"), ("K12", "Khối 12")],
                        validators=[InputRequired()],
                        render_kw={"placeholder": "Chọn khối học"})
    if Regulation.type.__eq__(TYPE_REGULATION.RE_AMOUNT):
        class_size = IntegerField("Số lượng học sinh", validators=[InputRequired(),
                                                                   NumberRange(min=Regulation.min_value,
                                                                               max=Regulation.max_value)],
                                  render_kw={"placeholder": "Sỉ số lớp"})
    # Thêm ràng buộc quy định so lượng ở đây
    submit = SubmitField("Lưu")
#
#
# class Info_Account(FlaskForm):
#     name = StringField('Họ và tên',
#                        validators=[DataRequired()],
#                        render_kw={"placeholder": "Nhập họ và tên", "title": "Họ và tên đầy đủ"})
#
#     email = StringField('Email',
#                         validators=[DataRequired()],
#                         render_kw={"placeholder": "Nhập email của bạn", "title": "Địa chỉ email hợp lệ"})
#
#     birthday = DateField('Ngày sinh',
#                          validators=[DataRequired()],
#                          render_kw={"placeholder": "Chọn ngày sinh", "title": "Ngày sinh của bạn"})
#
#     gender = SelectField('Giới tính',
#                          choices=[('M', 'Nam'), ('F', 'Nữ')],
#                          validators=[DataRequired()],
#                          render_kw={"title": "Chọn giới tính của bạn"})
#
#     phone = StringField("Số điện thoại",
#                         validators=[DataRequired(), Length(max=10)],
#                         render_kw={"placeholder": "Nhập số điện thoại 10 chữ số",
#                                    "title": "Chỉ nhập số, tối đa 10 ký tự"})
#
#     address = StringField("Địa chỉ",
#                           validators=[InputRequired(), Length(max=255)],
#                           render_kw={"placeholder": "Nhập địa chỉ hiện tại", "title": "Địa chỉ tối đa 255 ký tự"})
#
#     avatar = FileField('Ảnh đại diện',
#                        validators=[
#                            FileAllowed(['jpg', 'jpeg', 'png'], 'Chỉ cho phép ảnh định dạng JPG, JPEG, PNG'),
#                            FileRequired('Bạn cần chọn một ảnh.')
#                        ],
#                        render_kw={"title": "Tải lên ảnh đại diện của bạn"})
#
#     submit = SubmitField('Cập nhật thông tin')