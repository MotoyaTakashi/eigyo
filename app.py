import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import hashlib
import shutil
import os

# データベース接続
def init_db():
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    # ユーザーテーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY,
         password TEXT NOT NULL,
         role TEXT NOT NULL)
    ''')
    # デフォルトユーザーの追加（パスワードは"password"のハッシュ）
    try:
        default_password = hashlib.sha256("password".encode()).hexdigest()
        c.execute('''
            INSERT OR IGNORE INTO users (username, password, role)
            VALUES (?, ?, ?)
        ''', ('admin', default_password, 'admin'))
    except:
        pass
    # 顧客テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers
        (corporate_number TEXT PRIMARY KEY,
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
         corporate_number TEXT,
         project_name TEXT NOT NULL,
         status TEXT,
         start_date TEXT,
         end_date TEXT,
         budget INTEGER,
         sales_person TEXT,
         description TEXT,
         FOREIGN KEY (corporate_number) REFERENCES customers (corporate_number))
    ''')
    # 営業日報テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_reports
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         report_date TEXT NOT NULL,
         corporate_number TEXT,
         project_id INTEGER,
         contact_type TEXT,
         contact_content TEXT,
         next_action TEXT,
         notes TEXT,
         FOREIGN KEY (corporate_number) REFERENCES customers (corporate_number),
         FOREIGN KEY (project_id) REFERENCES projects (id))
    ''')
    conn.commit()
    conn.close()

# 顧客データの追加
def add_customer(corporate_number, company_name, contact_person, email, phone, address, last_contact_date, notes):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO customers (corporate_number, company_name, contact_person, email, phone, address, last_contact_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (corporate_number, company_name, contact_person, email, phone, address, last_contact_date, notes))
    conn.commit()
    conn.close()

# 顧客データの取得
def get_customers():
    conn = sqlite3.connect('customers.db')
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()
    return df

# 顧客データの更新
def update_customer(corporate_number, company_name, contact_person, email, phone, address, last_contact_date, notes):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('''
        UPDATE customers
        SET company_name=?, contact_person=?, email=?, phone=?, address=?, last_contact_date=?, notes=?
        WHERE corporate_number=?
    ''', (company_name, contact_person, email, phone, address, last_contact_date, notes, corporate_number))
    conn.commit()
    conn.close()

# 顧客データの削除
def delete_customer(corporate_number):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('DELETE FROM customers WHERE corporate_number=?', (corporate_number,))
    conn.commit()
    conn.close()

# 案件データの追加
def add_project(corporate_number, project_name, status, start_date, end_date, budget, sales_person, description):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO projects (corporate_number, project_name, status, start_date, end_date, budget, sales_person, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (corporate_number, project_name, status, start_date, end_date, budget, sales_person, description))
    conn.commit()
    conn.close()

# 案件データの取得
def get_projects(corporate_number=None):
    conn = sqlite3.connect('customers.db')
    if corporate_number:
        df = pd.read_sql_query("""
            SELECT p.*, c.company_name
            FROM projects p
            JOIN customers c ON p.corporate_number = c.corporate_number
            WHERE p.corporate_number = ?
        """, conn, params=(corporate_number,))
    else:
        df = pd.read_sql_query("""
            SELECT p.*, c.company_name
            FROM projects p
            JOIN customers c ON p.corporate_number = c.corporate_number
        """, conn)
    conn.close()
    return df

# 案件データの更新
def update_project(id, corporate_number, project_name, status, start_date, end_date, budget, sales_person, description):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('''
        UPDATE projects
        SET corporate_number=?, project_name=?, status=?, start_date=?, end_date=?, budget=?, sales_person=?, description=?
        WHERE id=?
    ''', (corporate_number, project_name, status, start_date, end_date, budget, sales_person, description, id))
    conn.commit()
    conn.close()

# 案件データの削除
def delete_project(id):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('DELETE FROM projects WHERE id=?', (id,))
    conn.commit()
    conn.close()

# 営業日報の追加
def add_daily_report(report_date, corporate_number, project_id, contact_type, contact_content, next_action, notes):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO daily_reports (report_date, corporate_number, project_id, contact_type, contact_content, next_action, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (report_date, corporate_number, project_id, contact_type, contact_content, next_action, notes))
    conn.commit()
    conn.close()

# 営業日報の取得
def get_daily_reports():
    conn = sqlite3.connect('customers.db')
    df = pd.read_sql_query("""
        SELECT r.*, c.company_name, p.project_name
        FROM daily_reports r
        LEFT JOIN customers c ON r.corporate_number = c.corporate_number
        LEFT JOIN projects p ON r.project_id = p.id
        ORDER BY r.report_date DESC
    """, conn)
    conn.close()
    return df

# 営業日報の更新
def update_daily_report(id, report_date, corporate_number, project_id, contact_type, contact_content, next_action, notes):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('''
        UPDATE daily_reports
        SET report_date=?, corporate_number=?, project_id=?, contact_type=?, contact_content=?, next_action=?, notes=?
        WHERE id=?
    ''', (report_date, corporate_number, project_id, contact_type, contact_content, next_action, notes, id))
    conn.commit()
    conn.close()

# 営業日報の削除
def delete_daily_report(id):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute('DELETE FROM daily_reports WHERE id=?', (id,))
    conn.commit()
    conn.close()

# ユーザー認証
def authenticate_user(username, password):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

# データベースのダウンロード
def get_database_download():
    try:
        with open('customers.db', 'rb') as f:
            return f.read()
    except Exception as e:
        return None

# アプリケーションのメイン部分
def main():
    # データベースの初期化
    init_db()
    
    # セッション状態の初期化
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None

    # ログイン画面
    if not st.session_state.authenticated:
        st.sidebar.title("ログイン")
        username = st.sidebar.text_input("ユーザー名")
        password = st.sidebar.text_input("パスワード", type="password")
        
        if st.sidebar.button("ログイン"):
            user = authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.username = user[0]
                st.session_state.role = user[2]
                st.sidebar.success("ログイン成功！")
                st.rerun()
            else:
                st.sidebar.error("ユーザー名またはパスワードが正しくありません。")
        
        st.stop()
    
    # メインアプリケーション
    st.title("営業管理システム")
    
    # サイドバーで操作を選択
    st.sidebar.title('メニュー')
    
    # GitHubのIssuesページへのリンクを追加
    st.sidebar.markdown("[GitHub Issues](https://github.com/MotoyaTakashi/eigyo/issues)")
    
    # 言語選択
    language = st.sidebar.selectbox(
        '言語 / Language',
        ['日本語', 'English']
    )
    
    # メインカテゴリの選択
    main_category = st.sidebar.selectbox(
        '管理カテゴリを選択' if language == '日本語' else 'Select Category',
        ['顧客管理', '案件管理', '営業日報'] if language == '日本語' else ['Customer Management', 'Project Management', 'Daily Report']
    )
    
    # メニュー項目の定義
    menu_items = {
        '日本語': {
            '顧客管理': {
                'header': '顧客管理メニュー',
                'items': ['顧客一覧', '顧客追加', '顧客編集', '顧客削除']
            },
            '案件管理': {
                'header': '案件管理メニュー',
                'items': ['案件一覧', '案件追加', '案件編集', '案件削除']
            },
            '営業日報': {
                'header': '営業日報メニュー',
                'items': ['日報一覧', '日報追加', '日報編集', '日報削除']
            }
        },
        'English': {
            'Customer Management': {
                'header': 'Customer Management Menu',
                'items': ['Customer List', 'Add Customer', 'Edit Customer', 'Delete Customer']
            },
            'Project Management': {
                'header': 'Project Management Menu',
                'items': ['Project List', 'Add Project', 'Edit Project', 'Delete Project']
            },
            'Daily Report': {
                'header': 'Daily Report Menu',
                'items': ['Report List', 'Add Report', 'Edit Report', 'Delete Report']
            }
        }
    }
    
    # メニュー項目の対応関係
    menu_mapping = {
        '日本語': {
            '顧客管理': 'Customer Management',
            '案件管理': 'Project Management',
            '営業日報': 'Daily Report'
        },
        'English': {
            'Customer Management': '顧客管理',
            'Project Management': '案件管理',
            'Daily Report': '営業日報'
        }
    }
    
    # 現在の言語とカテゴリに対応するメニュー項目を取得
    current_menu = menu_items[language][main_category]
    st.sidebar.header(current_menu['header'])
    
    # サブメニューの選択
    sub_menu = st.sidebar.selectbox(
        '操作を選択' if language == '日本語' else 'Select Operation',
        current_menu['items']
    )
    
    # データベースダウンロードボタンを追加
    st.sidebar.markdown("---")  # 区切り線を追加
    db_data = get_database_download()
    if db_data:
        st.sidebar.download_button(
            label="データベースをダウンロード",
            data=db_data,
            file_name="customers.db",
            mime="application/x-sqlite3"
        )
    else:
        st.sidebar.error("データベースファイルの読み込みに失敗しました。")
    
    # メインカテゴリの処理
    if main_category in ['顧客管理', 'Customer Management']:
        # 顧客管理の処理
        if sub_menu in ['顧客一覧', 'Customer List']:
            st.header('顧客一覧')
            df = get_customers()
            if not df.empty:
                # 表示する列を選択
                display_columns = ['corporate_number', 'company_name', 'contact_person', 'email', 'phone', 'address', 'last_contact_date', 'notes']
                display_df = df[display_columns].copy()
                
                # 列名を日本語に変更
                column_names = {
                    'corporate_number': '法人番号',
                    'company_name': '会社名',
                    'contact_person': '担当者名',
                    'email': 'メールアドレス',
                    'phone': '電話番号',
                    'address': '住所',
                    'last_contact_date': '最終接触日',
                    'notes': '備考'
                }
                display_df = display_df.rename(columns=column_names)
                
                # データフレームを表示（インデックスを非表示に）
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.info('登録されている顧客がありません。')
            
        elif sub_menu in ['顧客追加', 'Add Customer']:
            st.header('顧客追加')
            with st.form('add_customer_form'):
                corporate_number = st.text_input('法人番号')
                company_name = st.text_input('会社名')
                contact_person = st.text_input('担当者名')
                email = st.text_input('メールアドレス')
                phone = st.text_input('電話番号')
                address = st.text_area('住所')
                last_contact_date = st.date_input('最終接触日')
                notes = st.text_area('備考')
                
                if st.form_submit_button('追加'):
                    if company_name:
                        add_customer(
                            corporate_number,
                            company_name,
                            contact_person,
                            email,
                            phone,
                            address,
                            last_contact_date.strftime('%Y-%m-%d'),
                            notes
                        )
                        st.success('顧客を追加しました！')
                    else:
                        st.error('会社名は必須です。')
            
        elif sub_menu in ['顧客編集', 'Edit Customer']:
            st.header('顧客編集')
            df = get_customers()
            if not df.empty:
                corporate_number = st.selectbox('編集する顧客を選択', df['corporate_number'])
                customer = df[df['corporate_number'] == corporate_number].iloc[0]
                
                with st.form('edit_customer_form'):
                    company_name = st.text_input('会社名', customer['company_name'])
                    contact_person = st.text_input('担当者名', customer['contact_person'])
                    email = st.text_input('メールアドレス', customer['email'])
                    phone = st.text_input('電話番号', customer['phone'])
                    address = st.text_area('住所', customer['address'])
                    last_contact_date = st.date_input('最終接触日', datetime.strptime(customer['last_contact_date'], '%Y-%m-%d'))
                    notes = st.text_area('備考', customer['notes'])
                    
                    if st.form_submit_button('更新'):
                        if company_name:
                            update_customer(
                                corporate_number,
                                company_name,
                                contact_person,
                                email,
                                phone,
                                address,
                                last_contact_date.strftime('%Y-%m-%d'),
                                notes
                            )
                            st.success('顧客情報を更新しました！')
                        else:
                            st.error('会社名は必須です。')
            else:
                st.info('編集可能な顧客がありません。')
            
        elif sub_menu in ['顧客削除', 'Delete Customer']:
            st.header('顧客削除')
            df = get_customers()
            if not df.empty:
                corporate_number = st.selectbox('削除する顧客を選択', df['corporate_number'])
                if st.button('削除'):
                    delete_customer(corporate_number)
                    st.success('顧客を削除しました！')
            else:
                st.info('削除可能な顧客がありません。')
    
    elif main_category in ['案件管理', 'Project Management']:
        # 案件管理の処理
        if sub_menu in ['案件一覧', 'Project List']:
            st.header('案件一覧')
            df = get_projects()
            if not df.empty:
                # 表示する列を選択
                display_columns = ['id', 'company_name', 'project_name', 'status', 'start_date', 'end_date', 'budget', 'sales_person']
                display_df = df[display_columns].copy()
                
                # 列名を日本語に変更
                column_names = {
                    'id': 'ID',
                    'company_name': '顧客名',
                    'project_name': '案件名',
                    'status': 'ステータス',
                    'start_date': '開始日',
                    'end_date': '終了予定日',
                    'budget': '予算',
                    'sales_person': '営業担当'
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
                    st.write(f"**終了予定日:** {selected_project['end_date']}")
                    st.write(f"**予算（千円）:** {selected_project['budget']}")
                
                with col2:
                    st.write(f"**説明:**")
                    st.write(selected_project['description'])
            else:
                st.info('登録されている案件がありません。')
        
        elif sub_menu in ['案件追加', 'Add Project']:
            st.header('案件追加')
            customers_df = get_customers()
            if not customers_df.empty:
                with st.form('add_project_form'):
                    # 顧客選択用の辞書を作成
                    customer_options = {f"{row['company_name']} ({row['corporate_number']})": row['corporate_number'] 
                                      for _, row in customers_df.iterrows()}
                    selected_customer = st.selectbox('顧客を選択', options=list(customer_options.keys()))
                    corporate_number = customer_options[selected_customer]
                    
                    project_name = st.text_input('案件名')
                    status = st.selectbox('ステータス', ['未着手', '進行中', '完了', '保留'])
                    start_date = st.date_input('開始日')
                    end_date = st.date_input('終了予定日')
                    budget = st.number_input('予算（千円）', min_value=0)
                    sales_person = st.text_input('担当者名')
                    description = st.text_area('説明')
                    
                    if st.form_submit_button('追加'):
                        if project_name:
                            add_project(
                                corporate_number,
                                project_name,
                                status,
                                start_date.strftime('%Y-%m-%d'),
                                end_date.strftime('%Y-%m-%d'),
                                budget,
                                sales_person,
                                description
                            )
                            st.success('案件を追加しました！')
                        else:
                            st.error('案件名は必須です。')
            else:
                st.info('先に顧客を登録してください。')
        
        elif sub_menu in ['案件編集', 'Edit Project']:
            st.header('案件編集')
            df = get_projects()
            if not df.empty:
                project_id = st.selectbox('編集する案件を選択', df['id'])
                project = df[df['id'] == project_id].iloc[0]
                
                with st.form('edit_project_form'):
                    # 顧客選択用の辞書を作成
                    customers_df = get_customers()
                    customer_options = {f"{row['company_name']} ({row['corporate_number']})": row['corporate_number'] 
                                      for _, row in customers_df.iterrows()}
                    
                    # 現在の顧客の法人番号に対応する表示名を探す
                    current_customer_display = None
                    for display, corp_num in customer_options.items():
                        if corp_num == project['corporate_number']:
                            current_customer_display = display
                            break
                    
                    # デフォルト値として現在の顧客を設定
                    selected_customer = st.selectbox('顧客を選択', 
                                                   options=list(customer_options.keys()),
                                                   index=list(customer_options.keys()).index(current_customer_display) if current_customer_display else 0)
                    corporate_number = customer_options[selected_customer]
                    
                    project_name = st.text_input('案件名', project['project_name'])
                    status = st.selectbox('ステータス', ['未着手', '進行中', '完了', '保留'],
                                        index=['未着手', '進行中', '完了', '保留'].index(project['status']))
                    start_date = st.date_input('開始日', datetime.strptime(project['start_date'], '%Y-%m-%d'))
                    end_date = st.date_input('終了予定日', datetime.strptime(project['end_date'], '%Y-%m-%d'))
                    budget = st.number_input('予算（千円）', min_value=0, value=project['budget'])
                    sales_person = st.text_input('担当者名', project['sales_person'])
                    description = st.text_area('説明', project['description'])
                    
                    if st.form_submit_button('更新'):
                        if project_name:
                            update_project(
                                project_id,
                                corporate_number,
                                project_name,
                                status,
                                start_date.strftime('%Y-%m-%d'),
                                end_date.strftime('%Y-%m-%d'),
                                budget,
                                sales_person,
                                description
                            )
                            st.success('案件を更新しました！')
                        else:
                            st.error('案件名は必須です。')
            else:
                st.info('編集可能な案件がありません。')
        
        elif sub_menu in ['案件削除', 'Delete Project']:
            st.header('案件削除')
            df = get_projects()
            if not df.empty:
                project_id = st.selectbox('削除する案件を選択', df['id'])
                if st.button('削除'):
                    delete_project(project_id)
                    st.success('案件を削除しました！')
            else:
                st.info('削除可能な案件がありません。')
    
    else:
        # 営業日報の処理
        if sub_menu in ['日報一覧', 'Report List']:
            st.header('営業日報一覧')
            df = get_daily_reports()
            if not df.empty:
                # 表示する列を選択
                display_columns = ['id', 'report_date', 'company_name', 'project_name', 'contact_type', 'contact_content']
                display_df = df[display_columns].copy()
                
                # 列名を日本語に変更
                column_names = {
                    'id': 'ID',
                    'report_date': '日付',
                    'company_name': '顧客名',
                    'project_name': '案件名',
                    'contact_type': '接触種別',
                    'contact_content': '内容'
                }
                display_df = display_df.rename(columns=column_names)
                
                # データフレームを表示（インデックスを非表示に）
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # 日報の詳細を表示するセクション
                st.subheader('日報詳細')
                report_id = st.selectbox('詳細を表示する日報を選択', df['id'])
                selected_report = df[df['id'] == report_id].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**日付:** {selected_report['report_date']}")
                    st.write(f"**顧客名:** {selected_report['company_name']}")
                    st.write(f"**案件名:** {selected_report['project_name']}")
                    st.write(f"**接触種別:** {selected_report['contact_type']}")
                
                with col2:
                    st.write(f"**接触内容:**")
                    st.write(selected_report['contact_content'])
                    st.write(f"**次回アクション:**")
                    st.write(selected_report['next_action'])
                    st.write(f"**備考:**")
                    st.write(selected_report['notes'])
            else:
                st.info('登録されている日報がありません。')
        
        elif sub_menu in ['日報追加', 'Add Report']:
            st.header('営業日報追加')
            customers_df = get_customers()
            if not customers_df.empty:
                with st.form('add_report_form'):
                    report_date = st.date_input('日付', datetime.now())
                    
                    # 顧客選択用の辞書を作成
                    customer_options = {f"{row['company_name']} ({row['corporate_number']})": row['corporate_number'] 
                                      for _, row in customers_df.iterrows()}
                    selected_customer = st.selectbox('顧客を選択', options=list(customer_options.keys()))
                    corporate_number = customer_options[selected_customer]
                    
                    # 選択された顧客の案件を取得
                    projects_df = get_projects(corporate_number)
                    project_id = None
                    if not projects_df.empty:
                        # 案件選択用の辞書を作成
                        project_options = {f"{row['project_name']}": row['id'] 
                                         for _, row in projects_df.iterrows()}
                        selected_project = st.selectbox('案件を選択', options=list(project_options.keys()))
                        project_id = project_options[selected_project]
                    
                    contact_type = st.selectbox('接触種別', ['電話', 'メール', '訪問', 'オンライン会議', 'その他'])
                    contact_content = st.text_area('接触内容')
                    next_action = st.text_area('次回アクション')
                    notes = st.text_area('備考')
                    
                    if st.form_submit_button('追加'):
                        add_daily_report(
                            report_date.strftime('%Y-%m-%d'),
                            corporate_number,
                            project_id,
                            contact_type,
                            contact_content,
                            next_action,
                            notes
                        )
                        st.success('営業日報を追加しました！')
            else:
                st.info('先に顧客を登録してください。')
        
        elif sub_menu in ['日報編集', 'Edit Report']:
            st.header('営業日報編集')
            df = get_daily_reports()
            if not df.empty:
                report_id = st.selectbox('編集する日報を選択', df['id'])
                report = df[df['id'] == report_id].iloc[0]
                
                with st.form('edit_report_form'):
                    report_date = st.date_input('日付', datetime.strptime(report['report_date'], '%Y-%m-%d'))
                    
                    # 顧客選択用の辞書を作成
                    customers_df = get_customers()
                    customer_options = {f"{row['company_name']} ({row['corporate_number']})": row['corporate_number'] 
                                      for _, row in customers_df.iterrows()}
                    
                    # 現在の顧客の法人番号に対応する表示名を探す
                    current_customer_display = None
                    for display, corp_num in customer_options.items():
                        if corp_num == report['corporate_number']:
                            current_customer_display = display
                            break
                    
                    # デフォルト値として現在の顧客を設定
                    selected_customer = st.selectbox('顧客を選択', 
                                                   options=list(customer_options.keys()),
                                                   index=list(customer_options.keys()).index(current_customer_display) if current_customer_display else 0)
                    corporate_number = customer_options[selected_customer]
                    
                    # 選択された顧客の案件を取得
                    projects_df = get_projects(corporate_number)
                    project_options = {f"{row['project_name']}": row['id'] 
                                     for _, row in projects_df.iterrows()}
                    
                    # 現在の案件のIDに対応する案件名を探す
                    current_project_name = None
                    if report['project_id'] is not None:  # project_idがNoneでない場合のみ処理
                        for project_name, pid in project_options.items():
                            if pid == report['project_id']:
                                current_project_name = project_name
                                break
                    
                    # デフォルト値として現在の案件を設定
                    selected_project = st.selectbox('案件を選択', 
                                                  options=list(project_options.keys()),
                                                  index=list(project_options.keys()).index(current_project_name) if current_project_name else 0)
                    project_id = project_options[selected_project]
                    
                    contact_type = st.selectbox('接触種別', ['電話', 'メール', '訪問', 'オンライン会議', 'その他'],
                                              index=['電話', 'メール', '訪問', 'オンライン会議', 'その他'].index(report['contact_type']))
                    contact_content = st.text_area('接触内容', report['contact_content'])
                    next_action = st.text_area('次回アクション', report['next_action'])
                    notes = st.text_area('備考', report['notes'])
                    
                    if st.form_submit_button('更新'):
                        update_daily_report(
                            report_id,
                            report_date.strftime('%Y-%m-%d'),
                            corporate_number,
                            project_id,
                            contact_type,
                            contact_content,
                            next_action,
                            notes
                        )
                        st.success('営業日報を更新しました！')
            else:
                st.info('編集可能な日報がありません。')
        
        elif sub_menu in ['日報削除', 'Delete Report']:
            st.header('営業日報削除')
            df = get_daily_reports()
            if not df.empty:
                report_id = st.selectbox('削除する日報を選択', df['id'])
                if st.button('削除'):
                    delete_daily_report(report_id)
                    st.success('営業日報を削除しました！')
            else:
                st.info('削除可能な日報がありません。')

if __name__ == '__main__':
    main() 