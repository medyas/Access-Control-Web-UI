import MySQLdb, datetime

class dataBase:
    def __init__(self):
        self.db = MySQLdb.connect("localhost","python","python3","userData" )
        self.cursor = self.db.cursor()

    def checkUser(self, username):
        sql = "select * from users where username='"+username+"'"
        data = None
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except:
            return False, ""

        if(len(data) != 0):
            return True, data[0]
        else:
            return False, ""

    def empJson(self, d):
        data = []
        for l in d:
            temp = {
                    'id': l[0],
                    'firstname':l[1],
                    'lastname':l[2],
                    'address':l[3],
                    'card_uid':l[4],
                    'img_path':l[5] 
                }
            data.append(temp)
        return data

    def findEmployee(self, string):
        sql = "select * from employees where firstname like '%"+string+"%' or lastname like '%"+string+"%'"
        d = None
        try:
            self.cursor.execute(sql)
            d = self.cursor.fetchall()
        except:
            return False, ""
        
        if(len(d) == 0):
            return False, ""

        data = self.empJson(d)

        return True, data

    def employee(self, uid):
        sql = "select * from employees where id="+uid
        d = None
        try:
            self.cursor.execute(sql)
            d = self.cursor.fetchall()
        except:
            return False, ""

        if(len(d) != 0):
            data = self.empJson(d)
            return True, data
        else:
            return True, ""

    def employeeLogs(self, uid):
        sql = "select * from employee_logs where user_id="+uid+" ORDER BY date, time asc"
        d = None
        try:
            self.cursor.execute(sql)
            d = self.cursor.fetchall()
        except:
            return False, ""

        if(len(d) != 0):
            data = []
            for l in d:
                temp = {
                        'id': l[0],
                        'user_id':l[1],
                        'date':l[2].strftime("%Y-%m-%d"),
                        'time':str(l[3])
                    }
                data.append(temp)
            return True, data
        else:
            return True, ""


    def employeesLogs(self):
        sql = "select * from employee_logs ORDER BY date, time asc"
        d = None
        try:
            self.cursor.execute(sql)
            d = self.cursor.fetchall()
        except:
            return False, ""
        
        sql = "select * from employees"
        e = None
        try:
            self.cursor.execute(sql)
            e = self.cursor.fetchall()
        except:
            return False, ""

        if(len(d) != 0 and len(e) != 0):
            print(d[0][1])
            data = []
            for l in d:
                temp = {
                        'scan_id': l[0],
                        'user_id':l[1],
                        'name': e[l[1]-1][1]+", "+e[l[1]-1][2],
                        'card_uid': e[l[1]-1][4],
                        'date':l[2].strftime("%Y-%m-%d"),
                        'time':str(l[3])
                    }
                data.append(temp)
            return True, data
        else:
            return True, ""

    def addUser(first, last, user, password, email, edit, add, block, delete):
        sql = "insert into users (firstname, lastname, username, password, email) values (%s,)" % (first, last)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            return False, "Couldn't add the requested user!"

        return True, "User has been added"


        
