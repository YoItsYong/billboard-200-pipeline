import pandas as pd
import sqlite3
import requests

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    
    url = 'https://www.dropbox.com/s/ahog97hcatpiddk/billboard-200.db?dl=1'
    response = requests.get(url)

    with open('billboard-200.db', 'wb') as f:
        f.write(response.content)

    conn = sqlite3.connect('billboard-200.db')
    cursor = conn.cursor()

    # Connects to SQLite Master file to get 'name' column where row type is 'table'
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    table_name = tables[0][0]
    query = (f'SELECT * FROM {table_name}')

    csv_path = '../bb200_albums.csv'

    df = pd.read_sql_query(query, conn) \
        .to_csv(csv_path, compression='gzip')
    
    data = pd.read_csv(csv_path, compression='gzip')
    print(data.dtypes)
    
    return data