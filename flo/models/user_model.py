#### 사용자 관련

from flo import db

# Users Model
class Users(db.Model):
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    password_chk = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(5), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    member_name = db.Column(db.String(10), unique=True, nullable=False)
    perm = db.Column(db.String(1), nullable=False, default='N')

    def perm_admin(self):
        return self.perm == 'Y'
