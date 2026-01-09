import mysql.connector  # mysql-connector-python を使ってMySQL接続する

def connect_db():       # MySQLへ接続してコネクションを返す関数
    con = mysql.connector.connect(  # MySQLへ接続
        host='localhost',           # DBホスト
        user='root',                # DBユーザー名
        passwd='',                  # DBパスワード
        db='decilog',               # 使用するDB名
        port=3306,                  # MySQLのポート
        auth_plugin="mysql_native_password"  # 認証方式
    )  
    return con          # 接続オブジェクトを返す
