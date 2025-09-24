import os

def get_db_params():
    """Get database-specific parameters and syntax"""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///attendance.db')
    
    if database_url.startswith('postgresql'):
        return {
            'placeholder': '%s',
            'returning': 'RETURNING id',
            'now': 'NOW()',
            'datetime_now': 'NOW()',
            'bool_true': 'TRUE',
            'bool_false': 'FALSE'
        }
    else:
        return {
            'placeholder': '?',
            'returning': '',
            'now': 'CURRENT_TIMESTAMP',
            'datetime_now': "datetime('now')",
            'bool_true': '1',
            'bool_false': '0'
        }

def execute_query(conn, query, params=None, fetch_one=False, fetch_all=False):
    """Execute query with proper parameter handling"""
    db_params = get_db_params()
    
    # Replace placeholders if needed
    if db_params['placeholder'] == '%s':
        query = query.replace('?', '%s')
    
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    if fetch_one:
        return cursor.fetchone()
    elif fetch_all:
        return cursor.fetchall()
    else:
        return cursor