import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ==========================================
# 1. Models
# ==========================================


class Event:

    def __init__(self, event_id, event_name, date, venue, max_participants):
        self.event_id = event_id
        self.event_name = event_name
        self.date = date
        self.venue = venue
        self.max_participants = max_participants
        self.participants = []

    def add_participant(self, student_id):
        if len(self.participants) >= self.max_participants:
            raise Exception("Event is full!")
        if student_id in self.participants:
            raise Exception("Student already registered!")
        self.participants.append(student_id)

    def remove_participant(self, student_id):
        if student_id in self.participants:
            self.participants.remove(student_id)


class Student:

    def __init__(self, student_id, name, email, department):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.department = department


class Registration:

    def __init__(self, registration_id, student_id, event_id):
        self.registration_id = registration_id
        self.student_id = student_id
        self.event_id = event_id


# ==========================================
# 2. Collections & Management Functions
# ==========================================

events = []
students = []
registrations = []


def save_events():
    os.makedirs("data", exist_ok=True)
    with open("data/events.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["event_id", "event_name", "date", "venue", "max_participants"]
        )
        for event in events:
            writer.writerow(
                [
                    event.event_id,
                    event.event_name,
                    event.date,
                    event.venue,
                    event.max_participants,
                ]
            )


def save_students():
    os.makedirs("data", exist_ok=True)
    with open("data/students.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["student_id", "name", "email", "department"])
        for student in students:
            writer.writerow(
                [
                    student.student_id,
                    student.name,
                    student.email,
                    student.department,
                ]
            )


def save_registrations():
    os.makedirs("data", exist_ok=True)
    with open(
        "data/registrations.csv", "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["registration_id", "student_id", "event_id"])
        for registration in registrations:
            writer.writerow(
                [
                    registration.registration_id,
                    registration.student_id,
                    registration.event_id,
                ]
            )


def load_events():
    file_path = "data/events.csv"
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            event = Event(
                row["event_id"],
                row["event_name"],
                row["date"],
                row["venue"],
                int(row["max_participants"]),
            )
            events.append(event)


def load_students():
    file_path = "data/students.csv"
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            student = Student(
                row["student_id"],
                row["name"],
                row["email"],
                row["department"],
            )
            students.append(student)


def load_registrations():
    file_path = "data/registrations.csv"
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            registration = Registration(
                row["registration_id"], row["student_id"], row["event_id"]
            )
            registrations.append(registration)
            for event in events:
                if event.event_id == row["event_id"]:
                    if row["student_id"] not in event.participants:
                        event.participants.append(row["student_id"])
                    break


def load_all_data():
    load_events()
    load_students()
    load_registrations()


def create_event():
    event_id = input("Enter Event ID: ")
    for event in events:
        if event.event_id == event_id:
            raise Exception("Event ID already exists!")

    event_name = input("Enter Event Name: ")
    date = input("Enter Event Date: ")
    venue = input("Enter Venue: ")
    max_participants = int(input("Enter Maximum Participants: "))

    event = Event(event_id, event_name, date, venue, max_participants)
    events.append(event)
    save_events()
    print("Event created successfully!")


def view_events():
    if not events:
        print("No events available.")
        return

    print("\n----- EVENT LIST -----")
    for event in events:
        print("\nEvent ID:", event.event_id)
        print("Event Name:", event.event_name)
        print("Date:", event.date)
        print("Venue:", event.venue)
        print("Maximum Participants:", event.max_participants)
        print("Registered:", len(event.participants))
        print("----------------------")


def add_student():
    student_id = input("Enter Student ID: ")
    for student in students:
        if student.student_id == student_id:
            raise Exception("Student ID already exists!")

    name = input("Enter Student Name: ")
    email = input("Enter Email: ")
    department = input("Enter Department: ")

    student = Student(student_id, name, email, department)
    students.append(student)
    save_students()
    print("Student added successfully!")


def register_student():
    student_id = input("Enter Student ID: ")
    event_id = input("Enter Event ID: ")

    student = next((s for s in students if s.student_id == student_id), None)
    event = next((e for e in events if e.event_id == event_id), None)

    if student is None:
        raise Exception("Invalid Student ID!")
    if event is None:
        raise Exception("Invalid Event ID!")

    for registration in registrations:
        if (
            registration.student_id == student_id
            and registration.event_id == event_id
        ):
            raise Exception("Student already registered for this event!")

    if len(event.participants) >= event.max_participants:
        raise Exception("Event is full!")

    event.add_participant(student_id)
    registration_id = "R" + str(len(registrations) + 1)
    registration = Registration(registration_id, student_id, event_id)

    registrations.append(registration)
    save_registrations()
    print("Registration successful!")


def search_registered_students():
    event_id = input("Enter Event ID: ")
    event = next((e for e in events if e.event_id == event_id), None)

    if event is None:
        raise Exception("Invalid Event ID!")

    print("\n----- REGISTERED STUDENTS -----")
    if not event.participants:
        print("No students registered for this event.")
        return

    for student_id in event.participants:
        for student in students:
            if student.student_id == student_id:
                print("Student ID:", student.student_id)
                print("Name:", student.name)
                print("Email:", student.email)
                print("Department:", student.department)
                print("----------------------")


def cancel_registration():
    student_id = input("Enter Student ID: ")
    event_id = input("Enter Event ID: ")

    registration_found = next(
        (
            r
            for r in registrations
            if r.student_id == student_id and r.event_id == event_id
        ),
        None,
    )

    if registration_found is None:
        raise Exception("Registration not found!")

    registrations.remove(registration_found)
    for event in events:
        if event.event_id == event_id:
            event.remove_participant(student_id)
            break

    save_registrations()
    print("Registration cancelled successfully!")


def give_feedback():
    event_id = input("Enter Event ID: ")
    student_id = input("Enter Student ID: ")

    event = next((e for e in events if e.event_id == event_id), None)
    if event is None:
        raise Exception("Invalid Event ID!")

    if student_id not in event.participants:
        raise Exception("Student is not registered for this event!")

    rating = int(input("Enter Rating (1-5): "))
    if rating < 1 or rating > 5:
        raise Exception("Rating must be between 1 and 5!")

    comment = input("Enter Feedback Comment: ")

    os.makedirs("data", exist_ok=True)
    file_exists = os.path.exists("data/feedback.csv")

    with open("data/feedback.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["event_id", "student_id", "rating", "comment"])
        writer.writerow([event_id, student_id, rating, comment])

    print("Feedback submitted successfully!")


# ==========================================
# 3. Data Analysis & Visualization
# ==========================================


def load_feedback():
    file_path = "data/feedback.csv"
    if not os.path.exists(file_path):
        print("No feedback file found.")
        return None
    df = pd.read_csv(file_path)
    if df.empty:
        print("No feedback available.")
        return None
    return df


def average_rating():
    df = load_feedback()
    if df is None:
        return
    average = np.mean(df["rating"].to_numpy())
    print("\n----- AVERAGE RATING -----")
    print("Average Rating:", round(average, 2))


def rating_analysis():
    df = load_feedback()
    if df is None:
        return
    print("\n----- RATING ANALYSIS -----")
    rating_count = df["rating"].value_counts().sort_index()
    print(rating_count)


def total_feedback():
    df = load_feedback()
    if df is None:
        return
    print("\n----- TOTAL FEEDBACK -----")
    print("Total Feedback:", len(df))


def event_participation():
    file_path = "data/registrations.csv"
    if not os.path.exists(file_path):
        print("Registration file not found.")
        return
    registrations_df = pd.read_csv(file_path)
    if registrations_df.empty:
        print("No registration data.")
        return
    participation = registrations_df.groupby("event_id").size()
    print("\n----- EVENT-WISE PARTICIPATION -----")
    print(participation)


def feedback_summary():
    df = load_feedback()
    if df is None:
        return
    print("\n================================")
    print("       FEEDBACK SUMMARY")
    print("================================")
    print("Total Feedback:", len(df))
    print("Average Rating:", round(df["rating"].mean(), 2))
    print("\nRating Distribution:")
    print(df["rating"].value_counts().sort_index())
    print("\nEvent-wise Average Rating:")
    print(df.groupby("event_id")["rating"].mean().round(2))


def feedback_bar_chart():
    df = load_feedback()
    if df is None:
        return
    os.makedirs("charts", exist_ok=True)
    rating_count = df["rating"].value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    plt.bar(
        rating_count.index,
        rating_count.values,
        color="skyblue",
        edgecolor="black",
    )
    plt.xlabel("Rating")
    plt.ylabel("Number of Students")
    plt.title("Feedback Rating Distribution (Bar Chart)")
    plt.xticks([1, 2, 3, 4, 5])
    plt.tight_layout()
    plt.savefig("charts/feedback_bar_chart.png")
    plt.show()
    print("Feedback bar chart created!")


def feedback_histogram():
    df = load_feedback()
    if df is None:
        return
    os.makedirs("charts", exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.hist(
        df["rating"].to_numpy(),
        bins=np.arange(0.5, 6.5, 1),
        color="lightgreen",
        edgecolor="black",
    )
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.title("Feedback Rating Histogram")
    plt.xticks([1, 2, 3, 4, 5])
    plt.tight_layout()
    plt.savefig("charts/feedback_histogram.png")
    plt.show()
    print("Feedback histogram created!")


def event_participation_chart():
    file_path = "data/registrations.csv"
    if not os.path.exists(file_path):
        print("Registration file not found.")
        return
    registrations_df = pd.read_csv(file_path)
    if registrations_df.empty:
        print("No registration data.")
        return

    participation = registrations_df.groupby("event_id").size()
    os.makedirs("charts", exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.bar(
        participation.index.astype(str),
        participation.values,
        color="orange",
        edgecolor="black",
    )
    plt.xlabel("Event ID")
    plt.ylabel("Number of Participants")
    plt.title("Event-wise Participation Graph")
    plt.tight_layout()
    plt.savefig("charts/event_participation.png")
    plt.show()
    print("Event participation chart created!")


# ==========================================
# 4. Main Menu Program Executable
# ==========================================

if __name__ == "__main__":
    load_all_data()

    while True:
        print("\n========================================")
        print(" CAMPUS EVENT MANAGEMENT & FEEDBACK")
        print("========================================")
        print("1. Create Event")
        print("2. View Events")
        print("3. Add Student")
        print("4. Register Student")
        print("5. Search Registered Students")
        print("6. Cancel Registration")
        print("7. Give Feedback")
        print("8. Analyze Feedback")
        print("9. Show Charts")
        print("10. Exit")

        choice = input("\nEnter your choice: ")

        try:
            if choice == "1":
                create_event()
            elif choice == "2":
                view_events()
            elif choice == "3":
                add_student()
            elif choice == "4":
                register_student()
            elif choice == "5":
                search_registered_students()
            elif choice == "6":
                cancel_registration()
            elif choice == "7":
                give_feedback()
            elif choice == "8":
                print("\n========================================")
                print("        FEEDBACK ANALYSIS")
                print("========================================")
                average_rating()
                rating_analysis()
                total_feedback()
                event_participation()
                feedback_summary()
            elif choice == "9":
                print("\n========================================")
                print("             SHOW CHARTS")
                print("========================================")
                print("\nCreating Feedback Bar Chart...")
                feedback_bar_chart()
                print("\nCreating Feedback Histogram...")
                feedback_histogram()
                print("\nCreating Event Participation Graph...")
                event_participation_chart()
                print("\nAll charts created successfully!")
                print("Check the 'charts' folder for saved PNG files.")
            elif choice == "10":
                print("\nThank you for using")
                print("Campus Event Management & Feedback System!")
                print("Program closed.")
                break
            else:
                print("\nInvalid choice!")
                print("Please enter a number from 1 to 10.")
        except Exception as e:
            print("\nError:", e)