#### 관리자 공지 게시판 댓글 컨트롤러

from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from flo import db
from flo.form import NoticeCommentForm
from flo.models.notice_model import Notice, NoticeComment
from flo.views.auth_view import login_required


bp = Blueprint('noticecomment', __name__, url_prefix='/noticecomment')


# 공지 댓글 작성
@bp.route('/write/<int:notice_idx>', methods=('POST',))
@login_required                                         # 로그인 검증
def write(notice_idx):
    try:
        form = NoticeCommentForm()
        notice = Notice.query.get(notice_idx)

        if form.validate_on_submit():
            content = request.form['content']
            noticecomment = NoticeComment(content=form.content.data, write_t=datetime.now(), user=g.user)

            notice.comment_set.append(noticecomment)
            db.session.commit()

            return redirect(url_for('notice.detail', notice_idx=notice_idx))

        if notice is None:
            raise ValueError("게시글을 찾을 수 없습니다")

        return render_template('notice/notice_detail.html', notice=notice, form=form)

    except ValueError as e:
        return board_error(e)


# 공지 댓글 삭제
@bp.route('/delete/<int:noticecomment_idx>')
@login_required
def delete(noticecomment_idx):
    try:
            noticecomment = NoticeComment.query.get(noticecomment_idx)
            notice_idx = noticecomment.notice.idx

            # 댓글은 직접 작성한 사용자만 삭제 가능
            if g.user != noticecomment.user:
                flash('삭제권한이 없습니다')
            else:
                db.session.delete(noticecomment)
                db.session.commit()

            return redirect(url_for('notice.detail', notice_idx=notice_idx))

    except ValueError as e:
            return board_error(e)


@bp.errorhandler(ValueError)
def board_error(e):
    return render_template('errors/404.html'), 404