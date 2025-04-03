import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# データベース接続
def init_db():
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    # 顧客テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         company_name TEXT NOT NULL,
         contact_person TEXT,
         email TEXT,
         phone TEXT,
         address TEXT,
         last_contact_date TEXT,
         notes TEXT)
    ''')
    # 案件テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         customer_id INTEGER,
         project_name TEXT NOT NULL,
         status TEXT,
         start_date TEXT,
         end_date TEXT,
         budget INTEGER,
         description TEXT,
         FOREIGN KEY (customer_id) REFERENCES customers (id))
    ''')
    conn.commit()
    conn.close()

# 顧客データの追加
def add_customer(company_name, contact_person, email, phone, address, notes):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO customers (company_name, contact_person, email, phone, address, last_contact_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (company_name, contact_person, email, phone, address, datetime.now().strftime('%Y-%m-%d'), notes))
    conn.commit()
    conn.close()

# 案件データの追加
def add_project(customer_id, project_name, status, start_date, end_date, budget, description):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO projects (customer_id, project_name, status, start_date, end_date, budget, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (customer_id, project_name, status, start_date, end_date, budget, description))
    conn.commit()
    conn.close()

# 顧客データの取得
def get_customers():
    conn = sqlite3.connect('customers.db')
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()
    return df

# 案件データの取得
def get_projects(customer_id=None):
    conn = sqlite3.connect('customers.db')
    if customer_id:
        df = pd.read_sql_query("""
            SELECT p.*, c.company_name 
            FROM projects p 
            JOIN customers c ON p.customer_id = c.id 
            WHERE p.customer_id = ?
        """, conn, params=(customer_id,))
    else:
        df = pd.read_sql_query("""
            SELECT p.*, c.company_name 
            FROM projects p 
            JOIN customers c ON p.customer_id = c.id
        """, conn)
    conn.close()
    return df

# 顧客データの更新
def update_customer(id, company_name, contact_person, email, phone, address, notes):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('''
        UPDATE customers
        SET company_name=?, contact_person=?, email=?, phone=?, address=?, notes=?
        WHERE id=?
    ''', (company_name, contact_person, email, phone, address, notes, id))
    conn.commit()
    conn.close()

# 案件データの更新
def update_project(id, project_name, status, start_date, end_date, budget, description):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('''
        UPDATE projects
        SET project_name=?, status=?, start_date=?, end_date=?, budget=?, description=?
        WHERE id=?
    ''', (project_name, status, start_date, end_date, budget, description, id))
    conn.commit()
    conn.close()

# 顧客データの削除
def delete_customer(id):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('DELETE FROM customers WHERE id=?', (id,))
    conn.commit()
    conn.close()

# 案件データの削除
def delete_project(id):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('DELETE FROM projects WHERE id=?', (id,))
    conn.commit()
    conn.close()

