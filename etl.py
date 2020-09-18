import configparser
import psycopg2
from sql_queries import copy_table_queries
from sql_queries import insert_table_queries



def load_staging_tables(cur, conn):
    """
    his method is used for loading staging tables 
    using the copy command
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

def insert_tables(cur, conn):
    """
    This method is used to insert into fact and dimensional 
    tables from the staging tables in redshift
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    This is the main which calls two methods:
    - load_staging_tables
    - insert_tables
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()