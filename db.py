import mysql.connector

con = mysql.connector.connect(
    host='sql6.freesqldatabase.com',
    user='sql6637839',
    password='H4SEpRlrcf',
    db='sql6637839'
)

query = '''
CREATE TABLE complaints (
  `regno` varchar(10),
  `complaint` varchar(300)
);
'''

# query = "drop table leaverequests"

cursor = con.cursor()

cursor.execute(query)

con.commit()

cursor.close()
con.close()