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

           
