import sqlite3

def show_schema():
    conn = sqlite3.connect('customers.db')
    cursor = conn.cursor()
    
    # テーブル一覧を取得
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("=== データベーススキーマ ===")
    
    for table in tables:
        table_name = table[0]
        print(f"\n=== {table_name} テーブル ===")
        
        # テーブルのスキーマを取得
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        # カラム情報を表示
        for col in columns:
            col_id, name, type_, notnull, default_value, pk = col
            print(f"カラム名: {name}")
            print(f"型: {type_}")
            print(f"NULL許可: {'No' if notnull else 'Yes'}")
            print(f"デフォルト値: {default_value}")
            print(f"主キー: {'Yes' if pk else 'No'}")
            print("---")
    
    conn.close()

if __name__ == "__main__":
    show_schema() 