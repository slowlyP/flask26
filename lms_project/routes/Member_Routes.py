
from flask import Blueprint, render_template, request, redirect, session
from service.Member_Service import delete_member, login
from service.Member_Service import signup
from service.Member_Service import get_member_list
from service.Member_Service import change_status
from service.Member_Service import get_member
from service.Member_Service import update_member
import os
from werkzeug.utils import secure_filename
from service.Member_Service import update_profile



member_bp = Blueprint(
    "member",
    __name__,
    url_prefix="/member"
)


# 로그인 route

@member_bp.route("/login", methods=["GET","POST"])
def login_page():

    if request.method =="POST":

        uid = request.form["uid"]
        upw = request.form["upw"]

        user = login(uid, upw)

        if user:
            session["login_user"] = user["uid"]
            session["role"] = user["role"]
            session["profile_img"] = user["profile_img"]

            return redirect("/")

        else:
            return render_template(
            "member/login.html",
            error="아이디 또는 비밀번호가 틀렸습니다."
    )

    return render_template("member/login.html")


# 로그아웃

@member_bp.route("/logout")
def logout():
    
    session.clear()

    return redirect("/")



# 회원가입

@member_bp.route("/join", methods=["GET","POST"])
def join_page():
    
    if request.method =="POST":
        
        uid = request.form["uid"]
        upw = request.form["upw"]
        upw_confirm = request.form["upw_confirm"]
        name = request.form["name"]

        if upw != upw_confirm:
            return "비밀번호가 일치하지 않습니다."

        signup(uid, upw, name)
        
        return redirect("/member/login")

    return render_template("member/join.html")


# 관리자 로그인시

@member_bp.route("/admin")
def admin_page():

    #로그인 체크
    if not session.get("login_user"):
        return redirect("/member/login")

    # 관리자 권한체크
    if session.get("role") != "admin":
        return "접근 권한 없음"

    return render_template("member/admin_page.html")

# 관리자 회원관리 목록 
@member_bp.route("/list")
def member_list():

    # 로그인체크
    if not session.get("login_user"):
        return redirect("/member/login")

    # 관리자 체크
    if session.get("role") != "admin":
        return "접근 권한 없음"
    members = get_member_list()

    return render_template(
        "member/member_list.html",
        members=members
    )

# 회원 active 변경

@member_bp.route("/status/<int:member_id>/<status>")
def member_status(member_id, status):
    #로그인체크
    if not session.get("login_user"):
        return redirect("/member/login")

    #관리자 체크
    if session.get("role") != "admin":
        return "접근 권한 없음"

    #상태변경 
    change_status(member_id, status)

    return redirect("/member/list")

# 회원 delete

@member_bp.route("/delete/<int:member_id>")
def member_delete(member_id):

    #로그인체크
    if not session.get("login_user"):
        return redirect("/member/login")

    #관리자 체크
    if session.get("role") != "admin":
        return "접근 권한 없음"

    delete_member(member_id)

    return redirect("/member/list")

# mypage

@member_bp.route("/mypage")
def mypage():

    #로그인 체크
    if not session.get("login_user"):
        return redirect("/member/login")

    uid = session.get("login_user")

    member = get_member(uid)

    return render_template(
        "member/mypage.html",
        member=member
    )

# update

@member_bp.route("/edit", methods=["GET","POST"])
def member_edit():

    if not session.get("login_user"):
        return redirect("/member/login")

    uid = session.get("login_user")

    if request.method == "POST":

        upw = request.form["upw"]
        name = request.form["name"]

        member = get_member(uid)

        # 비번 입력 안 했으면 기존 비번 유지
        if upw == "":
            upw = member["upw"]

        update_member(uid, upw, name)

        # 파일 처리
        file = request.files["profile_img"]

        if file and file.filename != "":

            filename = secure_filename(file.filename)

            filepath = os.path.join(
                "static/uploads",
                filename
            )

            file.save(filepath)

            update_profile(uid, filename)

        return redirect("/member/mypage")

    member = get_member(uid)

    return render_template(
        "member/edit.html",
        member=member
    )
