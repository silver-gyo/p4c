# flo

**flask + mysql 를 이용한 MVC 패턴의 웹 페이지 구축**
=============


## 프로젝트 소개
![image](https://github.com/silver-gyo/flo/assets/83441042/a925bfff-cb3f-45d1-8b7c-c3e3cb6cd25e)

flask와 mysql을 이용한 일반 사용자 또는 관리자가 자유롭게 사용할 수 있는 게시판


## 사용 라이브러리
![image](https://github.com/silver-gyo/flo/assets/83441042/84a86c1f-9a6d-414e-b6a6-766bec537125)


## 디렉터리 구조
![image](https://github.com/silver-gyo/flo/assets/83441042/c2b74150-a51e-4bf7-8f28-77527a30474f)

## 세부 구조
#### /__init__.py
app 등록 및 관리
#### /forms.py
입력값 검증과 관련한 로직 수행
#### /models/
- board_model.py  :  일반 사용자 게시판 모델
- notice_model.py  :  관리자 게시판 모델
- user_model.py  :  사용자 모델
#### /views/
- auth_view.py  :   사용자 컨트롤러 
- board_view.py  :  일반 게시판 게시글 컨트롤러
- comment_view.py  : 일반 게시판의 댓글 컨트롤러
- main_view.py  :  메인 화면 컨트롤러
- notice_comment_view.py  :  관리자 공지 게시판 댓글 컨트롤러
- notice_view.py  :  관리자 공지 게시글 컨트롤러
#### /static/
- css/  :  css 파일 디렉터리
- js/  :  js 파일 디렉터리
- img/  :  업로드 되는 파일 경로
#### /templates
##### auth/ 
  - auth_join.html  :  회원가입 화면
  - auth_login.html  :  로그인 화면
  - forgot_id.html  : 아이디 분실 화면
##### board/
  - board_detail.html  :  일반 게시글 상세보기
  - board_list.html  :  일반 게시판 목록
  - board_password.html  :  일반 게시판 비밀글
  - board_write.html  :  일반 게시글 작성
##### errors/
  - 404.html  :  error 핸들러용 페이지
  - form_errors.html  :  form error 핸들러용 페이지
##### notice/
  - notice_detail.html  :  관리자 공지 상세보기
  - notice_list.html  :  관리자 공지 목록
  - notice_write.html  :  관리자 공지 작성
- base.html   :  기본 html
- navbar.html  :  navbar
- main.html  :  메인 화면
#### config.py
각종 설정(데이터베이스, 이메일)
#### app.py
메인 코드 실행


## 필수 기능 구현
1. 회원가입
   - 이메일 인증 🔺
    비밀번호 유효성 검사 ✔
2. 로그인
   - 아이디 찾기 기능 ✔
3. 권한
   - 관리자 권한 추가 ✔
4. 게시판
   - 글 작성 ✔
   - 비밀글 ✔
   - 파일 업로드 및 다운로드 ✔
   - 댓글 ✔
   - 게시글 추천 ✔
5. 검색
   - 게시판 별 검색 ✔


## 기능 상세 소개

### 회원가입
![image](https://github.com/silver-gyo/flo/assets/83441042/4f90ebb8-1e88-44c9-82d9-9d617e7c3181)

- 아이디, 비밀번호, 비밀번호 확인, 이름, 이메일, 닉네임은 필수 입력 사항 입니다.
- 아이디, 이메일, 닉네임은 중복된 사용자 값이 존재하지 않도록 하기 위하여 회원가입 시 검증됩니다.
- 아이디는 영어 소문자와 숫자를 혼합한 6~20 자리로 설정하여야 합니다.
- 비밀번호는 영어 대소문자와 숫자, 특수문자 ! @ # ^ _ 를 혼합한 8~20 자리로 설정하여야 합니다.
- 비밀번호와 비밀번호 확인 필드의 두 값이 일치하여야 합니다.
- 이름은 한글 또는 영문으로 입력하여야 합니다.
- 이메일은 아이디 찾기에 필요하며, 중복된 이메일로 가입하지 못합니다.
- 닉네임은 게시판에 나타나며, 중복된 닉네임은 가입할 수 없습니다.

--------------------------------------------------

### 로그인
![image](https://github.com/silver-gyo/flo/assets/83441042/1731135a-e0fa-4a7d-b2ef-0683f62fc6c2)

- 아이디와 비밀번호는 필수로 입력하여야 합니다.
- 로그인 된 사용자는 session으로 관리합니다.

--------------------------------------------------

### 로그아웃
![image](https://github.com/silver-gyo/flo/assets/83441042/65ffe2da-627c-41df-a302-0f831ad7dde6)

- 현재 로그인한 사용자를 로그아웃 합니다.
- 로그아웃한 사용자를 현재 session에서 제거합니다.

--------------------------------------------------

### 아이디 찾기
![image](https://github.com/silver-gyo/flo/assets/83441042/7f2f770e-ed91-4971-8d0f-4f8b7e91fbdb)

![image](https://github.com/silver-gyo/flo/assets/83441042/0db8605d-b500-4505-be76-9348d3ad7cd5)

- 로그인 시 아이디가 기억이 나지 않는다면, 회원가입 시 작성했던 이메일로 아이디를 전송합니다.
- 가입한 적이 있는 사용자에게만 이메일이 전송되며, 가입되어있는 이름과 이메일이 일치하여야 합니다.

--------------------------------------------------

### Board
![image](https://github.com/silver-gyo/flo/assets/83441042/165c6e2f-a12d-420b-a5f6-0639c2eae264)

![image](https://github.com/silver-gyo/flo/assets/83441042/9c0292eb-85f7-48bf-829f-c4785dcb84dc)

![image](https://github.com/silver-gyo/flo/assets/83441042/924cec52-a29e-4be1-ae84-a95bef14256f)

- 일반 사용자와 관리자 모두 쓰기 기능을 가지고 있는 일반 게시판 입니다.
- 로그인 되어있는 사용자만 글쓰기, 댓글 작성, 좋아요 기능을 사용할 수 있습니다.
- 로그인하지 않은 상태에서 기능 사용을 하려 하면 로그인 페이지로 이동됩니다.
- 게시글을 작성한 사용자만 수정, 삭제가 가능합니다.
- 관리자는 일반 게시글에 대하여 삭제할 수 있는 권한을 가지고 있습니다.
- 게시글에는 비밀번호를 입력해야지만 조회할 수 있는 비밀글 기능이 있습니다.
- 비밀글은 비밀번호를 아는 사용자와 관리자만 조회할 수 있습니다.
- 본인이 작성한 게시글에는 좋아요를 누를 수 없습니다.
- 파일 업로드는 'png', 'jpg', 'jpeg', 'gif' 확장자만 가능합니다.
- 가장 최근 게시글, 가장 최신 댓글부터 위에서 아래로 등록됩니다.

--------------------------------------------------

### Notice
![image](https://github.com/silver-gyo/flo/assets/83441042/ad4e7b83-2892-4184-8af6-a058f6a8edbf)

![image](https://github.com/silver-gyo/flo/assets/83441042/d4194815-e6b8-4910-8dba-a0867c33e862)

- 관리자만 쓰기 기능을 가지고 있는 공지 게시판 입니다.
- 관리자에게만 작성하기 버튼이 활성화 됩니다.
- 게시글 조회, 파일 다운로드, 댓글 작성, 좋아요 등의 기능은 로그인한 사용자라면 사용 가능합니다.
- 본인이 작성한 게시글에는 좋아요를 누를 수 없습니다.
- 파일 업로드는 'png', 'jpg', 'jpeg', 'gif' 확장자만 가능합니다.
- 가장 최근 게시글, 가장 최신 댓글부터 위에서 아래로 등록됩니다.

--------------------------------------------------

### 검색
![image](https://github.com/silver-gyo/flo/assets/83441042/80d9b07a-6cf8-447c-803e-91af2a0c0ac9)

- 게시판 별로 제목+내용, 제목, 내용 중에 옵션을 선택하여 검색할 수 있는 검색창이 있습니다.



## 보완해야 될 부분
1. 회원가입 시 이메일 인증
회원가입 시 이메일까지 인증하는 로직을 구현하였으면 좋았을 것 같아서 계속해서 진행해볼 예정 입니다.
- 23/10/30 - 인증번호 전송과 url 클릭 시 자동으로 인증되는 방법 구현 중 
3. 회원 탈퇴
회원 탈퇴에 대한 기능이 누락되어 추가로 구현할 예정 입니다.



## 개인적인 회고
- 가장 어려웠던 점
1. git 사용
   중간에 git repo를 잘못 삭제한 사실을 인지하지 못한 상태에서 개발을 진행하다가 실행이 안 되어 확인해보니 파일이 삭제되어 발생했던 문제였다.
   git에 대해 공부하면서 기본적인 사용법은 분명 숙지했다고 생각했지만, 삭제에 대한 개념은 공부하지 못했었다. 알고보니 삭제된 repo도 임시 휴지통에 보관되어 있는 사실을 늦게 알게 되었지만 git을 잘 사용하면 언제 어디서나 유지보수가 쉬울 것 같아 앞으로 잘 사용할 수 있을 것 같다는 점을 얻었다.
2. 데이터 베이스 연결
   기존 sql 문을 파이썬 언어로 작성하는 데에 이해하기까지 꽤나 오래걸렸다. 처음엔 이해를 잘못해서 아예 sql 문을 짜서 실행시키는 방향으로 진행하다가 나중에 model 추가 반영 사항이 있을 때 그 방법이 더 복잡하다고 느껴졌다.
   나중에는 플라스크 ORM 라이브러리를 사용하여 파이썬 코드로 작성하는 방법을 택했는데 훨씬 편했다. model 추가 사항이나, 전반적인 추가 기능을 구현하는데 데이터베이스를 업데이트 하고 반영하는 게 명령어 두 개면(flask db migrate, flask db upgrade) 쉽게 수정이 가능해서 좋았다. 나중에는 개인적으로 사용한다면 sqllite을 사용해도 괜찮을 거 같다고 생각이 들었다.
3. 비밀글 구현
   처음엔 파일업로드나 비밀글에 대해서 Y/N 체크를 통해 먼저 검증 후 Y 면 비밀번호를 받거나, N 면 그냥 통과하는 식으로 구현하고자 하였으나 controller 역할을 했던 view 파일들에서 pass를 써도 에러로 진행이 안 되거나 비밀번호를 무조건 받아야 했다. 간단하게 두 기능 다 업로드 되거나 작성된 내역이 있으면 그때서야 검증해도 되겠다는 생각이 들고 방향을 바꿔 데이터베이스에서 체크하려 했던 Y/N 을 빼고 view에서 검증을 하였다. 그 후에 동일한 패스워드를 입력해도 게시글이 조회가 되지 않아 엄청난 좌절을 맛보았지만 막상 다 구현한 뒤에 예외처리 등을 미숙하게 해서 그랬던 것이라는 걸 알았다. 웹 취약점 공부를 하면서 개발 시 예외처리가 정말 중요하다고 느꼈지만 이런 류의 중요함도 깨닫게 되어 확실히 큰 도움이 되었다. 
   


## 프로젝트 참고
- 점프 투 플라스크 ( https://wikidocs.net/book/4542 )
- 플라스크로 만드는 myBlog ( https://wikidocs.net/book/5490 )
- 📝 Flask, MVC 패턴을 활용한 도서관 책 대여 서비스 ( https://github.com/bky373/elice_library/tree/master )
- Wilkyway Tistory ( https://streamls.tistory.com/entry/Flask%EA%B0%95%EC%A2%8C-%EB%A1%9C%EA%B7%B8%EC%9D%B8 )
- Flask ( https://flask-docs-kr.readthedocs.io/ko/latest/index.html )
- L3m0n $0ju Tistory ( https://lemon-soju.tistory.com/258 )
- Dragonz Titory ( https://roksf0130.tistory.com/126 )
- bootstrap ( https://getbootstrap.com/ )
- 도서 : (Flask 기반의) 파이썬 웹 프로그래밍, 이지호 지음
- 도서 : 혼자 공부하는 SQL, 우재남 지음


