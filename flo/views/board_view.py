#### 일반 사용자 게시판

from flask import Blueprint, render_template, request, url_for, redirect, send_file,g, flash
from datetime import datetime
from werkzeug.utils import redirect
from sqlalchemy.exc import SQLAlchemyError
import os

from .. import db
from flo.models.board_model import Board
from flo.form import BoardCreateForm, CommentForm
from flo.views.auth_view import login_required


# 파일 업로드
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'C:/project/myproject/flo/static/img/') # 경로
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])                   # 허용 가능한 확장자

# 확장자 검증
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 블루프린트
bp = Blueprint('board', __name__, url_prefix='/board')


# 게시글 목록
@bp.route('/list/', methods=('GET', 'POST'))
def board_li():
    try:
        page = request.args.get('page', type=int, default=1)
        board_list = Board.query.order_by(Board.write_t.desc())

        # 검색 기능
        search_option = request.args.get('search_option', default='all')
        search_keyword = request.args.get('search_keyword', type=str, default='')
        search_query = '%%{}%%'.format(search_keyword)

        # 검색 여부
        if search_keyword:
            if search_option == 'title':
                board_list = board_list.join(Board.user).filter(
                    Board.title.ilike(search_query)
                ).distinct()  # 중복 제거
            elif search_option == 'content':
                board_list = board_list.join(Board.user).filter(
                    Board.content.ilike(search_query)
                ).distinct()
            else:  # 전체 검색
                board_list = board_list.join(Board.user).filter(
                    (Board.title.ilike(search_query)) | (Board.content.ilike(search_query))
                ).distinct()

        board_list = board_list.paginate(page=page, per_page=10)

        return render_template('board/board_list.html', board_list=board_list)

    except ValueError as e:
        return board_error(e)


# 게시글 작성하기
@bp.route('/write/', methods=('GET', 'POST'))
@login_required                                         # 로그인 검증
def write():
    try:
        form = BoardCreateForm()
        posting_password = request.form.get('posting_password')

        if request.method == 'POST' and form.validate_on_submit():
            if form.validate_on_submit():

                # 제목과 내용 필수 입력
                if not form.title.data or not form.content.data:
                    flash( "제목과 내용을 입력해주세요")
                elif len(form.posting_password.data) > 8:
                    flash("게시글 비밀번호는 8자리 이하로 설정해주세요")

                # 파일은 업로드 하지 않을 경우 빈 문자열로 저장
                else:
                    file = request.files['fileupload']
                    filename = ''
                    file_path = ''

                    if file and allowed_file(file.filename):
                        filename = file.filename
                        file_path = os.path.join(UPLOAD_FOLDER, filename)
                        file.save(file_path)  # 파일 저장

                    posting_password = form.posting_password.data
                    if not posting_password:
                        posting_password = None

                    board = Board(
                        title=form.title.data,
                        content=form.content.data,
                        write_t=datetime.now(),
                        filename=filename,
                        file_path=file_path,
                        user=g.user,
                        posting_password=form.posting_password.data)
                    db.session.add(board)
                    db.session.commit()

                    return redirect(url_for('board.board_li'))

            else:
                flash('입력 양식을 확인해주세요')
                return render_template('board/board_write.html', form=form)



        return render_template('board/board_write.html', form=form)

    except SQLAlchemyError as e:
        board_error(e)



# 비밀글
@bp.route('/secret/<int:board_idx>/', methods=('POST', 'GET'))
def secret(board_idx):
    try:
        form = BoardCreateForm()
        board = Board.query.get(board_idx)

        # 게시글 조회
        if board.posting_password == 'NULL' or g.user.id == 'iamadmin':
            return render_template('board/board_detail.html', board=board, form=form)

        # 비밀번호 검증
        if request.method == 'POST' and form.validate_on_submit():
                if board.posting_password == form.posting_password.data:
                    return render_template('board/board_detail.html', board=board, form=form)

        return render_template('board/board_password.html', board=board, form=form)

    except ValueError as e:
        return board_error(e)

    except AttributeError as e:
        flash('권한이 없습니다')
        return redirect(url_for('board.board_li'))


# 게시글 조회
@bp.route('/detail/<int:board_idx>/', methods=('GET', 'POST'))
def detail(board_idx):
    try:
        pass_form = BoardCreateForm()
        form = CommentForm()
        board = Board.query.get(board_idx)

        # 게시글 없을 때
        if board is None:
            raise ValueError

        return render_template('board/board_detail.html', board=board, form=form)

    except ValueError as e:
        return board_error(e)


# 첨부파일 다운로드
@bp.route('/download/<path:filename>',  methods=('POST',))
def download(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path, filename, as_attachment=True)


# 게시글 수정
@bp.route('/update/<int:board_idx>', methods=('GET', 'POST'))
@login_required
def update(board_idx):
    try:
        # 게시글 가져오기
        board = Board.query.get(board_idx)

        # 작성한 사용자만 수정 가능함
        if g.user != board.user:
            flash('수정권한이 없습니다')

            return redirect(url_for('board.detail', board_idx=board_idx))

        if request.method == 'POST':
            form = BoardCreateForm(request.form)  # 기존 글 가져오기

            if form.validate_on_submit():
                form.populate_obj(board)
                board.write_t = datetime.now()

                db.session.commit()

                flash('게시글이 성공적으로 수정되었습니다.')

                return redirect(url_for('board.detail', board_idx=board_idx))
        else:
            form = BoardCreateForm(obj=board)

        return render_template('board/board_write.html', form=form)

    except Exception as e:
        return board_error(e)

# 게시글 삭제
@bp.route('/delete/<int:board_idx>')
@login_required
def delete(board_idx):
    try:
        board = Board.query.get(board_idx)

        # 작성한 사용자 또는 관리자만 삭제 가능
        if g.user != board.user and not g.user.id == 'iamadmin':
            flash('권한이 없습니다')
            return redirect(url_for('board.detail', board_idx=board_idx))

        db.session.delete(board)
        db.session.commit()

        return redirect(url_for('board.board_li'))

    except ValueError as e:
        return board_error(e)


# 게시글 좋아요
@bp.route('/like/<int:board_idx>/')
@login_required
def like(board_idx):
    board = Board.query.get(board_idx)

    if g.user == board.user:
        flash('본인이 작성한 글은 공감할 수 없습니다')
    else:
        if g.user in board.like:
            flash('이미 공감 했습니다')
        else:
            board.like.append(g.user)
            db.session.commit()

    return redirect(url_for('board.detail', board_idx=board_idx))


# 오류 핸들러
@bp.errorhandler(ValueError)
def board_error(e):
    return render_template('errors/404.html')