import db
import random
import string
# connector
import mysql.connector as a
connect = a.connect(host="localhost",
                    user="root",
                    password="root",  # change this to whatever your password is
                    database="Rtickets",
                    autocommit=True,
                    )
c = connect.cursor()
# code


def admin():
    print("------------------------------------------- WELCOME ADMINISTRATOR --------------------------------------------")
    passwd = input("ENTER YOUR PASSWORD: ")

    if passwd == "admin@123":
        print("""1. Add movies 
2. Remove movies
3. Your movies
4. Exit""")

        choice_admin = int(input("Enter your selection: "))
        if choice_admin == 1:
            theatres = []
            c.execute("select theatre from theatres where available = 1")
            availabletheatres = c.fetchall()
            for i in availabletheatres:
                theatres.append(i[0])

            c.execute("select theatreroom from movies")

            select_theatres = c.fetchall()
            taken_Theatres = []
            for i in select_theatres:
                taken_Theatres += [i[0]]

            for i in theatres:
                if i in taken_Theatres:
                    theatres.remove(i)

            lenTheatres = len(theatres)

            numMovies = int(input("How many movies do you want to add? "))
            if numMovies <= lenTheatres:
                for i in range(numMovies):
                    movie = input("Enter movie name: ")
                    print(f"Available Theatrerooms: {theatres}")
                    theatreroom = int(input("Enter theatre room: "))

                    if theatreroom in theatres:
                        c.execute("insert into movies values('{}',{},30)".format(
                            movie, theatreroom))
                        c.execute(
                            f"update theatres set available = 0 where theatre = {theatreroom}")
                        theatres.remove(theatreroom)
                        print(f"Movie {movie} added to Theatre #{theatreroom}")
                    else:
                        print("Theatreroom is not available")
                        break
            else:
                print("Number of theatres is not available")

        if choice_admin == 2:
            c.execute("select * from movies")
            movies = c.fetchall()
            totalmovies = len(movies)
            print("MOVIE & TOTAL SEATS")
            for i in range(totalmovies):
                print(movies[i][0], movies[i][2])
            numMovies = int(
                input("Enter the number of movies you want to remove: "))
            for i in range(numMovies):
                removie = input("Enter the movie you want to remove: ")
                c.execute('show tables like "_____";')
                userids = c.fetchall()
                for i in userids:
                    # removes the tickets from the user ids
                    c.execute(f'delete from {i[0]} where movie = "{removie}";')
                c.execute(
                    f'select TheatreRoom from movies where Movie = "{removie}"')
                retheatre = c.fetchall()
                c.execute(
                    f'update theatres set available = 1 where theatre = "{retheatre[0][0]}"')
                c.execute(
                    f"delete from movies where movie = '{removie}'")

            print(f"{removie} succesfully removed.")
        if choice_admin == 3:
            c.execute("select * from movies;")
            info = c.fetchall()
            print("*******************************")
            for i in info:
                print(
                    f"""Movie: {i[0]}
Theatre: {i[1]}
No.of seats available: {i[2]}
*******************************""")


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def user():
    print("Do you have an existing booking ID? (Y/N): ")
    existing_id = input()
    if existing_id == "N":
        c.execute("select * from movies")
        movies = c.fetchall()
        totalmovies = len(movies)
        print("MOVIE & TOTAL SEATS")
        for i in range(totalmovies):
            print(movies[i][0], movies[i][2])
        print("TYPE THE MOVIE NAME YOU WANT TO BUY")
        movieChoice = input("Enter movie here: ")

        print("AVAILABLE SEATS:")
        c.execute(
            f"select theatreroom from movies where movie='{movieChoice}'")
        userTheatre = c.fetchall()
        userTheatre = userTheatre[0][0]
        c.execute(f"select available from seats{userTheatre}")
        selectSeats = c.fetchall()
        getSeats = []
        for i in selectSeats:
            getSeats += [i[0]]

        print("  1   2   3   4   5   6   7   8   9   10  ")
        print("A", end=' ')
        for i in range(10):
            if getSeats[i] == 1 and i != 9:
                print("O", end='   ')
            if i == 9 and getSeats[i] == 1:
                print("O")
            if getSeats[i] == 0 and i != 9:
                print("*", end='   ')
            if i == 9 and getSeats[i] == 0:
                print('*')

        print("B", end=' ')
        for i in range(10, 20):
            if getSeats[i] == 1 and i != 19:
                print("O", end='   ')
            if i == 19 and getSeats[i] == 1:
                print("O")
            if getSeats[i] == 0 and i != 19:
                print("*", end='   ')
            if i == 19 and getSeats[i] == 0:
                print('*')

        print("C", end=' ')
        for i in range(20, 30):
            if getSeats[i] == 1 and i != 29:
                print("O", end='   ')
            if i == 29 and getSeats[i] == 1:
                print("O")
            if getSeats[i] == 0 and i != 29:
                print("*", end='   ')
            if i == 29 and getSeats[i] == 0:
                print('*')

        print("PLEASE SELECT YOUR SEAT")
        userSeat = input().upper()
        c.execute(
            f"select Available from seats{userTheatre} where Seat = '{userSeat}'")
        available = c.fetchall()

        if available[0][0] == 1:
            c.execute(
                f"update seats{userTheatre} set available = 0 where seat = '{userSeat}'")
            c.execute(
                f"update movies set seats = seats - 1 where movie = '{movieChoice}'")

            userid = get_random_string(5)
            ticketid = random.randint(10000000, 99999999)

            c.execute(
                f"create table {userid}(movie varchar(20), theatre int(1), seat char(2), id int)")
            c.execute(
                f"insert into {userid} values('{movieChoice}',{userTheatre},'{userSeat}',{ticketid})")
            print("TICKET SUCCESSFULLY BOOKED!")
            print(
                f"Your ticket for {movieChoice} is in Theatre {userTheatre} and seat number {userSeat} has been successfully booked.")
            print(
                f"Please note down your booking id: {userid} | Your ticket ID: {ticketid}")
        else:
            print("Seat already taken")
    if existing_id == "Y":
        userid = input("Enter user id: ")
        useridtup = (userid,)
        c.execute('show tables like "_____";')
        userids = c.fetchall()
        if useridtup in userids:
            c.execute("select * from movies")
            movies = c.fetchall()
            totalmovies = len(movies)
            print("MOVIE & TOTAL SEATS")
            for i in range(totalmovies):
                print(movies[i][0], movies[i][2])
            print("TYPE THE MOVIE NAME YOU WANT TO BUY")
            movieChoice = input()

            print("AVAILABLE SEATS:")
            c.execute(
                "select theatreroom from movies where movie='{}'".format(movieChoice))
            userTheatre = c.fetchall()
            userTheatre = userTheatre[0][0]
            c.execute("select available from seats{}".format(userTheatre))
            selectSeats = c.fetchall()
            getSeats = []
            for i in selectSeats:
                getSeats += [i[0]]

            print("  1   2   3   4   5   6   7   8   9   10  ")
            print("A", end=' ')
            for i in range(10):
                if getSeats[i] == 1 and i != 9:
                    print("O", end='   ')
                if i == 9 and getSeats[i] == 1:
                    print("O")
                if getSeats[i] == 0 and i != 9:
                    print("*", end='   ')
                if i == 9 and getSeats[i] == 0:
                    print('*')

            print("B", end=' ')
            for i in range(10, 20):
                if getSeats[i] == 1 and i != 19:
                    print("O", end='   ')
                if i == 19 and getSeats[i] == 1:
                    print("O")
                if getSeats[i] == 0 and i != 19:
                    print("*", end='   ')
                if i == 19 and getSeats[i] == 0:
                    print('*')

            print("C", end=' ')
            for i in range(20, 30):
                if getSeats[i] == 1 and i != 29:
                    print("O", end='   ')
                if i == 29 and getSeats[i] == 1:
                    print("O")
                if getSeats[i] == 0 and i != 29:
                    print("*", end='   ')
                if i == 29 and getSeats[i] == 0:
                    print('*')

            print("PLEASE SELECT YOUR SEAT")
            userSeat = input().upper()
            c.execute(
                f"select Available from seats{userTheatre} where Seat = '{userSeat}'")
            available = c.fetchall()
            if available[0][0] == 1:
                c.execute("update seats{} set available = 0 where seat = '{}'".format(
                    userTheatre, userSeat))
                c.execute(
                    "update movies set seats = seats - 1 where movie = '{}'".format(movieChoice))

                ticketid = random.randint(10000000, 99999999)

                print(ticketid)

                c.execute("insert into {} values('{}',{},'{}',{})".format(
                    userid, movieChoice, userTheatre, userSeat, ticketid))
                print("TICKET SUCCESSFULLY BOOKED!")
                print("Your ticket for {} is in Theatre {} and seat number {} has been successfully booked.".format(
                    movieChoice, userTheatre, userSeat))
                print("Your ticket ID: {}".format(ticketid))
            else:
                print("Seat already taken")
        else:
            print("User ID doesnt exist")


