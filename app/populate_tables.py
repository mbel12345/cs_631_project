# python3 -m app.populate_tables

from app.database import query_file

if __name__ == '__main__':

    query_file('sql/schema/create_tables.sql')
    query_file('sql/insert/insert_data.sql')

    print('Tables populated successfully')
