import sqlite3
from datetime import date, timedelta
from datetime import datetime

task = "0"

def print_row(row):
    print("|", end="")
    for value in row:
        print(f" {str(value).ljust(20)} |", end="")
    print()

while task != "9":
    conn = sqlite3.connect('Library.db')

    print("1. Find an item in the library \n")
    print("2. Borrow an item from the library \n")
    print("3. Return a borrow item \n")
    print("4. Donate an item to the library \n")
    print("5. Find an event in the library \n")
    print("6. Register for an event in the library \n")
    print("7. Volunteer for the library \n")
    print("8. Ask for help from a librarian \n")
    print("9. Exit\n")

    task = input("Enter the number of task that you want to choose ")
    
    if task == "9":
        if conn:
            conn.close()
            print("Closed database successfully")

#======================================================================================
    elif task == "1":
        itemName = input("Enter the name of the item that you want: ")

        cursor = conn.cursor()
        print("Opened database successfully \n")

        with conn:

            cur = conn.cursor()

            myQuery = "SELECT * FROM items WHERE itemName=:name"

            cur.execute(myQuery,{"name":itemName})

            rows=cur.fetchall()
            if rows:
                print("We do have the following item " + itemName + ": ")
                header = [description[0] for description in cur.description]      
                print_row(header)
                print("-" * (22 * len(header) + len(header) - 1))           
                for row in rows:
                    print_row(row)              
            else:
                print("Unfortunately, we do not have item " + itemName + "!\n")
                print("Below are the list of items we have to offer and their current status\n")
                allItemsQuery = "SELECT * FROM items"
                cur.execute(allItemsQuery)
                rows=cur.fetchall()
                header = [description[0] for description in cur.description]
                print_row(header)
                print("-" * (22 * len(header) + len(header) - 1))
                for row in rows:
                    print_row(row)


#==========================================================================================================

    elif task == "2":
        itemName = input("Enter the name of the item that you want to borrow: ")

        cursor = conn.cursor()

        with conn:

            cur = conn.cursor()

            myQuery = "SELECT * FROM items WHERE itemName=:name AND status = 'Available'"

            cur.execute(myQuery,{"name":itemName})

            rows=cur.fetchall()
            if rows:
                print("We do have the following item " + itemName + ": ")
                header = [description[0] for description in cur.description]
                print_row(header)
                print("-" * (22 * len(header) + len(header) - 1))               
                for row in rows:
                    print_row(row)   

                itemID= input("Enter the id of the item that you want to borrow: ")
                mySecondQuery = "UPDATE items SET status  = 'Unavailable' WHERE itemId =:Id"
                cur.execute(mySecondQuery,{"Id":itemID})
                
                today = date.today()
                due = today + timedelta(days = 7)
                    
                personID = input("Please provide your personID (If you do not have ID, please type no) :")

                if personID == "no":
                    fName = input("Please provide your first name : ")
                    lName = input("Please provide your last name : ")

                    age = input("Are you children or adult : ")
                    sql = "INSERT INTO people VALUES ( NULL, :ps, :fn, :ln)"
                    cur.execute(sql,{"ps":age, "fn":fName, "ln":lName})
                    conn.commit()
                    sql2 = "SELECT * FROM people WHERE firstName = :fn AND lastName = :ln "
                    cur.execute(sql2,{"fn":fName,"ln":lName})
                    personRow = cur.fetchall()
                    personID, person_status, first_name, last_name = personRow[0]
                    # print(str(personID) +" " +person_status + first_name + last_name)
                    header = [description[0] for description in cur.description]
                    print_row(header)
                    print("-" * (22 * len(header) + len(header) - 1))                
                    for row in personRow:
                        print_row(row)                     
                    
                
                insert = "INSERT INTO borrow VALUES ( NULL, :Id, :pId, :borrowDay, :dueDay, 'notReturn')"
                cur.execute(insert,{"Id":itemID, "pId":personID, "borrowDay":today, "dueDay":due})
                conn.commit
                print("Thank you for your patient, the process is complete")
            else:
                print("Unfortunately, we do not have item " + itemName + "!\n")

#=======================================================================================

    elif task == "3":
        with conn:
            cur =conn.cursor()

            person_id = input("Please provide your personID: ")
            sql = "SELECT * FROM borrow b JOIN items i ON b.itemId = i.itemId WHERE personId = :id AND returnStatus = 'notReturn'"
            cur.execute(sql,{"id":person_id})
            rows = cur.fetchall()
            if rows :
                header = [description[0] for description in cur.description]
                print_row(header)
                print("-" * (22 * len(header) + len(header) - 1))                
                for row in rows:
                    print_row(row)
                # for row in rows:
                #     print(row)
                #     print("\n")
                book_id = input("Please provide your bookID that you want to return: ")
                today = date.today()
                sql2 = "UPDATE borrow SET returnStatus  = 'returned' WHERE itemId =:Id"
                cur.execute(sql2,{"Id":book_id})
                sql4 = "UPDATE items SET status  = 'Available' WHERE itemId =:Id"
                cur.execute(sql4,{"Id":book_id})
                sql3 = "SELECT * FROM borrow WHERE itemId = :id"
                cur.execute(sql3,{"id":book_id})
                detail = cur.fetchall()
                if detail:
                    borrow_id, item_id, person_id, borrow_day, due_day, return_status = detail[0]
                    date_format = '%Y-%m-%d'
                    if datetime.strptime(due_day,date_format).date() > today:
                        conn.commit()
                        print("Thank you for your patient, the book has been returned")
                    else:
                        conn.commit()
                        print("Thank you for your patient, the book has been returned, but you are late for the book return.\n Please charge for 100 dollar in the front side.")
                else:
                    print("The book id you input is incorrect\n")
            else:
                print("You haven't borrow any books")

        
