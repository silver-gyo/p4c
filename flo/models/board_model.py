#### 일반 게시판

from flo import db

# 좋아요 임시 테이블
board_like = db.Table(
    'board_like',
    db.Column('user_idx', db.Integer, db.ForeignKey('users.idx', ondelete='CASCADE'), primary_key=True),
    db.Column('board_idx', db.Integer, db.ForeignKey('board.idx', ondelete='CASCADE'), primary_key=True)
)


# Board Model
class Board(db.Model):

    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    write_t = db.Column(db.DateTime(), nullable=False)
    update_t = db.Column(db.DateTime(), nullable=True)
    filename = db.Column(db.String(100))
    file_path = db.Column(db.String(200))
    posting_password = db.Column(db.String(8), nullable=True)

    user_idx = db.Column(db.Integer, db.ForeignKey('users.idx', ondelete='CASCADE'), nullable=False)
    user = db.relationship('Users', backref=db.backref('board_user_set'))

    like = db.relationship('Users', secondary=board_like, backref=db.backref('board_like_set'))


# 댓글 - Comment Model
class Comment(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    board_idx = db.Column(db.Integer, db.ForeignKey('board.idx', ondelete='CASCADE'))
    board = db.relationship('Board', backref=db.backref('comment_set'))
    content = db.Column(db.String(100), nullable=False)
    write_t = db.Column(db.DateTime(), nullable=False)

    user_idx = db.Column(db.Integer, db.ForeignKey('users.idx', ondelete='CASCADE'), nullable=False)
    user = db.relationship('Users', backref=db.backref('comment_user_set'))