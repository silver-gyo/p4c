from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, Email

# 게시글 관련
class BoardCreateForm(FlaskForm):
    title = StringField('제목')
    content = TextAreaField('내용')
    posting_password = PasswordField('비밀번호')
    filename = StringField('파일 이름')
    file_path = StringField('파일 경로')

class NoticeCreateForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired('제목을 입력해주세요.')])
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력해주세요')])
    filename = StringField('파일 이름')
    file_path = StringField('파일 경로')


# 댓글 관련
class CommentForm(FlaskForm):
    content = TextAreaField('댓글', validators=[DataRequired('내용을 입력해주세요')])

class NoticeCommentForm(FlaskForm):
    content = TextAreaField('댓글', validators=[DataRequired('내용을 입력해주세요')])


# 사용자 관련
class UserCreateForm(FlaskForm):
    id = StringField('ID')
    password = PasswordField('Password')
    password_chk = PasswordField('비밀번호 확인')
    name = StringField('이 름')
    email = EmailField('이메일', validators=[Email()])
    member_name = StringField('닉네임')
    verification_code = StringField('인증 코드')
    perm = 1

class UserLoginForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])


# 이메일 검증
class EmailForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])