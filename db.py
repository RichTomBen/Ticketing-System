# Connecting to Database
import mysql.connector as a
connect = a.connect(
    host="localhost",
    user="root",
    password="root",  # change this to whatever your password is
    autocommit=True
)
# Selection or Creation of Database
c = connect.cursor()
c.execute("show databases")
f = c.fetchall()
f1 = []
for i in f:
    f1.append(i)

if ('rtickets',) not in f1:
    try:
        c.execute("create database Rtickets")
        c.execute("use Rtickets")
        c.execute(
            "create table Movies(Movie varchar(30), TheatreRoom int(2), Seats int(2))")

        no_of_theatres = int(input("How many theatres are in your cinema?: "))

        for i in range(1, no_of_theatres+1):
            c.execute(f"create table Seats{i}(Seat char(3), Available int(1))")
            for j in range(1, 11):
                Seats = "insert into Seats{} values('A{}',1)".format(i, j)
                c.execute(Seats)
            for j in range(1, 11):
                Seats = "insert into Seats{} values('B{}',1)".format(i, j)
                c.execute(Seats)
            for j in range(1, 11):
                Seats = "insert into Seats{} values('C{}',1)".format(i, j)
                c.execute(Seats)

        c.execute("create table theatres(theatre int, available int);")

        for i in range(1, no_of_theatres+1):
            c.execute(f"insert into theatres values({i},1)")

        print("CREATED DATABASE 'RTICKETS'")
    except:
        connect.rollback()

# completed
