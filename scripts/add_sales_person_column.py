import sqlite3

def add_sales_person_column():
    conn = sqlite3.connect('customers.db')
    cursor = conn.cursor()
    
    try:
        # sales_personカラムを追加
        cursor.execute('ALTER TABLE daily_reports ADD COLUMN sales_person TEXT;')
        conn.commit()
        print("営業担当カラムを追加しました。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    add_sales_person_column() 