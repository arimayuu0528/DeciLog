from flask import Blueprint, render_template, request, redirect, url_for  # Blueprint/テンプレ表示/フォーム取得/リダイレクト/URL生成を使う
from decilog.db import connect_db                                         # MySQLへ接続する関数を読み込む

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")  # Blueprint名=tasks、URLの先頭に /tasks を付ける

ALLOWED_STATUSES = {"todo", "doing", "done"}                  # タスクの状態はこの3種類に固定する（入力チェック用）

@tasks_bp.route("/", methods=["GET"], strict_slashes=False)   # GET /tasks と /tasks/ を受け付ける
def tasks_list():  # タスク一覧を表示する処理
    sql = """  # 一覧表示用SQL（タスク+プロジェクト名をJOINして取得する）
    SELECT t.id, t.title, t.status, t.due_date, t.assignee, p.name AS project_name  -- タスク情報＋表示用にプロジェクト名も取得
    FROM tasks t  -- tasksテーブルをtとして扱う
    JOIN projects p ON p.id = t.project_id  -- tasks.project_id に対応する projects を結合
    ORDER BY t.id DESC;  -- 新しいタスクが上に来るように並べる
    """  # SQL文字列の終わり
    con = connect_db()                 # DBに接続（コネクション取得）
    cur = con.cursor(dictionary=True)  # 結果を辞書形式（列名で参照）にするカーソル
    cur.execute(sql)                   # SELECTを実行する
    tasks = cur.fetchall()             # 結果を全件取得（list[dict]）
    cur.close()                        # カーソルを閉じる（後片付け）
    con.close()                        # DB接続を閉じる（後片付け）
    return render_template("tasks_list.html", tasks=tasks or [])  # テンプレにtasksを渡して表示（None対策で空配列）

@tasks_bp.route("/", methods=["POST"], strict_slashes=False)  # POST /tasks でタスク新規作成を受け付ける
def tasks_create():  # タスクを作成する処理
    project_id = request.form.get("project_id")              # フォームからproject_idを取得（必須）
    title = (request.form.get("title") or "").strip()        # フォームからtitleを取得して前後空白を除去（必須）
    assignee = (request.form.get("assignee") or "").strip()  # 担当者（任意）を取得して整形
    due_date = request.form.get("due_date") or None          # 期限（任意）を取得（空ならNone）

    if not project_id or not title:  # 必須項目が欠けていたら
        return redirect(url_for("tasks.tasks_list"))  # 一覧へ戻す（入力エラー表示は後で拡張）

    sql = "INSERT INTO tasks (project_id, title, assignee, due_date) VALUES (%s, %s, %s, %s);"  # INSERT文（%sはプレースホルダ）
    con = connect_db()  # DBに接続
    cur = con.cursor()  # INSERTなので辞書形式は不要
    cur.execute(sql, (project_id, title, assignee if assignee else None, due_date))  # SQL実行（空文字はNULLに寄せる）
    con.commit() # 変更を確定（コミット）
    cur.close()  # カーソルを閉じる
    con.close()  # DB接続を閉じる

    return redirect(url_for("tasks.tasks_list"))  # 作成後は一覧へ戻す（POST→Redirect→GET）

@tasks_bp.route("/<int:task_id>/status", methods=["POST"], strict_slashes=False)  # POST /tasks/<id>/status で状態変更を受け付ける
def tasks_update_status(task_id):  # タスクのstatus（todo/doing/done）を更新する処理
    status = (request.form.get("status") or "").strip()  # フォームからstatusを取得して整形
    if status not in ALLOWED_STATUSES:  # 想定外のstatusが来たら
        return redirect(url_for("tasks.tasks_list"))     # 一覧へ戻す（不正入力を無視）

    sql = "UPDATE tasks SET status = %s WHERE id = %s;"  # statusだけ更新するUPDATE文
    con = connect_db()  # DBに接続
    cur = con.cursor()  # UPDATEなので通常カーソルでOK
    cur.execute(sql, (status, task_id))  # UPDATEを実行（statusと対象idを渡す）
    con.commit() # 変更を確定（コミット）
    cur.close()  # カーソルを閉じる
    con.close()  # DB接続を閉じる

    return redirect(url_for("tasks.tasks_list"))  # 更新後は一覧へ戻す
