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

@projects_bp.route("/<int:project_id>", methods=["GET"], strict_slashes=False)  # GET /projects/<id>（末尾スラッシュ有無も許可）
def projects_detail(project_id):  # 指定されたproject_idのプロジェクト詳細を表示する
    sql = "SELECT id, name, description FROM projects WHERE id = %s;"  # 1件取得用SQL（%sはプレースホルダ）
    con = connect_db()                                                 # MySQLへ接続してコネクションを取得する
    cur = con.cursor(dictionary=True)                                  # 結果を辞書形式で受け取れるカーソルを作る（列名で参照できる）
    cur.execute(sql, (project_id,))                                    # project_idをSQLに渡してSELECTを実行する（タプルなので末尾カンマ必須）
    project = cur.fetchone()                                           # 取得結果を1件だけ取り出す（該当なしならNone）
    cur.close()                                                        # カーソルを閉じる（後片付け）
    con.close()                                                        # DB接続を閉じる（後片付け）

    if project is None:  # 該当IDのプロジェクトが存在しない場合
        # とりあえず一覧へ戻す（本番は404ページでもOK）＝ いったん安全に一覧へ逃がす（後で404実装でも良い）
        return redirect(url_for("projects.projects_list"))  # プロジェクト一覧へリダイレクトする

    return render_template("project_detail.html", project=project)  # 詳細テンプレへprojectを渡して表示する

@projects_bp.route("/<int:project_id>/edit", methods=["POST"], strict_slashes=False)  # POST /projects/<id>/edit で更新を受け付ける
def projects_update(project_id):  # 指定されたproject_idのプロジェクト情報を更新する
    name = (request.form.get("name") or "").strip()                # フォームからnameを取得し、未入力は空文字にして前後空白を除去する
    description = (request.form.get("description") or "").strip()  # フォームからdescriptionを取得し、前後空白を除去する

    if not name:  # nameが空なら（必須チェック）
        return redirect(url_for("projects.projects_detail", project_id=project_id))  # 詳細画面へ戻して入力をやり直す

    sql = "UPDATE projects SET name = %s, description = %s WHERE id = %s;"  # UPDATE文（対象IDのname/descriptionを更新）
    con = connect_db()  # MySQLへ接続してコネクションを取得する
    cur = con.cursor()  # UPDATEなので通常カーソルで十分（dictionary不要）
    cur.execute(sql, (name, description if description else None, project_id))  # 空descriptionはNULLとして更新し、対象IDを指定する
    con.commit() # 変更を確定する（コミット）
    cur.close()  # カーソルを閉じる（後片付け）
    con.close()  # DB接続を閉じる（後片付け）

    return redirect(url_for("projects.projects_detail", project_id=project_id))  # 更新後に詳細画面へ戻して結果を確認できるようにする
