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
	cur.execute("CREATE TABLE IF NOT EXISTS {} (value TEXT, data TEXT)".format(table_name))
	cur.execute("INSERT INTO {} VALUES(?,?)".format(table_name), (value_entered, data_entered))
	connect_me.commit()
	connect_me.close()	

store('TEST12','ayushagr','hbcse','disc_meta.db')
store('TEST12','ayushagr','bits', 'disc_meta.db')
print(identify('TEST12','ayushagr','disc_meta.db'))
store('category','kanav','mor','disc_meta.db')
store('TEST5','ayush','the great','disc_meta.db')
