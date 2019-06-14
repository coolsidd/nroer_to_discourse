import sqlite3


def identify(name_entered, value_entered, filename):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    value_entered = str(value_entered)
    name_entered = str(name_entered)
    t = c.execute(
        "SELECT data FROM {} WHERE value=?".format(name_entered), (value_entered,)
    ).fetchall()
    if len(t) != 0:
        data = [x[0] for x in t]
        if len(data) > 1:
            return data
        else:
            return data[0]
    else:
        return None


def store(table_name, value_entered, data_entered, db_name):
    table_name = str(table_name)
    value_entered = str(value_entered)
    connect_me = sqlite3.connect(db_name)
    cur = connect_me.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS {} (value TEXT, data TEXT)".format(table_name)
    )
    cur.execute(
        "INSERT INTO {} VALUES(?,?)".format(table_name), (value_entered, data_entered)
    )
    connect_me.commit()
    connect_me.close()


def convert_to_csv(csv_file_name, db_file_name):
    import csv

    with open(csv_file_name, "a+") as csv_file:
        writer = csv.writer(csv_file)
        conn = sqlite3.connect(db_file_name)
        c = conn.cursor()
        tables = [
            x[0]
            for x in c.execute(
                "select name from sqlite_master where type = 'table'"
            ).fetchall()
        ]
        for table in tables:
            for row in c.execute("select * from {}".format(table)).fetchall():
                csv_row = list(row)
                csv_row.insert(0, table)
                writer.writerow(csv_row)
        csv_file.flush()
