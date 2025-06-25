import sqlite3
import pandas as pd
import os

def migrate_database():
    # 既存のデータベースファイルを削除
    if os.path.exists('customers.db'):
        os.remove('customers.db')
        print("既存のcustomers.dbを削除しました。")
    
    # ソースデータベースとターゲットデータベースの接続
    source_conn = sqlite3.connect('customers_moto.db')
    target_conn = sqlite3.connect('customers.db')
    
    try:
        # 顧客データの移行
        customers_df = pd.read_sql_query("SELECT * FROM customers", source_conn)
        customers_df.to_sql('customers', target_conn, if_exists='replace', index=False)
        print(f"顧客データを移行しました: {len(customers_df)}件")
        
        # 案件データの移行
        projects_df = pd.read_sql_query("SELECT * FROM projects", source_conn)
        projects_df.to_sql('projects', target_conn, if_exists='replace', index=False)
        print(f"案件データを移行しました: {len(projects_df)}件")
        
        # 営業日報データの移行
        daily_reports_df = pd.read_sql_query("SELECT * FROM daily_reports", source_conn)
        daily_reports_df.to_sql('daily_reports', target_conn, if_exists='replace', index=False)
        print(f"営業日報データを移行しました: {len(daily_reports_df)}件")
        
        # 添付ファイルデータの移行
        attachments_df = pd.read_sql_query("SELECT * FROM attachments", source_conn)
        attachments_df.to_sql('attachments', target_conn, if_exists='replace', index=False)
        print(f"添付ファイルデータを移行しました: {len(attachments_df)}件")
        
        # ユーザーデータの移行
        users_df = pd.read_sql_query("SELECT * FROM users", source_conn)
        users_df.to_sql('users', target_conn, if_exists='replace', index=False)
        print(f"ユーザーデータを移行しました: {len(users_df)}件")
        
        print("データ移行が完了しました。")
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
    finally:
        source_conn.close()
        target_conn.close()

if __name__ == '__main__':
    migrate_database() 