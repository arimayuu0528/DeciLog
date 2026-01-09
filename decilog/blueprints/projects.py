from flask import Blueprint, render_template, request, redirect, url_for
from decilog.db import connect_db # MySQLへ接続する関数を読み込む

# Blueprint名=projects URLの先頭に/projectsを付ける
projects_bp = Blueprint("projects", __name__, url_prefix="/projects") 

@projects_bp.route("/", methods=["GET"], strict_slashes=False)# GET /projects または /projects/ を受け付ける
# プロジェクト一覧表示の処理
def projects_list():
    sql = "SELECT id, name, description FROM projects ORDER BY id DESC;" # 一覧表示用SQL(新しい順)
    con = connect_db()                # DBへ接続
    cur = con.cursor(dictionary=True) # 取得結果を辞書形式にするカーソル
    cur.execute(sql)                  # SQLを実行
    projects = cur.fetchall()         # 結果を全件取得
    cur.close()                       # カーソルを閉じる
    con.close()                       # DB接続を閉じる

    if not projects:    # 取得結果が None/空 なら
        projects = []   # テンプレ側で扱いやすい用に空リストに統一

    return render_template("projects_list.html", projects=projects)   # projects_list.htmlを渡して表示する

@projects_bp.route("/", methods=["POST"], strict_slashes=False)       # POST /projects で新規作成を受け付ける
# プロジェクト作成の処理
def projects_create():
    name = (request.form.get("name") or "").strip()                   # フォームの name を取得して前後空白を除去(未入力なら空白)
    description = (request.form.get("description") or "").strip()     # フォームの description を取得して前後空白を除去

    if not name:                                                      # name が空なら(必須チェック)
        return redirect(url_for("projects.projects_list"))            # 一覧へ戻す(Blueprint名.関数名でURL生成)

    sql = "INSERT INTO projects (name, description) VALUES (%s, %s);" # INSERT(%sはプレースホルダ)
    con = connect_db() # DBへ接続
    cur = con.cursor() # 通常カーソル(dictionary不要)
    cur.execute(sql, (name, description if description else None))    # SQL実行(descriptionが空ならNULL)
    con.commit()       # INSERTを確定
    cur.close()        # カーソルを閉じる
    con.close()        # DB接続を閉じる

    return redirect(url_for("projects.projects_list")) # 作成後に一覧へ戻す
