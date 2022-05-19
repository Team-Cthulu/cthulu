import MySQLdb as mariadb
from db_credentials import host, user, passwd, db

def connect_to_database(host = host, user = user, passwd = passwd, db = db):
    db_connection = mariadb.connect(host,user,passwd,db)
    return db_connection

def execute_query(db_connection = None, query = None, query_params = ()):
    if db_connection is None:
        print("No connection to the database!")
        return None

    if query is None or len(query.strip()) == 0:
        print("Query is empty")
        return None

    print("Executing %s with %s" % (query, query_params))
    cursor = db_connection.cursor()

    cursor.execute(query, query_params)

    db_connection.commit()

    return cursor

if __name__ == '__main__':
    print("Executing a sample query on the database using db_credentials.py")
    db = connect_to_database()
    query = "SELECT * from Orcs;"
    results = execute_query(db, query)
    print("Printing results of %s" %s query)

    for r in results.fetchall():
        print(r)