#=======================================================================================
    elif task == "4":

        with conn:

            cur = conn.cursor()

            item_name = input("Please provide us with the name of the book: ")
            genre = input("What is the genre of the book you donated? Is it Print book, Online book, Magazine, Scientific Journal, or CD? ")
            author = input("Please provide us the name of the author? ")
            published_date = input("When was the book publihsed? ")
            myQuery = "INSERT INTO items VALUES (NULL, :Genre, :Author, :PublishedDate, 'Available', :Name)"
            cur.execute(myQuery, {"Genre": genre, "Author": author, "PublishedDate": published_date, "Name": item_name})

#==========================================================================================================

    elif task == "5":
        event_name = input("Enter the name of the event: ")
        event_date = input("Enter the date of the event: ")

        cursor = conn.cursor()

        if conn:

            cur = conn.cursor()

            myQuery = "SELECT * FROM events WHERE eventName=:name AND eventDate=:date"
            cur.execute(myQuery,{"name":event_name, "date": event_date})
            rows1=cur.fetchall()

            mySecondQuery = "SELECT * FROM events WHERE eventName=:name OR eventDate=:date"
            cur.execute(mySecondQuery,{"name":event_name, "date": event_date})
            rows2 = cur.fetchall()

            myThirdQuery = "SELECT * FROM events"
            cur.execute(myThirdQuery)
            rows3 = cur.fetchall()

            if rows1:
                print("You might be looking for the following events: ")
                header = [description[0] for description in cur.description]
                print_row(header)
                print("-" * (22 * len(header) + len(header) - 1))                
                for row in rows1:
                    print_row(row)
                # for row in rows1:
                #     print(row)
                #     print("\n")
            elif rows2: 
                header = [description[0] for description in cur.description]
                print_row(header)
                print("-" * (22 * len(header) + len(header) - 1))                
                for row in rows2:
                    print_row(row)                
                # for row in rows2:
                #     print(row)
                #     print("\n")
            else:
                print("Sorry, we cannot find the events that matches your description, the list below are the events that will be held recently\n")
                header = [description[0] for description in cur.description]
                print_row(header)
                print("-" * (22 * len(header) + len(header) - 1))                
                for row in rows3:
                    print_row(row)
                # for row in rows3:
                #     print(row)
                #     print("\n")

#=======================================================================================
    elif task == "6":

        with conn:

            cur = conn.cursor()

            event_name = input("Enter the name of the event: ")
            event_date = input("Enter the date of the event in the following form year-month-day(ie. 2006-03-25): ")
            event_time = input("Enter the time of the event in the following form hour:minute:sec(ie. 09:30:00): ")
            print("What is the type of the event? Is it for children, adult, or teens?\n")
            event_type = input("Please enter 'For children', 'For teens', or 'For adults':\n")
            roomQuery = "SELECT * FROM rooms WHERE roomNumber NOT IN (SELECT roomNumber FROM events WHERE eventDate=:EventDate AND eventTime=:EventTime)"
            cur.execute(roomQuery, {"EventDate": event_date, "EventTime": event_time})
            rows = cur.fetchall()

            if rows:
                room_number, location = rows[0]
                insertQuery = "INSERT INTO events VALUES (NULL, :EventName, :EventType, :EventDate, :EventTime, :RoomNumber)"
                cur.execute(insertQuery, {"EventName": event_name, "EventType": event_type, "EventDate": event_date, "EventTime": event_time, "RoomNumber": room_number})
                print("Your activity will be held in " + location + "\n")
            else:
                print("Unfortunately, all rooms are booked at this time")

#=======================================================================================
    elif task == "7":
        with conn:
            cur = conn.cursor()
            personID = input("Please provide your personID (If you do not have ID, please type no) :")

            if personID == "no":
                fName = input("Please provide your first name : ")
                lName = input("Please provide your last name : ")
                age = input("Are you children or adult : ")
                sql = "INSERT INTO people VALUES ( NULL, :ps, :fn, :ln)"
                cur.execute(sql,{"ps":age, "fn":fName, "ln":lName})
                conn.commit()
                sql2 = "SELECT * FROM people WHERE firstName = :fn AND lastName = :ln "
                cur.execute(sql2,{"fn":fName,"ln":lName})
                personRow = cur.fetchall()
                personID, person_status, first_name, last_name = personRow[0]

            sql3 = "INSERT INTO staffs VALUES (NULL, :id, 'volunteer', 'Unavailable')"
            cur.execute(sql3,{"id": personID})
            sql4 = "SELECT * FROM staffs WHERE personId = :id"
            cur.execute(sql4,{"id": personID})
            staff = cur.fetchall()
            staff_id, person_id, position, status = staff[0]
            conn.commit()
            print("Thank you for your patient, you have been one of the volunteer for this library with staff ID " + str(staff_id))

            

#=======================================================================================
    elif task == "8":

        with conn:

            cur = conn.cursor()

            myQuery = "SELECT * FROM staffs WHERE status = 'Available' AND position = 'Librarian'"

            cur.execute(myQuery)

            staffRows=cur.fetchall()
            if staffRows:
                staff_id, person_id, position, status = staffRows[0]
                mySecondQuery = "SELECT * FROM people WHERE personId=:Id"

                cur.execute(mySecondQuery,{"Id":person_id})
                personRows = cur.fetchall()
                personId, person_status, first_name, last_name = personRows[0]

                print(first_name + " will assist you!")

                myThirdQuery = "UPDATE staffs SET status  = 'Unavailable' WHERE staffId =:Id"
                cur.execute(myThirdQuery, {"Id":staff_id})
            else:
                print("All of our staffs are currently busy!\n")       

#=======================================================================================
    else:
        print("Your input is invalid, please try again")    

              