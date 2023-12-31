import mysql.connector


def databaseConnect():#connects to database
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="sailboat11",
        database="testdb",
        auth_plugin='mysql_native_password'#this is too ingnore the double authinticator I don't exactly remember but do not delete.
        #code was inspired by https://www.youtube.com/watch?v=x7SwgcpACng
    )



def add_athlete():# this is used to add a athlete to athlete table
    db = databaseConnect() #databaseConnect makes it alot simpler to connect to the database as now you only need to call a function.
    cursor = db.cursor() #you can pass the cursor through the def but not the db
    firstName = input("Enter athlete's first name: ")
    lastName = input("Enter athlete's last name: ")
    grade = input("Enter athlete's grade: ")
    schoolName = input("Enter athlete's school name: ")

    sql = "INSERT INTO Athletes (first_name, last_name, grade, school_name) VALUES (%s, %s, %s, %s)"
    inputs = (firstName, lastName, grade, schoolName)
    cursor.execute(sql, inputs)
    db.commit() #commits the data to the database
    print("1 athlete added.")
    cursor.close()
    db.close()


def get_athlete_id():#this is used to get althete id to use for other functions
    db = databaseConnect()
    cursor = db.cursor()
    firstName = input("Enter athlete's first name: ")
    lastName = input("Enter athlete's last name: ")
    schoolName = input("Enter athlete's school name: ")
    sql = "SELECT athlete_id FROM Athletes WHERE first_name = %s AND last_name = %s AND school_name = %s"
    data = (firstName, lastName, schoolName)
    cursor.execute(sql, data)
    queryOutput = cursor.fetchone()
    cursor.close()
    db.close()

    if queryOutput:
        print("Athlete ID:", queryOutput[0])
        return None
    else:
        print("No athlete found with the provided details.")
        return None

def get_race_id():#this is used so that you can get the race id with the race name to use for other operations
    db = databaseConnect()
    cursor = db.cursor()

    race_name = input("Enter race name: ")

    sql = "SELECT race_id FROM Races WHERE race_name = %s"
    data = (race_name,) #neeeds to be a list or tuple

    cursor.execute(sql, data)
    queryOutput = cursor.fetchone()

    cursor.close()
    db.close()

    if queryOutput:
        print("Race ID: ", queryOutput[0])
        return None
    else:
        print("No race found")
        return None


def update_runner_time():#this is used so that you can alter a runners time
    db = databaseConnect()
    cursor = db.cursor()

    athleteID = input("Enter athlete ID: ")
    raceID = input("Enter race ID: ")
    newTime = input("Enter new time in format 00:00:00  ")
    gender = input("Enter gender (male/female): ")


    inputs = (newTime, athleteID, raceID)

    if gender == 'male':
        sql = "UPDATE MaleRaceResults SET time = %s WHERE athlete_id = %s AND race_id = %s"
    elif gender == 'female':
        sql = "UPDATE FemaleRaceResults SET time = %s WHERE athlete_id = %s AND race_id = %s"
    else:
        print("Invalid gender entered.")
        cursor.close()
        db.close()
        #need to close them and return so it does not print the runner time updated successfully
        return

    cursor.execute( sql, inputs)
    db.commit()

    print("Runner time updated successfully.")

    cursor.close()
    db.close()


def delete_runner_time(): #this is used so that you can remove a runners time from the race results
    db = databaseConnect()
    cursor = db.cursor()

    athleteID = input("Enter athlete id: ")
    raceID = input("Enter race ID: ")
    gender = input("Enter gender male or female: ")



    if gender == "male":
        sql = "DELETE FROM MaleRaceResults WHERE athlete_id = %s AND race_id = %s"
    elif gender == "female":
        sql = "DELETE FROM FemaleRaceResults WHERE athlete_id = %s AND race_id = %s"
    else:
        print("Invalid gender input. Please enter 'male' or 'female'.")
        cursor.close()
        db.close()
        return

    inputs = (athleteID, raceID)
    cursor.execute(sql, inputs)
    db.commit()

    print(f"{gender} runner time deleted successfully.")

    cursor.close()
    db.close()

