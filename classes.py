import MySQLdb, datetime

# db class
class dataBase:
    def __init__(self):
        self.db = MySQLdb.connect("localhost","python","python3","userData" )
        self.cursor = self.db.cursor()

    # check if the card uid already existes in the db
    def checkUID(self, card_uid):
        sql = "select * from employees where card_uid="+card_uid
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if(len(data) == 0):
                return True
            return False, data[0]
        except:
            return False, None

    # check the permissions the selected user id has
    def checkPermission(self, uid, per):
        sql = "select "+per+" from users where id="+str(uid)
        data = None
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except:
            self.db.rollback()
            return False, ""

        if(len(data) != 0):
            if(data[0][0] == True):
                return True
            return False
        else:
            return False

    # find the username in the db
    def checkUser(self, username):
        sql = "select * from users where username='"+username+"'"
        data = None
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except:
            self.db.rollback()
            return False, ""

        if(len(data) != 0):
            return True, data[0]
        else:
            return False, ""

    # conve the object to json
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

    # match the first or last name of the employee
    def findEmployee(self, string):
        sql = "select * from employees where firstname like '%"+string+"%' or lastname like '%"+string+"%'"
        d = None
        try:
            self.cursor.execute(sql)
            d = self.cursor.fetchall()
        except:
            self.db.rollback()
            return False, ""
        
        if(len(d) == 0):
            return False, ""

        data = self.empJson(d)

        return True, data

    # return the employee data from their uid
    def employee(self, uid):
        sql = "select * from employees where id="+uid
        d = None
        try:
            self.cursor.execute(sql)
            d = self.cursor.fetchall()
        except:
            self.db.rollback()
            return False, ""

        if(len(d) != 0):
            data = self.empJson(d)
            return True, data
        else:
            return True, ""

    # return the logs data of the spec user id
    def employeeLogs(self, uid):
        sql = "select * from employee_logs where user_id="+uid+" ORDER BY date, time asc"
        d = None
        try:
            self.cursor.execute(sql)
            d = self.cursor.fetchall()
        except:
            self.db.rollback()
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

    # return all employee logs 
    def employeesLogs(self):
        sql = "select * from employee_logs ORDER BY date, time asc"
        d = None
        try:
            self.cursor.execute(sql)
            d = self.cursor.fetchall()
        except:
            self.db.rollback()
            return False, ""
        
        sql = "select * from employees"
        e = None
        try:
            self.cursor.execute(sql)
            e = self.cursor.fetchall()
        except:
            self.db.rollback()
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

    # add user to db
    def addUser(self, first, last, user, password, email, edit, add, block, delete):
        sql = "insert into users (firstname, lastname, username, password, email, edit_per, add_per, block_per, delete_per) values ('%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s)" % (first, last, user, password, email, edit, add, block, delete)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            return False, "Couldn't add the requested user!"

        return True, "User has been added"

    # check if new username and email are unique in the db
    def uniqueUser(self, username, email):
        sql = "select * from users where username='"+username+"' or email='"+email+"'"
        d = None
        try:
            self.cursor.execute(sql)
            d = self.cursor.fetchall()
        except:
            self.db.rollback()
            return False

        if(len(d) == 0):
            return True
        return False

    # add new employee to db
    def addEmployee(self, first, last, address, card_uid, path):
        sql = "insert into employees (firstname, lastname, address, card_uid, img_path) values ('%s', '%s', '%s', '%s', '%s')" % (first, last, address, card_uid, path)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            return False, "Couldn't add the requested employee!"

        return True, "Employee has been added"

    # set employee block
    def setBlock(self, uid, start, end):
        sql = "insert into blocked_employee (user_id, block_start, block_end) values ('%s', '%s', '%s')" % (uid, start, end)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            return False, "Couldn't block the requested employee!"

        return True, "Employee has been blocked"

    # check whether the supplied uid is blocked
    def check_block(self, uid):
        sql = "select * from blocked_employee where user_id="+str(uid)
        d = None
        date = None
        
        try:
            self.cursor.execute(sql)
            d = self.cursor.fetchall()
        except:
            return False, None, None

        if(len(d) != 0):
            data = d[len(d)-1]
        else:
            return False, None, None

        start_date = data[2] 
        end_date = data[3]
        current_date = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        
        if(current_date >= start_date and current_date <= end_date):
            return True, start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return False, None, None
