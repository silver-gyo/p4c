#### 사용자 관련 컨트롤러

from flask import Blueprint, url_for, render_template, flash, request, redirect, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import functools
from flask_mail import Mail, Message
import re            # 정규식 모듈
import secrets

from .. import db, mail
from flo.form import UserCreateForm, UserLoginForm
from flo.models.user_model import Users


bp = Blueprint('auth', __name__, url_prefix='/auth')


# 먼저 실행되어 seesion 체크
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.get(user_id)


# 비로그인 상태에서 접근 시 로그인 페이지로 리다이렉트 기능
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view


# 회원가입
@bp.route('/join/', methods=('GET', 'POST'))
def join():
    try:
        form = UserCreateForm()

        if request.method == 'POST' and form.validate_on_submit():
            id = request.form.get('id')
            password = request.form.get('password')
            password_chk = request.form.get('password_chk')
            name = request.form.get('name')
            email = request.form.get('email')
            member_name = request.form.get('member_name')
            verification_code = request.form.get('verification_code')

            error = None

            # 필수 필드 값 입력 검증
            if not id:
                error = "ID를 입력해주세요."
            elif not password:
                error = "비밀번호를 입력해주세요."
            elif not password_chk:
                error = "비밀번호 확인을 입력해주세요."
            elif not name:
                error = "이름을 입력해주세요."
            elif not email:
                error = "이메일을 입력해주세요."
            elif not member_name:
                error = "닉네임을 입력해주세요."

            # 아이디 규칙
            if not id.isalnum() or len(id) < 6 or len(id) > 20:
                error = "아이디는 6~20자리로 영어 소문자, 숫자를 포함해야 합니다."

            # 패스워드 정규식
            pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$'
            if not re.match(pattern, password):
                error = "패스워드는 8~20자리로 영어 대소문자 + 숫자 + 특수문자 ! @ # ^ _ 를 포함해야 합니다."

            # 패스워드 두 개 비교
            if password != password_chk:
                error = "비밀번호가 일치하지 않습니다."

            if error:
                flash(error)
                return render_template('auth/auth_join.html', form=form)

            # 중복검사
            existed_user = Users.query.filter_by(id=id).first()
            existed_email = Users.query.filter_by(email=email).first()
            existed_member_name = Users.query.filter_by(member_name=member_name).first()

            # 저장
            if not existed_user and not existed_email and not existed_member_name:


                user = Users(
                    id=id,
                    password=generate_password_hash(password),
                    password_chk=generate_password_hash(password),
                    name=name,
                    email=email,
                    member_name=member_name,
                    perm='N'
                )

                # 관리자 아이디 설정해주기
                if id == '관리자':
                    user.perm = 'Y'

                db.session.add(user)
                db.session.commit()

                flash('가입되었습니다.')

                return redirect(url_for('auth.login'))


            # 중복일 경우
            else:
                if existed_user and existed_user.id == id:
                    error = "존재하는 ID입니다."
                elif existed_email and existed_email.email == email:
                    error = "사용 중인 이메일입니다."
                elif existed_member_name and existed_member_name.member_name == member_name:
                    error = "사용 중인 닉네임입니다."

            flash(error)

        return render_template('auth/auth_join.html', form=form)

    except ValueError as e:
        return print(e)


# 로그인
@bp.route('/login/', methods=('GET', 'POST'))
def login():
    try:
        form = UserLoginForm()

        if request.method == 'POST' and form.validate_on_submit():
            error = None
            user = Users.query.filter_by(id=form.id.data).first()

            # id 체크
            if not user:
                error = "존재하지 않는 사용자입니다."

            # password 체크
            elif not check_password_hash(user.password, form.password.data):
                error = "비밀번호가 올바르지 않습니다."

            # 위의 에러가 발생하지 않았을 때
            if error is None:
                session.clear()
                session['user_id'] = user.idx

                # 비 로그인으로 접근했는지 확인
                _next = request.args.get('next', '')
                if _next:                               # 게시글에 비 로그인으로 접근했다가 로그인 후 원래 페이지로
                    return redirect(_next)
                else:                                   # 로그인 후 메인 페이지로
                    return redirect(url_for('main.index'))

            flash(error)

        return render_template('auth/auth_login.html', form=form)

    except ValueError as e:
        return print(e)


# 로그아웃
@bp.route('/logout/')
def logout():
    session.clear()

    return redirect(url_for('main.index'))


# 아이디 분실
@bp.route('/forgot_id/', methods=('GET', 'POST'))
def forgot_id():
    form = UserCreateForm()

    error = None

    # 이름과 이메일 검증 후 일치하는 사용자가 있을 경우 해당 메일로 아이디 전송
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data

        user = Users.query.filter_by(email=email, name=name).first()

        if user:
            # 이메일로 전송
            send_id_to_user(user)

            flash('아이디가 이메일로 전송되었습니다.')

            return redirect(url_for('auth.login'))

        # 이메일이나 사용자를 찾을 수 없을 경우
        else:
            error = '입력하신 정보로 가입된 회원을 찾을 수 없습니다.'

        flash(error)

    return render_template('auth/forgot_id.html', form=form)


# 이메일 내용 및 전송 함수
def send_id_to_user(user):
    msg = Message('flo 아이디 찾기', sender='junmyeonaaa@gmail.com', recipients=[user.email])
    msg.body = '안녕하세요, {} 님. \n가입하신 flo 아이디는 {} 입니다.'.format(user.name, user.id)
    mail.send(msg)


# 오류 핸들러
@bp.errorhandler(ValueError)
def board_error(e):
    return render_template('errors/404.html')