def add_male_runner_time():#used for adding times to the male racre results table
    db = databaseConnect()
    cursor = db.cursor()

    raceID = input("Enter race ID: ")
    athleteID = input("Enter athlete ID: ")
    time = input("Enter time in form 00:??:?? : ")
    teamID = input("Enter TeamID: ")

    sql = "INSERT INTO MaleRaceResults (race_id, athlete_id, team_id, time) VALUES (%s, %s, %s, %s)"
    inputs = (raceID, athleteID, teamID, time)

    cursor.execute(sql,  inputs)
    db.commit()

    print("Male runner time added successfully.")

    cursor.close()
    db.close()


def add_female_runner_time():
    db = databaseConnect()
    cursor = db.cursor()

    raceID = input("Enter race ID: ")
    athleteID = input("Enter athlete ID: ")
    time = input("Enter time in form 00:??:?? ")
    teamID = input("Enter TeamID: ")

    sql = "INSERT INTO FemaleRaceResults (race_id, athlete_id, team_id, time) VALUES (%s, %s, %s, %s)"
    inputs = (raceID, athleteID, teamID, time)

    cursor.execute(sql,  inputs)
    db.commit()

    print("Female runner time added successfully.")

    cursor.close()
    db.close()

def get_team_id(): #this is needed for get team status
    db = databaseConnect()
    cursor = db.cursor()
    schoolName = input("Enter school name: ")


    sql = "SELECT team_id FROM Teams WHERE school_name = %s"
    inputs = (schoolName,)
    cursor.execute(sql,  inputs)

    queryOutput = cursor.fetchone()
    if queryOutput:
        print(f"Team ID for {schoolName}: {queryOutput[0]}")
    else:
        print("No team found for the given school name.")

    cursor.close()
    db.close()



def get_pr(): #this command finds the athletes fastest time
    db = databaseConnect()
    cursor = db.cursor()

    firstName = input("Enter athlete's first name: ")
    lastName = input("Enter athlete's last name: ")
    schoolName = input("Enter school name: ")
    gender = input("Enter gender (male/female): ").lower()

    if gender == "male":
        sql =  """
               SELECT MIN(time) FROM MaleRaceResults 
               WHERE athlete_id IN 
               (SELECT athlete_id FROM Athletes WHERE first_name = %s AND last_name = %s AND school_name = %s)
               """ #for long queries you can use """ and lay it our on seperate lines to increase readability
    elif gender == "female":
        sql = """SELECT MIN(time) FROM FemaleRaceResults 
               WHERE athlete_id IN 
               (SELECT athlete_id FROM Athletes WHERE first_name = %s AND last_name = %s AND school_name = %s)
               """
    else:
        print("Invalid gender input. Please enter 'male' or 'female'.")
        return

    inputs = (firstName, lastName, schoolName)
    cursor.execute(sql,  inputs)

    queryOutput = cursor.fetchone()
    if queryOutput:
        print(f"PR for {firstName} {lastName} is: {queryOutput[0]}")
    else:
        print("No PR found for the given athlete.")
    cursor.close()
    db.close()

def find_placement(): #this shows the place the athlete came in the race for men or women
    db = databaseConnect()
    cursor = db.cursor()

    raceID = input("Enter race ID: ")
    athleteID = input("Enter athlete ID: ")
    gender = input("Enter gender (male/female): ").lower()

    if gender == "male":
        sql = """
               SELECT COUNT(*) + 1 AS position FROM MaleRaceResults 
               WHERE race_id = %s AND time < (SELECT time FROM MaleRaceResults WHERE athlete_id = %s AND race_id = %s)"""
    elif gender == "female":
        sql = """
               SELECT COUNT(*) + 1 AS position FROM FemaleRaceResults 
               WHERE race_id = %s AND time < (SELECT time FROM FemaleRaceResults WHERE athlete_id = %s AND race_id = %s)"""
    else:
        print("Invalid gender input. Please enter 'male' or 'female'.")
        return

    inputs = (raceID, athleteID, raceID)
    cursor.execute(sql,  inputs)

    queryOutput = cursor.fetchone()
    if queryOutput:
        print(f"Placement for athlete ID {athleteID} in race {raceID} for {gender}s is {queryOutput[0]}")
    else:
        print("No placement data found for the given athlete and race.")

    cursor.close()
    db.close()

