#### 관리자 공지 게시판

from flo import db


# 좋아요 임시 테이블
notice_like = db.Table(
    'notice_like',
    db.Column('user_idx', db.Integer, db.ForeignKey('users.idx', ondelete='CASCADE'), primary_key=True),
    db.Column('notice_idx', db.Integer, db.ForeignKey('notice.idx', ondelete='CASCADE'), primary_key=True)
)


# Notice Model
class Notice(db.Model):
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    write_t = db.Column(db.DateTime(), nullable=False)
    update_t = db.Column(db.DateTime(), nullable=True)
    filename = db.Column(db.String(100))
    file_path = db.Column(db.String(200))

    user_idx = db.Column(db.Integer, db.ForeignKey('users.idx', ondelete='CASCADE'), nullable=False)
    user = db.relationship('Users', backref=db.backref('notice_user_set'))

    like = db.relationship('Users', secondary=notice_like, backref=db.backref('notice_like_set'))


# 공지 댓글 - Notice Comment Model
class NoticeComment(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    notice_idx = db.Column(db.Integer, db.ForeignKey('notice.idx', ondelete='CASCADE'))
    notice = db.relationship('Notice', backref=db.backref('comment_set'))
    content = db.Column(db.String(100), nullable=False)
    write_t = db.Column(db.DateTime(), nullable=False)

    user_idx = db.Column(db.Integer, db.ForeignKey('users.idx', ondelete='CASCADE'), nullable=False)
    user = db.relationship('Users', backref=db.backref('notice_comment_user_set'))