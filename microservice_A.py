# microservice_A - Create Exercise

# This microservice will listen for changes to the 'action' cell
# of communication.db, and if action == 1, the microservice will
# create a workout with 'name', 'sets', and 'reps' and store it
# in the workout_tracker.db.


import sqlite3

conn = sqlite3.connect('workout_tracker.db')
cursor = conn.cursor()

comm_conn = sqlite3.connect('communication.db')
comm_cursor = comm_conn.cursor()


def create_exercise(name, sets, reps):
    cursor.execute("INSERT INTO exercises (name, sets, reps) VALUES (?, ?, ?)", (name, sets, reps))
    conn.commit()


while True:
    comm_cursor.execute("SELECT action FROM communication")
    action = comm_cursor.fetchone()
    if action is not None:
        if action[0] == 1:
            # create workout
            comm_cursor.execute("SELECT * FROM communication")
            workout = comm_cursor.fetchall()
            workout = workout[0]
            create_exercise(workout[1], workout[2], workout[3])
            print("Workout created")

            # reset communication
            comm_cursor.execute("DELETE FROM communication WHERE action=1")
            comm_conn.commit()