def get_athlete_information():#used to learn more about the athlete from their id
    db = databaseConnect()
    cursor = db.cursor()

    athleteID = input("Enter athlete ID: ")

    sql = "SELECT first_name, last_name, grade, school_name FROM Athletes WHERE athlete_id = %s"
    inputs = (athleteID,)#needs to be in list formating
    cursor.execute(sql,  inputs)

    queryOutput = cursor.fetchone()
    if queryOutput:
        print(f"Athlete Information:\nFirst Name: {queryOutput[0]}\nLast Name: {queryOutput[1]}\nGrade: {queryOutput[2]}\nSchool Name: {queryOutput[3]}")
    else:
        print("No athlete found with the given ID.")

    cursor.close()
    db.close()

def get_athlete_information():
    db = databaseConnect()
    cursor = db.cursor()

    athleteID = input("Enter athlete ID: ")

    sql = "SELECT first_name, last_name, grade, school_name FROM Athletes WHERE athlete_id = %s"
    inputs = (athleteID,)
    cursor.execute(sql,  inputs)

    queryOutput = cursor.fetchone()
    if queryOutput:
        print(f"Athlete Information:\nFirst Name: {queryOutput[0]}\nLast Name: {queryOutput[1]}\nGrade: {queryOutput[2]}\nSchool Name: {queryOutput[3]}")
    else:
        print("No athlete found with the given ID.")

    cursor.close()
    db.close()

def show_all_athletes():
    db = databaseConnect()
    cursor = db.cursor()

    cursor.execute("SELECT athlete_id, first_name, last_name, grade, school_name FROM Athletes")
    athletes = cursor.fetchall()

    print("\nAll Athletes:")
    for athlete in athletes:
        print(f"ID: {athlete[0]}, Name: {athlete[1]} {athlete[2]}, Grade: {athlete[3]}, School: {athlete[4]}")

    cursor.close()
    db.close()

def get_race_details(): #this function connects 5 tables and shows details on each of the runners and the races
    db = databaseConnect()
    cursor = db.cursor()

    raceID = input("Enter race ID: ")
    gender = input("Enter gender for the results male or female: ").lower()

    if gender == "male":
        sql = """
        SELECT R.race_id, R.race_name, R.race_location, RP.race_date, T.team_id, T.coach_name, A.athlete_id, A.first_name, A.last_name, A.grade, A.school_name, MRR.time
        FROM Races R
        JOIN RaceParticipants RP ON R.race_id = RP.race_id
        JOIN Teams T ON RP.team_id = T.team_id
        JOIN Athletes A ON T.school_name = A.school_name
        JOIN MaleRaceResults MRR ON A.athlete_id = MRR.athlete_id AND T.team_id = MRR.team_id
        WHERE R.race_id = %s
        ORDER BY MRR.time ASC;
        """
    elif gender == "female": #needs a seperate table for females as race results females is different than males
        sql = """
        SELECT R.race_id, R.race_name, R.race_location, RP.race_date, T.team_id, T.coach_name, A.athlete_id, A.first_name, A.last_name, A.grade, A.school_name, FRR.time
        FROM Races R
        JOIN RaceParticipants RP ON R.race_id = RP.race_id
        JOIN Teams T ON RP.team_id = T.team_id
        JOIN Athletes A ON T.school_name = A.school_name
        JOIN FemaleRaceResults FRR ON A.athlete_id = FRR.athlete_id AND T.team_id = FRR.team_id
        WHERE R.race_id = %s
        ORDER BY FRR.time ASC;
        """
    else:
        print("Invalid gender input. Please enter 'male' or 'female'.")
        cursor.close()
        db.close()
        return

    inputs = (raceID,)
    cursor.execute(sql, inputs)

    query_output = cursor.fetchall()
    if query_output:
        print("Race Details:")
        print(f"Race ID: {query_output[0][0]}, Race Name: {query_output[0][1]}, Location: {query_output[0][2]}, Date: {query_output[0][3]}")

        for row in query_output:
            print(f"Team ID: {row[4]}, Coach: {row[5]}, Athlete ID: {row[6]}, Athlete Name: {row[7]} {row[8]}, Grade: {row[9]}, School: {row[10]}, Time: {row[11]}")
    else:
        print("No details found for the given race ID.")

    cursor.close()
    db.close()


