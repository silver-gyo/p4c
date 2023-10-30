#### 메인 화면 컨트롤러

from flask import Blueprint, render_template

from flo.models.board_model import Board

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('main.html')