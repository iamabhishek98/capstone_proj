import psycopg2
import time

class DB():
    def __init__(self):
        #Establish the connection
        self.conn = psycopg2.connect(
            database="cg4002",
            user="postgres",
            password="cg4002",
            host="localhost",
            port="5433")

        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()

    def insertBeetle(self, dev, time, ax, ay, az, gx, gy, gz, activation=1): 
        query = "insert into Beetle(uid, time, yaw, pitch, roll, x, y, z, activation) values ('{}', {}, {}, {}, {}, {}, {}, {}, '{}')".format(dev, time, gx, gy, gz, ax, ay, az, activation)
        self.cur.execute(query)
        self.conn.commit()
        print(query)

    def insertEMG(self, time, rms, mav, zcs):
        query = "insert into EMG(time, rms, mav, zcs) values ({}, {}, {}, {})".format(time, rms, mav, zcs)
        self.cur.execute(query)
        self.conn.commit()
        print(query)

    def insertMove(self, start_time_one, start_time_two, start_time_three, prediction, start_time = 0):
        query = "insert into DanceMove(start_time, start_time_one, start_time_two, start_time_three, prediction) values({}, {}, {}, {}, '{}')".format(start_time, start_time_one, start_time_two, start_time_three, prediction)
        self.cur.execute(query)
        self.conn.commit()
        print(query)

    def insertPosition(self, left_slot, middle_slot, right_slot, start_time = 0):
        query = "insert into DancePosition(start_time, left_slot, middle_slot, right_slot) values({}, '{}', '{}', '{}')".format(start_time, left_slot, middle_slot, right_slot)  
        self.cur.execute(query)
        self.conn.commit()  
        print(query)
        
def main():
    #driver code solely for debug purposes.
    a = 1617114953641623423
    print(int(a))
    print("jojo")
    db = DB()
    # insert sample msg here.
    msg = "!M|#1 2 3|sidepump|26 0 45"
    #

    tokens = msg.split('|')

    # insert parsing and saving here.
    delays = list(map(int, tokens[3].split(" ")))
    prediction = tokens[2]
    db.insertMove(delays[0], delays[1], delays[2], prediction)
    db.insertPosition(tokens[1][1], tokens[1][3], tokens[1][5])
    #


if __name__ == '__main__':
    main()

#Establish the connection
# conn = psycopg2.connect(
#     database="cg4002",
#     user="postgres",
#     password="cg4002",
#     host="localhost",
#     port="5433")

# cur = conn.cursor()


# test_query = "select 1;"
# cur.execute(test_query)
# print()
# print(cur.fetchone())

# cur.close()



# def insertEMGData(voltage):
#     insert into EMG(voltage) values (${voltage});


## LEGACY

# create_bettle_query = """ CREATE TABLE bettle (
#                         dancer_id integer not null,
#                         time timestamp not null,
#                         x numeric not null,
#                         y numeric not null,
#                         z numeric not null
#                       );"""

# cur.execute("CREATE TABLE beetle(id integer primary key, x numeric, y numeric, z numeric);")
# cur.execute("INSERT INTO beetle VALUES(2, 1, 2, 3);")
# conn.commit()

# cur.execute("SELECT * FROM beetle;")