#### 일반 게시글의 댓글 컨트롤러

from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from flo import db
from flo.form import CommentForm
from flo.models.board_model import Board, Comment
from flo.views.auth_view import login_required


bp = Blueprint('comment', __name__, url_prefix='/comment')


# 댓글 작성하기
@bp.route('/write/<int:board_idx>', methods=('POST',))
@login_required                                         # 로그인 검증
def write(board_idx):
    try:
        form = CommentForm()
        board = Board.query.get(board_idx)
        content = request.form['content']

        # 댓글 낸용, 작성 시간, 작성자 정보
        if form.validate_on_submit():
            content = request.form['content']
            comment = Comment(content=content, write_t=datetime.now(), user=g.user)

            board.comment_set.append(comment)
            db.session.commit()

            return redirect(url_for('board.detail', board_idx=board_idx))

        if board is None:
            raise ValueError("게시글을 찾을 수 없습니다")

        return render_template('board/board_detail.html', board=board, form=form)

    except ValueError as e:
        return board_error(e)


# 댓굴 삭제
@bp.route('/delete/<int:comment_idx>')
@login_required
def delete(comment_idx):
    try:
        comment = Comment.query.get(comment_idx)
        board_idx = comment.board.idx

        # 댓글은 작성자만 삭제 가능
        if g.user != comment.user:
            flash('삭제권한이 없습니다')
        else:
            db.session.delete(comment)
            db.session.commit()

        return redirect(url_for('board.detail', board_idx=board_idx))

    except ValueError as e:
        return board_error(e)


@bp.errorhandler(ValueError)
def board_error(e):
    return render_template('errors/404.html'), 404