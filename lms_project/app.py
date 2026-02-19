from flask import Flask, render_template
from routes.Member_Routes import member_bp
from config import SECRET_KEY
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY

# 업로드 폴더 설정
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.register_blueprint(member_bp)

# 메인 페이지
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5022)
