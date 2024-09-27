import db
from functions import admin, user, yourUser, cancelTickets
import mysql.connector as a
connect = a.connect(host="localhost",
                    user="root",
                    password="root",  # change this to whatever your passwrod is
                    database="Rtickets",
                    autocommit=True,
                    )
c = connect.cursor()

while True:
    print("""------------------------------------------- WELCOME TO RTICKETS -------------------------------------------
1. Buy Tickets
2. Your Tickets
3. Cancel Tickets
4. Admin     
5. Exit""")

    chUser = int(input("Choose your selection: "))
    if chUser == 1:
        user()
    if chUser == 2:
        yourUser()
    if chUser == 3:
        cancelTickets()
    if chUser == 4:
        admin()
    if chUser == 5:
        connect.close()
        break