# アプリケーションのメイン部分
def main():
    st.title('営業顧客管理システム')
    
    # データベースの初期化
    init_db()
    
    # サイドバーで操作を選択
    menu = st.sidebar.selectbox(
        'メニュー',
        ['顧客一覧', '顧客追加', '顧客編集', '顧客削除', '案件一覧', '案件追加', '案件編集', '案件削除']
    )
    
    if menu == '顧客一覧':
        st.header('顧客一覧')
        df = get_customers()
        st.dataframe(df)
        
    elif menu == '顧客追加':
        st.header('顧客追加')
        with st.form('add_customer_form'):
            company_name = st.text_input('会社名')
            contact_person = st.text_input('担当者名')
            email = st.text_input('メールアドレス')
            phone = st.text_input('電話番号')
            address = st.text_input('住所')
            notes = st.text_area('備考')
            
            if st.form_submit_button('追加'):
                if company_name:
                    add_customer(company_name, contact_person, email, phone, address, notes)
                    st.success('顧客を追加しました！')
                else:
                    st.error('会社名は必須です。')
                    
    elif menu == '顧客編集':
        st.header('顧客編集')
        df = get_customers()
        if not df.empty:
            customer_id = st.selectbox('編集する顧客を選択', df['id'])
            customer = df[df['id'] == customer_id].iloc[0]
            
            with st.form('edit_customer_form'):
                company_name = st.text_input('会社名', customer['company_name'])
                contact_person = st.text_input('担当者名', customer['contact_person'])
                email = st.text_input('メールアドレス', customer['email'])
                phone = st.text_input('電話番号', customer['phone'])
                address = st.text_input('住所', customer['address'])
                notes = st.text_area('備考', customer['notes'])
                
                if st.form_submit_button('更新'):
                    update_customer(customer_id, company_name, contact_person, email, phone, address, notes)
                    st.success('顧客情報を更新しました！')
        else:
            st.info('編集可能な顧客がありません。')
            
    elif menu == '顧客削除':
        st.header('顧客削除')
        df = get_customers()
        if not df.empty:
            customer_id = st.selectbox('削除する顧客を選択', df['id'])
            if st.button('削除'):
                delete_customer(customer_id)
                st.success('顧客を削除しました！')
        else:
            st.info('削除可能な顧客がありません。')

    elif menu == '案件一覧':
        st.header('案件一覧')
        df = get_projects()
        if not df.empty:
            # 表示する列を選択
            display_columns = ['id', 'company_name', 'project_name', 'status', 'start_date', 'end_date', 'budget']
            display_df = df[display_columns].copy()
            
            # 列名を日本語に変更
            column_names = {
                'id': 'ID',
                'company_name': '顧客名',
                'project_name': '案件名',
                'status': 'ステータス',
                'start_date': '開始日',
                'end_date': '終了予定日',
                'budget': '予算（円）'
            }
            display_df = display_df.rename(columns=column_names)
            
            # データフレームを表示
            st.dataframe(display_df, use_container_width=True)
            
            # 案件の詳細を表示するセクション
            st.subheader('案件詳細')
            project_id = st.selectbox('詳細を表示する案件を選択', df['id'])
            selected_project = df[df['id'] == project_id].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**顧客名:** {selected_project['company_name']}")
                st.write(f"**案件名:** {selected_project['project_name']}")
                st.write(f"**ステータス:** {selected_project['status']}")
                st.write(f"**開始日:** {selected_project['start_date']}")
            
            with col2:
                st.write(f"**終了予定日:** {selected_project['end_date']}")
                st.write(f"**予算:** {selected_project['budget']:,}円")
                st.write(f"**案件詳細:**")
                st.write(selected_project['description'])
        else:
            st.info('登録されている案件がありません。')

    elif menu == '案件追加':
        st.header('案件追加')
        customers_df = get_customers()
        if not customers_df.empty:
            with st.form('add_project_form'):
                customer_id = st.selectbox('顧客を選択', customers_df['id'])
                project_name = st.text_input('案件名')
                status = st.selectbox('ステータス', ['未着手', '進行中', '完了', '中断'])
                start_date = st.date_input('開始日')
                end_date = st.date_input('終了予定日')
                budget = st.number_input('予算（円）', min_value=0, step=10000)
                description = st.text_area('案件詳細')
                
                if st.form_submit_button('追加'):
                    if project_name:
                        add_project(customer_id, project_name, status, 
                                  start_date.strftime('%Y-%m-%d'),
                                  end_date.strftime('%Y-%m-%d'),
                                  budget, description)
                        st.success('案件を追加しました！')
                    else:
                        st.error('案件名は必須です。')
        else:
            st.info('先に顧客を登録してください。')

    elif menu == '案件編集':
        st.header('案件編集')
        df = get_projects()
        if not df.empty:
            project_id = st.selectbox('編集する案件を選択', df['id'])
            project = df[df['id'] == project_id].iloc[0]
            
            with st.form('edit_project_form'):
                project_name = st.text_input('案件名', project['project_name'])
                status = st.selectbox('ステータス', ['未着手', '進行中', '完了', '中断'], 
                                    index=['未着手', '進行中', '完了', '中断'].index(project['status']))
                start_date = st.date_input('開始日', datetime.strptime(project['start_date'], '%Y-%m-%d'))
                end_date = st.date_input('終了予定日', datetime.strptime(project['end_date'], '%Y-%m-%d'))
                budget = st.number_input('予算（円）', min_value=0, step=10000, value=project['budget'])
                description = st.text_area('案件詳細', project['description'])
                
                if st.form_submit_button('更新'):
                    update_project(project_id, project_name, status,
                                 start_date.strftime('%Y-%m-%d'),
                                 end_date.strftime('%Y-%m-%d'),
                                 budget, description)
                    st.success('案件情報を更新しました！')
        else:
            st.info('編集可能な案件がありません。')

    elif menu == '案件削除':
        st.header('案件削除')
        df = get_projects()
        if not df.empty:
            project_id = st.selectbox('削除する案件を選択', df['id'])
            if st.button('削除'):
                delete_project(project_id)
                st.success('案件を削除しました！')
        else:
            st.info('削除可能な案件がありません。')

if __name__ == '__main__':
    main() 