def yourUser():  # take booking id from user and display the info
    print("Enter your Booking ID:")
    bookID = input()
    c.execute(f"select * from {bookID}")
    userInfo = c.fetchall()
    print("Your Tickets: ")
    for i in userInfo:
        print(f'''Movie: {i[0]}
Theatre Number: {i[1]}
Seat Number: {i[2]}
Ticket ID: {i[3]}''')
        print('*****************')


def cancelTickets():  # cancel the tickets already booked
    print("Enter your booking ID: ")
    bookID = input()
    bookIDtup = (bookID,)
    c.execute('show tables LIKE "_____"')
    bookIDs = c.fetchall()
    if bookIDtup in bookIDs:
        c.execute(f"select id from {bookID}")
        ticketIDs = c.fetchall()
        ticID = int(input("Enter the ticket ID you wish to delete: "))
        tickID = (ticID,)
        if tickID in ticketIDs:
            confirmation = input(
                f"Are you sure you want to cancel ticket #{ticID}? Y/N: ")
            if confirmation == "Y":
                c.execute(
                    f"select theatre,seat from {bookID} where id = {ticID}")
                theatreseat = c.fetchall()
                c.execute(
                    f'update seats{theatreseat[0][0]} set Available = 1 where Seat = "{theatreseat[0][1]}";')
                c.execute(f"delete from {bookID} where id = {ticID};")
                c.execute(
                    f"update movies set seats = seats + 1 where theatreroom = '{theatreseat[0][0]}'")
                connect.commit()
                print("Ticket deleted")
            else:
                print("Invalid Ticket ID")
    else:
        print("Booking ID not found")
