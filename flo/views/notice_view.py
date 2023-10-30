#### 관리자 공지 게시판 컨트롤러

from flask import Blueprint, render_template, request, url_for, redirect, send_file, g, flash
from datetime import datetime
from werkzeug.utils import redirect
import os

from .. import db
from flo.models.notice_model import Notice
from flo.form import NoticeCreateForm, NoticeCommentForm
from flo.views.auth_view import login_required


# 파일 업로드
UPLOAD_FOLDER = os.path.join(os.getcwd(), '') # 경로
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])                   # 허용 가능한 확장자

# 확장자 검증
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 블루프린트
bp = Blueprint('notice', __name__, url_prefix='/notice')


# 공지 목록
@bp.route('/list/',  methods=('GET', 'POST'))
def notice_li():
    try:
        page = request.args.get('page', type=int, default=1)
        notice_list = Notice.query.order_by(Notice.write_t.desc())

        # 검색 기능
        search_option = request.args.get('search_option', default='all')
        search_keyword = request.args.get('search_keyword', type=str, default='')
        search_query = '%%{}%%'.format(search_keyword)

        # 검색 여부
        if search_keyword:
            if search_option == 'title':
                notice_list = notice_list.join(Notice.user).filter(
                    Notice.title.ilike(search_query)
                ).distinct()  # 중복 제거
            elif search_option == 'content':
                notice_list = notice_list.join(Notice.user).filter(
                    Notice.content.ilike(search_query)
                ).distinct()
            else:  # 전체 검색
                notice_list = notice_list.join(Notice.user).filter(
                    (Notice.title.ilike(search_query)) | (Notice.content.ilike(search_query))
                ).distinct()

        notice_list = notice_list.paginate(page=page, per_page=10)

        return render_template('notice/notice_list.html', notice_list=notice_list)

    except ValueError as e:
        return board_error(e)


# 관리자의 공지 작성하기
@bp.route('/write/', methods=('GET', 'POST'))
@login_required                                         # 로그인 검증
def write():
    form = NoticeCreateForm()

    if request.method == 'POST' and form.validate_on_submit():

        # 제목과 내용 필수 입력
        if not form.title.data or not form.content.data:
            flash("제목과 내용을 입력해주세요")

        file = request.files['fileupload']
        filename = ''
        file_path = ''

        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)  # 파일 저장

        # 관리자가 아니면 등록 되지 않음
        if g.user.id == '관리자':
            notice = Notice(
                title=form.title.data,
                content=form.content.data,
                user=g.user,
                write_t=datetime.now(),
                filename=filename,
                file_path=file_path
            )

            db.session.add(notice)
            db.session.commit()

            return redirect(url_for('notice.notice_li'))

        else:
            flash('권한이 없습니다.')

    return render_template('notice/notice_write.html', form=form)


# 공지글 조회
@bp.route('/detail/<int:notice_idx>/', methods=('GET', 'POST'))
def detail(notice_idx):
    try:
        form = NoticeCommentForm()
        notice = Notice.query.get(notice_idx)

        # 게시글 없을 때
        if notice is None:
            raise ValueError

        return render_template('notice/notice_detail.html', notice=notice, form=form)

    except ValueError as e:
        return board_error(e)


# 첨부파일 다운로드
@bp.route('/download/<path:filename>',  methods=('POST',))
def download(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path, filename, as_attachment=True)


# 공지 수정
@bp.route('/update/<int:notice_idx>', methods=('GET', 'POST'))
@login_required
def update(notice_idx):
    try:
        # 게시글 가져오기
        notice = Notice.query.get(notice_idx)

        # 작성한 사용자만 수정 가능함
        if g.user != notice.user:
            flash('수정권한이 없습니다')

            return redirect(url_for('notice.detail', notice_idx=notice_idx))

        if request.method == 'POST':
            form = NoticeCreateForm(request.form)  # 기존 글 가져오기

            if form.validate_on_submit():
                form.populate_obj(notice)
                notice.write_t = datetime.now()

                db.session.commit()

                flash('게시글이 성공적으로 수정되었습니다.')

                return redirect(url_for('notice.detail', notice_idx=notice_idx))
        else:
            form = NoticeCreateForm(obj=notice)     # 데이터 전달

        return render_template('notice/notice_write.html', form=form)

    except Exception as e:
        return board_error(e)


# 공지 삭제
@bp.route('/delete/<int:notice_idx>')
@login_required
def delete(notice_idx):
    try:
        notice = Notice.query.get(notice_idx)

        # 사용자 확인
        if g.user != notice.user or not g.user.id == '관리자':
            flash('권한이 없습니다')
            return redirect(url_for('notice.detail', notice_idx=notice_idx))

        db.session.delete(notice)
        db.session.commit()

        return redirect(url_for('notice.notice_li'))

    except ValueError as e:
        return board_error(e)


# 공지 좋아요
@bp.route('/like/<int:notice_idx>/')
@login_required
def like(notice_idx):
    notice = Notice.query.get(notice_idx)

    if g.user == notice.user:
        flash('본인이 작성한 글은 공감할 수 없습니다')
    else:
        if g.user in notice.like:
            flash('이미 공감 했습니다')
        else:
            notice.like.append(g.user)
            db.session.commit()

    return redirect(url_for('notice.detail', notice_idx=notice_idx))


# 오류 핸들러
@bp.errorhandler(ValueError)
def board_error(e):
    return render_template('errors/404.html')