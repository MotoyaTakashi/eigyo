import sqlite3

def add_management_url_column():
    conn = sqlite3.connect('customers.db')
    cursor = conn.cursor()
    
    try:
        # management_urlカラムを追加
        cursor.execute('ALTER TABLE projects ADD COLUMN management_url TEXT;')
        conn.commit()
        print("management_urlカラムを追加しました。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_management_url_column() 