import MySQLdb, datetime

class dataBase:
    def __init__(self):
        self.db = MySQLdb.connect("localhost","rfid","password","userData" )
        self.cursor = self.db.cursor()

    def checkUser(self, username):
        sql = "select * from users where username='"+username+"'"
        data = None
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except:
            return False, None

        if(len(data) != 0):
            return True, data[0]
        else:
            return False, None
