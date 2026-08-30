"""
Übung: Notenverwaltungssystem

Ziel: Baue ein kleines System zur Verwaltung von Schüler:innen und ihren Noten.

Geübte Konzepte:
- Klassen & OOP (Attribute, Methoden, __init__, __repr__)
- Eigene Exceptions
- Dictionaries & List Comprehensions
- Sortieren mit key-Funktionen (lambda)
- String-Formatierung (f-strings)

"""



class InvalidGradeError(Exception):
    """Raised when grades are either below 1.0 or above 6.0"""

    pass



class Student:
    def __init__(self, name):
        self.name = name
        self.grades = {}

    def add_grade(self, subject, grade):

        try:
            if grade >= 1.0 and grade <= 6.0:
                if subject not in self.grades:
                    self.grades[subject] = grade
                else:
                    self.grades[subject].append(grade)

        except InvalidGradeError as e:
            print(f"{e} grade is either to low or to high")



        pass

    def average(self, subject=None):

        if subject is not None:
            grade = self.grades[subject]

            avg = sum(grade)

            avg = round(avg/len(grade), 2)
            return avg
        else:

            flatlist = [x for l in self.grades.values() for x in l]

            avg = sum(flatlist)
            avg = round(avg / len(flatlist), 2)
            return avg




        pass

    def __repr__(self):
        # TODO 5: Gib eine sinnvolle String-Repräsentation zurück, z.B.:
        #         "Student(name='Anna', durchschnitt=2.15)"
        #         Nutze dafür self.average().
        pass


class ClassRoom:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def best_students(self, n=3):
        """Gibt die n besten Studierenden zurück (niedrigster Durchschnitt = am besten).

        TODO 6: Sortiere self.students nach ihrem Gesamtdurchschnitt
                (aufsteigend, kleinster Wert zuerst) und gib die
                ersten n Elemente als Liste zurück.
                Nutze sorted() mit einem key=lambda.
        """
        pass

    def subject_ranking(self, subject):
        """Gibt eine Liste von (name, durchschnitt) Tupeln zurück, sortiert
        nach dem besten Durchschnitt in einem bestimmten Fach.

        TODO 7: Nur Studierende berücksichtigen, die überhaupt Noten in
                diesem Fach haben. Nutze dafür list comprehension +
                Exception-Handling (z.B. try/except oder Prüfung mit `in`).
        """
        pass


# ---------------------------------------------------------------------------
# Testblock — hier prüfst du deine Lösung. Nicht verändern, nur ausführen.
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    anna = Student('Anna')
    anna.add_grade('Mathe', 1.7)
    anna.add_grade('Mathe', 2.0)
    anna.add_grade('Deutsch', 2.3)

    ben = Student('Ben')
    ben.add_grade('Mathe', 3.0)
    ben.add_grade('Deutsch', 1.3)

    print(anna)
    print(ben)

    print(f"Annas Mathe-Durchschnitt: {anna.average('Mathe')}")
    print(f"Annas Gesamtdurchschnitt: {anna.average()}")

    try:
        anna.add_grade('Mathe', 7.0)
    except InvalidGradeError as e:
        print(f"Erwarteter Fehler abgefangen: {e}")

    klasse = ClassRoom()
    klasse.add_student(anna)
    klasse.add_student(ben)

    print("Beste Studierende:", klasse.best_students(2))
    print("Ranking Mathe:", klasse.subject_ranking('Mathe'))
