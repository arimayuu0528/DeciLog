from flask import Flask    # Flaskアプリ本体を使う

def create_app():          # アプリ生成（Factoryパターン：拡張しやすい）
    app = Flask(__name__)  # Flaskアプリを作成（__name__でテンプレ/静的パスの基準が決まる）

    # .pyファイルを追加したらここに追記　------------------------------------------------------------------------------------
    from .blueprints.projects import projects_bp  # Blueprintを読み込む（循環import回避のため関数内import）
    app.register_blueprint(projects_bp)           # Blueprintをアプリに登録（/projects が有効になる）
    from .blueprints.tasks import tasks_bp
    app.register_blueprint(tasks_bp)
    # --------------------------------------------------------------------------------------------------------------------
    @app.get("/")            # GET / のルート（動作確認用）
    def health():            # ヘルスチェック（サーバが生きてるか確認）
        return {"ok": True}  # JSONで返す（簡易）

    return app               # 組み立て終わったFlaskアプリを返す