def facilitator_login(): #this is for facilitators to login as only they can change the database
   db = databaseConnect()
   cursor = db.cursor()

   facilitator_id = input("Enter faciletator id: ")
   facilitator_password = input("Enter faciltator password: ")


   sql = "SELECT * FROM FacilitatorLogin WHERE facilitator_id = %s AND facilitator_password = %s"
   inputs = (facilitator_id, facilitator_password)


   cursor.execute(sql, inputs)
   result = cursor.fetchone()

   cursor.close()
   db.close()

   if result:
       print("Login successful")
       return True
   else:
       print("Login failed incorrect ID or password.")
       return False

# Other functions...
# - get_race_id
# - show_race_data
# - update_athlete
# - delete_male_runner_time
# - ...

def main():

    print("Are you a facilitator? (Y/N)")
    userCommand = input()

    if  userCommand == "Y":
        holder = facilitator_login()
        if holder == True:
            while True:
                print("1: Add Athlete")
                print("2: Get Athlete ID")
                print("3: Get race ID")
                print("4: Show Race Data")
                print("5: Update Athlete Time")
                print("6: Delete Runner Time")
                print("7: Add Male Runner Time")
                print("8: Add Female Runner Time")
                print("9: Get Team ID")
                print("10: Get PR")
                print("11: Find Placement")
                print("12: Show All Athletes")
                print("Enter your command or use 'exit' to quit: ")

                userCommand = input()

                if  userCommand == '1':
                    add_athlete()
                elif  userCommand == '2':
                    get_athlete_id()
                elif  userCommand == '3':
                    get_race_id()
                elif userCommand == '4':
                    get_race_details()
                elif  userCommand == '5':
                    update_runner_time()
                elif  userCommand == '6':
                    delete_runner_time()
                elif  userCommand == '7':
                    add_male_runner_time()
                elif  userCommand == '8':
                    add_female_runner_time()
                elif  userCommand == '9':
                    get_team_id()
                elif  userCommand == '10':
                    get_pr()
                elif  userCommand == '11':
                    find_placement()
                elif  userCommand == '12':
                    show_all_athletes()
                elif  userCommand == 'exit':
                    break
                else:
                    print("Wrong input please try again")

                # ... other elif conditions for each function
    else:
        while True:
            print("1: Get Athlete ID")
            print("2: Get race ID")
            print("3: Show Race Data")
            print("4: Get Team ID")
            print("5: Get PR")
            print("6: Find Placement")
            print("7: Show All Athletes")
            print("Enter your  userCommand or use 'exit' to quit: ")

            userCommand = input()
            if  userCommand == '1':
                get_athlete_id()
            elif  userCommand == '2':
                get_race_id()
            elif  userCommand == '3':
                get_race_details()
            elif  userCommand == '4':
                get_team_id()
            elif  userCommand == '5':
                get_pr()
            elif  userCommand == '6':
                find_placement()
            elif  userCommand == '7':
                show_all_athletes()
            elif  userCommand == 'exit':
                break
            else:
                print("Wrong input please try again")


if __name__ == "__main__":
    main()

