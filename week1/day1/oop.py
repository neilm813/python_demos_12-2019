# let's represent this lecture with OOP


class Person():
    def __init__(self, first_name, last_name, hobbies=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.hobbies = hobbies

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lecture():
    def __init__(self, topic, date, location, instructor, attendees=[]):
        self.topic = topic
        self.date = date
        self.location = location
        self.instructor = instructor
        self.attendees = attendees

    def print_attendees(self):
        for attendee in self.attendees:
            print(attendee)

    def print_shared_hobbies(self):
        frequency_of_hobbies = {}

        for attendee in self.attendees:
            for hobby in attendee.hobbies:
                if frequency_of_hobbies.get(hobby):
                    frequency_of_hobbies[hobby].append(
                        f"{attendee.first_name} {attendee.last_name}"
                    )
                else:
                    # hobby not in dictionary yet
                    frequency_of_hobbies[hobby] = [
                        f"{attendee.first_name} {attendee.last_name}"
                    ]

        for hobby, enthusiasts in frequency_of_hobbies.items():
            if len(enthusiasts) > 1:
                print(hobby)
                print(enthusiasts)
                print("-" * 15)


current_lecture = Lecture(
    "Python OOP",
    "11/25/2019",
    "Back Room",
    Person("Neil", "M", ["code", "climbing"]),
    [
        Person("Arsalan", "R", ["sleeping", "code", "eating"]),
        Person("Chris", "P", ["Basketball", "code", "cars"]),
        Person("Zion", "H", ["troublemaking", "code", "gaming"]),
        Person("Shaun", "D", ["Jager", "HGH", "gaming"]),
        Person("Duane", "R", ["code", "exercise", "gaming"]),
        Person("Rolando", "L", ["code", "exercise", "eating"]),
    ]
)

other_lecture = Lecture(
    "Csharp OOP",
    "11/25/2019",
    "Fish Bowl",
    Person("Nadia", "N", ["code"]),
    [
        Person("Zara", "G", ["sleeping", "code", "eating"]),
        Person("Kathy", "D", ["dodgeball", "code"]),
    ]
)


class Dojo():
    def __init__(self, location, current_lectures=[]):
        self.location = location
        self.current_lectures = current_lectures

    def print_current_lectures_details(self):
        for lecture in self.current_lectures:
            print(f"Lecture Topic: {lecture.topic}")
            print(f"Instructor: {lecture.instructor}")
            print("Attendees:")
            lecture.print_attendees()
            print("-" * 15)


our_dojo = Dojo("OC", [
    current_lecture,
    other_lecture
])

# our_dojo.print_current_lectures_details()
print(
    our_dojo.current_lectures[0].print_shared_hobbies()
)
