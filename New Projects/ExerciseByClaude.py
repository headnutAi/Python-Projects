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


        if grade >= 1.0 and grade <= 6.0:
            self.grades.setdefault(subject, []).append(grade)
        else:
            raise InvalidGradeError(f"{grade} liegt nicht innerhalb des Spektrums, nicht zwischen 1 & 6")

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

        return f"Student(name={self.name!r}, durchschnitt={self.average()})"

        pass


class ClassRoom:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def best_students(self, x=3):

        n = len(self.students)

        for i in range(n-1):
            for j in range(n-1-i):
                if self.students[j].average() > self.students[j+1].average():
                    self.students[j], self.students[j+1] = self.students[j+1], self.students[j]

        return self.students[:x]

    def subject_ranking(self, subject):
        """Gibt eine Liste von (name, durchschnitt) Tupeln zurück, sortiert
        nach dem besten Durchschnitt in einem bestimmten Fach.

        TODO 7: Nur Studierende berücksichtigen, die überhaupt Noten in
                diesem Fach haben. Nutze dafür list comprehension +
                Exception-Handling (z.B. try/except oder Prüfung mit `in`).
        """


        try:
            ranking = []
            for s in self.students:
                if subject in s.grades:  # nur wer im Fach Noten hat
                    ranking.append((s.name, s.average(subject)))

            n = len(ranking)
            for x in range(
                    n - 1):  # Bubble Sort
                for y in range(n - 1 - x):
                    if ranking[y][1] > ranking[y + 1][
                        1]:  # nach Durchschnitt vergleichen
                        ranking[y], ranking[y + 1] = ranking[y + 1], ranking[y]

            return ranking
        except KeyError as e:
            print("Liste konnte nicht erstellt werden.", e)
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
