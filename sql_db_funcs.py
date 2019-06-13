import sqlite3

def identify(name_entered, value_entered, filename):
	conn = sqlite3.connect(filename)
	c = conn.cursor()
	value_entered = str(value_entered)
	name_entered = str(name_entered)
	t=c.execute('SELECT data FROM {} WHERE value=?'.format(name_entered),(value_entered,)).fetchall()
	if(len(t) != 0):
		data = [x[0] for x in t]
		if len(data) >1:
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
        data_check = (cur.execute("SELECT COUNT(*) FROM {} WHERE value=?", .format(table_name), (value_entered))).fetchone()[0]

        if data_check != 0:
                cur.execute("UPDATE {} SET data=data+{} WHERE value=?", .format(table_name,data_entered), (value_entered))

        else:
                cur.execute("INSERT INTO {} VALUES(?,?)", .format(table_name), (value_entered, data_entered))

        connect_me.commit()
        connect_me.close()


