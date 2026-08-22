"""
Übung: Notenverwaltungssystem

Ziel: Baue ein kleines System zur Verwaltung von Schüler:innen und ihren Noten.

Geübte Konzepte:
- Klassen & OOP (Attribute, Methoden, __init__, __repr__)
- Eigene Exceptions
- Dictionaries & List Comprehensions
- Sortieren mit key-Funktionen (lambda)
- String-Formatierung (f-strings)

Bearbeite die TODOs der Reihe nach. Am Ende steht ein Testblock,
mit dem du dein Ergebnis überprüfen kannst (einfach ausführen).
"""


# TODO 1: Erstelle eine eigene Exception-Klasse "InvalidGradeError",
#         die von Exception erbt. Sie soll geworfen werden, wenn eine
#         ungültige Note (nicht zwischen 1.0 und 6.0) eingetragen wird.


class Student:
    def __init__(self, name):
        self.name = name
        # TODO 2: Lege ein leeres Dictionary "self.grades" an.
        #         Struktur: {"Mathe": [2.0, 1.7], "Deutsch": [3.0]}
        pass

    def add_grade(self, subject, grade):
        """Fügt eine Note für ein Fach hinzu.

        TODO 3: Prüfe, ob grade zwischen 1.0 und 6.0 liegt (beide inklusive).
                Falls nicht: wirf InvalidGradeError mit einer sinnvollen
                Fehlermeldung.
                Falls doch: füge die Note zur Liste des Fachs in
                self.grades hinzu. Falls das Fach noch nicht existiert,
                lege es an.
        """
        pass

    def average(self, subject=None):
        """Berechnet den Notendurchschnitt.

        TODO 4a: Wenn subject angegeben ist, gib den Durchschnitt für
                 genau dieses Fach zurück (float, gerundet auf 2 Nachkommastellen).
        TODO 4b: Wenn subject None ist, gib den Gesamtdurchschnitt über
                 ALLE Noten in ALLEN Fächern zurück.
        Hinweis: Nutze eine List Comprehension, um alle Noten aus
                 self.grades.values() in eine flache Liste zu bringen.
        """
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
